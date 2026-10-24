"""Queue management utilities."""
from __future__ import annotations

from .models import Message, Queue

__all__ = ["Message", "Queue", "create_message", "create_queue", "enqueue"]

def create_message(msg_id: str, payload: dict[str, str], priority: int = 0) -> Message:
    return Message(id=msg_id, payload=payload, priority=priority)

def create_queue(name: str) -> Queue:
    return Queue(name=name, messages=[])

def enqueue(queue: Queue, message: Message) -> Queue:
    queue.messages.append(message)
    return queue
