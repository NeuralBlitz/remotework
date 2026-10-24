from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Event:
    event_type: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    source: str = ""
    correlation_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "correlation_id": self.correlation_id,
        }


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Any]] = {}
        self._published: list[Event] = []

    def subscribe(self, event_type: str, handler: Any) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def unsubscribe(self, event_type: str, handler: Any) -> bool:
        handlers = self._subscribers.get(event_type)
        if handlers and handler in handlers:
            handlers.remove(handler)
            return True
        return False

    def publish(self, event: Event) -> int:
        self._published.append(event)
        handlers = self._subscribers.get(event.event_type, [])
        for handler in handlers:
            if callable(handler):
                handler(event)
        return len(handlers)

    def get_subscriber_count(self, event_type: str) -> int:
        return len(self._subscribers.get(event_type, []))

    @property
    def published_count(self) -> int:
        return len(self._published)

    @property
    def event_types(self) -> list[str]:
        return list(self._subscribers.keys())
