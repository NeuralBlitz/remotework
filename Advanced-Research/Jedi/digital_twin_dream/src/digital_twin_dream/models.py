import statistics

from digital_twin_dream import DigitalTwin


class FactoryTwin(DigitalTwin):
    def __init__(self, factory_id: str) -> None:
        super().__init__(factory_id, f"Factory {factory_id}")


class AnomalyDetector:
    def __init__(self, threshold: float = 2.0) -> None:
        self.threshold = threshold

    def detect(self, values: list[float]) -> bool:
        if len(values) < 3:
            return False
        mean = statistics.mean(values[:-1])
        std = statistics.stdev(values[:-1]) if len(values) > 1 else 0.1
        last = values[-1]
        return abs(last - mean) > self.threshold * std
