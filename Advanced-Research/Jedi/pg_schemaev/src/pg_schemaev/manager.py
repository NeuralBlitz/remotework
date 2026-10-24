"""Schema migration manager."""

from __future__ import annotations

from typing import Any

from pg_schemaev.commands import CommandHistory, MigrationCommand
from pg_schemaev.models import Migration, MigrationStatus


class SchemaManager:
    """Manages schema migrations using the Command pattern."""

    def __init__(self) -> None:
        self._migrations: dict[str, Migration] = {}
        self._history = CommandHistory()
        self._execution_order: list[str] = []

    def register(self, migration: Migration) -> None:
        self._migrations[migration.migration_id] = migration

    def apply(self, migration_id: str) -> dict[str, Any]:
        migration = self._migrations.get(migration_id)
        if migration is None:
            raise ValueError(f"Unknown migration: {migration_id}")
        if migration.is_applied:
            raise RuntimeError(f"Migration {migration_id} already applied")

        command = MigrationCommand(migration=migration)
        errors = command.validate()
        if errors:
            migration.mark_failed()
            raise ValueError(f"Validation failed: {'; '.join(errors)}")

        result = command.execute()
        self._history.record(command)
        self._execution_order.append(migration_id)
        return result

    def rollback(self, migration_id: str) -> dict[str, Any]:
        migration = self._migrations.get(migration_id)
        if migration is None:
            raise ValueError(f"Unknown migration: {migration_id}")
        if not migration.can_rollback:
            raise RuntimeError(f"Migration {migration_id} cannot be rolled back")

        command = MigrationCommand(migration=migration, _applied=True)
        result = command.undo()
        self._history.record(command)
        if migration_id in self._execution_order:
            self._execution_order.remove(migration_id)
        return result

    def status(self, migration_id: str) -> MigrationStatus:
        migration = self._migrations.get(migration_id)
        if migration is None:
            raise ValueError(f"Unknown migration: {migration_id}")
        return migration.status

    def apply_all(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for mid in sorted(self._migrations.keys()):
            m = self._migrations[mid]
            if not m.is_applied:
                results.append(self.apply(mid))
        return results

    def rollback_all(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for mid in reversed(self._execution_order):
            results.append(self.rollback(mid))
        return results

    @property
    def applied_migrations(self) -> list[str]:
        return [mid for mid, m in self._migrations.items() if m.is_applied]

    @property
    def pending_migrations(self) -> list[str]:
        return [mid for mid, m in self._migrations.items() if m.status == MigrationStatus.PENDING]

    @property
    def migration_count(self) -> int:
        return len(self._migrations)

    @property
    def history(self) -> CommandHistory:
        return self._history
