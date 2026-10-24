"""Query optimization — adapts index parameters at runtime."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from vector_search.strategies import HNSWIndex, IndexStrategy, IVFFlatIndex

logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult:
    """Result of a query optimization pass."""

    original_strategy: IndexStrategy
    optimized_params: dict[str, int]
    reason: str


class QueryOptimizer:
    """Tunes index parameters based on query patterns and data characteristics.

    Optimizations:
    - HNSW ef_search: increase for high-recall queries, decrease for speed
    - IVFFlat probes: increase for recall, decrease for speed
    - Lists recalculation when row count changes significantly
    """

    def optimize(self, strategy: IndexStrategy, row_count: int) -> OptimizationResult:
        """Analyze and suggest optimized parameters."""
        if isinstance(strategy, HNSWIndex):
            return self._optimize_hnsw(strategy, row_count)
        elif isinstance(strategy, IVFFlatIndex):
            return self._optimize_ivfflat(strategy, row_count)
        return OptimizationResult(strategy, {}, "No optimization needed")

    def _optimize_hnsw(self, idx: HNSWIndex, row_count: int) -> OptimizationResult:
        params: dict[str, int] = {}
        reasons: list[str] = []

        # Scale ef_search with dataset size for better recall
        if row_count > 1_000_000 and idx.hnsw.ef_search < 100:
            params["ef_search"] = min(idx.hnsw.ef_search * 2, 200)
            reasons.append(f"Increased ef_search to {params['ef_search']} for large dataset")

        # Scale m for larger datasets
        if row_count > 5_000_000 and idx.hnsw.m < 32:
            params["m"] = min(idx.hnsw.m * 2, 48)
            reasons.append(f"Increased m to {params['m']} for better connectivity")

        return OptimizationResult(
            original_strategy=idx,
            optimized_params=params,
            reason="; ".join(reasons) if reasons else "HNSW parameters already optimal",
        )

    def _optimize_ivfflat(self, idx: IVFFlatIndex, row_count: int) -> OptimizationResult:
        params: dict[str, int] = {}
        reasons: list[str] = []

        # Recalculate optimal lists
        import math

        optimal_lists = max(1, min(int(math.sqrt(row_count)), 65_535))
        if optimal_lists != idx.ivf.lists:
            params["lists"] = optimal_lists
            reasons.append(f"Recommends lists={optimal_lists} for {row_count} rows")

        # Scale probes with lists
        optimal_probes = max(1, optimal_lists // 10)
        if optimal_probes != idx.ivf.probes:
            params["probes"] = optimal_probes
            reasons.append(f"Recommends probes={optimal_probes} (~10% of lists)")

        return OptimizationResult(
            original_strategy=idx,
            optimized_params=params,
            reason="; ".join(reasons) if reasons else "IVFFlat parameters already optimal",
        )
