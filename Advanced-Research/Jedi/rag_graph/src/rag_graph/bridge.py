from __future__ import annotations

from abc import ABC, abstractmethod

from rag_graph.models import Subgraph, Triplet


class GraphBackend(ABC):
    @abstractmethod
    def add_triplet(self, triplet: Triplet) -> None: ...

    @abstractmethod
    def get_by_head(self, entity: str) -> list[Triplet]: ...

    @abstractmethod
    def get_by_relation(self, relation: str) -> list[Triplet]: ...

    @abstractmethod
    def get_neighbors(self, entity: str) -> list[Triplet]: ...

    @abstractmethod
    def count(self) -> int: ...


class InMemoryBackend(GraphBackend):
    def __init__(self) -> None:
        self._triplets: list[Triplet] = []

    def add_triplet(self, triplet: Triplet) -> None:
        self._triplets.append(triplet)

    def get_by_head(self, entity: str) -> list[Triplet]:
        return [t for t in self._triplets if t.head == entity]

    def get_by_relation(self, relation: str) -> list[Triplet]:
        return [t for t in self._triplets if t.relation == relation]

    def get_neighbors(self, entity: str) -> list[Triplet]:
        return [t for t in self._triplets if t.head == entity or t.tail == entity]

    def count(self) -> int:
        return len(self._triplets)
