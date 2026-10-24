from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pg_distvec.models import ShardedQuery, ShardResult


class SearchStrategy(ABC):
    @abstractmethod
    def select_shards(self, query: ShardedQuery, available_shards: list[str]) -> list[str]: ...

    @abstractmethod
    def merge_results(self, results: list[ShardResult], top_k: int) -> list[dict[str, Any]]: ...


class ScatterGatherStrategy(SearchStrategy):
    def select_shards(self, query: ShardedQuery, available_shards: list[str]) -> list[str]:
        return list(available_shards)

    def merge_results(self, results: list[ShardResult], top_k: int) -> list[dict[str, Any]]:
        all_matches: list[dict[str, Any]] = []
        for r in results:
            if r.is_ok:
                all_matches.extend(r.matches)
        all_matches.sort(key=lambda m: m.get("score", 0.0), reverse=True)
        return all_matches[:top_k]


class RouteByTenantStrategy(SearchStrategy):
    def select_shards(self, query: ShardedQuery, available_shards: list[str]) -> list[str]:
        if query.tenant_id and query.shard_ids:
            return [s for s in available_shards if s in query.shard_ids]
        if query.tenant_id:
            idx = hash(query.tenant_id) % len(available_shards)
            return [available_shards[idx]]
        return list(available_shards)

    def merge_results(self, results: list[ShardResult], top_k: int) -> list[dict[str, Any]]:
        all_matches: list[dict[str, Any]] = []
        for r in results:
            if r.is_ok:
                all_matches.extend(r.matches)
        return all_matches[:top_k]
