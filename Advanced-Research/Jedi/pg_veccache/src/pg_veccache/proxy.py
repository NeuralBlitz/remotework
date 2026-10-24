from __future__ import annotations

from collections import OrderedDict
from datetime import datetime

from pg_veccache.models import CacheConfig, CacheEntry


class EmbeddingBackend:
    def __init__(self) -> None:
        self._store: dict[str, CacheEntry] = {}
        self._fetch_count = 0

    def get(self, key: str) -> CacheEntry | None:
        self._fetch_count += 1
        return self._store.get(key)

    def put(self, entry: CacheEntry) -> None:
        self._store[entry.key] = entry

    def delete(self, key: str) -> bool:
        return self._store.pop(key, None) is not None

    def exists(self, key: str) -> bool:
        return key in self._store

    def list_keys(self) -> list[str]:
        return list(self._store.keys())

    @property
    def fetch_count(self) -> int:
        return self._fetch_count

    @property
    def size(self) -> int:
        return len(self._store)


class EmbeddingCacheProxy:
    def __init__(
        self, backend: EmbeddingBackend | None = None, config: CacheConfig | None = None
    ) -> None:
        self._config = config or CacheConfig()
        if not self._config.validate():
            raise ValueError("Invalid cache config")
        self._backend = backend or EmbeddingBackend()
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> CacheEntry | None:
        if key in self._cache:
            entry = self._cache[key]
            self._cache.move_to_end(key)
            entry.touch()
            self._hits += 1
            return entry
        self._misses += 1
        entry = self._backend.get(key)
        if entry is not None:
            self._put_cache(key, entry)
        return entry

    def put(self, entry: CacheEntry) -> None:
        self._backend.put(entry)
        self._put_cache(entry.key, entry)

    def _put_cache(self, key: str, entry: CacheEntry) -> None:
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = entry
        while len(self._cache) > self._config.max_entries:
            self._cache.popitem(last=False)

    def delete(self, key: str) -> bool:
        self._cache.pop(key, None)
        return self._backend.delete(key)

    def exists(self, key: str) -> bool:
        if key in self._cache:
            return True
        return self._backend.exists(key)

    def clear(self) -> None:
        self._cache.clear()

    @property
    def cache_size(self) -> int:
        return len(self._cache)

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def misses(self) -> int:
        return self._misses

    @property
    def hit_rate(self) -> float:
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0

    @property
    def config(self) -> CacheConfig:
        return self._config

    def keys(self) -> list[str]:
        return list(self._cache.keys())

    def warm(self, entries: list[CacheEntry]) -> int:
        count = 0
        for entry in entries:
            if entry.key not in self._cache:
                self._put_cache(entry.key, entry)
                count += 1
        return count

    def stats(self) -> dict[str, int | float]:
        return {
            "cache_size": self.cache_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hit_rate,
            "backend_fetches": self._backend.fetch_count,
            "backend_size": self._backend.size,
        }
