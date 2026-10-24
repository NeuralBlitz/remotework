"""
Mito Serializers
JSON, YAML, TOML, CSV, MessagePack serialization helpers
"""

import csv
import io
import json
from typing import Dict, List, Any, Optional
from pathlib import Path


def to_json(data: Any, indent: int = 2, sort_keys: bool = False) -> str:
    return json.dumps(data, indent=indent, sort_keys=sort_keys, default=str)


def from_json(text: str) -> Any:
    return json.loads(text)


def save_json(data: Any, filepath: str, indent: int = 2):
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=indent, default=str)


def load_json(filepath: str) -> Any:
    with open(filepath) as f:
        return json.load(f)


def to_yaml(data: Any) -> str:
    try:
        import yaml
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)
    except ImportError:
        raise ImportError("PyYAML not installed. Install with: pip install pyyaml")


def from_yaml(text: str) -> Any:
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        raise ImportError("PyYAML not installed")


def save_yaml(data: Any, filepath: str):
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(to_yaml(data))


def load_yaml(filepath: str) -> Any:
    with open(filepath) as f:
        try:
            import yaml
            return yaml.safe_load(f)
        except ImportError:
            raise ImportError("PyYAML not installed")


def to_csv(rows: List[Dict], columns: List[str] = None) -> str:
    output = io.StringIO()
    if not rows:
        return ""
    if not columns:
        columns = list(rows[0].keys())
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def from_csv(text: str) -> List[Dict]:
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)


def save_csv(rows: List[Dict], filepath: str, columns: List[str] = None):
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", newline="") as f:
        if not rows:
            return
        if not columns:
            columns = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_csv(filepath: str) -> List[Dict]:
    with open(filepath, newline="") as f:
        return list(csv.DictReader(f))


def to_tsv(rows: List[Dict]) -> str:
    return to_csv(rows).replace(",", "\t")


def to_ndjson(records: List[Dict]) -> str:
    return "\n".join(json.dumps(r, default=str) for r in records)


def from_ndjson(text: str) -> List[Dict]:
    return [json.loads(line) for line in text.strip().split("\n") if line.strip()]


def to_msgpack(data: Any) -> bytes:
    try:
        import msgpack
        return msgpack.packb(data, default=str)
    except ImportError:
        raise ImportError("msgpack not installed")


def from_msgpack(data: bytes) -> Any:
    try:
        import msgpack
        return msgpack.unpackb(data)
    except ImportError:
        raise ImportError("msgpack not installed")


def flatten_dict(d: Dict, prefix: str = "", sep: str = ".") -> Dict:
    result = {}
    for k, v in d.items():
        key = f"{prefix}{sep}{k}" if prefix else k
        if isinstance(v, dict):
            result.update(flatten_dict(v, key, sep))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                result[f"{key}[{i}]"] = item
        else:
            result[key] = v
    return result


def unflatten_dict(d: Dict, sep: str = ".") -> Dict:
    result = {}
    for key, value in d.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result


def deep_merge(base: Dict, override: Dict) -> Dict:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def pretty_print(data: Any):
    print(json.dumps(data, indent=2, default=str))
