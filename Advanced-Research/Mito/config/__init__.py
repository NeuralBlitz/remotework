"""
Mito Configuration System
Validation, profiles, hot reload, env overrides, schema
"""

import os
import json
import time
import threading
from pathlib import Path
from typing import Any, Dict, Optional, List, Callable, Set
from dataclasses import dataclass, field
import yaml


@dataclass
class ModelConfig:
    default_model: str = "gpt2"
    llama_model: str = "model.gguf"
    llama_ctx: int = 2048
    llama_threads: int = 4
    temperature: float = 0.7
    max_tokens: int = 256


@dataclass
class APIConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    cors_origins: list = field(default_factory=lambda: ["*"])
    api_keys: list = field(default_factory=list)
    rate_limit: int = 100
    timeout: int = 30
    max_request_size: int = 10485760


@dataclass
class StorageConfig:
    models_dir: str = "./models"
    data_dir: str = "./data"
    cache_dir: str = "./.cache"
    vector_store_path: str = "./data/vectorstore.json"
    max_cache_size_mb: int = 1024


@dataclass
class LoggingConfig:
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None
    max_size_mb: int = 100
    backup_count: int = 5


@dataclass
class ObservabilityConfig:
    enable_metrics: bool = True
    metrics_port: int = 9090
    enable_tracing: bool = False
    trace_sample_rate: float = 0.1
    health_check_interval: int = 30


@dataclass
class MitoConfig:
    version: str = "1.0.0"
    profile: str = "default"
    model: ModelConfig = field(default_factory=ModelConfig)
    api: APIConfig = field(default_factory=APIConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    observability: ObservabilityConfig = field(default_factory=ObservabilityConfig)
    custom: Dict[str, Any] = field(default_factory=dict)


class ConfigSchema:
    """Define and validate configuration schemas."""

    def __init__(self):
        self.rules: Dict[str, Dict] = {}
        self.required: Set[str] = set()

    def add_rule(self, path: str, rule_type: str = None, min_val: Any = None,
                 max_val: Any = None, allowed: List = None, required: bool = False):
        self.rules[path] = {
            "type": rule_type,
            "min": min_val,
            "max": max_val,
            "allowed": allowed,
        }
        if required:
            self.required.add(path)

    def validate(self, config: MitoConfig) -> List[str]:
        errors = []
        data = config_to_dict(config)

        for req in self.required:
            if self._get_nested(data, req) is None:
                errors.append(f"Missing required field: {req}")

        for path, rule in self.rules.items():
            value = self._get_nested(data, path)
            if value is None:
                continue

            if rule["type"] and not isinstance(value, {"int": int, "str": str, "float": float, "bool": bool, "list": list}.get(rule["type"])):
                errors.append(f"{path}: expected {rule['type']}, got {type(value).__name__}")
            if rule["min"] is not None and value < rule["min"]:
                errors.append(f"{path}: value {value} below minimum {rule['min']}")
            if rule["max"] is not None and value > rule["max"]:
                errors.append(f"{path}: value {value} above maximum {rule['max']}")
            if rule["allowed"] is not None and value not in rule["allowed"]:
                errors.append(f"{path}: value {value} not in allowed {rule['allowed']}")

        return errors

    def _get_nested(self, data: Dict, path: str):
        parts = path.split(".")
        obj = data
        for part in parts:
            if isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                return None
        return obj


class ConfigManager:
    def __init__(self, config_path: str = "mito.yaml", schema: ConfigSchema = None,
                 env_prefix: str = "MITO"):
        self.config_path = Path(config_path)
        self.config: MitoConfig = MitoConfig()
        self.schema = schema or ConfigSchema()
        self.env_prefix = env_prefix
        self._watchers: List[Callable] = []
        self._watch_thread: Optional[threading.Thread] = None
        self._watching = False
        self._last_modified = 0.0
        self._lock = threading.Lock()

    def load(self) -> MitoConfig:
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    self._apply_dict(data)
                    self._last_modified = self.config_path.stat().st_mtime

        self._apply_env_overrides()
        return self.config

    def save(self):
        data = config_to_dict(self.config)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def validate(self) -> List[str]:
        return self.schema.validate(self.config)

    def is_valid(self) -> bool:
        return len(self.validate()) == 0

    def _apply_dict(self, data: Dict):
        for key, value in data.items():
            if key == "profile":
                self.config.profile = value
            elif key == "custom":
                self.config.custom = value if isinstance(value, dict) else {}
            elif hasattr(self.config, key):
                config_section = getattr(self.config, key)
                if isinstance(config_section, dict):
                    config_section.update(value)
                elif hasattr(config_section, '__dataclass_fields__'):
                    for k, v in (value or {}).items():
                        if hasattr(config_section, k):
                            setattr(config_section, k, v)

    def _apply_env_overrides(self):
        prefix = f"{self.env_prefix}_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower().replace("_", ".")
                self._set_nested(config_key, self._parse_env_value(value))

    def _parse_env_value(self, value: str) -> Any:
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        if value.startswith("[") and value.endswith("]"):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        return value

    def _set_nested(self, path: str, value: Any):
        parts = path.split(".")
        obj = self.config
        for part in parts[:-1]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return
        if hasattr(obj, parts[-1]):
            setattr(obj, parts[-1], value)

    def get(self, key: str, default: Any = None) -> Any:
        parts = key.split('.')
        obj = self.config
        for part in parts:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            elif isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                return default
        return obj

    def set(self, key: str, value: Any):
        self._set_nested(key, value)

    def get_section(self, section: str) -> Any:
        return getattr(self.config, section, None)

    def merge(self, overrides: Dict):
        self._apply_dict(overrides)

    def on_change(self, callback: Callable):
        self._watchers.append(callback)

    def start_watching(self, interval: float = 2.0):
        if self._watching:
            return
        self._watching = True
        self._watch_thread = threading.Thread(target=self._watch_loop, args=(interval,), daemon=True)
        self._watch_thread.start()

    def stop_watching(self):
        self._watching = False

    def _watch_loop(self, interval: float):
        while self._watching:
            if self.config_path.exists():
                mtime = self.config_path.stat().st_mtime
                if mtime > self._last_modified:
                    self._last_modified = mtime
                    self.load()
                    for cb in self._watchers:
                        try:
                            cb(self.config)
                        except Exception:
                            pass
            time.sleep(interval)

    def get_profiles(self) -> List[str]:
        profiles_dir = self.config_path.parent / "profiles"
        if not profiles_dir.exists():
            return ["default"]
        return ["default"] + [f.stem for f in profiles_dir.glob("*.yaml")]

    def load_profile(self, profile_name: str):
        if profile_name == "default":
            return
        profile_path = self.config_path.parent / "profiles" / f"{profile_name}.yaml"
        if profile_path.exists():
            with open(profile_path) as f:
                data = yaml.safe_load(f)
                if data:
                    self._apply_dict(data)
            self.config.profile = profile_name

    def to_dict(self) -> Dict:
        return config_to_dict(self.config)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, default=str)


