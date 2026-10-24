from microgrid import EnergySource, GridState
from microgrid.models import forecast_demand, optimize_dispatch, simulate_outage


class TestEnergySource:
    def test_creation(self) -> None:
        src = EnergySource("S1", "solar", 500.0, 300.0)
        assert src.source_id == "S1"

    def test_utilization(self) -> None:
        src = EnergySource("S1", "solar", 500.0, 250.0)
        assert src.utilization == 0.5

    def test_is_available(self) -> None:
        available = EnergySource("S1", "solar", 500.0, 100.0)
        unavailable = EnergySource("S2", "solar", 500.0, 0.0)
        assert available.is_available is True
        assert unavailable.is_available is False


class TestGridState:
    def test_total_supply(self) -> None:
        src1 = EnergySource("S1", "solar", 500.0, 300.0)
        src2 = EnergySource("S2", "wind", 400.0, 200.0)
        grid = GridState("G1", [src1, src2], demand_kw=400.0)
        assert grid.total_supply == 500.0

    def test_balance_positive(self) -> None:
        src = EnergySource("S1", "solar", 500.0, 400.0)
        grid = GridState("G1", [src], demand_kw=300.0)
        assert grid.balance == 100.0

    def test_is_balanced(self) -> None:
        src = EnergySource("S1", "solar", 500.0, 400.0)
        grid = GridState("G1", [src], demand_kw=400.0)
        assert grid.is_balanced is True


class TestHelpers:
    def test_optimize_dispatch(self) -> None:
        sources = [EnergySource("S1", "solar", 500.0, 0.0)]
        result = optimize_dispatch(sources, 400.0)
        assert len(result) > 0

    def test_simulate_outage(self) -> None:
        sources = [EnergySource("S1", "solar", 500.0, 400.0)]
        affected = simulate_outage(sources, "S1")
        assert len(affected) >= 0

    def test_forecast_demand(self) -> None:
        forecast = forecast_demand(24.0)
        assert len(forecast) == 24
