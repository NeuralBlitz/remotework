"""Tests for metric_collector."""
from __future__ import annotations

from src.metric_collector import create_metric, create_series, get_total


def test_create_metric():
    metric = create_metric("requests", 100.0)
    assert metric.name == "requests"
    assert metric.value == 100.0

def test_create_metric_with_labels():
    metric = create_metric("requests", 50.0, {"service": "api"})
    assert metric.labels["service"] == "api"

def test_create_metric_default_labels():
    metric = create_metric("test", 1.0)
    assert metric.labels == {}

def test_create_series():
    metrics = [create_metric("m1", 10.0), create_metric("m2", 20.0)]
    series = create_series(metrics)
    assert len(series.metrics) == 2

def test_get_total():
    metrics = [
        create_metric("m1", 10.0),
        create_metric("m2", 20.0),
        create_metric("m3", 30.0),
    ]
    series = create_series(metrics)
    assert get_total(series) == 60.0

def test_get_total_empty_series():
    series = create_series([])
    assert get_total(series) == 0.0

def test_series_with_labels():
    metrics = [
        create_metric("req", 5.0, {"env": "prod"}),
        create_metric("req", 10.0, {"env": "dev"}),
    ]
    series = create_series(metrics)
    assert len(series.metrics) == 2
    assert series.metrics[0].labels["env"] == "prod"
