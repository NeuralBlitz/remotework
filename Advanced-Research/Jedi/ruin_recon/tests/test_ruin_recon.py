from ruin_recon import Reconstruction, RuinSite
from ruin_recon.models import calculate_distance, estimate_period, reconstruct_site


class TestRuinSite:
    def test_creation(self) -> None:
        site = RuinSite("R1", "Test", 41.9, 12.5, "Medieval")
        assert site.site_id == "R1"

    def test_location(self) -> None:
        site = RuinSite("R1", "Test", 41.9, 12.5, "Medieval")
        assert site.location == (41.9, 12.5)


class TestReconstruction:
    def test_reliable(self) -> None:
        site = RuinSite("R1", "Test", 41.9, 12.5, "Medieval")
        recon = Reconstruction(site, 0.8, 0.9)
        assert recon.is_reliable is True

    def test_not_reliable(self) -> None:
        site = RuinSite("R1", "Test", 41.9, 12.5, "Medieval")
        recon = Reconstruction(site, 0.3, 0.5)
        assert recon.is_reliable is False

    def test_missing_percentage(self) -> None:
        site = RuinSite("R1", "Test", 41.9, 12.5, "Medieval")
        recon = Reconstruction(site, 0.7, 0.8)
        assert recon.missing_percentage == 30.0


class TestHelpers:
    def test_reconstruct_site(self) -> None:
        site = RuinSite("R1", "Test", 41.9, 12.5, "Medieval")
        recon = reconstruct_site(site)
        assert recon.completeness > 0

    def test_estimate_period(self) -> None:
        period = estimate_period({"mosaic": 0.8, "columns": 0.6})
        assert period != ""

    def test_calculate_distance(self) -> None:
        dist = calculate_distance(41.9, 12.5, 42.0, 13.0)
        assert dist > 0
