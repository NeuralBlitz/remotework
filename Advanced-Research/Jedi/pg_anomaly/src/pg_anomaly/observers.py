from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Protocol

from pg_anomaly.models import AlertSeverity, AnomalyAlert, MetricPoint


class AnomalyObserver(Protocol):
    def update(self, point: MetricPoint, history: list[MetricPoint]) -> list[AnomalyAlert]: ...


class ZScoreObserver:
    def __init__(self, threshold: float = 3.0) -> None:
        self._threshold = threshold

    def update(self, point: MetricPoint, history: list[MetricPoint]) -> list[AnomalyAlert]:
        values = [p.value for p in history if p.name == point.name]
        if len(values) < 3:
            return []
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = math.sqrt(variance) if variance > 0 else 0.0
        if std == 0:
            if abs(point.value - mean) > 0:
                z = float("inf")
                return [
                    AnomalyAlert(
                        metric_name=point.name,
                        point=point,
                        severity=AlertSeverity.CRITICAL,
                        score=z,
                        message=f"Z-score inf exceeds threshold {self._threshold}",
                        threshold=self._threshold,
                    )
                ]
            return []
        z = abs(point.value - mean) / std
        if z >= self._threshold:
            severity = (
                AlertSeverity.CRITICAL if z >= self._threshold * 1.5 else AlertSeverity.WARNING
            )
            return [
                AnomalyAlert(
                    metric_name=point.name,
                    point=point,
                    severity=severity,
                    score=z,
                    message=f"Z-score {z:.2f} exceeds threshold {self._threshold}",
                    threshold=self._threshold,
                )
            ]
        return []


class IQRObserver:
    def __init__(self, multiplier: float = 1.5) -> None:
        self._multiplier = multiplier

    def _percentile(self, data: list[float], p: float) -> float:
        sorted_data = sorted(data)
        k = (len(sorted_data) - 1) * p
        f = int(k)
        c = f + 1 if f + 1 < len(sorted_data) else f
        return sorted_data[f] + (k - f) * (sorted_data[c] - sorted_data[f])

    def update(self, point: MetricPoint, history: list[MetricPoint]) -> list[AnomalyAlert]:
        values = [p.value for p in history if p.name == point.name]
        if len(values) < 4:
            return []
        q1 = self._percentile(values, 0.25)
        q3 = self._percentile(values, 0.75)
        iqr = q3 - q1
        lower = q1 - self._multiplier * iqr
        upper = q3 + self._multiplier * iqr
        if point.value < lower or point.value > upper:
            distance = max(abs(point.value - lower), abs(point.value - upper))
            score = distance / iqr if iqr > 0 else float("inf")
            return [
                AnomalyAlert(
                    metric_name=point.name,
                    point=point,
                    severity=AlertSeverity.WARNING,
                    score=score,
                    message=f"Value {point.value} outside IQR bounds [{lower:.2f}, {upper:.2f}]",
                    threshold=self._multiplier,
                )
            ]
        return []


class AnomalyDetector:
    def __init__(self) -> None:
        self._zscore = ZScoreObserver()
        self._iqr = IQRObserver()
        self._alerts: list[AnomalyAlert] = []

    def detect(self, point: MetricPoint, history: list[MetricPoint]) -> list[AnomalyAlert]:
        alerts = self._zscore.update(point, history)
        alerts.extend(self._iqr.update(point, history))
        self._alerts.extend(alerts)
        return alerts

    def get_alerts(self) -> list[AnomalyAlert]:
        return list(self._alerts)

    def clear_alerts(self) -> None:
        self._alerts.clear()

    @property
    def alert_count(self) -> int:
        return len(self._alerts)

    def get_critical_alerts(self) -> list[AnomalyAlert]:
        return [a for a in self._alerts if a.is_critical]
