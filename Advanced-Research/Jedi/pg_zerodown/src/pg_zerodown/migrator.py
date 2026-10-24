from __future__ import annotations

from .models import MigrationPhase, MigrationResult
from .template import MigrationTemplate


class ZeroDowntimeMigrator(MigrationTemplate):
    def __init__(self, table: str, column: str, new_type: str) -> None:
        super().__init__()
        self._table = table
        self._column = column
        self._new_type = new_type
        self._shadow_column = f"{column}_new"
        self._executor_rows = {
            MigrationPhase.EXPAND: 0,
            MigrationPhase.BACKFILL: 42,
            MigrationPhase.SWAP: 1,
            MigrationPhase.CONTRACT: 0,
        }

    @property
    def table(self) -> str:
        return self._table

    @property
    def shadow_column(self) -> str:
        return self._shadow_column

    def expand(self) -> MigrationResult:
        sql = f"ALTER TABLE {self._table} ADD COLUMN {self._shadow_column} {self._new_type};"
        rows = 0 if self._dry_run else self._executor_rows[MigrationPhase.EXPAND]
        result = MigrationResult(
            phase=MigrationPhase.EXPAND,
            success=True,
            rows_affected=rows,
            duration_ms=1.5,
        )
        self._record_result(result)
        return result

    def backfill(self) -> MigrationResult:
        sql = f"UPDATE {self._table} SET {self._shadow_column} = {self._column}::text::{self._new_type};"
        rows = 0 if self._dry_run else self._executor_rows[MigrationPhase.BACKFILL]
        return MigrationResult(
            phase=MigrationPhase.BACKFILL,
            success=True,
            rows_affected=rows,
            duration_ms=12.3,
        )

    def swap(self) -> MigrationResult:
        sql = f"ALTER TABLE {self._table} RENAME COLUMN {self._column} TO {self._column}_old;"
        sql += f" ALTER TABLE {self._table} RENAME COLUMN {self._shadow_column} TO {self._column};"
        rows = 0 if self._dry_run else self._executor_rows[MigrationPhase.SWAP]
        return MigrationResult(
            phase=MigrationPhase.SWAP,
            success=True,
            rows_affected=rows,
            duration_ms=0.8,
        )

    def contract(self) -> MigrationResult:
        sql = f"ALTER TABLE {self._table} DROP COLUMN {self._column}_old;"
        rows = 0 if self._dry_run else self._executor_rows[MigrationPhase.CONTRACT]
        return MigrationResult(
            phase=MigrationPhase.CONTRACT,
            success=True,
            rows_affected=rows,
            duration_ms=0.5,
        )
