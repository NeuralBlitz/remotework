"""Core models for shard routing."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ShardConfig:
    """Configuration for a sharded database cluster."""

    shard_count: int = 4
    hash_algorithm: str = "md5"
    schema: str = "public"


@dataclass
class ShardInfo:
    """Metadata about a single shard."""

    shard_id: int
    host: str
    port: int
    database: str
    is_active: bool = True
    tenant_count: int = 0
    size_bytes: int = 0


@dataclass
class TenantRoute:
    """Routing decision for a tenant query."""

    tenant_id: str
    shard_id: int
    host: str
    port: int
    database: str


@dataclass
class QueryContext:
    """Parsed query context for routing decisions."""

    original_sql: str
    tenant_id: str | None = None
    table_name: str | None = None
    is_write: bool = False
    is_distributed: bool = False
