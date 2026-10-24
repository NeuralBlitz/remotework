from pg_zerodown.migrator import ZeroDowntimeMigrator
from pg_zerodown.models import MigrationPhase


def test_migrator_expand() -> None:
    m = ZeroDowntimeMigrator("users", "email", "varchar(255)")
    result = m.expand()
    assert result.success
    assert result.phase == MigrationPhase.EXPAND


def test_migrator_full_execute() -> None:
    m = ZeroDowntimeMigrator("users", "email", "varchar(255)")
    results = m.execute()
    assert len(results) == 4
    assert all(r.success for r in results)
    assert results[0].phase == MigrationPhase.EXPAND
    assert results[3].phase == MigrationPhase.CONTRACT


def test_migrator_dry_run() -> None:
    m = ZeroDowntimeMigrator("users", "email", "varchar(255)")
    m.set_dry_run(True)
    results = m.execute()
    assert all(r.rows_affected == 0 for r in results)


def test_migrator_current_phase() -> None:
    m = ZeroDowntimeMigrator("users", "email", "varchar(255)")
    assert m.current_phase == "not_started"
    m.expand()
    assert m.current_phase == "expand"
    m.execute()
    assert m.current_phase == "done"


def test_migrator_shadow_column() -> None:
    m = ZeroDowntimeMigrator("users", "email", "varchar(255)")
    assert m.shadow_column == "email_new"


def test_migrator_table_name() -> None:
    m = ZeroDowntimeMigrator("orders", "amount", "numeric")
    assert m.table == "orders"
