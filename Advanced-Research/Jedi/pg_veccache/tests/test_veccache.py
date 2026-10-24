from __future__ import annotations

from datetime import datetime

import pytest

from pg_veccache.models import CacheConfig, CacheEntry
from pg_veccache.proxy import EmbeddingBackend, EmbeddingCacheProxy


@pytest.fixture
def config() -> CacheConfig:
    return CacheConfig(max_entries=5, ttl_seconds=3600)


@pytest.fixture
def backend() -> EmbeddingBackend:
    return EmbeddingBackend()


@pytest.fixture
def proxy(backend: EmbeddingBackend, config: CacheConfig) -> EmbeddingCacheProxy:
    return EmbeddingCacheProxy(backend, config)


def make_entry(key: str = "k1", dim: int = 3, value: float = 0.5) -> CacheEntry:
    return CacheEntry(key=key, embedding=[value] * dim, metadata={"source": "test"})


class TestCacheConfig:
    def test_validate_valid(self, config: CacheConfig) -> None:
        assert config.validate() is True

    def test_validate_invalid(self) -> None:
        assert CacheConfig(max_entries=0).validate() is False
        assert CacheConfig(ttl_seconds=0).validate() is False


class TestCacheEntry:
    def test_dimension(self) -> None:
        entry = make_entry(dim=128)
        assert entry.dimension == 128

    def test_touch(self) -> None:
        entry = make_entry()
        assert entry.access_count == 0
        entry.touch()
        assert entry.access_count == 1


class TestEmbeddingBackend:
    def test_put_get(self, backend: EmbeddingBackend) -> None:
        entry = make_entry()
        backend.put(entry)
        assert backend.get("k1") == entry

    def test_get_missing(self, backend: EmbeddingBackend) -> None:
        assert backend.get("missing") is None

    def test_delete(self, backend: EmbeddingBackend) -> None:
        backend.put(make_entry())
        assert backend.delete("k1") is True
        assert backend.delete("k1") is False

    def test_exists(self, backend: EmbeddingBackend) -> None:
        backend.put(make_entry())
        assert backend.exists("k1") is True
        assert backend.exists("k2") is False

    def test_size(self, backend: EmbeddingBackend) -> None:
        assert backend.size == 0
        backend.put(make_entry())
        assert backend.size == 1


class TestEmbeddingCacheProxy:
    def test_cache_miss_hits_backend(
        self, proxy: EmbeddingCacheProxy, backend: EmbeddingBackend
    ) -> None:
        entry = make_entry()
        backend.put(entry)
        result = proxy.get("k1")
        assert result is not None
        assert result.key == "k1"
        assert proxy.misses == 1

    def test_cache_hit(self, proxy: EmbeddingCacheProxy, backend: EmbeddingBackend) -> None:
        entry = make_entry()
        backend.put(entry)
        proxy.get("k1")
        result = proxy.get("k1")
        assert result is not None
        assert proxy.hits == 1
        assert proxy.misses == 1

    def test_put_populates_cache(self, proxy: EmbeddingCacheProxy) -> None:
        proxy.put(make_entry())
        assert proxy.cache_size == 1
        assert proxy.exists("k1")

    def test_lru_eviction(self, proxy: EmbeddingCacheProxy) -> None:
        for i in range(7):
            proxy.put(make_entry(key=f"k{i}"))
        assert proxy.cache_size == 5
        assert "k0" not in proxy.keys()
        assert "k6" in proxy.keys()

    def test_delete(self, proxy: EmbeddingCacheProxy) -> None:
        proxy.put(make_entry())
        assert proxy.delete("k1") is True
        assert proxy.cache_size == 0

    def test_clear(self, proxy: EmbeddingCacheProxy) -> None:
        proxy.put(make_entry("k1"))
        proxy.put(make_entry("k2"))
        proxy.clear()
        assert proxy.cache_size == 0

    def test_hit_rate(self, proxy: EmbeddingCacheProxy, backend: EmbeddingBackend) -> None:
        assert proxy.hit_rate == 0.0
        proxy.put(make_entry())
        proxy.get("k1")
        proxy.get("k2")
        assert proxy.hit_rate == pytest.approx(0.5)

    def test_warm(self, proxy: EmbeddingCacheProxy) -> None:
        entries = [make_entry(f"k{i}") for i in range(3)]
        count = proxy.warm(entries)
        assert count == 3
        assert proxy.cache_size == 3

    def test_stats(self, proxy: EmbeddingCacheProxy) -> None:
        proxy.put(make_entry())
        stats = proxy.stats()
        assert "cache_size" in stats
        assert "hit_rate" in stats
        assert stats["cache_size"] == 1

    def test_invalid_config_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid"):
            EmbeddingCacheProxy(config=CacheConfig(max_entries=0))
