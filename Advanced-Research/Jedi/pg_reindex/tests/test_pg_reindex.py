
import pytest

from pg_reindex.analyzer import FragmentationAnalyzer
from pg_reindex.facade import MaintenanceFacade
from pg_reindex.models import FragmentationReport, IndexInfo


def _make_index(
    name: str = "idx_orders_created",
    table: str = "orders",
    schema: str = "public",
    bloat: float = 0.1,
    size: int = 1_000_000,
    table_size: int = 5_000_000,
    scans: int = 500,
    unique: bool = False,
    primary: bool = False,
) -> IndexInfo:
    return IndexInfo(
        schema_name=schema,
        table_name=table,
        index_name=name,
        index_size_bytes=size,
        table_size_bytes=table_size,
        bloat_ratio=bloat,
        is_unique=unique,
        is_primary=primary,
        index_scan_count=scans,
    )


class TestIndexInfo:
    def test_is_bloated(self) -> None:
        idx = _make_index(bloat=0.5)
        assert idx.is_bloated is True

    def test_not_bloated(self) -> None:
        idx = _make_index(bloat=0.1)
        assert idx.is_bloated is False

    def test_needs_reindex(self) -> None:
        idx = _make_index(bloat=0.5, scans=1000)
        assert idx.needs_reindex is True

    def test_no_reindex_if_low_scans(self) -> None:
        idx = _make_index(bloat=0.5, scans=10)
        assert idx.needs_reindex is False


class TestFragmentationReport:
    def test_empty_report(self) -> None:
        report = FragmentationReport(schema_name="public")
        assert report.total_indexes == 0
        assert report.bloat_percentage == 0.0

    def test_bloated_index_names(self) -> None:
        indexes = [
            _make_index("idx1", bloat=0.5),
            _make_index("idx2", bloat=0.1),
        ]
        report = FragmentationReport(
            schema_name="public",
            total_indexes=2,
            bloated_indexes=1,
            indexes=indexes,
        )
        assert report.bloated_index_names == ["idx1"]

    def test_bloat_percentage(self) -> None:
        indexes = [
            _make_index("idx1", bloat=0.5),
            _make_index("idx2", bloat=0.5),
            _make_index("idx3", bloat=0.1),
        ]
        report = FragmentationReport(
            schema_name="public",
            total_indexes=3,
            bloated_indexes=2,
            indexes=indexes,
        )
        assert report.bloat_percentage == pytest.approx(2 / 3)


class TestFragmentationAnalyzer:
    def test_analyze_empty(self) -> None:
        analyzer = FragmentationAnalyzer()
        report = analyzer.analyze([])
        assert report.total_indexes == 0

    def test_analyze_indexes(self) -> None:
        analyzer = FragmentationAnalyzer()
        indexes = [
            _make_index("idx1", bloat=0.5, size=2_000_000),
            _make_index("idx2", bloat=0.1, size=1_000_000),
        ]
        report = analyzer.analyze(indexes)
        assert report.total_indexes == 2
        assert report.bloated_indexes == 1
        assert report.total_bloat_bytes == 2_000_000

    def test_find_bloated_indexes(self) -> None:
        analyzer = FragmentationAnalyzer()
        indexes = [
            _make_index("idx1", bloat=0.5, scans=500),
            _make_index("idx2", bloat=0.1, scans=100),
        ]
        bloated = analyzer.find_bloated_indexes(indexes)
        assert len(bloated) == 1
        assert bloated[0].index_name == "idx1"

    def test_estimate_reindex_time(self) -> None:
        analyzer = FragmentationAnalyzer()
        idx = _make_index(size=10 * 1024 * 1024, unique=False)
        time_est = analyzer.estimate_reindex_time(idx)
        assert time_est == pytest.approx(3.0)

    def test_estimate_reindex_time_unique(self) -> None:
        analyzer = FragmentationAnalyzer()
        idx = _make_index(size=10 * 1024 * 1024, unique=True)
        time_est = analyzer.estimate_reindex_time(idx)
        assert time_est == pytest.approx(5.0)

    def test_recommend_concurrent_for_large(self) -> None:
        analyzer = FragmentationAnalyzer()
        idx = _make_index(table_size=100 * 1024 * 1024)
        assert analyzer.recommend_concurrent(idx) is True

    def test_recommend_non_concurrent_for_small(self) -> None:
        analyzer = FragmentationAnalyzer()
        idx = _make_index(table_size=1 * 1024 * 1024)
        assert analyzer.recommend_concurrent(idx) is False


class TestMaintenanceFacade:
    def test_run_concurrent_reindex(self) -> None:
        facade = MaintenanceFacade()
        idx = _make_index(size=5 * 1024 * 1024)
        result = facade.run_concurrent_reindex(idx, concurrent=True)
        assert result.success is True
        assert result.concurrent is True
        assert len(facade.results) == 1

    def test_run_tuesday_maintenance(self) -> None:
        facade = MaintenanceFacade()
        indexes = [
            _make_index("idx1", bloat=0.5, scans=500, size=10_000_000),
            _make_index("idx2", bloat=0.1, scans=200),
        ]
        report = facade.run_tuesday_maintenance(indexes)
        assert report.total_indexes == 2
        assert report.bloated_indexes == 1

    def test_run_index_rebuild(self) -> None:
        facade = MaintenanceFacade()
        idx = _make_index(table_size=50 * 1024 * 1024)
        result = facade.run_index_rebuild(idx)
        assert result.concurrent is True
        assert result.success is True

    def test_clear_results(self) -> None:
        facade = MaintenanceFacade()
        facade.run_concurrent_reindex(_make_index())
        assert len(facade.results) == 1
        facade.clear_results()
        assert len(facade.results) == 0

    def test_get_report(self) -> None:
        facade = MaintenanceFacade()
        indexes = [_make_index("a", bloat=0.4)]
        report = facade.get_report(indexes)
        assert report.total_indexes == 1
        assert report.bloated_indexes == 1
