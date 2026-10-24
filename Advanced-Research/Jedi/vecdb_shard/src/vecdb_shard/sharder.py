from __future__ import annotations

from vecdb_shard.flyweight import IndexFactory
from vecdb_shard.models import ShardConfig, TenantIndex


class VectorSharder:
    def __init__(self, config: ShardConfig) -> None:
        self._config = config
        self._factory = IndexFactory()
        self._tenants: dict[str, list[TenantIndex]] = {}

    def create_tenant(self, tenant_id: str) -> list[TenantIndex]:
        shards = []
        for i in range(self._config.num_shards):
            index = TenantIndex(
                tenant_id=tenant_id,
                shard_id=i,
                dimensions=self._config.dimensions,
            )
            shards.append(index)
        self._tenants[tenant_id] = shards
        return shards

    def add_vectors(self, tenant_id: str, vectors: list[list[float]]) -> dict[int, int]:
        if tenant_id not in self._tenants:
            raise ValueError(f"Tenant {tenant_id} not found")
        counts: dict[int, int] = {}
        for vec in vectors:
            shard_idx = hash(str(vec)) % self._config.num_shards
            shard = self._tenants[tenant_id][shard_idx]
            shard.index_data.append(vec)
            shard.vector_count += 1
            counts[shard_idx] = counts.get(shard_idx, 0) + 1
        return counts

    def get_shard(self, tenant_id: str, shard_id: int) -> TenantIndex:
        if tenant_id not in self._tenants:
            raise ValueError(f"Tenant {tenant_id} not found")
        if shard_id >= len(self._tenants[tenant_id]):
            raise IndexError(f"Shard {shard_id} out of range")
        return self._tenants[tenant_id][shard_id]

    def total_vectors(self, tenant_id: str) -> int:
        if tenant_id not in self._tenants:
            return 0
        return sum(s.vector_count for s in self._tenants[tenant_id])

    def shared_index(self) -> SharedIndexFlyweight:
        return self._factory.get_index(self._config)

    @property
    def factory(self) -> IndexFactory:
        return self._factory
