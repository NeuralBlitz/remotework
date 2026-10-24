from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol


class MigrationPhase(Enum):
    EXPAND = "expand"
    BACKFILL = "backfill"
    SWAP = "swap"
    CONTRACT = "contract"
    DONE = "done"


@dataclass
class MigrationStep:
    phase: MigrationPhase
    description: str
    sql: str
    reversible: bool = True


@dataclass
class MigrationResult:
    phase: MigrationPhase
    success: bool
    rows_affected: int = 0
    duration_ms: float = 0.0
    error: str | None = None


class MigrationExecutor(Protocol):
    def execute(self, sql: str) -> int: ...
    def dry_run(self, sql: str) -> int: ...
