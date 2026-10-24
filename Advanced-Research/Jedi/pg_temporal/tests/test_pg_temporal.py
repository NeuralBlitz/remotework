from __future__ import annotations

from pg_temporal.models import LSNPosition
from pg_temporal.temporal import TemporalManager


def test_set_and_get() -> None:
    tm = TemporalManager()
    tm.set("x", 42)
    assert tm.get("x") == 42
    assert tm.get("missing") is None


def test_snapshot_creates_memento() -> None:
    tm = TemporalManager()
    tm.set("a", 1)
    m = tm.snapshot("before_b")
    assert m.label == "before_b"
    assert m.state == {"a": 1}


def test_rewind_to_lsn() -> None:
    tm = TemporalManager()
    tm.set("x", 1)
    m1 = tm.snapshot("v1")
    tm.set("x", 2)
    tm.set("y", 99)
    tm.snapshot("v2")

    tm.rewind_to_lsn(m1.lsn)
    assert tm.get("x") == 1
    assert tm.get("y") is None


def test_rewind_to_label() -> None:
    tm = TemporalManager()
    tm.set("k", "a")
    tm.snapshot("alpha")
    tm.set("k", "b")
    tm.snapshot("beta")

    result = tm.rewind_to_label("alpha")
    assert result is not None
    assert tm.get("k") == "a"


def test_rewind_to_missing_label() -> None:
    tm = TemporalManager()
    result = tm.rewind_to_label("nope")
    assert result is None


def test_history_ordering() -> None:
    tm = TemporalManager()
    tm.set("a", 1)
    tm.snapshot()
    tm.set("a", 2)
    tm.snapshot()
    tm.set("a", 3)
    tm.snapshot()

    history = tm.history
    assert len(history) == 3
    assert history[0].lsn < history[1].lsn < history[2].lsn


def test_lsn_ordering() -> None:
    a = LSNPosition(0, 1)
    b = LSNPosition(0, 5)
    c = LSNPosition(1, 0)
    assert a < b < c
    assert str(a) == "0/1"


def test_snapshot_state_is_copy() -> None:
    tm = TemporalManager()
    tm.set("x", 1)
    m = tm.snapshot()
    m.state["x"] = 999
    assert tm.get("x") == 1


def test_multiple_rewinds() -> None:
    tm = TemporalManager()
    tm.set("v", 1)
    m1 = tm.snapshot("s1")
    tm.set("v", 2)
    m2 = tm.snapshot("s2")
    tm.set("v", 3)
    tm.snapshot("s3")

    tm.rewind_to_lsn(m2.lsn)
    assert tm.get("v") == 2

    tm.rewind_to_lsn(m1.lsn)
    assert tm.get("v") == 1

    tm.rewind_to_label("s3")
    assert tm.get("v") == 3


def test_empty_snapshot() -> None:
    tm = TemporalManager()
    m = tm.snapshot()
    assert m.state == {}
    assert m.lsn == LSNPosition(0, 0)
