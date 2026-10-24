from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class RestoreStatus(str, Enum):
    PENDING = "pending"
    VALIDATING = "validating"
    RESTORING = "restoring"
    COMPLETED = "completed"
    FAILED = "failed"


class RestoreMode(str, Enum):
    FULL = "full"
    POINT_IN_TIME = "point_in_time"
    SELECTIVE = "selective"


@dataclass
class RestoreConfig:
    name: str
    source_backup: str
    target_database: str
    mode: RestoreMode = RestoreMode.FULL
    point_in_time: datetime | None = None
    target_tables: list[str] = field(default_factory=list)
    overwrite: bool = False

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.name:
            errors.append("name is required")
        if not self.source_backup:
            errors.append("source_backup is required")
        if not self.target_database:
            errors.append("target_database is required")
        if self.mode == RestoreMode.POINT_IN_TIME and self.point_in_time is None:
            errors.append("point_in_time is required for point_in_time mode")
        if self.mode == RestoreMode.SELECTIVE and not self.target_tables:
            errors.append("target_tables required for selective mode")
        return errors


@dataclass
class RestoreEngine:
    configs: dict[str, RestoreConfig] = field(default_factory=dict)
    _history: list[dict[str, object]] = field(default_factory=list)

    def add_config(self, config: RestoreConfig) -> None:
        errors = config.validate()
        if errors:
            raise ValueError(f"Invalid config: {', '.join(errors)}")
        if config.name in self.configs:
            raise ValueError(f"Config {config.name!r} already exists")
        self.configs[config.name] = config

    def remove_config(self, name: str) -> bool:
        return self.configs.pop(name, None) is not None

    def get_config(self, name: str) -> RestoreConfig:
        if name not in self.configs:
            raise KeyError(f"Config {name!r} not found")
        return self.configs[name]

    def run_restore(self, config_name: str) -> dict[str, object]:
        config = self.get_config(config_name)
        entry = {
            "config_name": config_name,
            "source_backup": config.source_backup,
            "target_database": config.target_database,
            "mode": config.mode.value,
            "status": RestoreStatus.COMPLETED.value,
            "started_at": datetime.now(timezone.utc),
        }
        self._history.append(entry)
        return entry

    def get_history(self) -> list[dict[str, object]]:
        return list(self._history)

    @property
    def config_count(self) -> int:
        return len(self.configs)
