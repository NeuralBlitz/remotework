"""Graph component models using Composite Pattern."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class GraphComponent(ABC):
    """Base component for graph nodes and composite trees."""

    @property
    @abstractmethod
    def label(self) -> str: ...

    @abstractmethod
    def depth(self) -> int: ...

    @abstractmethod
    def collect_edges(self) -> list[Edge]: ...


@dataclass
class Edge:
    """Represents a relationship between two nodes."""

    source_id: str
    target_id: str
    weight: float = 1.0
    relation_type: str = "friend"
    metadata: dict[str, Any] = field(default_factory=dict)

    def reversed(self) -> Edge:
        return Edge(
            source_id=self.target_id,
            target_id=self.source_id,
            weight=self.weight,
            relation_type=self.relation_type,
            metadata=self.metadata,
        )


@dataclass
class Node(GraphComponent):
    """A single vertex in the graph."""

    node_id: str
    name: str
    properties: dict[str, Any] = field(default_factory=dict)
    _edges: list[Edge] = field(default_factory=list)

    @property
    def label(self) -> str:
        return self.name

    def depth(self) -> int:
        return 0

    def collect_edges(self) -> list[Edge]:
        return list(self._edges)

    def add_edge(self, edge: Edge) -> None:
        self._edges.append(edge)

    @property
    def degree(self) -> int:
        return len(self._edges)

    def neighbors(self) -> list[str]:
        return [e.target_id for e in self._edges]
