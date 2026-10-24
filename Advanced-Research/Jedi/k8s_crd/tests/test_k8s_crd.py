import pytest
from k8s_crd.crds import PGDatabaseCRD, PGBackupCRD, PGUserCRD
from k8s_crd.validator import CRDValidator, ValidationResult


def test_database_crd_creation() -> None:
    crd = PGDatabaseCRD(name="mydb", namespace="default", database_name="mydb", owner="admin")
    assert crd.name == "mydb"
    assert crd.encoding == "UTF8"


def test_database_crd_to_dict() -> None:
    crd = PGDatabaseCRD(name="mydb", namespace="default", database_name="mydb", owner="admin")
    d = crd.to_dict()
    assert d["kind"] == "PGDatabase"
    assert d["spec"]["databaseName"] == "mydb"


def test_backup_crd_creation() -> None:
    crd = PGBackupCRD(name="daily", namespace="default", source_cluster="pg-cluster")
    assert crd.backup_type == "full"
    assert crd.retention_days == 30


def test_backup_crd_to_dict() -> None:
    crd = PGBackupCRD(name="backup", namespace="prod", source_cluster="main-pg")
    d = crd.to_dict()
    assert d["kind"] == "PGBackup"
    assert d["spec"]["sourceCluster"] == "main-pg"


def test_user_crd_creation() -> None:
    crd = PGUserCRD(name="appuser", namespace="default", username="app", roles=["read", "write"])
    assert len(crd.roles) == 2


def test_user_crd_to_dict() -> None:
    crd = PGUserCRD(name="u", namespace="ns", username="user1")
    d = crd.to_dict()
    assert d["kind"] == "PGUser"


def test_validator_database_valid() -> None:
    v = CRDValidator()
    crd = PGDatabaseCRD(name="db", namespace="ns", database_name="db", owner="root")
    result = v.validate_database(crd)
    assert result.valid is True
    assert len(result.errors) == 0


def test_validator_database_invalid() -> None:
    v = CRDValidator()
    crd = PGDatabaseCRD(name="", namespace="ns", database_name="", owner="")
    result = v.validate_database(crd)
    assert result.valid is False
    assert len(result.errors) >= 3


def test_validator_backup_valid() -> None:
    v = CRDValidator()
    crd = PGBackupCRD(name="b", namespace="ns", source_cluster="pg")
    result = v.validate_backup(crd)
    assert result.valid is True


def test_validator_backup_invalid_retention() -> None:
    v = CRDValidator()
    crd = PGBackupCRD(name="b", namespace="ns", source_cluster="pg", retention_days=0)
    result = v.validate_backup(crd)
    assert result.valid is False


def test_validator_user_valid() -> None:
    v = CRDValidator()
    crd = PGUserCRD(name="u", namespace="ns", username="testuser", roles=["read"])
    result = v.validate_user(crd)
    assert result.valid is True


def test_validator_user_invalid_role() -> None:
    v = CRDValidator()
    crd = PGUserCRD(name="u", namespace="ns", username="test", roles=["invalid_role"])
    result = v.validate_user(crd)
    assert result.valid is False


def test_validator_unknown_kind() -> None:
    v = CRDValidator()
    result = v.validate_dict({"kind": "Unknown"})
    assert result.valid is False
