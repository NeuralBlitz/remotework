import pytest

from feature_tt.models import FeaturePoint, TimeRange
from feature_tt.snapshot import FeatureSnapshot, TemporalJoin
from feature_tt.store import TemporalFeatureStore


def test_snapshot_at():
    snap = FeatureSnapshot(100)
    p = FeaturePoint(entity_id="e1", feature_name="f1", value=1.0, timestamp=50)
    snap.add(p)
    assert snap.get("e1", "f1") is not None


def test_snapshot_excludes_future():
    snap = FeatureSnapshot(50)
    p = FeaturePoint(entity_id="e1", feature_name="f1", value=1.0, timestamp=100)
    snap.add(p)
    assert snap.get("e1", "f1") is None


def test_time_range_contains():
    tr = TimeRange(start_ts=10, end_ts=100)
    assert tr.contains(50)
    assert not tr.contains(5)
    assert tr.contains(10)


def test_time_range_overlaps():
    a = TimeRange(0, 50)
    b = TimeRange(30, 80)
    assert a.overlaps(b)
    assert not a.overlaps(TimeRange(60, 100))


def test_store_query():
    store = TemporalFeatureStore()
    store.ingest(FeaturePoint("e1", "f1", 1.0, timestamp=10))
    store.ingest(FeaturePoint("e1", "f1", 2.0, timestamp=20))
    result = store.query("e1", "f1", 15)
    assert result is not None
    assert result.value == 1.0


def test_store_query_latest():
    store = TemporalFeatureStore()
    store.ingest(FeaturePoint("e1", "f1", 1.0, timestamp=10))
    store.ingest(FeaturePoint("e1", "f1", 2.0, timestamp=20))
    result = store.query("e1", "f1", 25)
    assert result is not None
    assert result.value == 2.0


def test_temporal_join():
    join = TemporalJoin()
    s1 = FeatureSnapshot(10)
    s1.add(FeaturePoint("e1", "f1", 1.0, timestamp=5))
    s2 = FeatureSnapshot(20)
    s2.add(FeaturePoint("e1", "f2", 2.0, timestamp=15))
    join.add_snapshot(s1)
    join.add_snapshot(s2)
    merged = join.join_at(20)
    assert merged.get("e1", "f1") is not None
    assert merged.get("e1", "f2") is not None


def test_history():
    store = TemporalFeatureStore()
    store.ingest(FeaturePoint("e1", "f1", 1.0, timestamp=10))
    store.ingest(FeaturePoint("e1", "f1", 2.0, timestamp=20))
    store.ingest(FeaturePoint("e1", "f1", 3.0, timestamp=30))
    hist = store.history("e1", "f1")
    assert len(hist) == 3
    assert hist[0].value == 1.0


def test_query_missing():
    store = TemporalFeatureStore()
    assert store.query("ghost", "x", 100) is None


def test_range_query():
    join = TemporalJoin()
    for t in [10, 30, 50, 70]:
        s = FeatureSnapshot(t)
        s.add(FeaturePoint("e1", "f1", float(t), timestamp=t))
        join.add_snapshot(s)
    results = join.range_query(TimeRange(20, 60))
    assert len(results) == 2
