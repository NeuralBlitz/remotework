from dataclasses import dataclass


@dataclass
class EnergySource:
    source_id: str
    source_type: str
    capacity_kw: float
    current_output: float = 0.0

    @property
    def utilization(self) -> float:
        return self.current_output / self.capacity_kw if self.capacity_kw > 0 else 0.0

    @property
    def is_available(self) -> bool:
        return self.current_output > 0


@dataclass
class GridState:
    grid_id: str
    sources: list[EnergySource]
    demand_kw: float

    @property
    def total_supply(self) -> float:
        return sum(s.current_output for s in self.sources)

    @property
    def balance(self) -> float:
        return self.total_supply - self.demand_kw

    @property
    def is_balanced(self) -> bool:
        return abs(self.balance) < 0.1 * self.demand_kw


def optimize_dispatch(sources: list[EnergySource], demand: float) -> list[EnergySource]:
    sorted_sources = sorted(sources, key=lambda s: s.capacity_kw, reverse=True)
    remaining = demand
    for src in sorted_sources:
        dispatch = min(src.capacity_kw, remaining)
        src.current_output = dispatch
        remaining -= dispatch
    return sorted_sources


def simulate_outage(sources: list[EnergySource], source_id: str) -> list[str]:
    affected = []
    for src in sources:
        if src.source_id == source_id:
            src.current_output = 0.0
    for src in sources:
        if src.current_output == 0.0:
            affected.append(src.source_id)
    return affected


def forecast_demand(hours: float) -> list[float]:
    import math

    return [100 + 50 * math.sin(math.pi * h / 12) for h in range(int(hours))]
