from contract_comp import Contract, Interface
from contract_comp.models import compose_contracts, dependency_graph, validate_compatibility


class TestContract:
    def test_creation(self) -> None:
        c = Contract("Test", "0x123", ["func1"], [])
        assert c.name == "Test"

    def test_add_dependency(self) -> None:
        c = Contract("Test", "0x123", ["func1"], [])
        c.add_dependency("Other")
        assert "Other" in c.dependencies

    def test_is_valid(self) -> None:
        valid = Contract("Test", "0x123", ["func1"], [])
        invalid = Contract("Test", "", [], [])
        assert valid.is_valid is True
        assert invalid.is_valid is False


class TestInterface:
    def test_is_compatible(self) -> None:
        iface = Interface("IERC20", ["transfer", "balanceOf"], [])
        contract = Contract("Token", "0x123", ["transfer", "balanceOf", "mint"], [])
        assert iface.is_compatible(contract) is True


class TestHelpers:
    def test_compose_contracts(self) -> None:
        c1 = Contract("A", "0x1", ["a"], [])
        c2 = Contract("B", "0x2", ["b"], ["A"])
        result = compose_contracts([c1, c2])
        assert "A" in result

    def test_validate_compatibility(self) -> None:
        c = Contract("Test", "0x123", ["f1", "f2"], [])
        assert validate_compatibility(c) is True

    def test_dependency_graph(self) -> None:
        c1 = Contract("A", "0x1", ["a"], [])
        c2 = Contract("B", "0x2", ["b"], ["A"])
        graph = dependency_graph([c1, c2])
        assert "A" in graph
