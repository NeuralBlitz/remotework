from digital_twin_dream import DigitalTwin, Sensor
from digital_twin_dream.models import AnomalyDetector, FactoryTwin


class TestSensor:
    def test_creation(self) -> None:
        s = Sensor("test", 10.0, "kg")
        assert s.sensor_id == "test"
        assert s.value == 10.0

    def test_update(self) -> None:
        s = Sensor("test", 10.0)
        old_ts = s.timestamp
        s.update(20.0)
        assert s.value == 20.0
        assert s.timestamp >= old_ts


class TestDigitalTwin:
    def test_add_sensor(self) -> None:
        dt = DigitalTwin("1", "test")
        s = Sensor("temp", 25.0)
        dt.add_sensor(s)
        assert len(dt.sensors) == 1

    def test_get_state(self) -> None:
        dt = DigitalTwin("1", "test")
        dt.add_sensor(Sensor("temp", 25.0))
        state = dt.get_state()
        assert state["temp"] == 25.0


class TestFactoryTwin:
    def test_factory_creation(self) -> None:
        ft = FactoryTwin("f1")
        assert ft.name == "Factory 1"
        assert len(ft.sensors) >= 0


class TestAnomalyDetector:
    def test_no_anomaly(self) -> None:
        detector = AnomalyDetector(threshold=2.0)
        assert detector.detect([1.0, 1.1, 1.05, 0.99]) is False

    def test_anomaly_detected(self) -> None:
        detector = AnomalyDetector(threshold=2.0)
        assert detector.detect([1.0, 1.1, 10.0]) is True
