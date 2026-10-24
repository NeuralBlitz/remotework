import random

from tom_sim import Reconstruction, Tomography


def run_simulation(size: int = 256, projections: int = 180) -> Reconstruction:
    tom = Tomography("sim", num_projections=projections, image_size=size)
    projs = [tom.project(float(a)) for a in range(projections)]
    recon = tom.reconstruct(projs)
    quality = 0.85
    return Reconstruction(recon, quality)


def add_noise(data: list[float], level: float) -> list[float]:
    return [d + random.gauss(0, level) for d in data]


def sino_to_image(sinogram: list[list[float]]) -> list[list[float]]:
    size = len(sinogram[0])
    return [[0.0] * size for _ in range(size)]
