"""Tests for PostgreSQL Sharding Controller."""

from __future__ import annotations

import pytest

from pg_sharding.models import ShardConfig, ShardInfo
from pg_sharding.proxy import QueryRouter, TenantRoutingProxy
from pg_sharding.router import ShardMap


@pytest.fixture
def config() -> ShardConfig:
    return ShardConfig(shard_count=4)


@pytest.fixture
def shard_map(config: ShardConfig) -> ShardMap:
    sm = ShardMap(config)
    for i in range(4):
        sm.add_shard(ShardInfo(shard_id=i, host=f"db-{i}", port=5432, database=f"shard_{i}"))
    return sm


class TestShardMap:
    def test_consistent_routing(self, shard_map: ShardMap) -> None:
        s1 = shard_map.get_shard_for_tenant("tenant-1")
        s2 = shard_map.get_shard_for_tenant("tenant-1")
        assert s1 == s2

    def test_distribution(self, shard_map: ShardMap) -> None:
        shards = set()
        for i in range(100):
            shards.add(shard_map.get_shard_for_tenant(f"tenant-{i}"))
        assert len(shards) > 1

    def test_get_shard_info(self, shard_map: ShardMap) -> None:
        info = shard_map.get_shard_info(0)
        assert info is not None
        assert info.host == "db-0"

    def test_remove_shard(self, shard_map: ShardMap) -> None:
        shard_map.remove_shard(3)
        assert shard_map.get_shard_info(3) is None

    def test_list_shards(self, shard_map: ShardMap) -> None:
        assert len(shard_map.list_shards()) == 4


class TestQueryRouter:
    def test_parse_select(self, shard_map: ShardMap) -> None:
        router = QueryRouter(shard_map)
        ctx = router.parse("SELECT * FROM orders WHERE tenant_id = 'acme'")
        assert ctx.tenant_id == "acme"
        assert ctx.table_name == "orders"
        assert ctx.is_write is False

    def test_parse_insert(self, shard_map: ShardMap) -> None:
        router = QueryRouter(shard_map)
        ctx = router.parse("INSERT INTO orders (tenant_id) VALUES ('acme')")
        assert ctx.is_write is True

    def test_parse_numeric_tenant(self, shard_map: ShardMap) -> None:
        router = QueryRouter(shard_map)
        ctx = router.parse("SELECT * FROM users WHERE tenant_id = 42")
        assert ctx.tenant_id == "42"


class TestTenantRoutingProxy:
    def test_route_with_tenant_id(self, shard_map: ShardMap) -> None:
        proxy = TenantRoutingProxy(shard_map)
        route = proxy.route_query("SELECT 1", tenant_id="acme")
        assert 0 <= route.shard_id < 4
        assert route.host.startswith("db-")

    def test_route_extracts_tenant(self, shard_map: ShardMap) -> None:
        proxy = TenantRoutingProxy(shard_map)
        route = proxy.route_query("SELECT * FROM orders WHERE tenant_id = 'acme'")
        assert route.tenant_id == "acme"

    def test_route_no_tenant_raises(self, shard_map: ShardMap) -> None:
        proxy = TenantRoutingProxy(shard_map)
        with pytest.raises(ValueError, match="no tenant_id"):
            proxy.route_query("SELECT 1")

    def test_execute_returns_route(self, shard_map: ShardMap) -> None:
        proxy = TenantRoutingProxy(shard_map)
        route = proxy.execute("SELECT * FROM orders WHERE tenant_id = 'acme'")
        assert route.database.startswith("shard_")
