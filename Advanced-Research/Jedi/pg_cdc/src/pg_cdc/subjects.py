"""Subject that emits WAL change events to observers."""

from __future__ import annotations

import logging
from typing import Protocol, runtime_checkable

from pg_cdc.models import ChangeEvent

logger = logging.getLogger(__name__)


@runtime_checkable
class DataObserver(Protocol):
    """Observer interface for CDC events."""

    async def on_change(self, event: ChangeEvent) -> None: ...
    async def on_error(self, error: Exception) -> None: ...


class LogicalReplicationSubject:
    """Subject that manages observers and emits WAL events.
    Usage::
        subject = LogicalReplicationSubject()
        subject.attach(KafkaObserver("broker:9092"))
        subject.attach(ElasticsearchObserver("http://es:9200"))
        await subject.emit(event)
    """

    def __init__(self) -> None:
        self._observers: list[DataObserver] = []
        self._filters: list[str] = []

    def attach(self, observer: DataObserver) -> None:
        self._observers.append(observer)
        logger.info("Attached observer: %s", type(observer).__name__)

    def detach(self, observer: DataObserver) -> None:
        self._observers.remove(observer)
        logger.info("Detached observer: %s", type(observer).__name__)

    def filter_table(self, table_name: str) -> None:
        self._filters.append(table_name)

    async def emit(self, event: ChangeEvent) -> None:
        if self._filters and event.table_name not in self._filters:
            return
        for observer in self._observers:
            try:
                await observer.on_change(event)
            except Exception as e:
                logger.exception("Observer %s failed", type(observer).__name__)
                await observer.on_error(e)

    async def emit_batch(self, events: list[ChangeEvent]) -> None:
        for event in events:
            await self.emit(event)

    @property
    def observer_count(self) -> int:
        return len(self._observers)
