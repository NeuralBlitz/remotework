from material_gen.models import generate_perovskite


def main() -> None:
    mat = generate_perovskite("Ca", "Ti", "O")
    print(f"Material: {mat.formula}")
    print(f"Bandgap: {mat.bandgap:.2f} eV")
    print(f"Stability: {mat.stability:.2f}")


if __name__ == "__main__":
    main()
