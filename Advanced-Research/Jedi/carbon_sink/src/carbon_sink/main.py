from carbon_sink import Sink
from carbon_sink.models import calculate_total_capture


def main() -> None:
    forest = Sink("F1", "forest", 100.0, 10.0)
    ocean = Sink("O1", "ocean", 500.0, 5.0)
    sinks = [forest, ocean]
    total = calculate_total_capture(sinks)
    print(f"Total annual capture: {total:.1f} tons CO2")


if __name__ == "__main__":
    main()
