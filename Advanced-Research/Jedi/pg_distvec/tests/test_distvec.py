from pg_distvec.models import ShardedQuery, ShardResult
from pg_distvec.search import DistributedSearchEngine
from pg_distvec.strategies import RouteByTenantStrategy, ScatterGatherStrategy


class TestShardedQuery:
    def test_create_query(self) -> None:
        q = ShardedQuery(vector=[1.0, 2.0, 3.0], top_k=5)
        assert q.top_k == 5
        assert len(q.vector) == 3
        assert q.tenant_id is None

    def test_query_with_tenant(self) -> None:
        q = ShardedQuery(vector=[1.0], tenant_id="tenant-1")
        assert q.tenant_id == "tenant-1"


class TestShardResult:
    def test_ok_result(self) -> None:
        r = ShardResult(shard_id="s1", matches=[{"id": "1"}], latency_ms=2.0)
        assert r.is_ok is True

    def test_error_result(self) -> None:
        r = ShardResult(shard_id="s1", matches=[], latency_ms=0.0, error="timeout")
        assert r.is_ok is False


class TestScatterGatherStrategy:
    def test_selects_all_shards(self) -> None:
        strat = ScatterGatherStrategy()
        q = ShardedQuery(vector=[1.0])
        shards = strat.select_shards(q, ["s1", "s2", "s3"])
        assert shards == ["s1", "s2", "s3"]

    def test_merge_sorted_by_score(self) -> None:
        strat = ScatterGatherStrategy()
        results = [
            ShardResult("s1", [{"id": "a", "score": 0.5}], 1.0),
            ShardResult("s2", [{"id": "b", "score": 0.9}], 1.0),
        ]
        merged = strat.merge_results(results, top_k=10)
        assert merged[0]["id"] == "b"
        assert len(merged) == 2

    def test_merge_skips_errors(self) -> None:
        strat = ScatterGatherStrategy()
        results = [
            ShardResult("s1", [{"id": "a", "score": 0.8}], 1.0),
            ShardResult("s2", [], 0.0, error="fail"),
        ]
        merged = strat.merge_results(results, top_k=10)
        assert len(merged) == 1


class TestRouteByTenantStrategy:
    def test_route_by_tenant(self) -> None:
        strat = RouteByTenantStrategy()
        q = ShardedQuery(vector=[1.0], tenant_id="t1")
        shards = strat.select_shards(q, ["s1", "s2", "s3"])
        assert len(shards) == 1

    def test_route_with_explicit_shards(self) -> None:
        strat = RouteByTenantStrategy()
        q = ShardedQuery(vector=[1.0], tenant_id="t1", shard_ids=["s2"])
        shards = strat.select_shards(q, ["s1", "s2", "s3"])
        assert shards == ["s2"]

    def test_fallback_all_shards(self) -> None:
        strat = RouteByTenantStrategy()
        q = ShardedQuery(vector=[1.0])
        shards = strat.select_shards(q, ["s1", "s2"])
        assert len(shards) == 2


class TestDistributedSearchEngine:
    def test_search_returns_results(self) -> None:
        engine = DistributedSearchEngine(["s1", "s2"], ScatterGatherStrategy())
        results = engine.search(ShardedQuery(vector=[1.0, 2.0], top_k=5))
        assert len(results) > 0

    def test_switch_strategy(self) -> None:
        engine = DistributedSearchEngine(["s1", "s2"], ScatterGatherStrategy())
        assert isinstance(engine.strategy, ScatterGatherStrategy)
        engine.strategy = RouteByTenantStrategy()
        assert isinstance(engine.strategy, RouteByTenantStrategy)

    def test_shards_property(self) -> None:
        engine = DistributedSearchEngine(["s1", "s2"], ScatterGatherStrategy())
        assert engine.shards == ["s1", "s2"]
