from dataclasses import dataclass


@dataclass
class Contract:
    name: str
    address: str
    functions: list[str]
    dependencies: list[str]

    def add_dependency(self, dep: str) -> None:
        if dep not in self.dependencies:
            self.dependencies.append(dep)

    @property
    def is_valid(self) -> bool:
        return len(self.functions) > 0 and len(self.address) > 0


@dataclass
class Interface:
    name: str
    methods: list[str]
    events: list[str]

    def is_compatible(self, contract: Contract) -> bool:
        return all(m in contract.functions for m in self.methods)


def compose_contracts(contracts: list[Contract]) -> dict[str, Contract]:
    return {c.name: c for c in contracts}


def validate_compatibility(contract: Contract) -> bool:
    return contract.is_valid and len(contract.functions) > 0


def dependency_graph(contracts: list[Contract]) -> dict[str, list[str]]:
    graph = {c.name: c.dependencies for c in contracts}
    return graph
