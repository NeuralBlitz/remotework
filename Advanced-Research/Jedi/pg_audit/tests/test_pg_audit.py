from __future__ import annotations

from pg_audit.auditor import QueryAuditor
from pg_audit.models import AuditReport, PlanNode, PlanType
from pg_audit.visitors import CostEstimateVisitor, MissingIndexVisitor, PlanVisitor


class _DummyVisitor(PlanVisitor):
    def __init__(self) -> None:
        self.visited: list[PlanNode] = []

    def visit(self, node: PlanNode, report: AuditReport) -> None:
        self.visited.append(node)


def _make_plan() -> PlanNode:
    return PlanNode(
        node_type=PlanType.HASH_JOIN,
        cost=200.0,
        estimated_rows=50000,
        actual_rows=50000,
        children=[
            PlanNode(
                node_type=PlanType.SEQ_SCAN,
                table="orders",
                estimated_rows=100000,
                actual_rows=100000,
                cost=150.0,
            ),
            PlanNode(
                node_type=PlanType.INDEX_SCAN,
                table="customers",
                index_name="customers_pkey",
                estimated_rows=50000,
                actual_rows=50000,
                cost=50.0,
            ),
        ],
    )


def test_plan_from_dict() -> None:
    data = {
        "node_type": "SeqScan",
        "table": "users",
        "estimated_rows": 100,
        "cost": 5.0,
        "children": [
            {"node_type": "Sort", "cost": 2.0, "children": []},
        ],
    }
    node = PlanNode.from_dict(data)
    assert node.node_type == PlanType.SEQ_SCAN
    assert node.table == "users"
    assert len(node.children) == 1
    assert node.children[0].node_type == PlanType.SORT


def test_visitor_traversal() -> None:
    plan = _make_plan()
    dummy = _DummyVisitor()
    report = AuditReport()
    dummy.visit_tree(plan, report)
    assert len(dummy.visited) == 3  # root + 2 children


def test_missing_index_visitor() -> None:
    plan = PlanNode(
        node_type=PlanType.SEQ_SCAN,
        table="big_table",
        estimated_rows=50000,
        actual_rows=50000,
        cost=300.0,
    )
    auditor = QueryAuditor([MissingIndexVisitor()])
    report = auditor.audit(plan)
    assert report.has_issues
    assert any("big_table" in w for w in report.warnings)
    assert any("index" in s.lower() for s in report.suggestions)


def test_missing_index_visitor_small_table() -> None:
    plan = PlanNode(
        node_type=PlanType.SEQ_SCAN,
        table="tiny",
        estimated_rows=10,
        cost=0.1,
    )
    auditor = QueryAuditor([MissingIndexVisitor()])
    report = auditor.audit(plan)
    assert not report.has_issues


def test_cost_estimate_visitor() -> None:
    plan = PlanNode(
        node_type=PlanType.SEQ_SCAN,
        table="misestimated",
        estimated_rows=100,
        actual_rows=5000,
        cost=42.0,
    )
    auditor = QueryAuditor([CostEstimateVisitor()])
    report = auditor.audit(plan)
    assert report.total_cost == 42.0
    assert len(report.warnings) == 1
    assert "mismatch" in report.warnings[0].lower()


def test_auditor_multiple_visitors() -> None:
    plan = _make_plan()
    auditor = QueryAuditor([MissingIndexVisitor(), CostEstimateVisitor()])
    report = auditor.audit(plan)
    assert report.has_issues
    assert report.total_cost == 200.0 + 150.0 + 50.0


def test_audit_report_no_issues() -> None:
    report = AuditReport()
    assert not report.has_issues
    assert report.warnings == []
    assert report.suggestions == []
