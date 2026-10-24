from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ValidationStatus(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    WARNING = "warning"


@dataclass
class ValidationResult:
    status: ValidationStatus
    messages: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.status != ValidationStatus.INVALID


class RestoreValidator:
    def __init__(self) -> None:
        self._checks_run: int = 0

    def validate_backup_exists(self, backup_id: str) -> ValidationResult:
        self._checks_run += 1
        if not backup_id:
            return ValidationResult(ValidationStatus.INVALID, ["backup_id is empty"])
        return ValidationResult(ValidationStatus.VALID)

    def validate_target_available(self, target_db: str) -> ValidationResult:
        self._checks_run += 1
        if not target_db:
            return ValidationResult(ValidationStatus.INVALID, ["target_db is empty"])
        return ValidationResult(ValidationStatus.VALID)

    def validate_disk_space(self, required_gb: float, available_gb: float) -> ValidationResult:
        self._checks_run += 1
        if available_gb < required_gb:
            return ValidationResult(
                ValidationStatus.INVALID,
                [f"Insufficient space: need {required_gb}GB, have {available_gb}GB"],
            )
        if available_gb < required_gb * 1.5:
            return ValidationResult(
                ValidationStatus.WARNING,
                ["Disk space is low but sufficient"],
            )
        return ValidationResult(ValidationStatus.VALID)

    def validate_version_compatibility(
        self, backup_version: str, target_version: str
    ) -> ValidationResult:
        self._checks_run += 1
        backup_major = backup_version.split(".")[0]
        target_major = target_version.split(".")[0]
        if backup_major != target_major:
            return ValidationResult(
                ValidationStatus.INVALID,
                [f"Major version mismatch: backup={backup_version}, target={target_version}"],
            )
        return ValidationResult(ValidationStatus.VALID)

    @property
    def checks_run(self) -> int:
        return self._checks_run
