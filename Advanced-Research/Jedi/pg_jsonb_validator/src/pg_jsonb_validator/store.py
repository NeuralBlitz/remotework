"""Store with decorator pattern for JSONB validation."""

from __future__ import annotations

import abc
import logging
from typing import Any

from pg_jsonb_validator.schema import JsonSchema
from pg_jsonb_validator.validators import RequiredFieldsValidator, TypeValidator, Validator

logger = logging.getLogger(__name__)


class BaseStore(abc.ABC):
    """Abstract base for JSON storage."""

    @abc.abstractmethod
    def insert(self, table: str, data: dict[str, Any]) -> str:
        """Insert JSONB data. Returns the row ID."""
        ...

    @abc.abstractmethod
    def select(self, table: str, row_id: str) -> dict[str, Any] | None: ...


class JsonStore(BaseStore):
    """In-memory JSON store (placeholder for real PostgreSQL)."""

    def __init__(self) -> None:
        self._tables: dict[str, dict[str, dict[str, Any]]] = {}
        self._counter = 0

    def insert(self, table: str, data: dict[str, Any]) -> str:
        if table not in self._tables:
            self._tables[table] = {}
        self._counter += 1
        row_id = str(self._counter)
        self._tables[table][row_id] = data
        return row_id

    def select(self, table: str, row_id: str) -> dict[str, Any] | None:
        return self._tables.get(table, {}).get(row_id)


class StoreDecorator(BaseStore):
    """Base decorator wrapping a store."""

    def __init__(self, wrapped: BaseStore) -> None:
        self._wrapped = wrapped

    def insert(self, table: str, data: dict[str, Any]) -> str:
        return self._wrapped.insert(table, data)

    def select(self, table: str, row_id: str) -> dict[str, Any] | None:
        return self._wrapped.select(table, row_id)


class EnforceSchemaDecorator(StoreDecorator):
    """Validates JSONB against a schema before insert. Raises on invalid data."""

    def __init__(self, wrapped: BaseStore, schema: JsonSchema) -> None:
        super().__init__(wrapped)
        self._validators: list[Validator] = [
            RequiredFieldsValidator(schema.required_fields),
            TypeValidator({k: eval(v) for k, v in schema.field_types.items()}),
        ]

    def insert(self, table: str, data: dict[str, Any]) -> str:
        errors: list[str] = []
        for v in self._validators:
            errors.extend(v.validate(data))
        if errors:
            raise ValueError(f"Validation failed: {'; '.join(errors)}")
        return super().insert(table, data)


class PydanticValidatorDecorator(StoreDecorator):
    """Validates using a callable validator function (simulates Pydantic)."""

    def __init__(self, wrapped: BaseStore, validate_fn: Any) -> None:
        super().__init__(wrapped)
        self._validate_fn = validate_fn

    def insert(self, table: str, data: dict[str, Any]) -> str:
        errors = self._validate_fn(data)
        if errors:
            raise ValueError(f"Pydantic validation failed: {'; '.join(errors)}")
        return super().insert(table, data)
