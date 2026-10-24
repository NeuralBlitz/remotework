from __future__ import annotations

from .models import LockHandle, LockStats, LockType


class LockProxy:
    def __init__(self) -> None:
        self._held_locks: dict[int, LockHandle] = {}
        self._stats = LockStats()
        self._shared_holders: dict[int, set[str]] = {}

    @property
    def stats(self) -> LockStats:
        return self._stats

    @property
    def held_locks(self) -> list[LockHandle]:
        return list(self._held_locks.values())

    def acquire(
        self, lock_id: int, owner: str, lock_type: LockType = LockType.EXCLUSIVE
    ) -> LockHandle:
        if lock_type == LockType.SHARED:
            return self._acquire_shared(lock_id, owner)
        return self._acquire_exclusive(lock_id, owner)

    def _acquire_shared(self, lock_id: int, owner: str) -> LockHandle:
        existing = self._held_locks.get(lock_id)
        if existing and existing.lock_type == LockType.EXCLUSIVE and existing.owner != owner:
            self._stats = LockStats(
                total_acquired=self._stats.total_acquired,
                total_released=self._stats.total_released,
                total_timeouts=self._stats.total_timeouts,
                total_conflicts=self._stats.total_conflicts + 1,
            )
            raise RuntimeError(f"Lock {lock_id} held exclusively by {existing.owner}")

        if lock_id not in self._shared_holders:
            self._shared_holders[lock_id] = set()
        self._shared_holders[lock_id].add(owner)

        handle = LockHandle(lock_id=lock_id, lock_type=LockType.SHARED, owner=owner, acquired=True)
        self._held_locks[lock_id] = handle
        self._stats = LockStats(
            total_acquired=self._stats.total_acquired + 1,
            total_released=self._stats.total_released,
            total_timeouts=self._stats.total_timeouts,
            total_conflicts=self._stats.total_conflicts,
        )
        return handle

    def _acquire_exclusive(self, lock_id: int, owner: str) -> LockHandle:
        existing = self._held_locks.get(lock_id)
        if existing and existing.acquired and existing.owner != owner:
            self._stats = LockStats(
                total_acquired=self._stats.total_acquired,
                total_released=self._stats.total_released,
                total_timeouts=self._stats.total_timeouts,
                total_conflicts=self._stats.total_conflicts + 1,
            )
            raise RuntimeError(f"Lock {lock_id} already held by {existing.owner}")

        handle = LockHandle(
            lock_id=lock_id, lock_type=LockType.EXCLUSIVE, owner=owner, acquired=True
        )
        self._held_locks[lock_id] = handle
        self._stats = LockStats(
            total_acquired=self._stats.total_acquired + 1,
            total_released=self._stats.total_released,
            total_timeouts=self._stats.total_timeouts,
            total_conflicts=self._stats.total_conflicts,
        )
        return handle

    def release(self, lock_id: int, owner: str) -> bool:
        handle = self._held_locks.get(lock_id)
        if handle is None or handle.owner != owner:
            return False
        del self._held_locks[lock_id]
        self._shared_holders.pop(lock_id, None)
        self._stats = LockStats(
            total_acquired=self._stats.total_acquired,
            total_released=self._stats.total_released + 1,
            total_timeouts=self._stats.total_timeouts,
            total_conflicts=self._stats.total_conflicts,
        )
        return True

    def is_held(self, lock_id: int) -> bool:
        handle = self._held_locks.get(lock_id)
        return handle is not None and handle.acquired
