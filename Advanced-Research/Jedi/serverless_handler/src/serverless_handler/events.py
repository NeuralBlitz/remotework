from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class TriggerEvent:
    event_type: str
    source: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "source": self.source,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "event_id": self.event_id,
        }


class EventMapper:
    def __init__(self) -> None:
        self._mappings: dict[str, list[str]] = {}

    def add_mapping(self, event_type: str, function_name: str) -> None:
        self._mappings.setdefault(event_type, []).append(function_name)

    def remove_mapping(self, event_type: str, function_name: str) -> bool:
        funcs = self._mappings.get(event_type)
        if funcs and function_name in funcs:
            funcs.remove(function_name)
            return True
        return False

    def get_targets(self, event_type: str) -> list[str]:
        return list(self._mappings.get(event_type, []))

    def get_event_types(self) -> list[str]:
        return list(self._mappings.keys())

    @property
    def mapping_count(self) -> int:
        return sum(len(fs) for fs in self._mappings.values())
