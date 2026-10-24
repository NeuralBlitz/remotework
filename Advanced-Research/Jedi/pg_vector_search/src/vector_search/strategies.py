"""Index strategies — Factory Pattern for vector indexing."""

from __future__ import annotations

import abc
import logging

from vector_search.models import (
    DistanceMetric,
    HNSWConfig,
    IndexConfig,
    IVFFlatConfig,
    SearchQuery,
)

logger = logging.getLogger(__name__)


class IndexStrategy(abc.ABC):
    """Abstract base for all vector index strategies."""

    def __init__(self, config: IndexConfig) -> None:
        self.config = config

    @abc.abstractmethod
    def create_index_sql(self) -> str:
        """Return the SQL to create this index."""
        ...

    @abc.abstractmethod
    def search_sql(self, query: SearchQuery) -> str:
        """Return the SQL to search this index."""
        ...

    @abc.abstractmethod
    def insert_sql(self, rows: int) -> str:
        """Return the SQL to insert vectors."""
        ...

    @abc.abstractmethod
    def recommended_for(self, row_count: int) -> bool:
        """Whether this strategy is recommended for the given row count."""
        ...

    @abc.abstractmethod
    def maintenance_sql(self) -> list[str]:
        """Return SQL statements for index maintenance."""
        ...

    def distance_operator(self) -> str:
        """Return the pgvector distance operator."""
        match self.config.distance_metric:
            case DistanceMetric.COSINE:
                return "<=>"
            case DistanceMetric.L2:
                return "<->"
            case DistanceMetric.INNER_PRODUCT:
                return "<#>"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(table={self.config.table_name})"


class HNSWIndex(IndexStrategy):
    """HNSW (Hierarchical Navigable Small World) index.

    Best for: High recall, low latency queries on datasets up to ~10M vectors.
    Trade-off: Higher memory usage, slower build time than IVFFlat.
    """

    def __init__(self, config: IndexConfig, hnsw: HNSWConfig | None = None) -> None:
        super().__init__(config)
        self.hnsw = hnsw or HNSWConfig()

    def create_index_sql(self) -> str:
        metric_map = {
            DistanceMetric.COSINE: "vector_cosine_ops",
            DistanceMetric.L2: "vector_l2_ops",
            DistanceMetric.INNER_PRODUCT: "vector_ip_ops",
        }
        ops = metric_map[self.config.distance_metric]
        idx_name = f"idx_{self.config.table_name}_hnsw"

        return (
            f"CREATE INDEX IF NOT EXISTS {idx_name} "
            f"ON {self.config.table_name} "
            f"USING hnsw ({self.config.column_name} {ops}) "
            f"WITH (m = {self.hnsw.m}, ef_construction = {self.hnsw.ef_construction})"
        )

    def search_sql(self, query: SearchQuery) -> str:
        vec = "[" + ", ".join(f"{v:.6f}" for v in query.embedding) + "]"
        limit = f"LIMIT {query.top_k}"

        sql = (
            f"SET LOCAL hnsw.ef_search = {self.hnsw.ef_search};\n"
            f"SELECT id, {self.config.column_name} {self.distance_operator()} '{vec}' AS score"
        )

        if query.include_embeddings:
            sql += f", {self.config.column_name}"

        sql += f" FROM {self.config.table_name}"

        if query.filter_expr:
            sql += f" WHERE {query.filter_expr}"

        sql += f" ORDER BY score {limit}"
        return sql

    def insert_sql(self, rows: int) -> str:
        placeholders = ", ".join("(%s, %s::vector)" for _ in range(rows))
        return (
            f"INSERT INTO {self.config.table_name} (id, {self.config.column_name}) "
            f"VALUES {placeholders} ON CONFLICT (id) DO UPDATE "
            f"SET {self.config.column_name} = EXCLUDED.{self.config.column_name}"
        )

    def recommended_for(self, row_count: int) -> bool:
        return row_count <= 10_000_000

    def maintenance_sql(self) -> list[str]:
        return [
            f"REINDEX INDEX CONCURRENTLY idx_{self.config.table_name}_hnsw",
            f"ANALYZE {self.config.table_name}",
        ]


class IVFFlatIndex(IndexStrategy):
    """IVFFlat (Inverted File with Flat compression) index.

    Best for: Large datasets (>10M vectors) where memory is constrained.
    Trade-off: Lower recall than HNSW, requires tuning `lists` and `probes`.
    """

    def __init__(self, config: IndexConfig, ivf: IVFFlatConfig | None = None) -> None:
        super().__init__(config)
        self.ivf = ivf or IVFFlatConfig()

    def create_index_sql(self) -> str:
        metric_map = {
            DistanceMetric.COSINE: "vector_cosine_ops",
            DistanceMetric.L2: "vector_l2_ops",
            DistanceMetric.INNER_PRODUCT: "vector_ip_ops",
        }
        ops = metric_map[self.config.distance_metric]
        idx_name = f"idx_{self.config.table_name}_ivfflat"

        return (
            f"CREATE INDEX IF NOT EXISTS {idx_name} "
            f"ON {self.config.table_name} "
            f"USING ivfflat ({self.config.column_name} {ops}) "
            f"WITH (lists = {self.ivf.lists})"
        )

    def search_sql(self, query: SearchQuery) -> str:
        vec = "[" + ", ".join(f"{v:.6f}" for v in query.embedding) + "]"
        limit = f"LIMIT {query.top_k}"

        sql = (
            f"SET LOCAL ivfflat.probes = {self.ivf.probes};\n"
            f"SELECT id, {self.config.column_name} {self.distance_operator()} '{vec}' AS score"
        )

        if query.include_embeddings:
            sql += f", {self.config.column_name}"

        sql += f" FROM {self.config.table_name}"

        if query.filter_expr:
            sql += f" WHERE {query.filter_expr}"

        sql += f" ORDER BY score {limit}"
        return sql

    def insert_sql(self, rows: int) -> str:
        placeholders = ", ".join("(%s, %s::vector)" for _ in range(rows))
        return (
            f"INSERT INTO {self.config.table_name} (id, {self.config.column_name}) "
            f"VALUES {placeholders} ON CONFLICT (id) DO UPDATE "
            f"SET {self.config.column_name} = EXCLUDED.{self.config.column_name}"
        )

    def recommended_for(self, row_count: int) -> bool:
        return row_count > 10_000_000

    def maintenance_sql(self) -> list[str]:
        return [
            f"REINDEX INDEX CONCURRENTLY idx_{self.config.table_name}_ivfflat",
            f"ANALYZE {self.config.table_name}",
        ]
