"""Tests for JSONB Schema Validator."""

from __future__ import annotations

import pytest

from pg_jsonb_validator.schema import JsonSchema, SchemaRegistry
from pg_jsonb_validator.store import EnforceSchemaDecorator, JsonStore, PydanticValidatorDecorator
from pg_jsonb_validator.validators import RequiredFieldsValidator, TypeValidator


class TestSchemaRegistry:
    def test_register_and_get(self) -> None:
        reg = SchemaRegistry()
        schema = JsonSchema(name="user", required_fields=["name", "email"])
        reg.register(schema)
        assert reg.get("user") is schema

    def test_list_schemas(self) -> None:
        reg = SchemaRegistry()
        reg.register(JsonSchema(name="a"))
        reg.register(JsonSchema(name="b"))
        assert set(reg.list_schemas()) == {"a", "b"}


class TestRequiredFieldsValidator:
    def test_valid(self) -> None:
        v = RequiredFieldsValidator(["name", "email"])
        assert v.validate({"name": "a", "email": "b"}) == []

    def test_missing(self) -> None:
        v = RequiredFieldsValidator(["name", "email"])
        errors = v.validate({"name": "a"})
        assert len(errors) == 1
        assert "email" in errors[0]


class TestTypeValidator:
    def test_valid(self) -> None:
        v = TypeValidator({"age": int, "name": str})
        assert v.validate({"age": 25, "name": "test"}) == []

    def test_wrong_type(self) -> None:
        v = TypeValidator({"age": int})
        errors = v.validate({"age": "not_int"})
        assert len(errors) == 1


class TestJsonStore:
    def test_insert_and_select(self) -> None:
        store = JsonStore()
        row_id = store.insert("users", {"name": "Alice"})
        assert store.select("users", row_id) == {"name": "Alice"}

    def test_select_missing(self) -> None:
        store = JsonStore()
        assert store.select("users", "999") is None


class TestEnforceSchemaDecorator:
    def test_valid_insert(self) -> None:
        schema = JsonSchema(name="user", required_fields=["name"], field_types={"name": "str"})
        store = EnforceSchemaDecorator(JsonStore(), schema)
        row_id = store.insert("users", {"name": "Alice"})
        assert row_id is not None

    def test_invalid_raises(self) -> None:
        schema = JsonSchema(name="user", required_fields=["name", "email"])
        store = EnforceSchemaDecorator(JsonStore(), schema)
        with pytest.raises(ValueError, match="Missing required field"):
            store.insert("users", {"name": "Alice"})


class TestPydanticValidatorDecorator:
    def test_valid(self) -> None:
        def validate(data):
            return [] if "id" in data else ["id required"]

        store = PydanticValidatorDecorator(JsonStore(), validate)
        row_id = store.insert("t", {"id": 1})
        assert row_id is not None

    def test_invalid_raises(self) -> None:
        def validate(data):
            return ["id required"]

        store = PydanticValidatorDecorator(JsonStore(), validate)
        with pytest.raises(ValueError, match="Pydantic validation failed"):
            store.insert("t", {})
