"""Audit data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class AuditAction(str, Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    SELECT = "SELECT"
    TRUNCATE = "TRUNCATE"


@dataclass(frozen=True)
class AuditEntry:
    """Immutable record of a database operation."""

    action: AuditAction
    table_name: str
    user_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    row_id: str | None = None
    old_data: dict[str, Any] | None = None
    new_data: dict[str, Any] | None = None
    query_text: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_write(self) -> bool:
        return self.action in {AuditAction.INSERT, AuditAction.UPDATE, AuditAction.DELETE}

    @property
    def summary(self) -> str:
        parts = [self.action.value, self.table_name]
        if self.row_id:
            parts.append(f"id={self.row_id}")
        parts.append(f"by={self.user_id}")
        return " ".join(parts)
