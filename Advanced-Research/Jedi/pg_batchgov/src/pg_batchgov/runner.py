from __future__ import annotations

import time
from collections.abc import Callable
from datetime import datetime
from typing import Any

from pg_batchgov.models import BatchConfig, JobResult, Priority, ResourceLimits


class BatchRunner:
    def __init__(self, default_limits: ResourceLimits | None = None) -> None:
        self.default_limits = default_limits or ResourceLimits()
        self._jobs: dict[str, Callable[..., Any]] = {}
        self._configs: dict[str, BatchConfig] = {}
        self._results: list[JobResult] = []

    def register(self, func: Callable[..., Any], config: BatchConfig | None = None) -> None:
        name = func.__name__
        self._jobs[name] = func
        if config is None:
            config = BatchConfig(
                name=name,
                priority=Priority.NORMAL,
                limits=self.default_limits,
            )
        self._configs[name] = config

    def run(self, job_name: str, *args: Any, **kwargs: Any) -> JobResult:
        if job_name not in self._jobs:
            return JobResult(
                job_name=job_name,
                success=False,
                error=f"Job '{job_name}' not registered",
            )

        func = self._jobs[job_name]
        config = self._configs[job_name]
        started = datetime.now()
        retries_used = 0

        for attempt in range(config.retry_count + 1):
            try:
                start_time = time.monotonic()
                result = func(*args, **kwargs)
                elapsed = (time.monotonic() - start_time) * 1000
                job_result = JobResult(
                    job_name=job_name,
                    success=True,
                    result=result,
                    started_at=started,
                    finished_at=datetime.now(),
                    duration_ms=elapsed,
                    retries_used=retries_used,
                )
                self._results.append(job_result)
                return job_result
            except Exception as exc:
                retries_used += 1
                if attempt == config.retry_count:
                    job_result = JobResult(
                        job_name=job_name,
                        success=False,
                        error=str(exc),
                        started_at=started,
                        finished_at=datetime.now(),
                        retries_used=retries_used,
                    )
                    self._results.append(job_result)
                    return job_result

        unreachable = JobResult(
            job_name=job_name,
            success=False,
            error="Unreachable",
        )
        self._results.append(unreachable)
        return unreachable

    def run_all(self, *args: Any, **kwargs: Any) -> list[JobResult]:
        priority_order = {
            Priority.LOW: 0,
            Priority.NORMAL: 1,
            Priority.HIGH: 2,
            Priority.CRITICAL: 3,
        }
        sorted_jobs = sorted(
            self._configs.items(),
            key=lambda item: priority_order[item[1].priority],
        )
        results: list[JobResult] = []
        for name, _config in sorted_jobs:
            results.append(self.run(name, *args, **kwargs))
        return results

    @property
    def results(self) -> list[JobResult]:
        return list(self._results)

    @property
    def registered_jobs(self) -> list[str]:
        return list(self._jobs.keys())
