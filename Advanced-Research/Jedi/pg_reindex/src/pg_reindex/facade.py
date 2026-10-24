from __future__ import annotations

from pg_reindex.analyzer import FragmentationAnalyzer
from pg_reindex.models import FragmentationReport, IndexInfo


class ReindexResult:
    def __init__(
        self,
        index_name: str,
        success: bool,
        concurrent: bool,
        duration_seconds: float,
        error_message: str | None = None,
    ) -> None:
        self.index_name = index_name
        self.success = success
        self.concurrent = concurrent
        self.duration_seconds = duration_seconds
        self.error_message = error_message


class MaintenanceFacade:
    def __init__(self, analyzer: FragmentationAnalyzer | None = None) -> None:
        self._analyzer = analyzer or FragmentationAnalyzer()
        self._results: list[ReindexResult] = []

    def run_tuesday_maintenance(
        self, indexes: list[IndexInfo], bloat_threshold: float = 0.3
    ) -> FragmentationReport:
        report = self._analyzer.analyze(indexes)
        bloated = [idx for idx in report.indexes if idx.is_bloated]
        for idx in bloated:
            concurrent = self._analyzer.recommend_concurrent(idx)
            self.run_concurrent_reindex(idx, concurrent=concurrent)
        return report

    def run_concurrent_reindex(self, index: IndexInfo, concurrent: bool = True) -> ReindexResult:
        duration = self._analyzer.estimate_reindex_time(index)
        result = ReindexResult(
            index_name=index.index_name,
            success=True,
            concurrent=concurrent,
            duration_seconds=duration,
        )
        self._results.append(result)
        return result

    def run_index_rebuild(self, index: IndexInfo) -> ReindexResult:
        concurrent = self._analyzer.recommend_concurrent(index)
        return self.run_concurrent_reindex(index, concurrent=concurrent)

    @property
    def results(self) -> list[ReindexResult]:
        return list(self._results)

    def clear_results(self) -> None:
        self._results.clear()

    def get_report(self, indexes: list[IndexInfo]) -> FragmentationReport:
        return self._analyzer.analyze(indexes)
