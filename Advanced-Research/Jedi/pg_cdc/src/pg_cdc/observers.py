"""Concrete observer implementations for CDC."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from pg_cdc.models import ChangeEvent

logger = logging.getLogger(__name__)


class KafkaObserver:
    """Sends change events to a Kafka topic."""

    def __init__(
        self, topic: str, transform: Callable[[ChangeEvent], dict[str, Any]] | None = None
    ) -> None:
        self.topic = topic
        self._transform = transform
        self._received: list[ChangeEvent] = []

    async def on_change(self, event: ChangeEvent) -> None:
        self._received.append(event)
        if self._transform:
            payload = self._transform(event)
        else:
            payload = {"table": event.table_name, "type": event.change_type.value}
        logger.info("Kafka -> %s: %s", self.topic, payload)

    async def on_error(self, error: Exception) -> None:
        logger.error("Kafka observer error: %s", error)

    @property
    def received(self) -> list[ChangeEvent]:
        return list(self._received)


class ElasticsearchObserver:
    """Indexes change events in Elasticsearch."""

    def __init__(self, index_prefix: str) -> None:
        self.index_prefix = index_prefix
        self._indexed: list[ChangeEvent] = []

    async def on_change(self, event: ChangeEvent) -> None:
        self._indexed.append(event)
        index = f"{self.index_prefix}_{event.table_name}"
        logger.info("ES -> %s: %s", index, event.change_type.value)

    async def on_error(self, error: Exception) -> None:
        logger.error("ES observer error: %s", error)

    @property
    def indexed(self) -> list[ChangeEvent]:
        return list(self._indexed)


class TransformObserver:
    """Applies a transformation function to each event before passing downstream."""

    def __init__(
        self, transform: Callable[[ChangeEvent], ChangeEvent], next_observer: Any = None
    ) -> None:
        self._transform = transform
        self._next = next_observer

    async def on_change(self, event: ChangeEvent) -> None:
        transformed = self._transform(event)
        if self._next:
            await self._next.on_change(transformed)

    async def on_error(self, error: Exception) -> None:
        logger.error("Transform observer error: %s", error)
        if self._next:
            await self._next.on_error(error)
