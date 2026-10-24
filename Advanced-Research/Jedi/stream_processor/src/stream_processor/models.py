from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Event:
    topic: str
    data: dict[str, str]
    timestamp: float

@dataclass
class ProcessedEvent:
    event: Event
    result: dict[str, str]
