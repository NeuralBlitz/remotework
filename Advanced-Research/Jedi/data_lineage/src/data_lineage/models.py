from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Node:
    id: str
    type: str
    name: str

@dataclass
class Edge:
    source: str
    target: str

    def to_dict(self) -> dict[str, str]:
        return {"source": self.source, "target": self.target}
