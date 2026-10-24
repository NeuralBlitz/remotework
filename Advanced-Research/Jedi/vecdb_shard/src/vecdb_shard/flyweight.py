from __future__ import annotations

from vecdb_shard.models import ShardConfig


class SharedIndexFlyweight:
    def __init__(self, index_type: str, dimensions: int) -> None:
        self._index_type = index_type
        self._dimensions = dimensions
        self._structure: list[float] = [0.0] * dimensions

    @property
    def index_type(self) -> str:
        return self._index_type

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def lookup(self, key: int) -> float:
        idx = key % self._dimensions
        return self._structure[idx]


class IndexFactory:
    def __init__(self) -> None:
        self._flyweights: dict[str, SharedIndexFlyweight] = {}

    def get_index(self, config: ShardConfig) -> SharedIndexFlyweight:
        key = f"{config.index_type}_{config.dimensions}"
        if key not in self._flyweights:
            self._flyweights[key] = SharedIndexFlyweight(config.index_type, config.dimensions)
        return self._flyweights[key]

    def cache_size(self) -> int:
        return len(self._flyweights)

    def clear(self) -> None:
        self._flyweights.clear()
