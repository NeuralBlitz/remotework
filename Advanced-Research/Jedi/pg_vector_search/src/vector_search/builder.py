"""VectorIndexBuilder — calculates optimal index parameters from row counts."""

from __future__ import annotations

import math
from dataclasses import dataclass

from vector_search.factory import IndexFactory
from vector_search.models import (
    DistanceMetric,
    IndexConfig,
    IndexType,
)
from vector_search.strategies import IndexStrategy


@dataclass
class BuildResult:
    """Result of building an index configuration."""

    strategy: IndexStrategy
    create_sql: str
    estimated_build_time_sec: float


class VectorIndexBuilder:
    """Calculates optimal parameters and builds index configuration.

    Usage::

        builder = VectorIndexBuilder()
        result = builder.build(
            table_name="documents",
            dimensions=1536,
            row_count=500_000,
        )
        print(result.create_sql)
    """

    def __init__(self) -> None:
        self._factory = IndexFactory()

    def build(
        self,
        table_name: str,
        dimensions: int,
        row_count: int,
        distance_metric: DistanceMetric = DistanceMetric.COSINE,
        index_type: IndexType | None = None,
    ) -> BuildResult:
        """Build the optimal index configuration for the given parameters.

        If index_type is None, the factory auto-selects based on row_count.
        """
        config = IndexConfig(
            table_name=table_name,
            dimensions=dimensions,
            distance_metric=distance_metric,
        )

        if index_type is not None:
            strategy = self._factory.create(index_type, config)
        else:
            strategy = self._factory.auto_select(config, row_count)

        return BuildResult(
            strategy=strategy,
            create_sql=strategy.create_index_sql(),
            estimated_build_time_sec=self._estimate_build_time(strategy, row_count),
        )

    def calculate_optimal_lists(self, row_count: int) -> int:
        """Calculate the optimal IVFFlat lists parameter.

        Formula: lists = sqrt(rows), clamped to [1, 65535].
        This balances recall (more lists = better) with build time.
        """
        return max(1, min(int(math.sqrt(row_count)), 65_535))

    @staticmethod
    def _estimate_build_time(strategy: IndexStrategy, row_count: int) -> float:
        """Rough estimate of index build time in seconds."""
        if isinstance(strategy, type(strategy)) and hasattr(strategy, "hnsw"):
            # HNSW: ~O(n * m * log(n))
            return row_count * 0.0001
        # IVFFlat: ~O(n * log(lists))
        return row_count * 0.00005
