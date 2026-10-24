from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import AuditFinding, AuditReport, BackupRecord
from .visitors import BackupVisitor


class BackupAuditor:
    def __init__(self) -> None:
        self._visitors: list[BackupVisitor] = []
        self._records: list[BackupRecord] = []

    def add_visitor(self, visitor: BackupVisitor) -> None:
        self._visitors.append(visitor)

    def remove_visitor(self, check_name: str) -> bool:
        for i, v in enumerate(self._visitors):
            if v.check_name == check_name:
                self._visitors.pop(i)
                return True
        return False

    def load_records(self, records: list[BackupRecord]) -> None:
        self._records = list(records)

    def add_record(self, record: BackupRecord) -> None:
        self._records.append(record)

    @property
    def record_count(self) -> int:
        return len(self._records)

    @property
    def visitor_count(self) -> int:
        return len(self._visitors)

    def audit(self) -> AuditReport:
        from .models import AuditReport

        findings: list[AuditFinding] = []
        for record in self._records:
            for visitor in self._visitors:
                finding = visitor.visit(record)
                findings.append(finding)

        passed = sum(1 for f in findings if f.passed)
        failed = sum(1 for f in findings if not f.passed)
        return AuditReport(
            total_backups=len(self._records),
            passed_checks=passed,
            failed_checks=failed,
            findings=findings,
        )

    def audit_with(self, visitor: BackupVisitor) -> list[AuditFinding]:
        return [visitor.visit(r) for r in self._records]
