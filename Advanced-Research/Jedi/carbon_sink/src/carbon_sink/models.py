from dataclasses import dataclass


@dataclass
class Sink:
    sink_id: str
    sink_type: str
    area_km2: float
    sequestration_rate: float

    @property
    def annual_capture_tons(self) -> float:
        return self.area_km2 * self.sequestration_rate


@dataclass
class CarbonMeasurement:
    measurement_id: str
    sink: Sink
    co2_tons: float
    timestamp: str

    @property
    def per_km2(self) -> float:
        return self.co2_tons / self.sink.area_km2 if self.sink.area_km2 > 0 else 0.0


def calculate_total_capture(sinks: list[Sink]) -> float:
    return sum(s.annual_capture_tons for s in sinks)


def model_climate_impact(co2_tons: float) -> float:
    return co2_tons * 0.001


def project_future_capacity(sink: Sink, years: float, degradation: float) -> float:
    factor = (1 - degradation) ** years
    return sink.annual_capture_tons * factor
