"""Tests for pg_schemaev."""

from __future__ import annotations

import pytest

from pg_schemaev.commands import CommandHistory, MigrationCommand
from pg_schemaev.manager import SchemaManager
from pg_schemaev.models import Migration, MigrationStatus


def _make_migration(
    mid: str = "001",
    up: str = "CREATE TABLE t (id INT)",
    down: str = "DROP TABLE t",
) -> Migration:
    return Migration(migration_id=mid, name=f"Migration {mid}", up_sql=up, down_sql=down)


class TestMigration:
    def test_defaults(self) -> None:
        m = _make_migration()
        assert m.status == MigrationStatus.PENDING
        assert not m.is_applied

    def test_mark_applied(self) -> None:
        m = _make_migration()
        m.mark_applied()
        assert m.is_applied
        assert m.applied_at is not None

    def test_mark_rolled_back(self) -> None:
        m = _make_migration()
        m.mark_applied()
        m.mark_rolled_back()
        assert m.status == MigrationStatus.ROLLED_BACK
        assert m.rolled_back_at is not None

    def test_can_rollback(self) -> None:
        m = _make_migration()
        m.mark_applied()
        assert m.can_rollback

    def test_cannot_rollback_without_down_sql(self) -> None:
        m = _make_migration(down="")
        m.mark_applied()
        assert not m.can_rollback


class TestMigrationCommand:
    def test_execute(self) -> None:
        m = _make_migration()
        cmd = MigrationCommand(migration=m)
        result = cmd.execute()
        assert result["status"] == "applied"
        assert m.is_applied
        assert cmd.was_applied

    def test_undo(self) -> None:
        m = _make_migration()
        cmd = MigrationCommand(migration=m)
        cmd.execute()
        result = cmd.undo()
        assert result["status"] == "rolled_back"
        assert m.status == MigrationStatus.ROLLED_BACK

    def test_undo_without_execute_raises(self) -> None:
        m = _make_migration()
        cmd = MigrationCommand(migration=m)
        with pytest.raises(RuntimeError, match="Cannot undo"):
            cmd.undo()

    def test_validate_empty_up(self) -> None:
        m = _make_migration(up="")
        cmd = MigrationCommand(migration=m)
        errors = cmd.validate()
        assert any("up_sql" in e for e in errors)

    def test_validate_empty_down(self) -> None:
        m = _make_migration(down="")
        cmd = MigrationCommand(migration=m)
        errors = cmd.validate()
        assert any("down_sql" in e for e in errors)


class TestCommandHistory:
    def test_record_and_count(self) -> None:
        history = CommandHistory()
        m = _make_migration()
        cmd = MigrationCommand(migration=m)
        cmd.execute()
        history.record(cmd)
        assert history.total_count == 1
        assert history.applied_count == 1

    def test_pop_undo(self) -> None:
        history = CommandHistory()
        m = _make_migration()
        cmd = MigrationCommand(migration=m)
        cmd.execute()
        history.record(cmd)
        popped = history.pop_undo()
        assert popped is cmd

    def test_pop_undo_empty(self) -> None:
        history = CommandHistory()
        assert history.pop_undo() is None

    def test_get_by_status(self) -> None:
        history = CommandHistory()
        m = _make_migration()
        cmd = MigrationCommand(migration=m)
        cmd.execute()
        history.record(cmd)
        applied = history.get_by_status(MigrationStatus.APPLIED)
        assert len(applied) == 1


class TestSchemaManager:
    def test_register_and_count(self) -> None:
        mgr = SchemaManager()
        mgr.register(_make_migration("001"))
        mgr.register(_make_migration("002"))
        assert mgr.migration_count == 2

    def test_apply(self) -> None:
        mgr = SchemaManager()
        mgr.register(_make_migration("001"))
        result = mgr.apply("001")
        assert result["status"] == "applied"
        assert mgr.status("001") == MigrationStatus.APPLIED

    def test_apply_already_applied_raises(self) -> None:
        mgr = SchemaManager()
        mgr.register(_make_migration("001"))
        mgr.apply("001")
        with pytest.raises(RuntimeError, match="already applied"):
            mgr.apply("001")

    def test_apply_unknown_raises(self) -> None:
        mgr = SchemaManager()
        with pytest.raises(ValueError, match="Unknown migration"):
            mgr.apply("999")

    def test_rollback(self) -> None:
        mgr = SchemaManager()
        mgr.register(_make_migration("001"))
        mgr.apply("001")
        result = mgr.rollback("001")
        assert result["status"] == "rolled_back"
        assert mgr.status("001") == MigrationStatus.ROLLED_BACK

    def test_rollback_not_applied_raises(self) -> None:
        mgr = SchemaManager()
        mgr.register(_make_migration("001", down=""))
        with pytest.raises(RuntimeError, match="cannot be rolled back"):
            mgr.rollback("001")

    def test_apply_all(self) -> None:
        mgr = SchemaManager()
        mgr.register(_make_migration("001"))
        mgr.register(_make_migration("002"))
        results = mgr.apply_all()
        assert len(results) == 2
        assert all(r["status"] == "applied" for r in results)

    def test_rollback_all(self) -> None:
        mgr = SchemaManager()
        mgr.register(_make_migration("001"))
        mgr.register(_make_migration("002"))
        mgr.apply_all()
        results = mgr.rollback_all()
        assert len(results) == 2
        assert mgr.applied_migrations == []

    def test_applied_and_pending(self) -> None:
        mgr = SchemaManager()
        mgr.register(_make_migration("001"))
        mgr.register(_make_migration("002"))
        mgr.apply("001")
        assert mgr.applied_migrations == ["001"]
        assert mgr.pending_migrations == ["002"]
