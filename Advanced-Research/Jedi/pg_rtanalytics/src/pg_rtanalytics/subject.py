"""Observer protocol and subject implementation."""

from __future__ import annotations

import logging
from typing import Protocol

from pg_rtanalytics.models import NotificationEvent, ThresholdConfig

logger = logging.getLogger(__name__)


class Observer(Protocol):
    """Protocol for notification observers."""

    def on_notify(self, event: NotificationEvent) -> None: ...

    def on_error(self, error: Exception) -> None: ...


class TableUpdateSubject:
    """Subject that notifies observers on table updates."""

    def __init__(self, config: ThresholdConfig | None = None) -> None:
        self._config = config or ThresholdConfig()
        self._observers: list[Observer] = []
        self._event_count: int = 0

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    @property
    def observer_count(self) -> int:
        return len(self._observers)

    def notify(self, event: NotificationEvent) -> None:
        self._event_count += 1
        for observer in self._observers:
            try:
                observer.on_notify(event)
            except Exception as exc:
                logger.exception("Observer error")
                observer.on_error(exc)

    def process_insert(self, table: str, row_data: dict[str, object]) -> NotificationEvent | None:
        if not self._config.is_watched_table(table):
            return None
        event = NotificationEvent(
            table_name=table,
            event_type=EventType.INSERT,
            row_data=row_data,
            threshold=self._config.min_amount,
        )
        amount = row_data.get("amount", 0)
        if isinstance(amount, (int, float)) and self._config.is_above_threshold(amount):
            self.notify(event)
        return event

    @property
    def event_count(self) -> int:
        return self._event_count


from pg_rtanalytics.models import EventType  # noqa: E402
