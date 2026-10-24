from pg_readreplica.models import ReplicaNode, ReplicaRegion
from pg_readreplica.router import ReplicaRouter
from pg_readreplica.strategies import (
    LatencyBasedStrategy,
    NearestReplicaStrategy,
    RoundRobinStrategy,
)


def _make_replicas() -> list[ReplicaNode]:
    return [
        ReplicaNode("r1", "10.0.0.1", 5432, ReplicaRegion.US_EAST, latency_ms=5.0),
        ReplicaNode("r2", "10.0.0.2", 5432, ReplicaRegion.EU_WEST, latency_ms=50.0),
        ReplicaNode("r3", "10.0.0.3", 5432, ReplicaRegion.AP_SOUTH, latency_ms=120.0),
    ]


def test_nearest_replica_selects_same_region() -> None:
    strategy = NearestReplicaStrategy()
    replicas = _make_replicas()
    result = strategy.select(replicas, ReplicaRegion.EU_WEST)
    assert result is not None
    assert result.name == "r2"


def test_latency_strategy_picks_fastest() -> None:
    strategy = LatencyBasedStrategy()
    replicas = _make_replicas()
    result = strategy.select(replicas, ReplicaRegion.US_EAST)
    assert result is not None
    assert result.latency_ms == 5.0


def test_round_robin_cycles() -> None:
    strategy = RoundRobinStrategy()
    replicas = _make_replicas()
    first = strategy.select(replicas, ReplicaRegion.US_EAST)
    second = strategy.select(replicas, ReplicaRegion.US_EAST)
    third = strategy.select(replicas, ReplicaRegion.US_EAST)
    fourth = strategy.select(replicas, ReplicaRegion.US_EAST)
    assert first is not None and second is not None and third is not None and fourth is not None
    assert first.name == "r1"
    assert second.name == "r2"
    assert third.name == "r3"
    assert fourth.name == "r1"


def test_router_returns_none_without_strategy() -> None:
    router = ReplicaRouter()
    assert router.route(ReplicaRegion.US_EAST) is None


def test_router_add_and_remove_replica() -> None:
    router = ReplicaRouter()
    r1 = ReplicaNode("r1", "10.0.0.1", 5432, ReplicaRegion.US_EAST, latency_ms=5.0)
    router.add_replica(r1)
    assert len(router.list_replicas()) == 1
    assert router.remove_replica("r1")
    assert len(router.list_replicas()) == 0


def test_router_routes_with_strategy() -> None:
    router = ReplicaRouter(strategy=LatencyBasedStrategy())
    for r in _make_replicas():
        router.add_replica(r)
    decision = router.route(ReplicaRegion.US_EAST)
    assert decision is not None
    assert decision.strategy == "latency"
    assert decision.endpoint == "10.0.0.1:5432"


def test_strategy_skips_unhealthy() -> None:
    strategy = LatencyBasedStrategy()
    replicas = [
        ReplicaNode("r1", "10.0.0.1", 5432, ReplicaRegion.US_EAST, latency_ms=5.0, healthy=False),
        ReplicaNode("r2", "10.0.0.2", 5432, ReplicaRegion.EU_WEST, latency_ms=50.0),
    ]
    result = strategy.select(replicas, ReplicaRegion.US_EAST)
    assert result is not None
    assert result.name == "r2"
