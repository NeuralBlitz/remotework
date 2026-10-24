"""Tests for the Vector Search Engine."""

from __future__ import annotations

import pytest

from vector_search.builder import VectorIndexBuilder
from vector_search.embeddings import EmbeddingLoader, EmbeddingRecord
from vector_search.engine import VectorSearchEngine
from vector_search.factory import IndexFactory
from vector_search.models import (
    DistanceMetric,
    IndexConfig,
    IndexType,
    IVFFlatConfig,
    SearchQuery,
)
from vector_search.optimizer import QueryOptimizer
from vector_search.strategies import HNSWIndex, IVFFlatIndex


@pytest.fixture
def config() -> IndexConfig:
    return IndexConfig(
        table_name="documents",
        dimensions=1536,
        distance_metric=DistanceMetric.COSINE,
    )


@pytest.fixture
def sample_embedding() -> list[float]:
    return [0.1] * 1536


# ── Factory Tests ──────────────────────────────────────────────────


class TestIndexFactory:
    def test_create_hnsw(self, config: IndexConfig) -> None:
        factory = IndexFactory()
        idx = factory.create(IndexType.HNSW, config)
        assert isinstance(idx, HNSWIndex)

    def test_create_ivfflat(self, config: IndexConfig) -> None:
        factory = IndexFactory()
        idx = factory.create(IndexType.IVFFLAT, config)
        assert isinstance(idx, IVFFlatIndex)

    def test_auto_select_small_dataset(self, config: IndexConfig) -> None:
        factory = IndexFactory()
        idx = factory.auto_select(config, row_count=100_000)
        assert isinstance(idx, HNSWIndex)

    def test_auto_select_large_dataset(self, config: IndexConfig) -> None:
        factory = IndexFactory()
        idx = factory.auto_select(config, row_count=50_000_000)
        assert isinstance(idx, IVFFlatIndex)

    def test_unknown_type_raises(self, config: IndexConfig) -> None:
        factory = IndexFactory()
        with pytest.raises(ValueError, match="Unknown index type"):
            # noinspection PyTypeChecker
            factory.create("nonexistent", config)  # type: ignore[arg-type]

    def test_register_custom_type(self, config: IndexConfig) -> None:
        factory = IndexFactory()
        factory.register(IndexType.HNSW, HNSWIndex)
        assert IndexType.HNSW in factory.available_types()


# ── HNSW Strategy Tests ────────────────────────────────────────────


class TestHNSWIndex:
    def test_create_index_sql(self, config: IndexConfig) -> None:
        idx = HNSWIndex(config)
        sql = idx.create_index_sql()
        assert "USING hnsw" in sql
        assert "vector_cosine_ops" in sql
        assert "m = 16" in sql
        assert "ef_construction = 200" in sql

    def test_search_sql(self, config: IndexConfig, sample_embedding: list[float]) -> None:
        idx = HNSWIndex(config)
        query = SearchQuery(embedding=sample_embedding, top_k=5)
        sql = idx.search_sql(query)
        assert "hnsw.ef_search" in sql
        assert "LIMIT 5" in sql
        assert "<=>" in sql  # cosine distance operator

    def test_search_sql_with_filter(
        self, config: IndexConfig, sample_embedding: list[float]
    ) -> None:
        idx = HNSWIndex(config)
        query = SearchQuery(embedding=sample_embedding, top_k=10, filter_expr="id > 100")
        sql = idx.search_sql(query)
        assert "WHERE id > 100" in sql

    def test_search_sql_l2_metric(self, sample_embedding: list[float]) -> None:
        config = IndexConfig(table_name="docs", distance_metric=DistanceMetric.L2)
        idx = HNSWIndex(config)
        query = SearchQuery(embedding=sample_embedding, top_k=3)
        sql = idx.search_sql(query)
        assert "<->" in sql  # L2 distance operator

    def test_recommended_for_small(self, config: IndexConfig) -> None:
        idx = HNSWIndex(config)
        assert idx.recommended_for(1_000_000) is True
        assert idx.recommended_for(10_000_000) is True
        assert idx.recommended_for(50_000_000) is False

    def test_maintenance_sql(self, config: IndexConfig) -> None:
        idx = HNSWIndex(config)
        sqls = idx.maintenance_sql()
        assert len(sqls) == 2
        assert "REINDEX" in sqls[0]


# ── IVFFlat Strategy Tests ─────────────────────────────────────────


class TestIVFFlatIndex:
    def test_create_index_sql(self, config: IndexConfig) -> None:
        idx = IVFFlatIndex(config, IVFFlatConfig(lists=256))
        sql = idx.create_index_sql()
        assert "USING ivfflat" in sql
        assert "lists = 256" in sql

    def test_search_sql(self, config: IndexConfig, sample_embedding: list[float]) -> None:
        idx = IVFFlatIndex(config, IVFFlatConfig(probes=15))
        query = SearchQuery(embedding=sample_embedding, top_k=10)
        sql = idx.search_sql(query)
        assert "ivfflat.probes = 15" in sql
        assert "LIMIT 10" in sql

    def test_recommended_for_large(self, config: IndexConfig) -> None:
        idx = IVFFlatIndex(config)
        assert idx.recommended_for(1_000_000) is False
        assert idx.recommended_for(50_000_000) is True


