from carbon_sink import CarbonMeasurement, Sink
from carbon_sink.models import (
    calculate_total_capture,
    model_climate_impact,
    project_future_capacity,
)


class TestSink:
    def test_creation(self) -> None:
        sink = Sink("S1", "forest", 100.0, 10.0)
        assert sink.sink_id == "S1"

    def test_annual_capture(self) -> None:
        sink = Sink("S1", "forest", 100.0, 10.0)
        assert sink.annual_capture_tons == 1000.0


class TestCarbonMeasurement:
    def test_per_km2(self) -> None:
        sink = Sink("S1", "forest", 100.0, 10.0)
        measurement = CarbonMeasurement("M1", sink, 500.0, "2024-01-01")
        assert measurement.per_km2 == 5.0

    def test_per_km2_zero_area(self) -> None:
        sink = Sink("S1", "forest", 0.0, 10.0)
        measurement = CarbonMeasurement("M1", sink, 500.0, "2024-01-01")
        assert measurement.per_km2 == 0.0


class TestHelpers:
    def test_calculate_total_capture(self) -> None:
        sinks = [
            Sink("S1", "forest", 100.0, 10.0),
            Sink("S2", "ocean", 500.0, 5.0),
        ]
        total = calculate_total_capture(sinks)
        assert total == 3500.0

    def test_model_climate_impact(self) -> None:
        impact = model_climate_impact(1000.0)
        assert impact > 0

    def test_project_future_capacity(self) -> None:
        sink = Sink("S1", "forest", 100.0, 10.0)
        future = project_future_capacity(sink, years=10, degradation=0.02)
        assert future < sink.annual_capture_tons
