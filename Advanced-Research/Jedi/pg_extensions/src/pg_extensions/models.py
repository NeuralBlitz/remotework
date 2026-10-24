from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExtensionInfo:
    name: str
    version: str = ""
    schema: str = "public"
    enabled: bool = False


@dataclass
class ExtensionCommand:
    sql: str
    rollback_sql: str
    description: str = ""
