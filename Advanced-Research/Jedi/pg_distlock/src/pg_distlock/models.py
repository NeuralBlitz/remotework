from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol


class LockType(Enum):
    SHARED = "shared"
    EXCLUSIVE = "exclusive"


@dataclass
class LockHandle:
    lock_id: int
    lock_type: LockType
    owner: str
    acquired: bool = False
    timeout_seconds: float = 30.0


@dataclass
class LockStats:
    total_acquired: int = 0
    total_released: int = 0
    total_timeouts: int = 0
    total_conflicts: int = 0


class LockBackend(Protocol):
    def try_acquire(self, lock_id: int, shared: bool) -> bool: ...
    def release(self, lock_id: int) -> bool: ...
    def is_held(self, lock_id: int) -> bool: ...
