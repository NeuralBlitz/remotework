"""Factory Pattern for instantiating vector index strategies."""

from __future__ import annotations

import logging
import math

from vector_search.models import (
    HNSWConfig,
    IndexConfig,
    IndexType,
    IVFFlatConfig,
)
from vector_search.strategies import HNSWIndex, IndexStrategy, IVFFlatIndex

logger = logging.getLogger(__name__)


class IndexFactory:
    """Creates index strategy instances based on configuration and data characteristics.

    Usage::

        factory = IndexFactory()
        idx = factory.create(IndexType.HNSW, config, hnsw=HNSWConfig(m=32))
        idx = factory.auto_select(config, row_count=5_000_000)
    """

    _registry: dict[IndexType, type[IndexStrategy]] = {
        IndexType.HNSW: HNSWIndex,
        IndexType.IVFFLAT: IVFFlatIndex,
    }

    def create(
        self,
        index_type: IndexType,
        config: IndexConfig,
        *,
        hnsw: HNSWConfig | None = None,
        ivf: IVFFlatConfig | None = None,
    ) -> IndexStrategy:
        """Create an index strategy by explicit type."""
        cls = self._registry.get(index_type)
        if cls is None:
            raise ValueError(f"Unknown index type: {index_type}")

        config = IndexConfig(
            table_name=config.table_name,
            column_name=config.column_name,
            dimensions=config.dimensions,
            distance_metric=config.distance_metric,
            index_type=index_type,
        )

        if index_type == IndexType.HNSW:
            return HNSWIndex(config, hnsw=hnsw)
        elif index_type == IndexType.IVFFLAT:
            return IVFFlatIndex(config, ivf=ivf)

        return cls(config)

    def auto_select(self, config: IndexConfig, row_count: int) -> IndexStrategy:
        """Automatically select the best index type based on row count.

        Rules:
        - <= 10M rows → HNSW (speed priority)
        - > 10M rows  → IVFFlat (memory priority)
        - Lists parameter is calculated as sqrt(rows), clamped to [1, 65535]
        """
        if row_count <= 10_000_000:
            logger.info("Auto-selected HNSW for %d rows", row_count)
            return self.create(IndexType.HNSW, config)
        else:
            optimal_lists = self._calculate_optimal_lists(row_count)
            logger.info(
                "Auto-selected IVFFlat for %d rows (lists=%d)",
                row_count,
                optimal_lists,
            )
            ivf = IVFFlatConfig(lists=optimal_lists)
            return self.create(IndexType.IVFFLAT, config, ivf=ivf)

    @staticmethod
    def _calculate_optimal_lists(row_count: int) -> int:
        """Calculate optimal IVFFlat lists parameter.

        Rule of thumb: lists = sqrt(rows), clamped and rounded.
        Minimum 1, maximum 65535 (PostgreSQL index limit).
        """
        optimal = int(math.sqrt(row_count))
        return max(1, min(optimal, 65_535))

    def register(self, index_type: IndexType, cls: type[IndexStrategy]) -> None:
        """Register a custom index strategy."""
        self._registry[index_type] = cls

    def available_types(self) -> list[IndexType]:
        """List all registered index types."""
        return list(self._registry.keys())
