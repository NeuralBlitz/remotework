import pytest
from pg_distlock.manager import LockManager
from pg_distlock.models import LockType
from pg_distlock.proxy import LockProxy


def test_proxy_acquire_exclusive() -> None:
    proxy = LockProxy()
    handle = proxy.acquire(1, "owner1")
    assert handle.acquired
    assert proxy.is_held(1)


def test_proxy_release() -> None:
    proxy = LockProxy()
    proxy.acquire(1, "owner1")
    assert proxy.release(1, "owner1")
    assert not proxy.is_held(1)


def test_proxy_conflict_raises() -> None:
    proxy = LockProxy()
    proxy.acquire(1, "owner1")
    with pytest.raises(RuntimeError):
        proxy.acquire(1, "owner2")


def test_proxy_shared_locks() -> None:
    proxy = LockProxy()
    h1 = proxy.acquire(1, "owner1", LockType.SHARED)
    h2 = proxy.acquire(1, "owner2", LockType.SHARED)
    assert h1.acquired and h2.acquired


def test_manager_acquire_and_release() -> None:
    mgr = LockManager()
    handle = mgr.acquire("my-lock", "worker1")
    assert handle.acquired
    assert mgr.is_locked("my-lock")
    mgr.release("my-lock", "worker1")
    assert not mgr.is_locked("my-lock")


def test_manager_context_manager() -> None:
    mgr = LockManager()
    with mgr.lock("my-lock", "worker1") as handle:
        assert handle.acquired
        assert mgr.is_locked("my-lock")
    assert not mgr.is_locked("my-lock")


def test_manager_namespace_isolation() -> None:
    mgr = LockManager()
    mgr.namespace = "ns1"
    mgr.acquire("lock1", "w1")
    mgr.namespace = "ns2"
    assert not mgr.is_locked("lock1")
