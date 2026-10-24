from debris_track import Debris, OrbitalState


def main() -> None:
    debris = Debris("D1", 12345, 5.0, "LEO")
    state = OrbitalState(debris, 400.0, 51.6)
    print(f"Debris: {debris.debris_id}")
    print(f"Orbital period: {state.orbital_period_min:.1f} min")


if __name__ == "__main__":
    main()
