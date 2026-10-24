from __future__ import annotations

from pg_backfiller.models import (
    BackfillConfig,
    BackfillJob,
    BackfillProgress,
    BackfillStatus,
    BackfillStrategy,
)
from pg_backfiller.strategies import (
    BatchStrategy,
    HybridStrategy,
    StreamingStrategy,
    BackfillStrategy as StrategyBase,
)


class FeatureBackfiller:
    def __init__(self, config: BackfillConfig | None = None) -> None:
        self._config = config or BackfillConfig()
        self._strategies: dict[str, StrategyBase] = {
            "batch": BatchStrategy(),
            "streaming": StreamingStrategy(),
            "hybrid": HybridStrategy(),
        }
        self._jobs: dict[str, BackfillJob] = {}
        self._history: list[BackfillProgress] = []

    @property
    def config(self) -> BackfillConfig:
        return self._config

    def register_job(self, job: BackfillJob) -> None:
        if not job.validate():
            raise ValueError(f"Invalid job: {job.job_id}")
        if job.job_id in self._jobs:
            raise ValueError(f"Job already exists: {job.job_id}")
        self._jobs[job.job_id] = job

    def unregister_job(self, job_id: str) -> bool:
        if job_id not in self._jobs:
            raise KeyError(f"Job not found: {job_id}")
        del self._jobs[job_id]
        return True

    def run(self, job_id: str) -> BackfillProgress:
        job = self._jobs.get(job_id)
        if job is None:
            raise KeyError(f"Job not found: {job_id}")
        strategy_name = job.strategy.value
        strategy = self._strategies.get(strategy_name)
        if strategy is None:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        progress = strategy.execute(job, self._config)
        self._history.append(progress)
        return progress

    def run_all(self) -> list[BackfillProgress]:
        results = []
        for job_id in list(self._jobs.keys()):
            results.append(self.run(job_id))
        return results

    def get_progress(self, job_id: str) -> BackfillProgress | None:
        for p in reversed(self._history):
            if p.job_id == job_id:
                return p
        return None

    def get_history(self) -> list[BackfillProgress]:
        return list(self._history)

    def list_jobs(self) -> list[str]:
        return list(self._jobs.keys())

    def register_strategy(self, name: str, strategy: StrategyBase) -> None:
        self._strategies[name] = strategy

    def available_strategies(self) -> list[str]:
        return list(self._strategies.keys())
