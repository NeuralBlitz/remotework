"""Tests for schema_registry."""
from __future__ import annotations

from src.schema_registry import check_compatibility, register_schema


def test_register_schema():
    schema = register_schema("users", 1, {"fields": [{"name": "id", "type": "int"}]})
    assert schema.name == "users"
    assert schema.version == 1

def test_register_schema_with_definition():
    definition = {"type": "record", "name": "Test"}
    schema = register_schema("test", 2, definition)
    assert schema.definition == definition

def test_check_compatibility():
    schema = register_schema("test", 1, {})
    compat = check_compatibility(schema, {"new": "def"})
    assert compat.compatible is True

def test_check_compatibility_preserves_schema():
    schema = register_schema("test", 3, {"old": True})
    compat = check_compatibility(schema, {"new": "def"})
    assert compat.schema.name == "test"
    assert compat.schema.version == 3

def test_multiple_versions():
    s1 = register_schema("t", 1, {})
    s2 = register_schema("t", 2, {})
    assert s1.version < s2.version

def test_schema_has_definition():
    schema = register_schema("test", 1, {"fields": []})
    assert hasattr(schema, "definition")
