from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ShardedQuery:
    vector: list[float]
    top_k: int = 10
    tenant_id: str | None = None
    shard_ids: list[str] = field(default_factory=list)
    distance_metric: str = "cosine"


@dataclass
class ShardResult:
    shard_id: str
    matches: list[dict[str, Any]]
    latency_ms: float
    error: str | None = None

    @property
    def is_ok(self) -> bool:
        return self.error is None
