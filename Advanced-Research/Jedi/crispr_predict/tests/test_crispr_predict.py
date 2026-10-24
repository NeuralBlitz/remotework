from crispr_predict import GuideRNA, PredictionResult
from crispr_predict.models import find_pam_sites, gc_content


class TestGuideRNA:
    def test_guide_creation(self) -> None:
        guide = GuideRNA(sequence="atcg")
        assert guide.sequence == "ATCG"

    def test_default_pam(self) -> None:
        guide = GuideRNA(sequence="ATCG")
        assert guide.pam == "NGG"


class TestPredictionResult:
    def test_viable_result(self) -> None:
        guide = GuideRNA(sequence="ATCG")
        result = PredictionResult(guide, 0.8, 0.9)
        assert result.is_viable is True

    def test_low_efficiency(self) -> None:
        guide = GuideRNA(sequence="ATCG")
        result = PredictionResult(guide, 0.3, 0.9)
        assert result.is_viable is False

    def test_low_off_target(self) -> None:
        guide = GuideRNA(sequence="ATCG")
        result = PredictionResult(guide, 0.8, 0.5)
        assert result.is_viable is False


class TestHelpers:
    def test_gc_content(self) -> None:
        assert gc_content("GCGC") == 1.0
        assert gc_content("AAAA") == 0.0
        assert gc_content("ATAT") == 0.0

    def test_find_pam_sites(self) -> None:
        dna = "ATCGATCGATCG"
        sites = find_pam_sites(dna, "CG")
        assert len(sites) == 3
