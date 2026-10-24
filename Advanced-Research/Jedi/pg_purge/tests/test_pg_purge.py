
from pg_purge.builder import PurgeJobBuilder
from pg_purge.executor import PurgeExecutor
from pg_purge.models import PurgeJob, PurgeStrategy


class TestPurgeJob:
    def test_qualified_table(self) -> None:
        job = PurgeJob(name="t", from_table="logs", from_schema="audit")
        assert job.qualified_table == "audit.logs"

    def test_default_strategy(self) -> None:
        job = PurgeJob(name="t", from_table="logs")
        assert job.strategy == PurgeStrategy.DELETE

    def test_total_affected(self) -> None:
        from pg_purge.models import PurgeResult

        result = PurgeResult(job_name="t", success=True, rows_archived=10, rows_deleted=5)
        assert result.total_affected == 15


class TestPurgeJobBuilder:
    def test_build_minimal(self) -> None:
        job = PurgeJobBuilder().with_name("purge_logs").from_table("app_logs").build()
        assert job.name == "purge_logs"
        assert job.from_table == "app_logs"
        assert job.strategy == PurgeStrategy.DELETE

    def test_build_with_archive(self) -> None:
        job = (
            PurgeJobBuilder()
            .with_name("archive_old")
            .from_table("events", schema="analytics")
            .archive_to("events_archive", schema="cold_storage")
            .where_older_than(days=180)
            .build()
        )
        assert job.strategy == PurgeStrategy.ARCHIVE_THEN_DELETE
        assert job.archive_config is not None
        assert job.archive_config.archive_table == "events_archive"

    def test_build_archive_only(self) -> None:
        job = (
            PurgeJobBuilder()
            .with_name("cold_archive")
            .from_table("metrics")
            .archive_only("metrics_cold")
            .build()
        )
        assert job.strategy == PurgeStrategy.ARCHIVE_ONLY

    def test_build_with_extra_conditions(self) -> None:
        job = (
            PurgeJobBuilder()
            .with_name("targeted")
            .from_table("orders")
            .where_older_than(days=365)
            .with_extra_conditions("status = 'completed'")
            .build()
        )
        assert job.extra_conditions == "status = 'completed'"

    def test_build_dry_run(self) -> None:
        job = PurgeJobBuilder().with_name("test_run").from_table("data").dry_run().build()
        assert job.dry_run is True

    def test_build_missing_name_raises(self) -> None:
        builder = PurgeJobBuilder().from_table("t")
        try:
            builder.build()
            assert False, "should raise"  # noqa: B011
        except ValueError as e:
            assert "name" in str(e)

    def test_build_missing_table_raises(self) -> None:
        builder = PurgeJobBuilder().with_name("x")
        try:
            builder.build()
            assert False, "should raise"  # noqa: B011
        except ValueError as e:
            assert "table" in str(e)

    def test_build_with_batch_size(self) -> None:
        job = (
            PurgeJobBuilder().with_name("batched").from_table("logs").with_batch_size(5000).build()
        )
        assert job.batch_size == 5000


class TestPurgeExecutor:
    def test_execute_delete(self) -> None:
        executor = PurgeExecutor()
        job = PurgeJob(name="del", from_table="old_data")
        result = executor.execute(job)
        assert result.success
        assert result.rows_deleted == 42

    def test_execute_archive_then_delete(self) -> None:
        executor = PurgeExecutor()
        job = PurgeJob(
            name="archive_del",
            from_table="events",
            strategy=PurgeStrategy.ARCHIVE_THEN_DELETE,
        )
        result = executor.execute(job)
        assert result.success
        assert result.rows_archived == 42
        assert result.rows_deleted == 42

    def test_execute_dry_run(self) -> None:
        executor = PurgeExecutor()
        job = PurgeJob(name="dry", from_table="data", dry_run=True)
        result = executor.execute(job)
        assert result.dry_run is True

    def test_execute_many(self) -> None:
        executor = PurgeExecutor()
        jobs = [PurgeJob(name=f"job_{i}", from_table=f"table_{i}") for i in range(3)]
        results = executor.execute_many(jobs)
        assert len(results) == 3
        assert all(r.success for r in results)

    def test_summary(self) -> None:
        executor = PurgeExecutor()
        executor.execute(PurgeJob(name="a", from_table="t1"))
        executor.execute(PurgeJob(name="b", from_table="t2"))
        s = executor.summary()
        assert s["total_jobs"] == 2
        assert s["failed_jobs"] == 0

    def test_results_history(self) -> None:
        executor = PurgeExecutor()
        executor.execute(PurgeJob(name="x", from_table="t"))
        assert len(executor.results) == 1

    def test_build_and_execute(self) -> None:
        executor = PurgeExecutor()
        builder = PurgeJobBuilder().with_name("quick").from_table("tmp")
        result = executor.build_and_execute(builder)
        assert result.success
        assert result.job_name == "quick"
