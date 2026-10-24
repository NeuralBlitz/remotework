from wildfire_sim import FireSpread
from wildfire_sim.models import create_terrain


def main() -> None:
    terrain = create_terrain(10, 10, vegetation=0.7, humidity=0.3)
    terrain[5][5].on_fire = True
    spread = FireSpread(terrain, wind_speed=10.0, wind_direction=90.0)
    spread.step()
    print("Fire spread simulation complete")


if __name__ == "__main__":
    main()
