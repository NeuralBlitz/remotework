from __future__ import annotations

import pytest

from pg_backfiller.backfiller import FeatureBackfiller
from pg_backfiller.models import (
    BackfillConfig,
    BackfillJob,
    BackfillProgress,
    BackfillStatus,
    BackfillStrategy,
)
from pg_backfiller.strategies import BatchStrategy, HybridStrategy, StreamingStrategy


@pytest.fixture
def config() -> BackfillConfig:
    return BackfillConfig()


@pytest.fixture
def backfiller(config: BackfillConfig) -> FeatureBackfiller:
    return FeatureBackfiller(config)


@pytest.fixture
def batch_job() -> BackfillJob:
    return BackfillJob(
        job_id="job1",
        table_name="features",
        feature_column="embedding",
        source_columns=["text", "metadata"],
        strategy=BackfillStrategy.BATCH,
        max_rows=5000,
    )


class TestBackfillJob:
    def test_validate_valid(self, batch_job: BackfillJob) -> None:
        assert batch_job.validate() is True

    def test_validate_invalid(self) -> None:
        job = BackfillJob(job_id="", table_name="", feature_column="")
        assert job.validate() is False


class TestBackfillConfig:
    def test_validate_valid(self, config: BackfillConfig) -> None:
        assert config.validate() is True

    def test_validate_invalid(self) -> None:
        assert BackfillConfig(connection_string="").validate() is False


class TestBackfillProgress:
    def test_percentage(self) -> None:
        p = BackfillProgress(job_id="j", rows_processed=500, rows_total=1000)
        assert p.percentage == pytest.approx(50.0)

    def test_percentage_zero_total(self) -> None:
        p = BackfillProgress(job_id="j", rows_processed=0, rows_total=0)
        assert p.percentage == 0.0


class TestBatchStrategy:
    def test_execute(self, batch_job: BackfillJob, config: BackfillConfig) -> None:
        strategy = BatchStrategy()
        result = strategy.execute(batch_job, config)
        assert result.status == BackfillStatus.COMPLETED
        assert result.rows_processed == 5000

    def test_dry_run(self, batch_job: BackfillJob) -> None:
        strategy = BatchStrategy()
        cfg = BackfillConfig(dry_run=True)
        result = strategy.execute(batch_job, cfg)
        assert result.status == BackfillStatus.PENDING
        assert result.rows_processed == 0

    def test_name(self) -> None:
        assert BatchStrategy().name() == "batch"


class TestStreamingStrategy:
    def test_execute(self) -> None:
        strategy = StreamingStrategy()
        job = BackfillJob("j1", "t", "f", ["s"], max_rows=3000)
        result = strategy.execute(job, BackfillConfig())
        assert result.status == BackfillStatus.COMPLETED
        assert result.rows_processed == 3000

    def test_name(self) -> None:
        assert StreamingStrategy().name() == "streaming"


class TestHybridStrategy:
    def test_execute(self) -> None:
        strategy = HybridStrategy()
        job = BackfillJob("j1", "t", "f", ["s"], max_rows=10000)
        result = strategy.execute(job, BackfillConfig())
        assert result.status == BackfillStatus.COMPLETED
        assert result.rows_processed == 10000

    def test_name(self) -> None:
        assert HybridStrategy().name() == "hybrid"


class TestFeatureBackfiller:
    def test_register_job(self, backfiller: FeatureBackfiller, batch_job: BackfillJob) -> None:
        backfiller.register_job(batch_job)
        assert "job1" in backfiller.list_jobs()

    def test_register_duplicate_raises(
        self, backfiller: FeatureBackfiller, batch_job: BackfillJob
    ) -> None:
        backfiller.register_job(batch_job)
        with pytest.raises(ValueError, match="already exists"):
            backfiller.register_job(batch_job)

    def test_register_invalid_raises(self, backfiller: FeatureBackfiller) -> None:
        bad = BackfillJob("", "", "")
        with pytest.raises(ValueError, match="Invalid"):
            backfiller.register_job(bad)

    def test_run(self, backfiller: FeatureBackfiller, batch_job: BackfillJob) -> None:
        backfiller.register_job(batch_job)
        result = backfiller.run("job1")
        assert result.status == BackfillStatus.COMPLETED
        assert backfiller.get_progress("job1") is not None

    def test_run_missing_raises(self, backfiller: FeatureBackfiller) -> None:
        with pytest.raises(KeyError, match="not found"):
            backfiller.run("nope")

    def test_run_all(self, backfiller: FeatureBackfiller) -> None:
        backfiller.register_job(BackfillJob("j1", "t", "f", ["s"], max_rows=100))
        backfiller.register_job(BackfillJob("j2", "t", "f", ["s"], max_rows=200))
        results = backfiller.run_all()
        assert len(results) == 2

    def test_unregister(self, backfiller: FeatureBackfiller, batch_job: BackfillJob) -> None:
        backfiller.register_job(batch_job)
        backfiller.unregister_job("job1")
        assert "job1" not in backfiller.list_jobs()

    def test_unregister_missing_raises(self, backfiller: FeatureBackfiller) -> None:
        with pytest.raises(KeyError):
            backfiller.unregister_job("nope")

    def test_available_strategies(self, backfiller: FeatureBackfiller) -> None:
        assert set(backfiller.available_strategies()) == {"batch", "streaming", "hybrid"}
