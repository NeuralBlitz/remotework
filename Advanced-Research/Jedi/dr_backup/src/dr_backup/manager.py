from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class BackupType(str, Enum):
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"


class BackupStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class BackupConfig:
    name: str
    database: str
    backup_type: BackupType = BackupType.FULL
    retention_days: int = 30
    compress: bool = True
    exclude_tables: list[str] = field(default_factory=list)
    max_parallel: int = 1

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.name:
            errors.append("name is required")
        if not self.database:
            errors.append("database is required")
        if self.retention_days < 1:
            errors.append("retention_days must be >= 1")
        if self.max_parallel < 1:
            errors.append("max_parallel must be >= 1")
        return errors


@dataclass
class BackupManager:
    configs: dict[str, BackupConfig] = field(default_factory=dict)
    _history: list[BackupRecord] = field(default_factory=list, repr=False)

    def add_config(self, config: BackupConfig) -> None:
        errors = config.validate()
        if errors:
            raise ValueError(f"Invalid config: {', '.join(errors)}")
        if config.name in self.configs:
            raise ValueError(f"Config {config.name!r} already exists")
        self.configs[config.name] = config

    def remove_config(self, name: str) -> bool:
        return self.configs.pop(name, None) is not None

    def get_config(self, name: str) -> BackupConfig:
        if name not in self.configs:
            raise KeyError(f"Config {name!r} not found")
        return self.configs[name]

    def run_backup(self, config_name: str) -> BackupRecord:
        config = self.get_config(config_name)
        record = BackupRecord(
            config_name=config_name,
            database=config.database,
            backup_type=config.backup_type,
            status=BackupStatus.COMPLETED,
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
        )
        self._history.append(record)
        return record

    def get_history(self, config_name: str | None = None) -> list[BackupRecord]:
        if config_name is None:
            return list(self._history)
        return [r for r in self._history if r.config_name == config_name]

    @property
    def config_count(self) -> int:
        return len(self.configs)


from dr_backup.storage import BackupRecord  # noqa: E402
