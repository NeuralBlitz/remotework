from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from k8s_crd.crds import PGDatabaseCRD, PGBackupCRD, PGUserCRD


@dataclass
class ValidationError:
    field: str
    message: str
    crd_type: str


@dataclass
class ValidationResult:
    valid: bool
    errors: list[ValidationError] = field(default_factory=list)


class CRDValidator:
    def __init__(self) -> None:
        self._registered_types: set[str] = {"PGDatabase", "PGBackup", "PGUser"}

    def register_type(self, crd_type: str) -> None:
        self._registered_types.add(crd_type)

    def validate_database(self, crd: PGDatabaseCRD) -> ValidationResult:
        errors: list[ValidationError] = []

        if not crd.name:
            errors.append(ValidationError("name", "Name is required", "PGDatabase"))
        if not crd.database_name:
            errors.append(
                ValidationError("databaseName", "Database name is required", "PGDatabase")
            )
        if not crd.owner:
            errors.append(ValidationError("owner", "Owner is required", "PGDatabase"))
        if crd.encoding not in ("UTF8", "LATIN1", "SQL_ASCII"):
            errors.append(
                ValidationError("encoding", f"Invalid encoding: {crd.encoding}", "PGDatabase")
            )

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def validate_backup(self, crd: PGBackupCRD) -> ValidationResult:
        errors: list[ValidationError] = []

        if not crd.name:
            errors.append(ValidationError("name", "Name is required", "PGBackup"))
        if not crd.source_cluster:
            errors.append(
                ValidationError("sourceCluster", "Source cluster is required", "PGBackup")
            )
        if crd.backup_type not in ("full", "incremental", "differential"):
            errors.append(
                ValidationError("backupType", f"Invalid backup type: {crd.backup_type}", "PGBackup")
            )
        if crd.retention_days < 1:
            errors.append(ValidationError("retentionDays", "Retention must be >= 1", "PGBackup"))

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def validate_user(self, crd: PGUserCRD) -> ValidationResult:
        errors: list[ValidationError] = []

        if not crd.name:
            errors.append(ValidationError("name", "Name is required", "PGUser"))
        if not crd.username:
            errors.append(ValidationError("username", "Username is required", "PGUser"))
        if len(crd.username) > 63:
            errors.append(ValidationError("username", "Username must be <= 63 chars", "PGUser"))

        valid_roles = {"read", "write", "admin", "replication", "superuser"}
        for role in crd.roles:
            if role not in valid_roles:
                errors.append(ValidationError("roles", f"Invalid role: {role}", "PGUser"))

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def validate_dict(self, data: dict[str, Any]) -> ValidationResult:
        kind = data.get("kind", "")
        if kind == "PGDatabase":
            crd = PGDatabaseCRD(
                name=data.get("metadata", {}).get("name", ""),
                namespace=data.get("metadata", {}).get("namespace", ""),
                database_name=data.get("spec", {}).get("databaseName", ""),
                owner=data.get("spec", {}).get("owner", ""),
                encoding=data.get("spec", {}).get("encoding", "UTF8"),
            )
            return self.validate_database(crd)
        return ValidationResult(
            valid=False, errors=[ValidationError("kind", f"Unknown kind: {kind}", "Unknown")]
        )
