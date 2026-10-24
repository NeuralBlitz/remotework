from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import QueryRequest, QueryResponse, ShedderStats


class QueryDecorator(ABC):
    def __init__(self, handler: object | None = None) -> None:
        self._handler = handler

    @abstractmethod
    def handle(self, request: QueryRequest) -> QueryResponse: ...


class RateLimitDecorator(QueryDecorator):
    def __init__(self, max_rps: float = 100.0, handler: object | None = None) -> None:
        super().__init__(handler)
        self._max_rps = max_rps
        self._tokens = max_rps
        self._last_refill = time.time()
        self._rejected_count = 0

    @property
    def rejected_count(self) -> int:
        return self._rejected_count

    @property
    def max_rps(self) -> float:
        return self._max_rps

    def _refill_tokens(self) -> None:
        now = time.time()
        elapsed = now - self._last_refill
        self._tokens = min(self._max_rps, self._tokens + elapsed * self._max_rps)
        self._last_refill = now

    def handle(self, request: QueryRequest) -> QueryResponse:
        from .models import QueryResponse

        self._refill_tokens()
        if self._tokens >= 1.0:
            self._tokens -= 1.0
            return QueryResponse(success=True, rows=[], duration_ms=1.0)
        self._rejected_count += 1
        return QueryResponse(success=False, rejected=True, error="Rate limit exceeded")

    def allow(self) -> bool:
        self._refill_tokens()
        if self._tokens >= 1.0:
            self._tokens -= 1.0
            return True
        self._rejected_count += 1
        return False


class CircuitBreakerDecorator(QueryDecorator):
    def __init__(
        self, failure_threshold: int = 5, reset_timeout: float = 30.0, handler: object | None = None
    ) -> None:
        super().__init__(handler)
        self._failure_threshold = failure_threshold
        self._reset_timeout = reset_timeout
        self._failure_count = 0
        self._last_failure_time = 0.0
        self._state = "closed"
        self._trip_count = 0

    @property
    def state(self) -> str:
        if self._state == "open":
            if time.time() - self._last_failure_time >= self._reset_timeout:
                self._state = "half_open"
        return self._state

    @property
    def failure_count(self) -> int:
        return self._failure_count

    @property
    def trip_count(self) -> int:
        return self._trip_count

    def record_success(self) -> None:
        self._failure_count = 0
        self._state = "closed"

    def record_failure(self) -> None:
        self._failure_count += 1
        self._last_failure_time = time.time()
        if self._failure_count >= self._failure_threshold:
            self._state = "open"
            self._trip_count += 1

    def allow(self) -> bool:
        return self.state != "open"

    def handle(self, request: QueryRequest) -> QueryResponse:
        from .models import QueryResponse

        if not self.allow():
            return QueryResponse(success=False, rejected=True, error="Circuit breaker open")
        return QueryResponse(success=True, rows=[], duration_ms=2.0)
