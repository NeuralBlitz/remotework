from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class ConversationNode:
    role: Role = Role.USER
    content: str = ""
    metadata: dict[str, str] = field(default_factory=dict)
    children: list[ConversationNode] = field(default_factory=list)
    parent: ConversationNode | None = None

    def add_child(self, child: ConversationNode) -> None:
        child.parent = self
        self.children.append(child)

    def depth(self) -> int:
        d = 0
        node = self.parent
        while node is not None:
            d += 1
            node = node.parent
        return d


@dataclass
class EvalScore:
    metric: str = ""
    score: float = 0.0
    explanation: str = ""
    node_id: str = ""

    def is_passing(self, threshold: float = 0.5) -> bool:
        return self.score >= threshold
