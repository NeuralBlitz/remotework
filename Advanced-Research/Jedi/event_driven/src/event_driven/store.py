from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class StoredEvent:
    id: str
    event_type: str
    payload: dict[str, Any]
    timestamp: datetime
    source: str = ""
    sequence: int = 0


class EventStore:
    def __init__(self) -> None:
        self._events: list[StoredEvent] = []
        self._sequence: int = 0

    def append(
        self, event_id: str, event_type: str, payload: dict[str, Any], source: str = ""
    ) -> StoredEvent:
        self._sequence += 1
        stored = StoredEvent(
            id=event_id,
            event_type=event_type,
            payload=payload,
            timestamp=datetime.now(timezone.utc),
            source=source,
            sequence=self._sequence,
        )
        self._events.append(stored)
        return stored

    def get_by_id(self, event_id: str) -> StoredEvent | None:
        for e in self._events:
            if e.id == event_id:
                return e
        return None

    def get_by_type(self, event_type: str) -> list[StoredEvent]:
        return [e for e in self._events if e.event_type == event_type]

    def get_after_sequence(self, sequence: int) -> list[StoredEvent]:
        return [e for e in self._events if e.sequence > sequence]

    def get_range(self, start: int, end: int) -> list[StoredEvent]:
        return [e for e in self._events if start <= e.sequence <= end]

    @property
    def count(self) -> int:
        return len(self._events)

    @property
    def latest_sequence(self) -> int:
        return self._sequence
