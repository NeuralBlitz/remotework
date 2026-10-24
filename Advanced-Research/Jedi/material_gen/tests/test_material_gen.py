from material_gen import CrystalStructure, Material
from material_gen.models import calculate_stability, doping_level, generate_perovskite


class TestMaterial:
    def test_creation(self) -> None:
        m = Material(formula="Si", bandgap=1.1, stability=0.8)
        assert m.formula == "Si"
        assert m.bandgap == 1.1

    def test_is_stable(self) -> None:
        stable = Material(formula="Si", stability=0.8)
        unstable = Material(formula="Si", stability=0.3)
        assert stable.is_stable is True
        assert unstable.is_stable is False

    def test_is_semiconductor(self) -> None:
        semi = Material(formula="Si", bandgap=1.1)
        insulator = Material(formula="Al2O3", bandgap=8.0)
        assert semi.is_semiconductor is True
        assert insulator.is_semiconductor is False


class TestCrystalStructure:
    def test_symmetry(self) -> None:
        cs = CrystalStructure(name="cubic", lattice_type="FCC", space_group=225)
        assert cs.get_symmetry_operations() == 225


class TestHelpers:
    def test_generate_perovskite(self) -> None:
        mat = generate_perovskite("Ca", "Ti", "O")
        assert mat.formula == "CaTiO3"
        assert mat.bandgap > 0

    def test_calculate_stability(self) -> None:
        assert calculate_stability(300, 1.0) > 0
        assert calculate_stability(2000, 1.0) < calculate_stability(300, 1.0)

    def test_doping_level(self) -> None:
        assert doping_level(1e18) == "low"
        assert doping_level(1e20) == "high"
