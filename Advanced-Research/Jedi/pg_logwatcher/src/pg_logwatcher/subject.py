from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from pg_logwatcher.models import LogEntry


class LogObserver(Protocol):
    def on_log_entry(self, entry: LogEntry) -> None: ...


class LogStream:
    def __init__(self) -> None:
        self._observers: list[LogObserver] = []
        self._entries: list[LogEntry] = []

    def subscribe(self, observer: LogObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: LogObserver) -> None:
        self._observers.remove(observer)

    def emit(self, entry: LogEntry) -> None:
        self._entries.append(entry)
        for observer in self._observers:
            observer.on_log_entry(entry)

    @property
    def entries(self) -> list[LogEntry]:
        return list(self._entries)

    @property
    def observer_count(self) -> int:
        return len(self._observers)
