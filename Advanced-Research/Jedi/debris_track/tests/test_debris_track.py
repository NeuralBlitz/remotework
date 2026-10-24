from debris_track import Debris, OrbitalState
from debris_track.models import catalog_debris, collision_probability, predict_conjunction


class TestDebris:
    def test_creation(self) -> None:
        d = Debris("D1", 12345, 5.0, "LEO")
        assert d.debris_id == "D1"

    def test_collision_risk_large(self) -> None:
        d = Debris("D1", 1, 15.0, "LEO")
        assert d.collision_risk == 0.8

    def test_collision_risk_small(self) -> None:
        d = Debris("D1", 1, 0.5, "LEO")
        assert d.collision_risk == 0.1


class TestOrbitalState:
    def test_orbital_period(self) -> None:
        d = Debris("D1", 1, 1.0, "LEO")
        state = OrbitalState(d, 400.0, 51.6)
        assert state.orbital_period_min > 80

    def test_predict_position(self) -> None:
        d = Debris("D1", 1, 1.0, "LEO")
        state = OrbitalState(d, 400.0, 51.6)
        pos = state.predict_position(45.0)
        assert len(pos) == 2


class TestHelpers:
    def test_catalog_debris(self) -> None:
        debris_list = catalog_debris()
        assert len(debris_list) > 0

    def test_predict_conjunction(self) -> None:
        result = predict_conjunction("D1", "D2", 24.0)
        assert result is not None

    def test_collision_probability(self) -> None:
        assert collision_probability(0.1, 0.1) > 0
