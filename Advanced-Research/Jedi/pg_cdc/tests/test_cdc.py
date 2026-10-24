"""Tests for CDC Observer Pattern."""

from __future__ import annotations

import pytest

from pg_cdc.models import ChangeEvent, ChangeType, WALPosition
from pg_cdc.observers import ElasticsearchObserver, KafkaObserver, TransformObserver
from pg_cdc.subjects import LogicalReplicationSubject


@pytest.fixture
def event() -> ChangeEvent:
    return ChangeEvent(
        table_name="orders",
        change_type=ChangeType.INSERT,
        position=WALPosition(lsn=100),
        new_data={"id": 1, "amount": 100},
    )


class TestLogicalReplicationSubject:
    @pytest.mark.asyncio
    async def test_attach_detach(self) -> None:
        subject = LogicalReplicationSubject()
        obs = KafkaObserver("topic")
        subject.attach(obs)
        assert subject.observer_count == 1
        subject.detach(obs)
        assert subject.observer_count == 0

    @pytest.mark.asyncio
    async def test_emit_reaches_observers(self, event: ChangeEvent) -> None:
        subject = LogicalReplicationSubject()
        kafka = KafkaObserver("topic")
        es = ElasticsearchObserver("idx")
        subject.attach(kafka)
        subject.attach(es)
        await subject.emit(event)
        assert len(kafka.received) == 1
        assert len(es.indexed) == 1

    @pytest.mark.asyncio
    async def test_filter_table(self, event: ChangeEvent) -> None:
        subject = LogicalReplicationSubject()
        kafka = KafkaObserver("topic")
        subject.attach(kafka)
        subject.filter_table("users")
        await subject.emit(event)
        assert len(kafka.received) == 0

    @pytest.mark.asyncio
    async def test_emit_batch(self, event: ChangeEvent) -> None:
        subject = LogicalReplicationSubject()
        kafka = KafkaObserver("topic")
        subject.attach(kafka)
        await subject.emit_batch([event, event])
        assert len(kafka.received) == 2


class TestKafkaObserver:
    @pytest.mark.asyncio
    async def test_receives_events(self, event: ChangeEvent) -> None:
        obs = KafkaObserver("test-topic")
        await obs.on_change(event)
        assert len(obs.received) == 1

    @pytest.mark.asyncio
    async def test_custom_transform(self, event: ChangeEvent) -> None:
        obs = KafkaObserver("topic", transform=lambda e: {"custom": e.table_name})
        await obs.on_change(event)
        assert len(obs.received) == 1


class TestElasticsearchObserver:
    @pytest.mark.asyncio
    async def test_indexes_events(self, event: ChangeEvent) -> None:
        obs = ElasticsearchObserver("cdc")
        await obs.on_change(event)
        assert len(obs.indexed) == 1


class TestTransformObserver:
    @pytest.mark.asyncio
    async def test_transforms_and_passes(self, event: ChangeEvent) -> None:
        kafka = KafkaObserver("topic")
        transform = TransformObserver(
            transform=lambda e: ChangeEvent(
                table_name=e.table_name.upper(),
                change_type=e.change_type,
                position=e.position,
            ),
            next_observer=kafka,
        )
        await transform.on_change(event)
        assert len(kafka.received) == 1
        assert kafka.received[0].table_name == "ORDERS"
