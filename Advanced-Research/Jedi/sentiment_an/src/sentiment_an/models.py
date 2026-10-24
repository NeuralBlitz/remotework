from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Text:
    content: str
    language: str = "en"


@dataclass
class SentimentResult:
    label: str = "neutral"
    score: float = 0.0
    confidence: float = 1.0

