from __future__ import annotations

from abc import ABC, abstractmethod

from pg_audit.models import AuditReport, PlanNode, PlanType


class PlanVisitor(ABC):
    @abstractmethod
    def visit(self, node: PlanNode, report: AuditReport) -> None: ...

    def visit_tree(self, node: PlanNode, report: AuditReport) -> None:
        self.visit(node, report)
        for child in node.children:
            self.visit_tree(child, report)


class MissingIndexVisitor(PlanVisitor):
    LARGE_TABLE_THRESHOLD = 10000

    def visit(self, node: PlanNode, report: AuditReport) -> None:
        if (
            node.node_type == PlanType.SEQ_SCAN
            and node.estimated_rows >= self.LARGE_TABLE_THRESHOLD
        ):
            report.add_warning(
                f"Sequential scan on '{node.table}' with ~{node.estimated_rows} rows"
            )
            report.add_suggestion(
                f"Consider adding an index on '{node.table}' to avoid sequential scan"
            )


class CostEstimateVisitor(PlanVisitor):
    def visit(self, node: PlanNode, report: AuditReport) -> None:
        report.total_cost += node.cost
        if node.estimated_rows > 0 and node.actual_rows > 0:
            ratio = node.actual_rows / node.estimated_rows
            if ratio > 10 or ratio < 0.1:
                report.add_warning(
                    f"Row estimate mismatch on '{node.table}': "
                    f"estimated={node.estimated_rows}, actual={node.actual_rows}"
                )
