from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Token:
    text: str
    start: int = 0
    end: int = 0
    pos: str = ""


@dataclass
class Entity:
    text: str
    label: str = ""
    start: int = 0
    end: int = 0
    confidence: float = 1.0

