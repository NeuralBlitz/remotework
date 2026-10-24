"""Validators — pluggable validation rules."""

from __future__ import annotations

import abc
from typing import Any


class Validator(abc.ABC):
    """Base validator interface."""

    @abc.abstractmethod
    def validate(self, data: dict[str, Any]) -> list[str]:
        """Validate data. Returns list of error messages (empty = valid)."""
        ...


class RequiredFieldsValidator(Validator):
    def __init__(self, required: list[str]) -> None:
        self._required = required

    def validate(self, data: dict[str, Any]) -> list[str]:
        missing = [f for f in self._required if f not in data or data[f] is None]
        return [f"Missing required field: {f}" for f in missing]


class TypeValidator(Validator):
    def __init__(self, field_types: dict[str, type]) -> None:
        self._types = field_types

    def validate(self, data: dict[str, Any]) -> list[str]:
        errors = []
        for field_name, expected_type in self._types.items():
            if field_name in data and not isinstance(data[field_name], expected_type):
                errors.append(f"Field '{field_name}' must be {expected_type.__name__}")
        return errors
