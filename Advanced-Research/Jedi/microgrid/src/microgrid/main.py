from microgrid import EnergySource, GridState


def main() -> None:
    solar = EnergySource("S1", "solar", 500.0, 350.0)
    battery = EnergySource("B1", "battery", 200.0, 150.0)
    grid = GridState("G1", [solar, battery], demand_kw=400.0)
    print(f"Grid balance: {grid.balance:.1f} kW")
    print(f"Balanced: {grid.is_balanced}")


if __name__ == "__main__":
    main()
