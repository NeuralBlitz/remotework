from sat_insurance import RiskAssessment, Satellite
from sat_insurance.models import assess_risk, calculate_premium, orbital_decay_rate


class TestSatellite:
    def test_creation(self) -> None:
        sat = Satellite("S1", "TestSat", "LEO", 2020, 100e6)
        assert sat.sat_id == "S1"

    def test_age(self) -> None:
        sat = Satellite("S1", "TestSat", "LEO", 2020, 100e6)
        assert sat.age == 6


class TestRiskAssessment:
    def test_total_risk(self) -> None:
        sat = Satellite("S1", "Test", "LEO", 2020, 100e6)
        ra = RiskAssessment(sat, 0.1, 0.2, 0.3)
        assert ra.total_risk == 0.2

    def test_premium_rate(self) -> None:
        sat = Satellite("S1", "Test", "LEO", 2020, 100e6)
        ra = RiskAssessment(sat, 0.1, 0.2, 0.3)
        assert ra.premium_rate == 0.02


class TestHelpers:
    def test_assess_risk(self) -> None:
        sat = Satellite("S1", "Test", "LEO", 2020, 100e6)
        ra = assess_risk(sat)
        assert ra.total_risk > 0

    def test_calculate_premium(self) -> None:
        sat = Satellite("S1", "Test", "LEO", 2020, 100e6)
        ra = assess_risk(sat)
        premium = calculate_premium(ra)
        assert premium > 0

    def test_orbital_decay_rate(self) -> None:
        assert orbital_decay_rate("LEO") > orbital_decay_rate("GEO")
