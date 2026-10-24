"""
Mito Message Queue
In-memory and file-backed task queue with priorities and dead letter support
"""

import json
import logging
import time
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
import heapq
import threading
from collections import deque

logger = logging.getLogger("mito.queue")


class MessagePriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


class MessageState(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD = "dead"


@dataclass
class Message:
    id: str
    queue: str
    body: Dict[str, Any]
    priority: MessagePriority = MessagePriority.NORMAL
    state: MessageState = MessageState.PENDING
    created_at: float = field(default_factory=time.time)
    processed_at: float = 0
    attempts: int = 0
    max_attempts: int = 3
    error: str = ""
    delay_until: float = 0
    correlation_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __lt__(self, other):
        return self.priority.value > other.priority.value


class MessageQueue:
    def __init__(self, persist_dir: str = None):
        self.queues: Dict[str, List[Message]] = {}
        self.dead_letters: List[Message] = []
        self.processing: Dict[str, Message] = {}
        self.persist_dir = Path(persist_dir) if persist_dir else None
        self._lock = threading.Lock()
        self._stats = {"enqueued": 0, "dequeued": 0, "completed": 0, "failed": 0}

        if self.persist_dir:
            self.persist_dir.mkdir(parents=True, exist_ok=True)

    def enqueue(self, queue: str, body: Dict[str, Any],
                priority: MessagePriority = MessagePriority.NORMAL,
                delay: float = 0, max_attempts: int = 3,
                correlation_id: str = "", metadata: Dict = None) -> Message:
        msg = Message(
            id=str(uuid.uuid4()),
            queue=queue,
            body=body,
            priority=priority,
            max_attempts=max_attempts,
            delay_until=time.time() + delay if delay > 0 else 0,
            correlation_id=correlation_id,
            metadata=metadata or {},
        )
        with self._lock:
            if queue not in self.queues:
                self.queues[queue] = []
            heapq.heappush(self.queues[queue], msg)
            self._stats["enqueued"] += 1

        if self.persist_dir:
            self._persist_message(msg)

        return msg

    def dequeue(self, queue: str, timeout: float = 0) -> Optional[Message]:
        start = time.time()
        while True:
            with self._lock:
                if queue in self.queues and self.queues[queue]:
                    for i, msg in enumerate(self.queues[queue]):
                        if msg.delay_until <= time.time():
                            msg.state = MessageState.PROCESSING
                            msg.processed_at = time.time()
                            msg.attempts += 1
                            self.queues[queue].pop(i)
                            heapq.heapify(self.queues[queue])
                            self.processing[msg.id] = msg
                            self._stats["dequeued"] += 1
                            return msg

            if timeout <= 0 or time.time() - start > timeout:
                return None
            time.sleep(0.1)

    def complete(self, message_id: str) -> bool:
        with self._lock:
            if message_id in self.processing:
                msg = self.processing.pop(message_id)
                msg.state = MessageState.COMPLETED
                self._stats["completed"] += 1
                return True
        return False

    def fail(self, message_id: str, error: str = "") -> bool:
        with self._lock:
            if message_id not in self.processing:
                return False
            msg = self.processing.pop(message_id)
            msg.error = error

            if msg.attempts < msg.max_attempts:
                msg.state = MessageState.PENDING
                msg.delay_until = time.time() + (2 ** msg.attempts)
                if msg.queue not in self.queues:
                    self.queues[msg.queue] = []
                heapq.heappush(self.queues[msg.queue], msg)
            else:
                msg.state = MessageState.DEAD
                self.dead_letters.append(msg)
                self._stats["failed"] += 1

            return True

    def peek(self, queue: str, limit: int = 10) -> List[Message]:
        with self._lock:
            if queue not in self.queues:
                return []
            return sorted(self.queues[queue], key=lambda m: m.priority.value, reverse=True)[:limit]

    def queue_size(self, queue: str) -> int:
        with self._lock:
            return len(self.queues.get(queue, []))

    def get_dead_letters(self, limit: int = 100) -> List[Message]:
        return self.dead_letters[-limit:]

    def requeue_dead_letter(self, message_id: str) -> bool:
        with self._lock:
            for i, msg in enumerate(self.dead_letters):
                if msg.id == message_id:
                    msg.state = MessageState.PENDING
                    msg.attempts = 0
                    msg.error = ""
                    self.dead_letters.pop(i)
                    if msg.queue not in self.queues:
                        self.queues[msg.queue] = []
                    heapq.heappush(self.queues[msg.queue], msg)
                    return True
        return False

    def purge(self, queue: str) -> int:
        with self._lock:
            if queue in self.queues:
                count = len(self.queues[queue])
                self.queues[queue] = []
                return count
        return 0

    def list_queues(self) -> List[str]:
        return list(self.queues.keys())

    def get_stats(self) -> Dict:
        with self._lock:
            return {
                **self._stats,
                "queues": {q: len(msgs) for q, msgs in self.queues.items()},
                "processing": len(self.processing),
                "dead_letters": len(self.dead_letters),
            }

    def _persist_message(self, message: Message):
        if not self.persist_dir:
            return
        try:
            file_path = self.persist_dir / f"{message.queue}.jsonl"
            with open(file_path, "a") as f:
                f.write(json.dumps(asdict(message)) + "\n")
        except Exception as e:
            logger.error(f"Failed to persist message: {e}")
