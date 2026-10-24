import pytest

from vecdb_shard.flyweight import IndexFactory, SharedIndexFlyweight
from vecdb_shard.models import ShardConfig, TenantIndex
from vecdb_shard.sharder import VectorSharder


def test_create_tenant():
    config = ShardConfig(num_shards=4, dimensions=128)
    sharder = VectorSharder(config)
    shards = sharder.create_tenant("tenant_1")
    assert len(shards) == 4
    assert all(s.tenant_id == "tenant_1" for s in shards)


def test_add_vectors():
    config = ShardConfig(num_shards=2, dimensions=4)
    sharder = VectorSharder(config)
    sharder.create_tenant("t1")
    vectors = [[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]]
    counts = sharder.add_vectors("t1", vectors)
    assert sharder.total_vectors("t1") == 2


def test_flyweight_sharing():
    factory = IndexFactory()
    config = ShardConfig(index_type="hnsw", dimensions=128)
    idx1 = factory.get_index(config)
    idx2 = factory.get_index(config)
    assert idx1 is idx2
    assert factory.cache_size() == 1


def test_different_configs_different_flyweights():
    factory = IndexFactory()
    config1 = ShardConfig(index_type="hnsw", dimensions=128)
    config2 = IndexFactory()
    idx1 = factory.get_index(config1)
    config2_cfg = ShardConfig(index_type="flat", dimensions=64)
    idx2 = factory.get_index(config2_cfg)
    assert factory.cache_size() == 2


def test_tenant_capacity():
    ti = TenantIndex(tenant_id="t", vector_count=500)
    assert ti.capacity_used(1000) == 0.5
    assert not ti.is_full(1000)
    assert ti.is_full(500)


def test_invalid_tenant():
    config = ShardConfig(num_shards=2, dimensions=4)
    sharder = VectorSharder(config)
    with pytest.raises(ValueError, match="not found"):
        sharder.add_vectors("ghost", [[1.0]])


def test_get_shard():
    config = ShardConfig(num_shards=3, dimensions=8)
    sharder = VectorSharder(config)
    sharder.create_tenant("t1")
    shard = sharder.get_shard("t1", 1)
    assert shard.shard_id == 1


def test_invalid_config():
    config = ShardConfig(num_shards=-1)
    assert not config.validate()


def test_factory_clear():
    factory = IndexFactory()
    factory.get_index(ShardConfig(index_type="hnsw", dimensions=64))
    assert factory.cache_size() == 1
    factory.clear()
    assert factory.cache_size() == 0


def test_total_vectors_empty():
    config = ShardConfig(num_shards=2, dimensions=4)
    sharder = VectorSharder(config)
    assert sharder.total_vectors("nonexistent") == 0
