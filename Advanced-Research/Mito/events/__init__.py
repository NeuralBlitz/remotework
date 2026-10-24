"""
Mito Event Bus
Core event system with typed events, handlers, middleware, and persistence
"""

import asyncio
import json
import logging
import time
import uuid
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime
from collections import defaultdict
from pathlib import Path

logger = logging.getLogger("mito.events")


class EventPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Event:
    id: str
    type: str
    data: Dict[str, Any]
    timestamp: float
    source: str = ""
    priority: EventPriority = EventPriority.NORMAL
    metadata: Dict[str, Any] = field(default_factory=dict)
    correlation_id: str = ""
    ttl: int = 0  # 0 = no expiry

    @classmethod
    def create(cls, event_type: str, data: Dict[str, Any] = None, source: str = "",
               priority: EventPriority = EventPriority.NORMAL, **kwargs) -> "Event":
        return cls(
            id=str(uuid.uuid4()),
            type=event_type,
            data=data or {},
            timestamp=time.time(),
            source=source,
            priority=priority,
            correlation_id=kwargs.get("correlation_id", str(uuid.uuid4())),
            ttl=kwargs.get("ttl", 0),
            metadata=kwargs.get("metadata", {}),
        )

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["priority"] = self.priority.value
        return d

    @classmethod
    def from_dict(cls, data: Dict) -> "Event":
        data["priority"] = EventPriority(data["priority"])
        return cls(**data)

    def is_expired(self) -> bool:
        if self.ttl <= 0:
            return False
        return time.time() > self.timestamp + self.ttl


@dataclass
class EventHandler:
    callback: Callable
    event_types: Set[str]
    priority: int = 0
    is_async: bool = False
    filter_func: Optional[Callable] = None
    name: str = ""

    def matches(self, event: Event) -> bool:
        if "*" not in self.event_types and event.type not in self.event_types:
            return False
        if self.filter_func and not self.filter_func(event):
            return False
        return True


class EventBus:
    def __init__(self, persist_dir: str = None):
        self.handlers: List[EventHandler] = []
        self.history: List[Event] = []
        self.persist_dir = Path(persist_dir) if persist_dir else None
        self._max_history = 10000
        self._middleware: List[Callable] = []
        self._subscribers_by_type: Dict[str, List[EventHandler]] = defaultdict(list)

        if self.persist_dir:
            self.persist_dir.mkdir(parents=True, exist_ok=True)
            self._load_history()

    def subscribe(self, event_types: List[str], callback: Callable, priority: int = 0,
                  name: str = "", filter_func: Callable = None) -> EventHandler:
        handler = EventHandler(
            callback=callback,
            event_types=set(event_types),
            priority=priority,
            is_async=asyncio.iscoroutinefunction(callback),
            filter_func=filter_func,
            name=name or callback.__name__,
        )
        self.handlers.append(handler)
        self.handlers.sort(key=lambda h: h.priority, reverse=True)

        for et in event_types:
            self._subscribers_by_type[et].append(handler)
            self._subscribers_by_type[et].sort(key=lambda h: h.priority, reverse=True)

        logger.debug(f"Subscribed handler '{handler.name}' to {event_types}")
        return handler

    def unsubscribe(self, handler: EventHandler):
        if handler in self.handlers:
            self.handlers.remove(handler)
            for et in handler.event_types:
                if handler in self._subscribers_by_type[et]:
                    self._subscribers_by_type[et].remove(handler)

    def add_middleware(self, middleware: Callable):
        self._middleware.append(middleware)

    def emit(self, event: Event) -> List[Any]:
        if event.is_expired():
            logger.debug(f"Skipping expired event {event.id}")
            return []

        for mw in self._middleware:
            event = mw(event)
            if event is None:
                return []

        self.history.append(event)
        if len(self.history) > self._max_history:
            self.history = self.history[-self._max_history:]

        if self.persist_dir:
            self._persist_event(event)

        results = []
        handlers = self._subscribers_by_type.get(event.type, [])

        wildcard_handlers = self._subscribers_by_type.get("*", [])
        all_handlers = sorted(handlers + wildcard_handlers, key=lambda h: h.priority, reverse=True)

        for handler in all_handlers:
            if handler.matches(event):
                try:
                    result = handler.callback(event)
                    results.append({"handler": handler.name, "result": result})
                except Exception as e:
                    logger.error(f"Handler '{handler.name}' error for {event.type}: {e}")
                    results.append({"handler": handler.name, "error": str(e)})

        return results

    async def emit_async(self, event: Event) -> List[Any]:
        if event.is_expired():
            return []

        for mw in self._middleware:
            event = mw(event)
            if event is None:
                return []

        self.history.append(event)

        results = []
        handlers = self._subscribers_by_type.get(event.type, [])
        wildcard_handlers = self._subscribers_by_type.get("*", [])
        all_handlers = sorted(handlers + wildcard_handlers, key=lambda h: h.priority, reverse=True)

        for handler in all_handlers:
            if handler.matches(event):
                try:
                    if handler.is_async:
                        result = await handler.callback(event)
                    else:
                        result = handler.callback(event)
                    results.append({"handler": handler.name, "result": result})
                except Exception as e:
                    logger.error(f"Async handler '{handler.name}' error: {e}")
                    results.append({"handler": handler.name, "error": str(e)})

        return results

    def emit_simple(self, event_type: str, data: Dict[str, Any] = None, source: str = "",
                    **kwargs) -> List[Any]:
        event = Event.create(event_type, data or {}, source=source, **kwargs)
        return self.emit(event)

    def get_history(self, event_type: str = None, limit: int = 100,
                    since: float = None) -> List[Event]:
        history = self.history
        if event_type:
            history = [e for e in history if e.type == event_type]
        if since:
            history = [e for e in history if e.timestamp >= since]
        return history[-limit:]

    def get_handler_count(self) -> Dict[str, int]:
        return {et: len(handlers) for et, handlers in self._subscribers_by_type.items()}

    def clear_history(self):
        self.history.clear()

    def _persist_event(self, event: Event):
        if not self.persist_dir:
            return
        try:
            date_str = datetime.fromtimestamp(event.timestamp).strftime("%Y-%m-%d")
            file_path = self.persist_dir / f"events-{date_str}.jsonl"
            with open(file_path, "a") as f:
                f.write(json.dumps(event.to_dict()) + "\n")
        except Exception as e:
            logger.error(f"Failed to persist event: {e}")

    def _load_history(self):
        if not self.persist_dir:
            return
        try:
            for file_path in sorted(self.persist_dir.glob("events-*.jsonl"))[-7:]:
                with open(file_path) as f:
                    for line in f:
                        if line.strip():
                            try:
                                data = json.loads(line)
                                self.history.append(Event.from_dict(data))
                            except Exception:
                                pass
        except Exception as e:
            logger.error(f"Failed to load event history: {e}")


