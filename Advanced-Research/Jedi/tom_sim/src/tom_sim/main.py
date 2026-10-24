from tom_sim import Tomography


def main() -> None:
    tom = Tomography("test", num_projections=180)
    projections = [tom.project(a) for a in range(180)]
    recon = tom.reconstruct(projections)
    print(f"Reconstruction size: {len(recon)}x{len(recon[0])}")


if __name__ == "__main__":
    main()
