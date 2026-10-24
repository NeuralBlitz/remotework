from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ShardConfig:
    num_shards: int = 4
    dimensions: int = 128
    max_vectors_per_shard: int = 10000
    replication_factor: int = 1
    index_type: str = "hnsw"

    def validate(self) -> bool:
        if self.num_shards <= 0 or self.dimensions <= 0:
            return False
        if self.max_vectors_per_shard <= 0:
            return False
        return self.replication_factor >= 1


@dataclass
class TenantIndex:
    tenant_id: str = ""
    shard_id: int = 0
    vector_count: int = 0
    dimensions: int = 128
    index_data: list[list[float]] = field(default_factory=list)

    def capacity_used(self, max_vectors: int) -> float:
        if max_vectors == 0:
            return 1.0
        return self.vector_count / max_vectors

    def is_full(self, max_vectors: int) -> bool:
        return self.vector_count >= max_vectors
