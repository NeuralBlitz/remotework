from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class User:
    user_id: str
    name: str = ""
    preferences: dict[str, float] = field(default_factory=dict)


@dataclass
class Item:
    item_id: str
    title: str = ""
    tags: list[str] = field(default_factory=list)
    category: str = ""


@dataclass
class Rating:
    user_id: str
    item_id: str
    score: float = 0.0

