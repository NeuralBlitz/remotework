from __future__ import annotations

import time
from typing import Any

from pg_purge.models import PurgeJob, PurgeResult, PurgeStrategy


class PurgeExecutor:
    def __init__(self, connection_factory: Any | None = None) -> None:
        self._connection_factory = connection_factory
        self._results: list[PurgeResult] = []

    def execute(self, job: PurgeJob) -> PurgeResult:
        start = time.monotonic()
        try:
            rows_archived = 0
            rows_deleted = 0

            if job.strategy in (
                PurgeStrategy.ARCHIVE_THEN_DELETE,
                PurgeStrategy.ARCHIVE_ONLY,
            ):
                rows_archived = self._simulate_archive(job)

            if job.strategy in (PurgeStrategy.DELETE, PurgeStrategy.ARCHIVE_THEN_DELETE):
                rows_deleted = self._simulate_delete(job)

            elapsed = (time.monotonic() - start) * 1000
            result = PurgeResult(
                job_name=job.name,
                success=True,
                rows_archived=rows_archived,
                rows_deleted=rows_deleted,
                duration_ms=elapsed,
                dry_run=job.dry_run,
            )
        except Exception as exc:
            result = PurgeResult(
                job_name=job.name,
                success=False,
                error=str(exc),
                dry_run=job.dry_run,
            )

        self._results.append(result)
        return result

    def _simulate_archive(self, job: PurgeJob) -> int:
        if job.dry_run:
            return 42
        return 42

    def _simulate_delete(self, job: PurgeJob) -> int:
        if job.dry_run:
            return 42
        return 42

    def build_and_execute(self, builder: Any) -> PurgeResult:
        job = builder.build()
        return self.execute(job)

    def execute_many(self, jobs: list[PurgeJob]) -> list[PurgeResult]:
        return [self.execute(job) for job in jobs]

    @property
    def results(self) -> list[PurgeResult]:
        return list(self._results)

    def summary(self) -> dict[str, Any]:
        total_archived = sum(r.rows_archived for r in self._results)
        total_deleted = sum(r.rows_deleted for r in self._results)
        failed = sum(1 for r in self._results if not r.success)
        return {
            "total_jobs": len(self._results),
            "total_rows_archived": total_archived,
            "total_rows_deleted": total_deleted,
            "failed_jobs": failed,
        }
