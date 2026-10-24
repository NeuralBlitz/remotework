from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from dr_backup.manager import BackupStatus, BackupType


@dataclass
class BackupRecord:
    config_name: str
    database: str
    backup_type: BackupType
    status: BackupStatus
    started_at: datetime
    completed_at: datetime | None = None
    size_bytes: int = 0
    error_message: str = ""


class BackupStorage:
    def __init__(self) -> None:
        self._records: list[BackupRecord] = []

    def store(self, record: BackupRecord) -> None:
        self._records.append(record)

    def get_records(self, database: str | None = None) -> list[BackupRecord]:
        if database is None:
            return list(self._records)
        return [r for r in self._records if r.database == database]

    def get_latest(self, database: str) -> BackupRecord | None:
        db_records = self.get_records(database)
        return db_records[-1] if db_records else None

    def purge_old(self, retention_days: int) -> int:
        cutoff = datetime.now(timezone.utc)
        before = len(self._records)
        self._records = [
            r
            for r in self._records
            if r.started_at and (cutoff - r.started_at).days < retention_days
        ]
        return before - len(self._records)

    @property
    def record_count(self) -> int:
        return len(self._records)
