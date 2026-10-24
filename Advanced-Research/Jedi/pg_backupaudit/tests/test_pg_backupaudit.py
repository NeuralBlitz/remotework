from datetime import datetime, timedelta

from pg_backupaudit.auditor import BackupAuditor
from pg_backupaudit.models import BackupRecord, BackupStatus, BackupType
from pg_backupaudit.visitors import CompletenessVisitor, RetentionVisitor


def _make_records() -> list[BackupRecord]:
    now = datetime.now()
    return [
        BackupRecord("b1", BackupType.FULL, BackupStatus.COMPLETED, 1024, now, 30, "db1"),
        BackupRecord("b2", BackupType.INCREMENTAL, BackupStatus.FAILED, 0, now, 30, "db1"),
        BackupRecord(
            "b3", BackupType.FULL, BackupStatus.COMPLETED, 2048, now - timedelta(days=40), 30, "db2"
        ),
    ]


def test_completeness_visitor_pass() -> None:
    v = CompletenessVisitor()
    rec = _make_records()[0]
    finding = v.visit(rec)
    assert finding.passed


def test_completeness_visitor_fail() -> None:
    v = CompletenessVisitor()
    rec = _make_records()[1]
    finding = v.visit(rec)
    assert not finding.passed


def test_retention_visitor_expired() -> None:
    v = RetentionVisitor(reference_time=datetime.now())
    rec = _make_records()[2]
    finding = v.visit(rec)
    assert not finding.passed


def test_auditor_runs_all_visitors() -> None:
    auditor = BackupAuditor()
    auditor.add_visitor(CompletenessVisitor())
    auditor.add_visitor(RetentionVisitor(reference_time=datetime.now()))
    auditor.load_records(_make_records())
    report = auditor.audit()
    assert report.total_backups == 3
    assert report.passed_checks + report.failed_checks == 6


def test_auditor_pass_rate() -> None:
    auditor = BackupAuditor()
    auditor.add_visitor(CompletenessVisitor())
    auditor.load_records(_make_records())
    report = auditor.audit()
    assert 0.0 < report.pass_rate < 1.0


def test_auditor_record_count() -> None:
    auditor = BackupAuditor()
    auditor.load_records(_make_records())
    assert auditor.record_count == 3
