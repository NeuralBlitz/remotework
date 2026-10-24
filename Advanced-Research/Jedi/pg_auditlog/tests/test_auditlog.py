"""Tests for pg_auditlog."""

from __future__ import annotations

import pytest

from pg_auditlog.decorators import AuditDecorator
from pg_auditlog.logger import AuditLogger
from pg_auditlog.models import AuditAction, AuditEntry


class TestAuditEntry:
    def test_creation(self) -> None:
        entry = AuditEntry(
            action=AuditAction.INSERT,
            table_name="users",
            user_id="admin",
        )
        assert entry.action == AuditAction.INSERT
        assert entry.table_name == "users"

    def test_is_write(self) -> None:
        assert AuditEntry(action=AuditAction.INSERT, table_name="t", user_id="u").is_write
        assert AuditEntry(action=AuditAction.UPDATE, table_name="t", user_id="u").is_write
        assert AuditEntry(action=AuditAction.DELETE, table_name="t", user_id="u").is_write
        assert not AuditEntry(action=AuditAction.SELECT, table_name="t", user_id="u").is_write

    def test_summary(self) -> None:
        entry = AuditEntry(
            action=AuditAction.INSERT,
            table_name="orders",
            user_id="alice",
            row_id="42",
        )
        assert entry.summary == "INSERT orders id=42 by=alice"

    def test_frozen(self) -> None:
        entry = AuditEntry(action=AuditAction.INSERT, table_name="t", user_id="u")
        with pytest.raises(AttributeError):
            entry.table_name = "other"  # type: ignore[misc]


class TestAuditLogger:
    def test_record_and_count(self) -> None:
        logger = AuditLogger()
        entry = AuditEntry(action=AuditAction.INSERT, table_name="t", user_id="u")
        logger.record(entry)
        assert logger.count == 1

    def test_query_by_table(self) -> None:
        logger = AuditLogger()
        logger.record(AuditEntry(action=AuditAction.INSERT, table_name="orders", user_id="u1"))
        logger.record(AuditEntry(action=AuditAction.INSERT, table_name="users", user_id="u2"))
        assert len(logger.query(table_name="orders")) == 1

    def test_query_by_action(self) -> None:
        logger = AuditLogger()
        logger.record(AuditEntry(action=AuditAction.INSERT, table_name="t", user_id="u"))
        logger.record(AuditEntry(action=AuditAction.DELETE, table_name="t", user_id="u"))
        assert len(logger.query(action=AuditAction.DELETE)) == 1

    def test_query_by_user(self) -> None:
        logger = AuditLogger()
        logger.record(AuditEntry(action=AuditAction.INSERT, table_name="t", user_id="alice"))
        logger.record(AuditEntry(action=AuditAction.INSERT, table_name="t", user_id="bob"))
        assert len(logger.query(user_id="alice")) == 1

    def test_clear(self) -> None:
        logger = AuditLogger()
        logger.record(AuditEntry(action=AuditAction.INSERT, table_name="t", user_id="u"))
        logger.clear()
        assert logger.count == 0

    def test_write_entries(self) -> None:
        logger = AuditLogger()
        logger.record(AuditEntry(action=AuditAction.INSERT, table_name="t", user_id="u"))
        logger.record(AuditEntry(action=AuditAction.SELECT, table_name="t", user_id="u"))
        assert len(logger.write_entries()) == 1


class TestAuditDecorator:
    def test_audit_insert(self) -> None:
        logger = AuditLogger()
        decorator = AuditDecorator(logger)

        @decorator.audit_insert(table_name="users", user_id="admin")
        def insert_user(name: str) -> str:
            return "1"

        result = insert_user(name="alice")
        assert result == "1"
        assert logger.count == 1
        assert logger.entries[0].action == AuditAction.INSERT

    def test_audit_update(self) -> None:
        logger = AuditLogger()
        decorator = AuditDecorator(logger)

        @decorator.audit_update(table_name="users", user_id="admin")
        def update_user(user_id: str, name: str, old_data: dict | None = None) -> bool:
            return True

        update_user("1", name="bob", old_data={"name": "alice"})
        assert logger.count == 1
        assert logger.entries[0].action == AuditAction.UPDATE

    def test_audit_delete(self) -> None:
        logger = AuditLogger()
        decorator = AuditDecorator(logger)

        @decorator.audit_delete(table_name="users", user_id="admin")
        def delete_user(user_id: str) -> bool:
            return True

        delete_user("42")
        assert logger.count == 1
        assert logger.entries[0].action == AuditAction.DELETE
        assert logger.entries[0].row_id == "42"
