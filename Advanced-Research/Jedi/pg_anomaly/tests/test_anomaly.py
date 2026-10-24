from __future__ import annotations

from datetime import datetime

import pytest

from pg_anomaly.models import AlertSeverity, AnomalyAlert, MetricPoint
from pg_anomaly.observers import AnomalyDetector, IQRObserver, ZScoreObserver
from pg_anomaly.subject import MetricSubject


def make_point(name: str = "cpu", value: float = 50.0, ts: datetime | None = None) -> MetricPoint:
    return MetricPoint(name=name, value=value, timestamp=ts or datetime.now())


class TestMetricPoint:
    def test_create(self) -> None:
        p = make_point(value=42.0)
        assert p.value == 42.0
        assert p.name == "cpu"

    def test_empty_name_raises(self) -> None:
        with pytest.raises(ValueError):
            MetricPoint(name="", value=1.0, timestamp=datetime.now())


class TestAnomalyAlert:
    def test_is_critical(self) -> None:
        alert = AnomalyAlert(
            metric_name="cpu",
            point=make_point(),
            severity=AlertSeverity.CRITICAL,
            score=5.0,
            message="test",
            threshold=3.0,
        )
        assert alert.is_critical is True

    def test_not_critical(self) -> None:
        alert = AnomalyAlert(
            metric_name="cpu",
            point=make_point(),
            severity=AlertSeverity.WARNING,
            score=2.0,
            message="test",
            threshold=3.0,
        )
        assert alert.is_critical is False


class TestMetricSubject:
    def test_emit(self) -> None:
        subject = MetricSubject()
        alerts = subject.emit(make_point())
        assert isinstance(alerts, list)

    def test_buffer(self) -> None:
        subject = MetricSubject()
        subject.emit(make_point(value=1))
        subject.emit(make_point(value=2))
        assert len(subject.get_buffer()) == 2

    def test_clear_buffer(self) -> None:
        subject = MetricSubject()
        subject.emit(make_point())
        subject.clear_buffer()
        assert len(subject.get_buffer()) == 0

    def test_observer_count(self) -> None:
        subject = MetricSubject()
        assert subject.observer_count == 0
        subject.attach(ZScoreObserver())
        assert subject.observer_count == 1


class TestZScoreObserver:
    def test_no_anomaly(self) -> None:
        obs = ZScoreObserver(threshold=3.0)
        history = [make_point(value=v) for v in [50, 51, 49, 50, 52]]
        alerts = obs.update(make_point(value=50), history)
        assert len(alerts) == 0

    def test_anomaly_detected(self) -> None:
        obs = ZScoreObserver(threshold=2.0)
        history = [make_point(value=v) for v in [50, 50, 50, 50, 50]]
        alerts = obs.update(make_point(value=100), history)
        assert len(alerts) == 1
        assert alerts[0].severity == AlertSeverity.CRITICAL

    def test_too_few_points(self) -> None:
        obs = ZScoreObserver()
        history = [make_point(value=1), make_point(value=2)]
        alerts = obs.update(make_point(value=100), history)
        assert len(alerts) == 0


class TestIQRObserver:
    def test_no_anomaly(self) -> None:
        obs = IQRObserver()
        history = [make_point(value=v) for v in [10, 20, 30, 40, 50]]
        alerts = obs.update(make_point(value=30), history)
        assert len(alerts) == 0

    def test_anomaly_detected(self) -> None:
        obs = IQRObserver(multiplier=1.5)
        history = [make_point(value=v) for v in [10, 20, 30, 40, 50]]
        alerts = obs.update(make_point(value=200), history)
        assert len(alerts) == 1

    def test_too_few_points(self) -> None:
        obs = IQRObserver()
        history = [make_point(value=1), make_point(value=2), make_point(value=3)]
        alerts = obs.update(make_point(value=100), history)
        assert len(alerts) == 0


class TestAnomalyDetector:
    def test_detect_combined(self) -> None:
        detector = AnomalyDetector()
        history = [make_point(value=v) for v in [50] * 10]
        alerts = detector.detect(make_point(value=999), history)
        assert len(alerts) >= 1
        assert detector.alert_count >= 1

    def test_clear_alerts(self) -> None:
        detector = AnomalyDetector()
        history = [make_point(value=v) for v in [50] * 10]
        detector.detect(make_point(value=999), history)
        detector.clear_alerts()
        assert detector.alert_count == 0

    def test_get_critical_alerts(self) -> None:
        detector = AnomalyDetector()
        history = [make_point(value=v) for v in [50] * 10]
        detector.detect(make_point(value=500), history)
        crit = detector.get_critical_alerts()
        assert all(a.is_critical for a in crit)


class TestSubjectIntegration:
    def test_emit_with_observers(self) -> None:
        subject = MetricSubject()
        subject.attach(ZScoreObserver(threshold=2.0))
        for v in [50, 50, 50, 50, 50]:
            subject.emit(make_point(value=v))
        alerts = subject.emit(make_point(value=200))
        assert len(alerts) >= 1
