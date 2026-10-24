from __future__ import annotations

from pg_audit.models import AuditReport, PlanNode
from pg_audit.visitors import PlanVisitor


class QueryAuditor:
    def __init__(self, visitors: list[PlanVisitor] | None = None) -> None:
        self._visitors: list[PlanVisitor] = visitors or []

    def add_visitor(self, visitor: PlanVisitor) -> None:
        self._visitors.append(visitor)

    def audit(self, root: PlanNode) -> AuditReport:
        report = AuditReport()
        for visitor in self._visitors:
            visitor.visit_tree(root, report)
        return report
