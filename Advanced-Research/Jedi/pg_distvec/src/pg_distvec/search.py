from __future__ import annotations

from typing import Any

from pg_distvec.models import ShardedQuery, ShardResult
from pg_distvec.strategies import SearchStrategy


class DistributedSearchEngine:
    def __init__(self, shards: list[str], strategy: SearchStrategy) -> None:
        self._shards = shards
        self._strategy = strategy

    @property
    def strategy(self) -> SearchStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: SearchStrategy) -> None:
        self._strategy = strategy

    @property
    def shards(self) -> list[str]:
        return list(self._shards)

    def search(self, query: ShardedQuery) -> list[dict[str, Any]]:
        target_shards = self._strategy.select_shards(query, self._shards)
        results = self._query_shards(query, target_shards)
        return self._strategy.merge_results(results, query.top_k)

    def _query_shards(self, query: ShardedQuery, shard_ids: list[str]) -> list[ShardResult]:
        results: list[ShardResult] = []
        for sid in shard_ids:
            matches = [
                {"id": f"{sid}-doc-{i}", "score": 0.9 - i * 0.1, "vector": query.vector}
                for i in range(min(query.top_k, 3))
            ]
            results.append(ShardResult(shard_id=sid, matches=matches, latency_ms=1.5))
        return results
