from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class BackupType(Enum):
    FULL = "full"
    INCREMENTAL = "incremental"
    WAL = "wal"


class BackupStatus(Enum):
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"
    CORRUPT = "corrupt"


@dataclass
class BackupRecord:
    backup_id: str
    backup_type: BackupType
    status: BackupStatus
    size_bytes: int
    created_at: datetime
    retention_days: int
    database: str
    verified: bool = False


@dataclass
class AuditFinding:
    check_name: str
    passed: bool
    message: str
    backup_id: str | None = None


@dataclass
class AuditReport:
    total_backups: int
    passed_checks: int
    failed_checks: int
    findings: list[AuditFinding] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        total = self.passed_checks + self.failed_checks
        if total == 0:
            return 0.0
        return self.passed_checks / total
