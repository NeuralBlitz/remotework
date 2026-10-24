from pg_trafficshed.decorators import CircuitBreakerDecorator, RateLimitDecorator
from pg_trafficshed.models import QueryRequest
from pg_trafficshed.shedder import TrafficShedder


def test_rate_limiter_allows_within_limit() -> None:
    rl = RateLimitDecorator(max_rps=1000.0)
    assert rl.allow()


def test_rate_limiter_rejects_when_exhausted() -> None:
    rl = RateLimitDecorator(max_rps=1.0)
    rl.allow()
    assert not rl.allow()
    assert rl.rejected_count == 1


def test_circuit_breaker_starts_closed() -> None:
    cb = CircuitBreakerDecorator(failure_threshold=3)
    assert cb.state == "closed"
    assert cb.allow()


def test_circuit_breaker_trips_open() -> None:
    cb = CircuitBreakerDecorator(failure_threshold=3)
    cb.record_failure()
    cb.record_failure()
    cb.record_failure()
    assert cb.state == "open"
    assert not cb.allow()


def test_circuit_breaker_reset_on_success() -> None:
    cb = CircuitBreakerDecorator(failure_threshold=3)
    cb.record_failure()
    cb.record_failure()
    cb.record_success()
    assert cb.failure_count == 0
    assert cb.state == "closed"


def test_shedder_accepts_when_healthy() -> None:
    shed = TrafficShedder(max_rps=1000.0)
    assert shed.should_accept()


def test_shedder_rejects_when_circuit_open() -> None:
    shed = TrafficShedder(max_rps=1000.0, failure_threshold=2)
    shed.record_outcome(False)
    shed.record_outcome(False)
    assert not shed.should_accept()


def test_shedder_handle_rejects_on_rate_limit() -> None:
    shed = TrafficShedder(max_rps=1.0)
    req = QueryRequest(sql="SELECT 1", database="db")
    r1 = shed.handle(req)
    assert r1.success
    r2 = shed.handle(req)
    assert r2.rejected


def test_shedder_stats() -> None:
    shed = TrafficShedder(max_rps=1000.0)
    shed.handle(QueryRequest(sql="SELECT 1", database="db"))
    stats = shed.get_stats()
    assert stats.total_requests == 1
