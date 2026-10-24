"""Tenant configuration models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class IsolationMode(str, Enum):
    SCHEMA = "schema"
    DATABASE = "database"
    ROW = "row"


@dataclass
class TenantConfig:
    """Configuration for a single tenant."""

    tenant_id: str
    name: str
    isolation_mode: IsolationMode = IsolationMode.SCHEMA
    connection_string: str = ""
    schema_name: str = ""
    database_name: str = ""
    rls_policy: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.schema_name:
            self.schema_name = f"tenant_{self.tenant_id}"
        if not self.database_name:
            self.database_name = f"db_tenant_{self.tenant_id}"

    @property
    def has_connection(self) -> bool:
        return bool(self.connection_string)

    @property
    def qualified_schema(self) -> str:
        return (
            f"{self.database_name}.{self.schema_name}" if self.database_name else self.schema_name
        )
