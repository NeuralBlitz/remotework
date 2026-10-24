import pytest
from datetime import datetime, timezone
from event_driven.bus import EventBus, Event
from event_driven.handlers import EventHandler, HandlerRegistry
from event_driven.store import EventStore, StoredEvent


def test_event_creation() -> None:
    e = Event(event_type="user.created", payload={"user_id": 1})
    assert e.event_type == "user.created"
    assert e.payload["user_id"] == 1


def test_event_to_dict() -> None:
    e = Event(event_type="order.placed", payload={"total": 100})
    d = e.to_dict()
    assert d["event_type"] == "order.placed"
    assert "timestamp" in d


def test_bus_subscribe_and_publish() -> None:
    bus = EventBus()
    received: list[Event] = []
    bus.subscribe("test", lambda e: received.append(e))
    e = Event(event_type="test")
    count = bus.publish(e)
    assert count == 1
    assert len(received) == 1


def test_bus_multiple_subscribers() -> None:
    bus = EventBus()
    results: list[str] = []
    bus.subscribe("evt", lambda e: results.append("a"))
    bus.subscribe("evt", lambda e: results.append("b"))
    bus.publish(Event(event_type="evt"))
    assert sorted(results) == ["a", "b"]


def test_bus_unsubscribe() -> None:
    bus = EventBus()
    handler = lambda e: None
    bus.subscribe("evt", handler)
    assert bus.get_subscriber_count("evt") == 1
    assert bus.unsubscribe("evt", handler)
    assert bus.get_subscriber_count("evt") == 0


def test_bus_unsubscribe_missing() -> None:
    bus = EventBus()
    assert not bus.unsubscribe("evt", lambda e: None)


def test_bus_no_subscribers() -> None:
    bus = EventBus()
    assert bus.publish(Event(event_type="none")) == 0


def test_bus_published_count() -> None:
    bus = EventBus()
    bus.publish(Event(event_type="a"))
    bus.publish(Event(event_type="b"))
    assert bus.published_count == 2


def test_bus_event_types() -> None:
    bus = EventBus()
    bus.subscribe("a", lambda e: None)
    bus.subscribe("b", lambda e: None)
    assert sorted(bus.event_types) == ["a", "b"]


class TestHandler(EventHandler):
    def __init__(self) -> None:
        self.handled: list[Event] = []

    def handle(self, event: Event) -> str:
        self.handled.append(event)
        return "ok"


def test_handler_registry_register() -> None:
    reg = HandlerRegistry()
    h = TestHandler()
    reg.register("evt", h)
    assert reg.handler_count == 1


def test_handler_registry_dispatch() -> None:
    reg = HandlerRegistry()
    h = TestHandler()
    reg.register("evt", h)
    e = Event(event_type="evt")
    results = reg.dispatch(e)
    assert results == ["ok"]
    assert len(h.handled) == 1


def test_handler_registry_unregister() -> None:
    reg = HandlerRegistry()
    h = TestHandler()
    reg.register("evt", h)
    assert reg.unregister("evt", h)
    assert reg.handler_count == 0


def test_handler_registry_registered_types() -> None:
    reg = HandlerRegistry()
    reg.register("a", TestHandler())
    reg.register("b", TestHandler())
    assert sorted(reg.registered_types) == ["a", "b"]


def test_event_store_append() -> None:
    store = EventStore()
    stored = store.append("e1", "user.created", {"id": 1})
    assert stored.sequence == 1
    assert store.count == 1


def test_event_store_get_by_id() -> None:
    store = EventStore()
    store.append("e1", "type1", {})
    assert store.get_by_id("e1") is not None
    assert store.get_by_id("missing") is None


def test_event_store_get_by_type() -> None:
    store = EventStore()
    store.append("e1", "type1", {})
    store.append("e2", "type2", {})
    store.append("e3", "type1", {})
    assert len(store.get_by_type("type1")) == 2


def test_event_store_get_after_sequence() -> None:
    store = EventStore()
    store.append("e1", "t", {})
    store.append("e2", "t", {})
    store.append("e3", "t", {})
    assert len(store.get_after_sequence(1)) == 2


def test_event_store_get_range() -> None:
    store = EventStore()
    store.append("e1", "t", {})
    store.append("e2", "t", {})
    store.append("e3", "t", {})
    assert len(store.get_range(1, 2)) == 2


def test_event_store_latest_sequence() -> None:
    store = EventStore()
    store.append("e1", "t", {})
    store.append("e2", "t", {})
    assert store.latest_sequence == 2
