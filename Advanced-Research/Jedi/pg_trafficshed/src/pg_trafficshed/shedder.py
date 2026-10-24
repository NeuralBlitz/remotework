from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import QueryRequest, QueryResponse, ShedderStats
from .decorators import CircuitBreakerDecorator, RateLimitDecorator


class TrafficShedder:
    def __init__(self, max_rps: float = 100.0, failure_threshold: int = 5) -> None:
        self._rate_limiter = RateLimitDecorator(max_rps=max_rps)
        self._circuit_breaker = CircuitBreakerDecorator(failure_threshold=failure_threshold)
        self._stats_calls = 0

    @property
    def rate_limiter(self) -> RateLimitDecorator:
        return self._rate_limiter

    @property
    def circuit_breaker(self) -> CircuitBreakerDecorator:
        return self._circuit_breaker

    def should_accept(self) -> bool:
        if not self._circuit_breaker.allow():
            return False
        if not self._rate_limiter.allow():
            return False
        return True

    def handle(self, request: QueryRequest) -> QueryResponse:
        from .models import QueryResponse, ShedderStats

        self._stats_calls += 1
        if not self._circuit_breaker.allow():
            return QueryResponse(success=False, rejected=True, error="Circuit breaker open")
        if not self._rate_limiter.allow():
            return QueryResponse(success=False, rejected=True, error="Rate limit exceeded")
        return QueryResponse(success=True, rows=[], duration_ms=3.0)

    def record_outcome(self, success: bool) -> None:
        if success:
            self._circuit_breaker.record_success()
        else:
            self._circuit_breaker.record_failure()

    def get_stats(self) -> ShedderStats:
        from .models import ShedderStats

        return ShedderStats(
            total_requests=self._stats_calls,
            accepted=self._stats_calls - self._rate_limiter.rejected_count,
            rejected=self._rate_limiter.rejected_count,
            circuit_trips=self._circuit_breaker.trip_count,
        )
