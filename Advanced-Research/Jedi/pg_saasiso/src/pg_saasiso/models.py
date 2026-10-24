from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class IsolationLevel(Enum):
    SCHEMA = "schema"
    DATABASE = "database"
    ROW_LEVEL = "row_level"


@dataclass
class TenantConfig:
    tenant_id: str
    name: str
    isolation: IsolationLevel = IsolationLevel.SCHEMA
    max_tables: int = 50
    max_indexes: int = 100


@dataclass
class SchemaDefinition:
    schema_name: str
    tenant_id: str
    tables: list[str] = field(default_factory=list)
    indexes: list[str] = field(default_factory=list)
    views: list[str] = field(default_factory=list)
    owner: str = ""

    @property
    def ddl_count(self) -> int:
        return len(self.tables) + len(self.indexes) + len(self.views)

    def add_table(self, name: str) -> None:
        if name not in self.tables:
            self.tables.append(name)

    def add_index(self, name: str) -> None:
        if name not in self.indexes:
            self.indexes.append(name)
