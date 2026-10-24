from tom_sim import Reconstruction, Tomography
from tom_sim.models import add_noise, sino_to_image


class TestTomography:
    def test_creation(self) -> None:
        tom = Tomography("test", num_projections=90)
        assert tom.name == "test"
        assert tom.num_projections == 90

    def test_project(self) -> None:
        tom = Tomography("test", image_size=128)
        proj = tom.project(45.0)
        assert len(proj) == 128

    def test_reconstruct(self) -> None:
        tom = Tomography("test", image_size=64)
        projections = [[0.0] * 64 for _ in range(180)]
        recon = tom.reconstruct(projections)
        assert len(recon) == 64


class TestReconstruction:
    def test_valid_reconstruction(self) -> None:
        recon = Reconstruction([[0.0] * 10 for _ in range(10)], quality=0.8)
        assert recon.is_valid is True

    def test_invalid_reconstruction(self) -> None:
        recon = Reconstruction([[0.0] * 10 for _ in range(10)], quality=0.3)
        assert recon.is_valid is False


class TestHelpers:
    def test_add_noise(self) -> None:
        data = [1.0, 2.0, 3.0]
        noisy = add_noise(data, 0.1)
        assert len(noisy) == len(data)

    def test_sino_to_image(self) -> None:
        sino = [[0.0] * 64 for _ in range(64)]
        img = sino_to_image(sino)
        assert len(img) == 64
