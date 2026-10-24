from __future__ import annotations

import pytest

from pg_pooler.bridge import PgBouncerBackend, PgpoolBackend
from pg_pooler.models import PoolConfig, PoolStats
from pg_pooler.pool import ConnectionPool, PoolExhaustedError


def _make_pool(max_size: int = 3) -> ConnectionPool:
    config = PoolConfig(min_size=0, max_size=max_size, timeout=0.5)
    return ConnectionPool(config, PgBouncerBackend())


def test_acquire_creates_connection() -> None:
    pool = _make_pool()
    conn = pool.acquire()
    assert conn.active is True
    assert conn.backend == "pgbouncer"
    assert conn.conn_id == "conn_1"


def test_release_returns_to_idle() -> None:
    pool = _make_pool()
    conn = pool.acquire()
    pool.release(conn)
    stats = pool.stats()
    assert stats.idle == 1
    assert stats.active == 0


def test_acquire_reuses_idle() -> None:
    pool = _make_pool()
    c1 = pool.acquire()
    pool.release(c1)
    c2 = pool.acquire()
    assert c1.conn_id == c2.conn_id


def test_pool_exhaustion() -> None:
    pool = _make_pool(max_size=1)
    pool.acquire()
    with pytest.raises(PoolExhaustedError):
        pool.acquire()


def test_pool_stats() -> None:
    pool = _make_pool()
    c1 = pool.acquire()
    pool.acquire()
    stats = pool.stats()
    assert stats.active == 2
    pool.release(c1)
    stats = pool.stats()
    assert stats.active == 1
    assert stats.idle == 1


def test_pool_utilization() -> None:
    s = PoolStats(total=10, active=5, idle=5)
    assert s.utilization == 0.5
    assert PoolStats().utilization == 0.0


def test_backend_switching() -> None:
    pool = _make_pool()
    assert pool.backend.backend_name == "pgbouncer"
    c1 = pool.acquire()
    pool.release(c1)
    pool.switch_backend(PgpoolBackend())
    assert pool.backend.backend_name == "pgpool"
    c2 = pool.acquire()
    assert c2.backend == "pgpool"


def test_pool_config_validation() -> None:
    with pytest.raises(ValueError):
        PoolConfig(min_size=-1)
    with pytest.raises(ValueError):
        PoolConfig(max_size=0)
    with pytest.raises(ValueError):
        PoolConfig(min_size=5, max_size=2)


def test_release_unknown_connection() -> None:
    pool = _make_pool()
    from pg_pooler.models import ConnectionInfo

    fake = ConnectionInfo(conn_id="fake", backend="x")
    pool.release(fake)  # should not raise
    assert pool.stats().total == 0
