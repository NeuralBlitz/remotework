"""Tests for stream_processor."""

from __future__ import annotations

from src.stream_processor import create_event, process_event


def test_create_event():
    event = create_event("topic1", {"key": "value"})
    assert event.topic == "topic1"
    assert event.data["key"] == "value"
    assert event.timestamp > 0


def test_process_event():
    event = create_event("topic1", {"data": "test"})
    result = process_event(event)
    assert result.result["processed"] == "true"


def test_process_event_preserves_topic():
    event = create_event("my_topic", {"x": "y"})
    result = process_event(event)
    assert result.result["topic"] == "my_topic"


def test_create_event_with_empty_data():
    event = create_event("topic", {})
    assert event.data == {}


def test_process_event_with_nested_data():
    event = create_event("topic", {"nested": '{"key": "value"}'})
    result = process_event(event)
    assert result.event.data["nested"] == '{"key": "value"}'


def test_event_timestamp_is_float():
    event = create_event("topic", {})
    assert isinstance(event.timestamp, float)
