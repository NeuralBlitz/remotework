import pytest

from pg_migrate.analyzer import LockAnalyzer
from pg_migrate.models import DDLCommand, LockLevel, MigrationPlan
from pg_migrate.proxy import DDLBlockedError, LockGuardProxy


def _make_ddl(
    cmd: str = "ADD COLUMN",
    table: str = "orders",
    lock: LockLevel = LockLevel.ACCESS_EXCLUSIVE,
) -> DDLCommand:
    return DDLCommand(
        command=cmd,
        table_name=table,
        lock_level=lock,
        raw_sql=f"ALTER TABLE {table} {cmd}",
    )


class TestDDLCommand:
    def test_is_dangerous(self) -> None:
        cmd = _make_ddl(lock=LockLevel.ACCESS_EXCLUSIVE)
        assert cmd.is_dangerous is True

    def test_not_dangerous(self) -> None:
        cmd = _make_ddl(lock=LockLevel.ACCESS_SHARE)
        assert cmd.is_dangerous is False

    def test_is_locking(self) -> None:
        cmd = _make_ddl(lock=LockLevel.SHARE)
        assert cmd.is_locking is True

    def test_not_locking(self) -> None:
        cmd = _make_ddl(lock=LockLevel.ROW_EXCLUSIVE)
        assert cmd.is_locking is False

    def test_requires_repack_suggestion(self) -> None:
        cmd = _make_ddl(cmd="ADD COLUMN DEFAULT")
        assert cmd.requires_repack_suggestion is True

    def test_no_repack_for_index(self) -> None:
        cmd = _make_ddl(cmd="CREATE INDEX")
        assert cmd.requires_repack_suggestion is False


class TestMigrationPlan:
    def test_has_dangerous_commands(self) -> None:
        plan = MigrationPlan(
            schema_name="public",
            commands=[_make_ddl(lock=LockLevel.ACCESS_EXCLUSIVE)],
            table_size_bytes=50_000_000,
        )
        assert plan.has_dangerous_commands is True

    def test_no_dangerous(self) -> None:
        plan = MigrationPlan(
            schema_name="public",
            commands=[_make_ddl(lock=LockLevel.ACCESS_SHARE)],
        )
        assert plan.has_dangerous_commands is False

    def test_total_commands(self) -> None:
        plan = MigrationPlan(
            schema_name="public",
            commands=[_make_ddl(), _make_ddl()],
        )
        assert plan.total_commands == 2

    def test_table_size_mb(self) -> None:
        plan = MigrationPlan(schema_name="public", table_size_bytes=100 * 1024 * 1024)
        assert plan.table_size_mb == pytest.approx(100.0)


