from pg_batchgov.decorators import LowPriorityDecorator, RetryDecorator
from pg_batchgov.models import BatchConfig, Priority, ResourceLimits
from pg_batchgov.runner import BatchRunner


class TestResourceLimits:
    def test_defaults(self) -> None:
        limits = ResourceLimits()
        assert limits.max_memory_mb == 512
        assert limits.timeout_seconds == 300.0

    def test_custom(self) -> None:
        limits = ResourceLimits(max_memory_mb=1024, max_cpu_percent=80.0)
        assert limits.max_memory_mb == 1024
        assert limits.max_cpu_percent == 80.0


class TestBatchConfig:
    def test_default_priority(self) -> None:
        config = BatchConfig(name="test_job")
        assert config.priority == Priority.NORMAL
        assert config.retry_count == 0

    def test_with_limits(self) -> None:
        limits = ResourceLimits(max_memory_mb=256)
        config = BatchConfig(name="light", priority=Priority.LOW, limits=limits)
        assert config.limits.max_memory_mb == 256


class TestLowPriorityDecorator:
    def test_preserves_function(self) -> None:
        config = BatchConfig(name="slow", priority=Priority.LOW)

        @LowPriorityDecorator(config)
        def my_job() -> str:
            return "done"

        assert my_job() == "done"
        assert my_job._batch_config.name == "slow"  # type: ignore[attr-defined]

    def test_normal_priority_runs(self) -> None:
        config = BatchConfig(name="normal_job", priority=Priority.NORMAL)

        @LowPriorityDecorator(config)
        def quick_job(x: int) -> int:
            return x * 2

        assert quick_job(5) == 10


class TestRetryDecorator:
    def test_succeeds_first_try(self) -> None:
        call_count = 0

        @RetryDecorator(max_retries=3)
        def stable_job() -> str:
            nonlocal call_count
            call_count += 1
            return "ok"

        assert stable_job() == "ok"
        assert call_count == 1

    def test_retries_on_failure(self) -> None:
        call_count = 0

        @RetryDecorator(max_retries=2)
        def flaky_job() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("not yet")
            return "finally"

        assert flaky_job() == "finally"
        assert call_count == 3

    def test_exhausts_retries(self) -> None:
        @RetryDecorator(max_retries=1)
        def always_fail() -> str:
            raise RuntimeError("boom")

        try:
            always_fail()
            assert False, "should have raised"  # noqa: B011
        except RuntimeError as e:
            assert str(e) == "boom"


class TestBatchRunner:
    def test_register_and_run(self) -> None:
        runner = BatchRunner()

        def add(a: int, b: int) -> int:
            return a + b

        runner.register(add)
        result = runner.run("add", 3, 4)
        assert result.success
        assert result.result == 7

    def test_run_unknown_job(self) -> None:
        runner = BatchRunner()
        result = runner.run("nonexistent")
        assert not result.success
        assert "not registered" in result.error  # type: ignore[union-attr]

    def test_run_with_retry(self) -> None:
        runner = BatchRunner()
        call_count = 0

        def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("fail")
            return "ok"

        config = BatchConfig(name="flaky", retry_count=2)
        runner.register(flaky, config)
        result = runner.run("flaky")
        assert result.success
        assert result.retries_used == 1

    def test_run_all_priority_order(self) -> None:
        runner = BatchRunner()
        order: list[str] = []

        def job_a() -> None:
            order.append("a")

        def job_b() -> None:
            order.append("b")

        runner.register(job_a, BatchConfig(name="job_a", priority=Priority.HIGH))
        runner.register(job_b, BatchConfig(name="job_b", priority=Priority.LOW))
        runner.run_all()
        assert order == ["b", "a"]

    def test_results_history(self) -> None:
        runner = BatchRunner()

        def noop() -> None:
            pass

        runner.register(noop)
        runner.run("noop")
        runner.run("noop")
        assert len(runner.results) == 2

    def test_registered_jobs(self) -> None:
        runner = BatchRunner()

        def x() -> None:
            pass

        def y() -> None:
            pass

        runner.register(x)
        runner.register(y)
        assert set(runner.registered_jobs) == {"x", "y"}

    def test_job_result_timing(self) -> None:
        runner = BatchRunner()

        import time

        def slow() -> str:
            time.sleep(0.01)
            return "done"

        runner.register(slow)
        result = runner.run("slow")
        assert result.success
        assert result.duration_ms >= 0
