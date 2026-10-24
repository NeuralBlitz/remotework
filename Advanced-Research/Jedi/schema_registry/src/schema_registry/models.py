from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Schema:
    name: str
    version: int
    definition: dict[str, str]

@dataclass
class SchemaCompatibility:
    schema: Schema
    compatible: bool
