from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Query:
    text: str
    filters: dict[str, str] = field(default_factory=dict)


@dataclass
class Document:
    document_id: str
    title: str = ""
    content: str = ""
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class Score:
    document_id: str
    value: float = 0.0

