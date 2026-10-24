from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Message:
    id: str
    payload: dict[str, str]
    priority: int

@dataclass
class Queue:
    name: str
    messages: list[Message] = field(default_factory=list)
