"""VectorSearchEngine — high-level orchestrator for RAG vector search."""

from __future__ import annotations

import logging
from typing import Any

from vector_search.builder import VectorIndexBuilder
from vector_search.embeddings import EmbeddingLoader, EmbeddingRecord
from vector_search.models import (
    DistanceMetric,
    IndexType,
    SearchQuery,
    SearchResult,
)
from vector_search.optimizer import QueryOptimizer
from vector_search.strategies import IndexStrategy

logger = logging.getLogger(__name__)


class VectorSearchEngine:
    """High-level API for vector similarity search.

    Usage::

        engine = VectorSearchEngine("documents", dimensions=1536)
        engine.build_index(row_count=500_000)

        results = engine.search(
            embedding=[0.1, 0.2, ...],
            top_k=10,
            filter_expr="metadata->>'category' = 'tech'",
        )
    """

    def __init__(
        self,
        table_name: str,
        dimensions: int = 1536,
        distance_metric: DistanceMetric = DistanceMetric.COSINE,
    ) -> None:
        self.table_name = table_name
        self.dimensions = dimensions
        self.distance_metric = distance_metric
        self._strategy: IndexStrategy | None = None
        self._builder = VectorIndexBuilder()
        self._optimizer = QueryOptimizer()

    def build_index(
        self,
        row_count: int,
        index_type: IndexType | None = None,
    ) -> str:
        """Build the optimal index for the given row count. Returns CREATE SQL."""
        result = self._builder.build(
            table_name=self.table_name,
            dimensions=self.dimensions,
            row_count=row_count,
            distance_metric=self.distance_metric,
            index_type=index_type,
        )
        self._strategy = result.strategy
        logger.info(
            "Built %s index for %d rows (est. %.1fs build time)",
            type(result.strategy).__name__,
            row_count,
            result.estimated_build_time_sec,
        )
        return result.create_sql

    def search(self, embedding: list[float], top_k: int = 10, **kwargs: Any) -> list[SearchResult]:
        """Search for similar vectors. Returns top_k results."""
        if self._strategy is None:
            raise RuntimeError("Call build_index() before searching")

        if len(embedding) != self.dimensions:
            raise ValueError(f"Embedding dimension {len(embedding)} != {self.dimensions}")

        query = SearchQuery(
            embedding=embedding,
            top_k=top_k,
            filter_expr=kwargs.get("filter_expr"),
            include_embeddings=kwargs.get("include_embeddings", False),
        )
        sql = self._strategy.search_sql(query)
        # In production: execute(sql) and parse results
        logger.info("Search SQL:\n%s", sql)
        return []

    def ingest(self, records: list[EmbeddingRecord], batch_size: int = 1000) -> int:
        """Ingest embeddings into the index."""
        if self._strategy is None:
            raise RuntimeError("Call build_index() before ingesting")

        loader = EmbeddingLoader(self._strategy, batch_size=batch_size)
        return loader.load(records)

    def optimize(self, row_count: int) -> dict[str, int]:
        """Run query optimizer and return suggested parameter changes."""
        if self._strategy is None:
            raise RuntimeError("Call build_index() before optimizing")

        result = self._optimizer.optimize(self._strategy, row_count)
        logger.info("Optimization: %s", result.reason)
        return result.optimized_params

    def maintenance_sql(self) -> list[str]:
        """Get maintenance SQL statements for the current index."""
        if self._strategy is None:
            raise RuntimeError("Call build_index() before maintenance")
        return self._strategy.maintenance_sql()
