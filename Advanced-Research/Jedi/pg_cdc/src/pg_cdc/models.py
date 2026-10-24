"""Models for CDC events."""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any


class ChangeType(str, enum.Enum):
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"


@dataclass
class WALPosition:
    """Represents a position in the WAL."""

    lsn: int
    xid: int = 0


@dataclass
class ChangeEvent:
    """A single change captured from the WAL."""

    table_name: str
    change_type: ChangeType
    position: WALPosition
    old_data: dict[str, Any] | None = None
    new_data: dict[str, Any] | None = None
    timestamp: float = 0.0
    schema_name: str = "public"

    @property
    def key(self) -> str:
        return f"{self.schema_name}.{self.table_name}"
