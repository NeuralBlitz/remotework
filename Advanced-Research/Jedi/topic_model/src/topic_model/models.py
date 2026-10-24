from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Document:
    document_id: str
    content: str = ""
    title: str = ""


@dataclass
class Topic:
    topic_id: str
    keywords: list[str] = field(default_factory=list)
    weight: float = 0.0

