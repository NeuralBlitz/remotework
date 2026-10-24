from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from event_driven.bus import Event


class EventHandler(ABC):
    @abstractmethod
    def handle(self, event: Event) -> Any: ...

    @property
    def name(self) -> str:
        return self.__class__.__name__


class HandlerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}

    def register(self, event_type: str, handler: EventHandler) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def unregister(self, event_type: str, handler: EventHandler) -> bool:
        handlers = self._handlers.get(event_type)
        if handlers and handler in handlers:
            handlers.remove(handler)
            return True
        return False

    def get_handlers(self, event_type: str) -> list[EventHandler]:
        return list(self._handlers.get(event_type, []))

    def dispatch(self, event: Event) -> list[Any]:
        results: list[Any] = []
        for handler in self._handlers.get(event.event_type, []):
            results.append(handler.handle(event))
        return results

    @property
    def registered_types(self) -> list[str]:
        return list(self._handlers.keys())

    @property
    def handler_count(self) -> int:
        return sum(len(hs) for hs in self._handlers.values())
