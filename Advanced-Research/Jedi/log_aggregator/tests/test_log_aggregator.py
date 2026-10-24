"""Tests for log_aggregator."""
from __future__ import annotations

from src.log_aggregator import create_log, filter_logs


def test_create_log():
    log = create_log("INFO", "Test message")
    assert log.level == "INFO"
    assert log.message == "Test message"
    assert log.timestamp > 0

def test_create_log_different_levels():
    log_error = create_log("ERROR", "Error occurred")
    assert log_error.level == "ERROR"
    log_warn = create_log("WARNING", "Warning")
    assert log_warn.level == "WARNING"

def test_filter_logs_empty():
    logs = []
    result = filter_logs(logs, "INFO")
    assert len(result) == 0

def test_filter_logs_single_match():
    logs = [create_log("INFO", "msg1"), create_log("ERROR", "msg2")]
    result = filter_logs(logs, "INFO")
    assert len(result) == 1
    assert result[0].level == "INFO"

def test_filter_logs_multiple_matches():
    logs = [
        create_log("INFO", "m1"),
        create_log("INFO", "m2"),
        create_log("ERROR", "m3"),
    ]
    result = filter_logs(logs, "INFO")
    assert len(result) == 2

def test_filter_logs_no_match():
    logs = [create_log("ERROR", "error msg")]
    result = filter_logs(logs, "INFO")
    assert len(result) == 0

def test_log_to_dict():
    log = create_log("DEBUG", "test")
    d = log.to_dict()
    assert d["level"] == "DEBUG"
    assert d["message"] == "test"
    assert "timestamp" in d
