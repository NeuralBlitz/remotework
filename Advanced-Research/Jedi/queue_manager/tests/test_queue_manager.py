"""Tests for queue_manager."""
from __future__ import annotations

from src.queue_manager import create_message, create_queue, enqueue


def test_create_message():
    msg = create_message("m1", {"data": "test"})
    assert msg.id == "m1"
    assert msg.payload["data"] == "test"
    assert msg.priority == 0

def test_create_message_with_priority():
    msg = create_message("m1", {"data": "test"}, priority=5)
    assert msg.priority == 5

def test_create_queue():
    queue = create_queue("my_queue")
    assert queue.name == "my_queue"
    assert len(queue.messages) == 0

def test_enqueue():
    queue = create_queue("q1")
    msg = create_message("m1", {"x": 1})
    result = enqueue(queue, msg)
    assert len(result.messages) == 1

def test_enqueue_multiple():
    queue = create_queue("q1")
    for i in range(3):
        queue = enqueue(queue, create_message(f"m{i}", {"i": i}))
    assert len(queue.messages) == 3

def test_message_order():
    queue = create_queue("q1")
    queue = enqueue(queue, create_message("first", {"order": 1}))
    queue = enqueue(queue, create_message("second", {"order": 2}))
    assert queue.messages[0].id == "first"
    assert queue.messages[1].id == "second"