class TestLockGuardProxy:
    def test_small_table_allows_dangerous(self) -> None:
        proxy = LockGuardProxy(table_size_bytes=10 * 1024 * 1024)
        cmd = _make_ddl()
        allowed, _ = proxy.check(cmd)
        assert allowed is True

    def test_large_table_blocks_dangerous(self) -> None:
        proxy = LockGuardProxy(table_size_bytes=500 * 1024 * 1024)
        cmd = _make_ddl()
        allowed, reason = proxy.check(cmd)
        assert allowed is False
        assert "large table" in reason

    def test_large_table_blocks_with_repack_hint(self) -> None:
        proxy = LockGuardProxy(table_size_bytes=500 * 1024 * 1024)
        cmd = _make_ddl(cmd="ADD COLUMN DEFAULT")
        allowed, reason = proxy.check(cmd)
        assert allowed is False
        assert "pg_repack" in reason

    def test_safe_commands_always_allowed(self) -> None:
        proxy = LockGuardProxy(table_size_bytes=500 * 1024 * 1024)
        cmd = _make_ddl(lock=LockLevel.ACCESS_SHARE)
        allowed, _ = proxy.check(cmd)
        assert allowed is True

    def test_execute_tracks_history(self) -> None:
        proxy = LockGuardProxy(table_size_bytes=10 * 1024 * 1024)
        cmd = _make_ddl()
        proxy.execute(cmd)
        assert len(proxy.executed_commands) == 1

    def test_execute_blocked_tracks(self) -> None:
        proxy = LockGuardProxy(table_size_bytes=500 * 1024 * 1024)
        cmd = _make_ddl()
        proxy.execute(cmd)
        assert len(proxy.blocked_commands) == 1

    def test_execute_safe_raises(self) -> None:
        proxy = LockGuardProxy(table_size_bytes=500 * 1024 * 1024)
        cmd = _make_ddl()
        with pytest.raises(DDLBlockedError):
            proxy.execute_safe(cmd)

    def test_review_plan(self) -> None:
        proxy = LockGuardProxy(table_size_bytes=500 * 1024 * 1024)
        plan = MigrationPlan(
            schema_name="public",
            commands=[
                _make_ddl(lock=LockLevel.ACCESS_SHARE),
                _make_ddl(lock=LockLevel.ACCESS_EXCLUSIVE),
            ],
        )
        results = proxy.review_plan(plan)
        assert results[0][1] is True
        assert results[1][1] is False

    def test_is_large_table(self) -> None:
        proxy = LockGuardProxy(table_size_bytes=200 * 1024 * 1024)
        assert proxy.is_large_table is True
        small = LockGuardProxy(table_size_bytes=10 * 1024 * 1024)
        assert small.is_large_table is False


class TestLockAnalyzer:
    def test_low_impact(self) -> None:
        analyzer = LockAnalyzer()
        cmd = _make_ddl(lock=LockLevel.ACCESS_SHARE)
        result = analyzer.analyze_lock_impact(cmd, 1_000_000)
        assert "Low impact" in result

    def test_high_impact(self) -> None:
        analyzer = LockAnalyzer()
        cmd = _make_ddl(lock=LockLevel.ACCESS_EXCLUSIVE)
        result = analyzer.analyze_lock_impact(cmd, 500 * 1024 * 1024)
        assert "HIGH impact" in result

    def test_medium_impact(self) -> None:
        analyzer = LockAnalyzer()
        cmd = _make_ddl(lock=LockLevel.SHARE)
        result = analyzer.analyze_lock_impact(cmd, 10 * 1024 * 1024)
        assert "Medium impact" in result

    def test_estimate_lock_wait(self) -> None:
        analyzer = LockAnalyzer()
        cmd = _make_ddl(lock=LockLevel.ACCESS_EXCLUSIVE)
        time_est = analyzer.estimate_lock_wait_time(cmd, active_queries=10)
        assert time_est == pytest.approx(7.0)

    def test_estimate_zero_for_non_locking(self) -> None:
        analyzer = LockAnalyzer()
        cmd = _make_ddl(lock=LockLevel.ACCESS_SHARE)
        assert analyzer.estimate_lock_wait_time(cmd, 5) == 0.0

    def test_suggest_alternatives(self) -> None:
        analyzer = LockAnalyzer()
        cmd = _make_ddl(cmd="ADD COLUMN DEFAULT")
        suggestions = analyzer.suggest_alternatives(cmd, 200 * 1024 * 1024)
        assert len(suggestions) >= 2
        assert any("pg_repack" in s for s in suggestions)

    def test_no_alternatives_for_safe(self) -> None:
        analyzer = LockAnalyzer()
        cmd = _make_ddl(cmd="CREATE INDEX", lock=LockLevel.ACCESS_SHARE)
        suggestions = analyzer.suggest_alternatives(cmd, 200 * 1024 * 1024)
        assert suggestions == []

    def test_analyze_plan(self) -> None:
        analyzer = LockAnalyzer()
        plan = MigrationPlan(
            schema_name="public",
            commands=[_make_ddl(), _make_ddl()],
            table_size_bytes=50 * 1024 * 1024,
        )
        results = analyzer.analyze_plan(plan)
        assert len(results) == 2
