from knowledge_trace import Lineage, Node
from knowledge_trace.models import build_lineage, calculate_impact, trace_provenance


class TestNode:
    def test_creation(self) -> None:
        n = Node("1", "Test", "data")
        assert n.node_id == "1"

    def test_depth(self) -> None:
        n = Node("1", "Test", "data", parents=["parent1", "parent2"])
        assert n.depth == 2


class TestLineage:
    def test_find_node(self) -> None:
        n1 = Node("1", "Root", "data")
        lineage = Lineage(n1, [n1])
        found = lineage.find_node("1")
        assert found == n1

    def test_find_node_not_found(self) -> None:
        n1 = Node("1", "Root", "data")
        lineage = Lineage(n1, [n1])
        found = lineage.find_node("999")
        assert found is None

    def test_get_ancestors(self) -> None:
        n1 = Node("1", "Root", "data")
        n2 = Node("2", "Child", "data", parents=["1"])
        lineage = Lineage(n1, [n1, n2])
        ancestors = lineage.get_ancestors("2")
        assert len(ancestors) == 1
        assert ancestors[0].name == "Root"


class TestHelpers:
    def test_build_lineage(self) -> None:
        lineage = build_lineage("root_id", [("1", "root_id"), ("2", "1")])
        assert lineage.root.node_id == "root_id"

    def test_trace_provenance(self) -> None:
        result = trace_provenance("node1", {("1", "root"), ("2", "1")})
        assert len(result) > 0

    def test_calculate_impact(self) -> None:
        impact = calculate_impact("1", [("1",), ("2", "1"), ("3", "1")])
        assert impact == 3
