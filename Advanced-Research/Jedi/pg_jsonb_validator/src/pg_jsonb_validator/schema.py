"""Schema registry for JSON validation rules."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class JsonSchema:
    """A JSON Schema definition."""

    name: str
    required_fields: list[str] = field(default_factory=list)
    field_types: dict[str, str] = field(default_factory=dict)
    max_length: dict[str, int] = field(default_factory=dict)
    pattern: dict[str, str] = field(default_factory=dict)


class SchemaRegistry:
    """Registry of JSON schemas for validation."""

    def __init__(self) -> None:
        self._schemas: dict[str, JsonSchema] = {}

    def register(self, schema: JsonSchema) -> None:
        self._schemas[schema.name] = schema

    def get(self, name: str) -> JsonSchema | None:
        return self._schemas.get(name)

    def list_schemas(self) -> list[str]:
        return list(self._schemas.keys())