def config_to_dict(config: MitoConfig) -> Dict:
    result = {"version": config.version, "profile": config.profile}
    for key in ['model', 'api', 'storage', 'logging', 'observability']:
        section = getattr(config, key)
        if hasattr(section, '__dataclass_fields__'):
            result[key] = {k: v for k, v in vars(section).items() if not k.startswith('_')}
    if config.custom:
        result["custom"] = config.custom
    return result


def create_default_schema() -> ConfigSchema:
    schema = ConfigSchema()
    schema.add_rule("api.port", rule_type="int", min_val=1, max_val=65535)
    schema.add_rule("api.workers", rule_type="int", min_val=1, max_val=32)
    schema.add_rule("api.rate_limit", rule_type="int", min_val=1)
    schema.add_rule("model.temperature", rule_type="float", min_val=0.0, max_val=2.0)
    schema.add_rule("model.max_tokens", rule_type="int", min_val=1)
    schema.add_rule("logging.level", rule_type="str", allowed=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    return schema


DEFAULT_CONFIG = """
version: "1.0.0"
profile: "default"

model:
  default_model: "gpt2"
  llama_model: "model.gguf"
  llama_ctx: 2048
  llama_threads: 4
  temperature: 0.7
  max_tokens: 256

api:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  cors_origins:
    - "*"
  api_keys: []
  rate_limit: 100
  timeout: 30

storage:
  models_dir: "./models"
  data_dir: "./data"
  cache_dir: "./.cache"
  vector_store_path: "./data/vectorstore.json"
  max_cache_size_mb: 1024

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: null
  max_size_mb: 100
  backup_count: 5

observability:
  enable_metrics: true
  metrics_port: 9090
  enable_tracing: false
  trace_sample_rate: 0.1
  health_check_interval: 30
"""


def load_config(path: str = "mito.yaml") -> MitoConfig:
    manager = ConfigManager(path, schema=create_default_schema())
    return manager.load()


def create_default_config(path: str = "mito.yaml"):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(DEFAULT_CONFIG)


if __name__ == '__main__':
    create_default_config()
    print("Created mito.yaml")
