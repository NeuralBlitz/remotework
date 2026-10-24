"""Command pattern implementation for migrations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pg_schemaev.models import Migration, MigrationStatus


@dataclass
class MigrationCommand:
    """Command that applies or rolls back a migration."""

    migration: Migration
    _applied: bool = False

    def execute(self) -> dict[str, Any]:
        self.migration.mark_applied()
        self._applied = True
        return {
            "migration_id": self.migration.migration_id,
            "status": "applied",
            "sql": self.migration.up_sql,
        }

    def undo(self) -> dict[str, Any]:
        if not self._applied:
            raise RuntimeError("Cannot undo a command that was not executed")
        self.migration.mark_rolled_back()
        self._applied = False
        return {
            "migration_id": self.migration.migration_id,
            "status": "rolled_back",
            "sql": self.migration.down_sql,
        }

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.migration.up_sql.strip():
            errors.append("up_sql cannot be empty")
        if not self.migration.down_sql.strip():
            errors.append("down_sql cannot be empty")
        if not self.migration.migration_id:
            errors.append("migration_id is required")
        return errors

    @property
    def was_applied(self) -> bool:
        return self._applied


@dataclass
class CommandHistory:
    """Tracks execution history of migration commands."""

    _history: list[MigrationCommand] = field(default_factory=list)
    _undo_stack: list[MigrationCommand] = field(default_factory=list)

    def record(self, command: MigrationCommand) -> None:
        self._history.append(command)
        if command.was_applied:
            self._undo_stack.append(command)

    def pop_undo(self) -> MigrationCommand | None:
        if not self._undo_stack:
            return None
        cmd = self._undo_stack.pop()
        return cmd

    @property
    def applied_count(self) -> int:
        return sum(1 for c in self._history if c.migration.is_applied)

    @property
    def total_count(self) -> int:
        return len(self._history)

    @property
    def pending_count(self) -> int:
        return sum(1 for c in self._history if c.migration.status == MigrationStatus.PENDING)

    def get_by_status(self, status: MigrationStatus) -> list[MigrationCommand]:
        return [c for c in self._history if c.migration.status == status]

    def clear(self) -> None:
        self._history.clear()
        self._undo_stack.clear()
