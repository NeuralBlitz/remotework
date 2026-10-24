from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import AuditFinding, BackupRecord


class BackupVisitor(ABC):
    @abstractmethod
    def visit(self, record: BackupRecord) -> AuditFinding: ...

    @property
    @abstractmethod
    def check_name(self) -> str: ...


class CompletenessVisitor(BackupVisitor):
    @property
    def check_name(self) -> str:
        return "completeness"

    def visit(self, record: BackupRecord) -> AuditFinding:
        from .models import AuditFinding, BackupStatus

        if record.status == BackupStatus.COMPLETED:
            return AuditFinding(
                check_name=self.check_name,
                passed=True,
                message=f"Backup {record.backup_id} completed successfully ({record.size_bytes} bytes)",
                backup_id=record.backup_id,
            )
        return AuditFinding(
            check_name=self.check_name,
            passed=False,
            message=f"Backup {record.backup_id} status: {record.status.value}",
            backup_id=record.backup_id,
        )


class RetentionVisitor(BackupVisitor):
    def __init__(self, reference_time: datetime | None = None) -> None:
        self._reference = reference_time or datetime.now()

    @property
    def check_name(self) -> str:
        return "retention"

    def visit(self, record: BackupRecord) -> AuditFinding:
        from .models import AuditFinding

        expiry = record.created_at + timedelta(days=record.retention_days)
        if expiry < self._reference:
            return AuditFinding(
                check_name=self.check_name,
                passed=False,
                message=f"Backup {record.backup_id} expired (retention: {record.retention_days}d)",
                backup_id=record.backup_id,
            )
        return AuditFinding(
            check_name=self.check_name,
            passed=True,
            message=f"Backup {record.backup_id} within retention",
            backup_id=record.backup_id,
        )
