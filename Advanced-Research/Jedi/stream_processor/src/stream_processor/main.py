"""Stream processing utilities."""

from __future__ import annotations

import time

from .models import Event, ProcessedEvent

__all__ = ["Event", "ProcessedEvent", "create_event", "process_event"]


def create_event(topic: str, data: dict[str, str]) -> Event:
    return Event(topic=topic, data=data, timestamp=time.time())


def process_event(event: Event) -> ProcessedEvent:
    result: dict[str, str] = {"processed": "true", "topic": event.topic}
    return ProcessedEvent(event=event, result=result)
