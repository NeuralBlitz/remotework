"""Shard map — maintains the mapping of tenants to shards."""

from __future__ import annotations

import hashlib

from pg_sharding.models import ShardConfig, ShardInfo


class ShardMap:
    """Manages tenant-to-shard mapping using consistent hashing.

    Usage::
        shard_map = ShardMap(config)
        shard_id = shard_map.get_shard("tenant-42")
    """

    def __init__(self, config: ShardConfig) -> None:
        self.config = config
        self._shards: dict[int, ShardInfo] = {}
        self._tenant_shards: dict[str, int] = {}

    def add_shard(self, shard: ShardInfo) -> None:
        self._shards[shard.shard_id] = shard

    def remove_shard(self, shard_id: int) -> None:
        self._shards.pop(shard_id, None)

    def get_shard_for_tenant(self, tenant_id: str) -> int:
        """Determine shard ID for a tenant using consistent hashing."""
        if tenant_id in self._tenant_shards:
            return self._tenant_shards[tenant_id]
        hash_val = int(hashlib.md5(tenant_id.encode()).hexdigest(), 16)
        shard_id = hash_val % self.config.shard_count
        self._tenant_shards[tenant_id] = shard_id
        return shard_id

    def get_shard_info(self, shard_id: int) -> ShardInfo | None:
        return self._shards.get(shard_id)

    def list_shards(self) -> list[ShardInfo]:
        return list(self._shards.values())

    def get_all_tenant_shards(self) -> dict[str, int]:
        return dict(self._tenant_shards)
