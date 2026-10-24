from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class SyncStatus(Enum):
    IDLE = "idle"
    SYNCING = "syncing"
    CONFLICT = "conflict"
    SYNCED = "synced"


@dataclass
class RegionNode:
    name: str
    endpoint: str
    active: bool = True
    last_sync: float = 0.0
    lag_ms: float = 0.0


@dataclass
class SyncEvent:
    source: str
    target: str
    status: SyncStatus
    records_synced: int = 0
    conflict_key: str | None = None


@dataclass
class SyncConfig:
    max_lag_ms: float = 1000.0
    batch_size: int = 100
    retry_count: int = 3
