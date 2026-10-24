from __future__ import annotations

from pg_reindex.models import FragmentationReport, IndexInfo


class FragmentationAnalyzer:
    def __init__(self, bloat_threshold: float = 0.3) -> None:
        self._bloat_threshold = bloat_threshold

    def analyze(self, indexes: list[IndexInfo]) -> FragmentationReport:
        if not indexes:
            return FragmentationReport(schema_name="public")
        bloated = [idx for idx in indexes if idx.is_bloated]
        total_bloat = sum(idx.index_size_bytes for idx in bloated)
        return FragmentationReport(
            schema_name=indexes[0].schema_name,
            total_indexes=len(indexes),
            bloated_indexes=len(bloated),
            total_bloat_bytes=total_bloat,
            indexes=list(indexes),
        )

    def find_bloated_indexes(self, indexes: list[IndexInfo]) -> list[IndexInfo]:
        return [idx for idx in indexes if idx.needs_reindex]

    def estimate_reindex_time(self, index: IndexInfo) -> float:
        size_mb = index.index_size_bytes / (1024 * 1024)
        if index.is_unique:
            return size_mb * 0.5
        return size_mb * 0.3

    def recommend_concurrent(self, index: IndexInfo) -> bool:
        return index.table_size_bytes > 10 * 1024 * 1024
