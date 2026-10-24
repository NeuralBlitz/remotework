"""Schema registry management."""
from __future__ import annotations

from .models import Schema, SchemaCompatibility

__all__ = ["Schema", "SchemaCompatibility", "register_schema", "check_compatibility"]

def register_schema(
    name: str,
    version: int,
    definition: dict[str, str],
) -> Schema:
    return Schema(name=name, version=version, definition=definition)

def check_compatibility(schema: Schema, new_def: dict[str, str]) -> SchemaCompatibility:
    return SchemaCompatibility(schema=schema, compatible=True)
