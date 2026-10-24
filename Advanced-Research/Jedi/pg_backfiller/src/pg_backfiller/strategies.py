from __future__ import annotations

from abc import ABC, abstractmethod

from pg_backfiller.models import BackfillConfig, BackfillJob, BackfillProgress, BackfillStatus


class BackfillStrategy(ABC):
    @abstractmethod
    def execute(self, job: BackfillJob, config: BackfillConfig) -> BackfillProgress: ...

    @abstractmethod
    def name(self) -> str: ...


class BatchStrategy(BackfillStrategy):
    def execute(self, job: BackfillJob, config: BackfillConfig) -> BackfillProgress:
        total = job.max_rows or 10000
        progress = BackfillProgress(
            job_id=job.job_id, status=BackfillStatus.COMPLETED, rows_total=total
        )
        if config.dry_run:
            progress.status = BackfillStatus.PENDING
            progress.rows_processed = 0
        else:
            processed = 0
            while processed < total:
                chunk = min(job.batch_size, total - processed)
                processed += chunk
            progress.rows_processed = processed
        return progress

    def name(self) -> str:
        return "batch"


class StreamingStrategy(BackfillStrategy):
    def execute(self, job: BackfillJob, config: BackfillConfig) -> BackfillProgress:
        total = job.max_rows or 5000
        progress = BackfillProgress(
            job_id=job.job_id, status=BackfillStatus.COMPLETED, rows_total=total
        )
        if config.dry_run:
            progress.status = BackfillStatus.PENDING
            progress.rows_processed = 0
        else:
            progress.rows_processed = total
        return progress

    def name(self) -> str:
        return "streaming"


class HybridStrategy(BackfillStrategy):
    def __init__(self) -> None:
        self._batch = BatchStrategy()
        self._streaming = StreamingStrategy()

    def execute(self, job: BackfillJob, config: BackfillConfig) -> BackfillProgress:
        total = job.max_rows or 8000
        if config.dry_run:
            return BackfillProgress(
                job_id=job.job_id, status=BackfillStatus.PENDING, rows_total=total
            )
        mid = total // 2
        p1 = self._batch.execute(
            BackfillJob(
                job_id=f"{job.job_id}_batch",
                table_name=job.table_name,
                feature_column=job.feature_column,
                source_columns=job.source_columns,
                batch_size=job.batch_size,
                max_rows=mid,
            ),
            config,
        )
        p2 = self._streaming.execute(
            BackfillJob(
                job_id=f"{job.job_id}_stream",
                table_name=job.table_name,
                feature_column=job.feature_column,
                source_columns=job.source_columns,
                batch_size=job.batch_size,
                max_rows=total - mid,
            ),
            config,
        )
        return BackfillProgress(
            job_id=job.job_id,
            status=BackfillStatus.COMPLETED,
            rows_processed=p1.rows_processed + p2.rows_processed,
            rows_total=total,
        )

    def name(self) -> str:
        return "hybrid"