class EventStore:
    """Persistent event store backed by JSONL files."""

    def __init__(self, store_dir: str = "data/events"):
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)

    def append(self, event: Event):
        date_str = datetime.fromtimestamp(event.timestamp).strftime("%Y-%m-%d")
        file_path = self.store_dir / f"{date_str}.jsonl"
        with open(file_path, "a") as f:
            f.write(json.dumps(event.to_dict()) + "\n")

    def query(self, event_type: str = None, start: float = None, end: float = None,
              limit: int = 1000) -> List[Event]:
        results = []
        for file_path in sorted(self.store_dir.glob("*.jsonl"), reverse=True):
            with open(file_path) as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        event = Event.from_dict(data)
                        if event_type and event.type != event_type:
                            continue
                        if start and event.timestamp < start:
                            continue
                        if end and event.timestamp > end:
                            continue
                        results.append(event)
                        if len(results) >= limit:
                            return results
                    except Exception:
                        pass
        return results

    def count(self, event_type: str = None) -> int:
        count = 0
        for file_path in self.store_dir.glob("*.jsonl"):
            with open(file_path) as f:
                for line in f:
                    if not line.strip():
                        continue
                    if event_type:
                        try:
                            data = json.loads(line)
                            if data.get("type") == event_type:
                                count += 1
                        except Exception:
                            pass
                    else:
                        count += 1
        return count

    def purge(self, before: float):
        for file_path in self.store_dir.glob("*.jsonl"):
            try:
                date_str = file_path.stem
                file_date = datetime.strptime(date_str, "%Y-%m-%d").timestamp()
                if file_date < before:
                    file_path.unlink()
            except Exception:
                pass


LRS_EVENT_TYPES = {
    "lrs.precision_update": "LRS precision value changed",
    "lrs.tool_execution": "LRS tool was executed",
    "lrs.adaptation": "LRS agent triggered adaptation",
    "lrs.policy_selection": "LRS agent selected a policy",
}


def setup_lrs_event_handlers(
    log_file: str = None,
    forward_to_lrs_logging: bool = False,
) -> List[EventHandler]:
    """
    Subscribe handlers for all LRS-Agents event types.

    If log_file is provided, writes structured JSON to it.
    If forward_to_lrs_logging is True and lrs-agents is installed,
    forwards events to lrs.monitoring.structured_logging.

    Returns the list of registered handlers so you can unsubscribe later.
    """
    handlers = []

    def make_handler(event_type: str):
        def handler(event: Event):
            if log_file:
                try:
                    with open(log_file, "a") as f:
                        f.write(json.dumps(event.to_dict()) + "\n")
                except Exception as e:
                    logger.error(f"Failed to write LRS event to {log_file}: {e}")

            if forward_to_lrs_logging:
                try:
                    from lrs_agents.monitoring.structured_logging import create_logger_for_agent
                    lrs_logger = create_logger_for_agent(event.data.get("agent_name", "unknown"))
                    if event_type == "lrs.precision_update":
                        lrs_logger.log_precision_update(**event.data)
                    elif event_type == "lrs.tool_execution":
                        lrs_logger.log_tool_execution(**{
                            k: v for k, v in event.data.items()
                            if k in ("tool_name", "success", "prediction_error", "latency")
                        })
                    elif event_type == "lrs.adaptation":
                        lrs_logger.log_adaptation_event(**{
                            k: v for k, v in event.data.items()
                            if k in ("level", "old_precision", "new_precision", "trigger")
                        })
                except ImportError:
                    logger.debug("lrs-agents not installed; skipping LRS logging forward")
                except Exception as e:
                    logger.warning(f"LRS logging forward failed: {e}")
        return handler

    bus = get_event_bus()
    for event_type in LRS_EVENT_TYPES:
        h = bus.subscribe([event_type], make_handler(event_type), name=f"lrs_{event_type}")
        handlers.append(h)

    logger.info(f"Registered {len(handlers)} LRS event handlers (log_file={log_file}, forward={forward_to_lrs_logging})")
    return handlers


# Global event bus instance
_global_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    global _global_bus
    if _global_bus is None:
        _global_bus = EventBus()
    return _global_bus


def emit(event_type: str, data: Dict[str, Any] = None, **kwargs) -> List[Any]:
    return get_event_bus().emit_simple(event_type, data, **kwargs)


def subscribe(event_types: List[str], callback: Callable, **kwargs) -> EventHandler:
    return get_event_bus().subscribe(event_types, callback, **kwargs)
