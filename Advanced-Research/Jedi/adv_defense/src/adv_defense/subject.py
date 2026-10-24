from __future__ import annotations

from adv_defense.models import ThreatAlert
from adv_defense.observers import Observer


class InputMonitor:
    def __init__(self) -> None:
        self._observers: list[Observer] = []
        self._alerts: list[ThreatAlert] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, text: str) -> list[ThreatAlert]:
        alerts: list[ThreatAlert] = []
        for obs in self._observers:
            alert = obs.scan(text)
            if alert is not None:
                alerts.append(alert)
                self._alerts.append(alert)
        return alerts

    def scan(self, text: str) -> list[ThreatAlert]:
        return self.notify(text)

    def observer_count(self) -> int:
        return len(self._observers)

    def alert_history(self) -> list[ThreatAlert]:
        return list(self._alerts)

    def clear_history(self) -> None:
        self._alerts.clear()
