from digital_twin_dream import Sensor
from digital_twin_dream.models import FactoryTwin


def main() -> None:
    factory = FactoryTwin("factory_1")
    factory.add_sensor(Sensor("temp", 25.0, "C"))
    print(f"Twin: {factory.name}")
    print(f"State: {factory.get_state()}")


if __name__ == "__main__":
    main()
