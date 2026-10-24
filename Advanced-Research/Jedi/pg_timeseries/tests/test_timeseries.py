from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from pg_timeseries.facade import HypertableFacade
from pg_timeseries.models import AggregateQuery, ChunkInfo, CompressionPolicy, HypertableConfig


@pytest.fixture
def facade() -> HypertableFacade:
    return HypertableFacade()


@pytest.fixture
def sample_config() -> HypertableConfig:
    return HypertableConfig(
        table_name="metrics",
        time_column="ts",
        chunk_interval="1 day",
        compression_policy=CompressionPolicy.AFTER_7_DAYS,
    )


class TestHypertableConfig:
    def test_validate_valid(self, sample_config: HypertableConfig) -> None:
        assert sample_config.validate() is True

    def test_validate_invalid(self) -> None:
        config = HypertableConfig(table_name="", time_column="")
        assert config.validate() is False


class TestChunkInfo:
    def test_duration_days(self) -> None:
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 8)
        chunk = ChunkInfo(
            chunk_name="chunk_1",
            hypertable_name="metrics",
            range_start=start,
            range_end=end,
        )
        assert chunk.duration_days == pytest.approx(7.0)


class TestAggregateQuery:
    def test_sql_definition_with_columns(self) -> None:
        q = AggregateQuery(
            name="hourly",
            source_table="metrics",
            time_bucket_interval="1 hour",
            aggregate_columns=["avg(cpu) as cpu", "max(mem) as mem"],
        )
        sql = q.sql_definition()
        assert "time_bucket('1 hour'" in sql
        assert "avg(cpu) as cpu" in sql
        assert "metrics" in sql

    def test_sql_definition_star(self) -> None:
        q = AggregateQuery(name="daily", source_table="logs", time_bucket_interval="1 day")
        assert "SELECT time_bucket" in q.sql_definition()


class TestHypertableFacade:
    def test_create_hypertable(
        self, facade: HypertableFacade, sample_config: HypertableConfig
    ) -> None:
        assert facade.create_hypertable(sample_config) is True
        assert facade.get_hypertable("metrics") == sample_config

    def test_create_duplicate_raises(
        self, facade: HypertableFacade, sample_config: HypertableConfig
    ) -> None:
        facade.create_hypertable(sample_config)
        with pytest.raises(ValueError, match="already exists"):
            facade.create_hypertable(sample_config)

    def test_create_invalid_config(self, facade: HypertableFacade) -> None:
        bad = HypertableConfig(table_name="", time_column="")
        with pytest.raises(ValueError, match="Invalid"):
            facade.create_hypertable(bad)

    def test_drop_hypertable(
        self, facade: HypertableFacade, sample_config: HypertableConfig
    ) -> None:
        facade.create_hypertable(sample_config)
        assert facade.drop_hypertable("metrics") is True
        assert facade.get_hypertable("metrics") is None

    def test_drop_nonexistent_raises(self, facade: HypertableFacade) -> None:
        with pytest.raises(KeyError, match="not found"):
            facade.drop_hypertable("nope")

    def test_compress_chunks(
        self, facade: HypertableFacade, sample_config: HypertableConfig
    ) -> None:
        facade.create_hypertable(sample_config)
        now = datetime(2024, 1, 1)
        facade.add_chunk(ChunkInfo("c1", "metrics", now, now + timedelta(days=1), size_bytes=1000))
        facade.add_chunk(
            ChunkInfo(
                "c2", "metrics", now + timedelta(days=1), now + timedelta(days=2), size_bytes=2000
            )
        )
        count = facade.compress_chunks("metrics")
        assert count == 2
        assert facade.is_compressed("metrics")
        for c in facade.get_chunks("metrics"):
            assert c.is_compressed

    def test_continuous_aggregate(
        self, facade: HypertableFacade, sample_config: HypertableConfig
    ) -> None:
        facade.create_hypertable(sample_config)
        agg = AggregateQuery(
            name="hourly_avg",
            source_table="metrics",
            time_bucket_interval="1 hour",
            aggregate_columns=["avg(cpu)"],
        )
        assert facade.create_continuous_aggregate(agg) is True
        assert "hourly_avg" in facade.list_aggregates()

    def test_aggregate_missing_source(self, facade: HypertableFacade) -> None:
        agg = AggregateQuery(name="x", source_table="missing", time_bucket_interval="1h")
        with pytest.raises(KeyError, match="Source"):
            facade.create_continuous_aggregate(agg)

    def test_drop_removes_aggregates(
        self, facade: HypertableFacade, sample_config: HypertableConfig
    ) -> None:
        facade.create_hypertable(sample_config)
        agg = AggregateQuery(name="h", source_table="metrics", time_bucket_interval="1h")
        facade.create_continuous_aggregate(agg)
        facade.drop_hypertable("metrics")
        assert "h" not in facade.list_aggregates()

    def test_list_hypertables(self, facade: HypertableFacade) -> None:
        facade.create_hypertable(HypertableConfig("t1", "ts"))
        facade.create_hypertable(HypertableConfig("t2", "ts"))
        assert set(facade.list_hypertables()) == {"t1", "t2"}

    def test_compression_policy(
        self, facade: HypertableFacade, sample_config: HypertableConfig
    ) -> None:
        facade.create_hypertable(sample_config)
        assert facade.get_compression_policy("metrics") == CompressionPolicy.AFTER_7_DAYS
