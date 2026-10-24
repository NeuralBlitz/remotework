from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from .models import LockHandle, LockType
from .proxy import LockProxy


class LockManager:
    def __init__(self) -> None:
        self._proxy = LockProxy()
        self._namespace: str = "default"

    @property
    def namespace(self) -> str:
        return self._namespace

    @namespace.setter
    def namespace(self, value: str) -> None:
        self._namespace = value

    def _make_id(self, name: str) -> int:
        return hash(f"{self._namespace}:{name}") & 0x7FFFFFFF

    def acquire(self, name: str, owner: str, exclusive: bool = True) -> LockHandle:
        lock_id = self._make_id(name)
        lock_type = LockType.EXCLUSIVE if exclusive else LockType.SHARED
        return self._proxy.acquire(lock_id, owner, lock_type)

    def release(self, name: str, owner: str) -> bool:
        lock_id = self._make_id(name)
        return self._proxy.release(lock_id, owner)

    def is_locked(self, name: str) -> bool:
        lock_id = self._make_id(name)
        return self._proxy.is_held(lock_id)

    @contextmanager
    def lock(self, name: str, owner: str, exclusive: bool = True) -> Iterator[LockHandle]:
        handle = self.acquire(name, owner, exclusive)
        try:
            yield handle
        finally:
            self.release(name, owner)

    @property
    def active_locks(self) -> list[LockHandle]:
        return self._proxy.held_locks