# ── Builder Tests ──────────────────────────────────────────────────


class TestVectorIndexBuilder:
    def test_build_auto_selects_hnsw(self) -> None:
        builder = VectorIndexBuilder()
        result = builder.build("docs", dimensions=768, row_count=100_000)
        assert isinstance(result.strategy, HNSWIndex)
        assert "hnsw" in result.create_sql.lower()

    def test_build_auto_selects_ivfflat(self) -> None:
        builder = VectorIndexBuilder()
        result = builder.build("docs", dimensions=768, row_count=50_000_000)
        assert isinstance(result.strategy, IVFFlatIndex)
        assert "ivfflat" in result.create_sql.lower()

    def test_build_explicit_type(self) -> None:
        builder = VectorIndexBuilder()
        result = builder.build("docs", dimensions=768, row_count=100, index_type=IndexType.IVFFLAT)
        assert isinstance(result.strategy, IVFFlatIndex)

    def test_calculate_optimal_lists(self) -> None:
        builder = VectorIndexBuilder()
        assert builder.calculate_optimal_lists(100) == 10
        assert builder.calculate_optimal_lists(10_000) == 100
        assert builder.calculate_optimal_lists(1_000_000) == 1000
        assert builder.calculate_optimal_lists(100_000_000_000) == 65_535  # clamped

    def test_estimated_build_time(self) -> None:
        builder = VectorIndexBuilder()
        result = builder.build("docs", dimensions=768, row_count=1_000_000)
        assert result.estimated_build_time_sec > 0


# ── Embedding Loader Tests ─────────────────────────────────────────


class TestEmbeddingLoader:
    def test_validate_dimensions(self, config: IndexConfig) -> None:
        idx = HNSWIndex(config)
        loader = EmbeddingLoader(idx)
        records = [
            EmbeddingRecord(id="1", embedding=[0.1] * 1536),
            EmbeddingRecord(id="2", embedding=[0.1] * 512),  # wrong dim
            EmbeddingRecord(id="3", embedding=[0.1] * 1536),
        ]
        valid = loader.validate_dimensions(records)
        assert len(valid) == 2

    def test_batch(self, config: IndexConfig) -> None:
        idx = HNSWIndex(config)
        loader = EmbeddingLoader(idx, batch_size=2)
        records = [EmbeddingRecord(id=str(i), embedding=[0.1] * 1536) for i in range(5)]
        batches = list(loader.batch(records))
        assert len(batches) == 3
        assert len(batches[0]) == 2
        assert len(batches[2]) == 1

    def test_load(self, config: IndexConfig) -> None:
        idx = HNSWIndex(config)
        loader = EmbeddingLoader(idx)
        records = [EmbeddingRecord(id=str(i), embedding=[0.1] * 1536) for i in range(10)]
        count = loader.load(records)
        assert count == 10


# ── Optimizer Tests ────────────────────────────────────────────────


class TestQueryOptimizer:
    def test_optimize_hnsw_large_dataset(self, config: IndexConfig) -> None:
        idx = HNSWIndex(config)
        optimizer = QueryOptimizer()
        result = optimizer.optimize(idx, row_count=5_000_000)
        assert "ef_search" in result.optimized_params or "m" in result.optimized_params

    def test_optimize_ivfflat(self, config: IndexConfig) -> None:
        idx = IVFFlatIndex(config)
        optimizer = QueryOptimizer()
        result = optimizer.optimize(idx, row_count=50_000_000)
        assert (
            "lists" in result.optimized_params
            or result.reason == "IVFFlat parameters already optimal"
        )


# ── Engine Integration Tests ───────────────────────────────────────


class TestVectorSearchEngine:
    def test_build_and_search(self, sample_embedding: list[float]) -> None:
        engine = VectorSearchEngine("documents", dimensions=1536)
        sql = engine.build_index(row_count=500_000)
        assert "hnsw" in sql.lower()

        # search should not raise
        engine.search(sample_embedding, top_k=5)

    def test_search_before_build_raises(self, sample_embedding: list[float]) -> None:
        engine = VectorSearchEngine("documents")
        with pytest.raises(RuntimeError, match="Call build_index"):
            engine.search(sample_embedding)

    def test_wrong_dimension_raises(self) -> None:
        engine = VectorSearchEngine("documents", dimensions=1536)
        engine.build_index(row_count=100)
        with pytest.raises(ValueError, match="dimension"):
            engine.search([0.1] * 768)

    def test_ingest(self) -> None:
        engine = VectorSearchEngine("documents", dimensions=1536)
        engine.build_index(row_count=100)
        records = [EmbeddingRecord(id=str(i), embedding=[0.1] * 1536) for i in range(5)]
        count = engine.ingest(records)
        assert count == 5

    def test_maintenance_sql(self) -> None:
        engine = VectorSearchEngine("documents", dimensions=1536)
        engine.build_index(row_count=100)
        sqls = engine.maintenance_sql()
        assert len(sqls) > 0
