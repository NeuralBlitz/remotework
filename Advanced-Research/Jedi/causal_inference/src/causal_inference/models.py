from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Treatment:
    name: str
    levels: list[float] = field(default_factory=lambda: [0.0, 1.0])


@dataclass
class Outcome:
    name: str
    values: list[float] = field(default_factory=list)


@dataclass
class CausalGraph:
    nodes: list[str] = field(default_factory=list)
    edges: list[tuple[str, str]] = field(default_factory=list)
    confounders: list[str] = field(default_factory=list)

    def parents(self, node: str) -> list[str]:
        return [src for src, dst in self.edges if dst == node]

    def children(self, node: str) -> list[str]:
        return [dst for src, dst in self.edges if src == node]

    def add_edge(self, source: str, target: str) -> None:
        if source not in self.nodes:
            self.nodes.append(source)
        if target not in self.nodes:
            self.nodes.append(target)
        if (source, target) not in self.edges:
            self.edges.append((source, target))
