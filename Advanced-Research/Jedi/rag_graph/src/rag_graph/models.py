from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Triplet:
    head: str
    relation: str
    tail: str
    score: float = 1.0


@dataclass
class Subgraph:
    triplets: list[Triplet] = field(default_factory=list)
    entities: set[str] = field(default_factory=set)

    def add_triplet(self, t: Triplet) -> None:
        self.triplets.append(t)
        self.entities.add(t.head)
        self.entities.add(t.tail)

    @property
    def size(self) -> int:
        return len(self.triplets)
