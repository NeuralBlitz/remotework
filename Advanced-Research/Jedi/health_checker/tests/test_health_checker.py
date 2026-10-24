"""Tests for health_checker."""
from __future__ import annotations

from src.health_checker import aggregate_statuses, create_status


def test_create_status_healthy():
    status = create_status("database", True)
    assert status.component == "database"
    assert status.healthy is True

def test_create_status_unhealthy():
    status = create_status("api", False, "Connection refused")
    assert status.healthy is False
    assert status.message == "Connection refused"

def test_create_status_with_message():
    status = create_status("cache", True, "OK")
    assert status.message == "OK"

def test_aggregate_statuses_all_healthy():
    statuses = [
        create_status("comp1", True),
        create_status("comp2", True),
    ]
    assert aggregate_statuses(statuses) is True

def test_aggregate_statuses_one_unhealthy():
    statuses = [
        create_status("comp1", True),
        create_status("comp2", False),
    ]
    assert aggregate_statuses(statuses) is False

def test_aggregate_statuses_empty():
    assert aggregate_statuses([]) is True

def test_status_to_dict():
    status = create_status("test", True, "OK")
    d = status.to_dict()
    assert d["component"] == "test"
    assert d["healthy"] is True
    assert d["message"] == "OK"
