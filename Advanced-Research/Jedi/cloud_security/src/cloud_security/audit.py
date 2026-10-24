from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AuditEvent:
    timestamp: datetime
    user: str
    action: str
    resource: str
    result: str
    metadata: dict[str, Any] = field(default_factory=dict)


class AuditLogger:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def log(
        self, user: str, action: str, resource: str, result: str, **metadata: Any
    ) -> AuditEvent:
        event = AuditEvent(
            timestamp=datetime.now(timezone.utc),
            user=user,
            action=action,
            resource=resource,
            result=result,
            metadata=metadata,
        )
        self._events.append(event)
        return event

    def get_events(self, user: str | None = None) -> list[AuditEvent]:
        if user is None:
            return list(self._events)
        return [e for e in self._events if e.user == user]

    def get_failed_events(self) -> list[AuditEvent]:
        return [e for e in self._events if e.result != "success"]

    @property
    def event_count(self) -> int:
        return len(self._events)

    def clear(self) -> None:
        self._events.clear()
