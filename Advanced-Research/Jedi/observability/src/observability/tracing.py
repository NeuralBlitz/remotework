from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Span:
    trace_id: str
    span_id: str
    operation: str
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: datetime | None = None
    parent_id: str = ""
    tags: dict[str, str] = field(default_factory=dict)
    logs: list[dict[str, Any]] = field(default_factory=list)
    error: str = ""

    def finish(self) -> None:
        self.end_time = datetime.now(timezone.utc)

    def set_tag(self, key: str, value: str) -> None:
        self.tags[key] = value

    def log(self, message: str, **fields: Any) -> None:
        self.logs.append({"message": message, **fields})

    @property
    def duration_ms(self) -> float | None:
        if self.end_time is None:
            return None
        delta = self.end_time - self.start_time
        return delta.total_seconds() * 1000


class Tracer:
    def __init__(self) -> None:
        self._spans: list[Span] = []
        self._trace_counter: int = 0
        self._span_counter: int = 0

    def start_trace(self, operation: str) -> Span:
        self._trace_counter += 1
        self._span_counter += 1
        span = Span(
            trace_id=f"trace-{self._trace_counter}",
            span_id=f"span-{self._span_counter}",
            operation=operation,
        )
        self._spans.append(span)
        return span

    def start_child_span(self, parent: Span, operation: str) -> Span:
        self._span_counter += 1
        span = Span(
            trace_id=parent.trace_id,
            span_id=f"span-{self._span_counter}",
            operation=operation,
            parent_id=parent.span_id,
        )
        self._spans.append(span)
        return span

    def get_spans_for_trace(self, trace_id: str) -> list[Span]:
        return [s for s in self._spans if s.trace_id == trace_id]

    def get_error_spans(self) -> list[Span]:
        return [s for s in self._spans if s.error]

    @property
    def span_count(self) -> int:
        return len(self._spans)
