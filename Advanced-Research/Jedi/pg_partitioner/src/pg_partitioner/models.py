"""Core data models for table partitioning."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any


class PartitionType(str, enum.Enum):
    """Partitioning method."""

    RANGE = "range"
    LIST = "list"
    HASH = "hash"


@dataclass
class PartitionConfig:
    """Configuration for a partitioned table."""

    table_name: str
    partition_column: str
    partition_type: PartitionType = PartitionType.RANGE
    schema_name: str = "public"
    retention_months: int = 12
    pre_create_months: int = 3
    hash_partitions: int = 16
    default_list_values: list[str] = field(default_factory=lambda: ["default"])


@dataclass
class PartitionInfo:
    """Metadata about a single partition."""

    partition_name: str
    parent_table: str
    partition_type: PartitionType
    from_value: Any | None = None
    to_value: Any | None = None
    list_values: list[str] | None = None
    hash_modulus: int | None = None
    hash_remainder: int | None = None
    row_count: int = 0
    size_bytes: int = 0
    is_detached: bool = False

    @property
    def full_name(self) -> str:
        return f"{self.parent_table}_{self.partition_name}"


@dataclass
class MaintenanceResult:
    """Result of a maintenance run."""

    created: list[str] = field(default_factory=list)
    dropped: list[str] = field(default_factory=list)
    detached: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def total_actions(self) -> int:
        return len(self.created) + len(self.dropped) + len(self.detached)

    @property
    def is_clean(self) -> bool:
        return len(self.errors) == 0
