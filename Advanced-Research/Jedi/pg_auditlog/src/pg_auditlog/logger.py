"""Audit log storage and querying."""

from __future__ import annotations

from pg_auditlog.models import AuditAction, AuditEntry


class AuditLogger:
    """Stores and queries audit trail entries."""

    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def record(self, entry: AuditEntry) -> None:
        self._entries.append(entry)

    @property
    def entries(self) -> list[AuditEntry]:
        return list(self._entries)

    @property
    def count(self) -> int:
        return len(self._entries)

    def query(
        self,
        *,
        table_name: str | None = None,
        action: AuditAction | None = None,
        user_id: str | None = None,
    ) -> list[AuditEntry]:
        results = self._entries
        if table_name is not None:
            results = [e for e in results if e.table_name == table_name]
        if action is not None:
            results = [e for e in results if e.action == action]
        if user_id is not None:
            results = [e for e in results if e.user_id == user_id]
        return results

    def clear(self) -> None:
        self._entries.clear()

    def entries_for_table(self, table_name: str) -> list[AuditEntry]:
        return self.query(table_name=table_name)

    def entries_by_user(self, user_id: str) -> list[AuditEntry]:
        return self.query(user_id=user_id)

    def write_entries(self) -> list[AuditEntry]:
        return [e for e in self._entries if e.is_write]
