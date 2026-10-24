from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Fact:
    predicate: str
    arguments: list[str]
    confidence: float = 1.0


@dataclass
class Rule:
    name: str
    head: Fact
    body: list[Fact]


@dataclass
class Query:
    predicate: str
    arguments: list[str]
    results: list[Fact] = field(default_factory=list)
