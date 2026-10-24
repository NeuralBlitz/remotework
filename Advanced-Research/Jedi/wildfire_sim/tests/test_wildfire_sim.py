from wildfire_sim import FireSpread, TerrainCell
from wildfire_sim.models import calculate_burn_area, create_terrain, simulate_wildfire


class TestTerrainCell:
    def test_creation(self) -> None:
        cell = TerrainCell(0, 0, 100.0, 0.8, 0.2)
        assert cell.row == 0

    def test_combustibility_high(self) -> None:
        cell = TerrainCell(0, 0, 100.0, 1.0, 0.0)
        assert cell.combustibility == 1.0

    def test_combustibility_low(self) -> None:
        cell = TerrainCell(0, 0, 100.0, 0.2, 1.0)
        assert cell.combustibility == 0.0


class TestFireSpread:
    def test_initialization(self) -> None:
        terrain = [[TerrainCell(0, 0, 100.0, 0.5, 0.3)]]
        spread = FireSpread(terrain, 10.0, 90.0)
        assert spread.wind_speed == 10.0

    def test_step_no_fire(self) -> None:
        terrain = [[TerrainCell(0, 0, 100.0, 0.5, 0.3)]]
        spread = FireSpread(terrain, 10.0, 90.0)
        spread.step()
        assert terrain[0][0].on_fire is False

    def test_step_with_fire(self) -> None:
        terrain = [[TerrainCell(0, 0, 100.0, 0.8, 0.2)]]
        terrain[0][0].on_fire = True
        spread = FireSpread(terrain, 10.0, 90.0)
        spread.step()


class TestHelpers:
    def test_create_terrain(self) -> None:
        terrain = create_terrain(5, 5, vegetation=0.7, humidity=0.3)
        assert len(terrain) == 5
        assert len(terrain[0]) == 5

    def test_simulate_wildfire(self) -> None:
        terrain = create_terrain(10, 10, vegetation=0.7, humidity=0.3)
        terrain[5][5].on_fire = True
        history = simulate_wildfire(terrain, steps=5)
        assert len(history) == 5

    def test_calculate_burn_area(self) -> None:
        terrain = create_terrain(10, 10, vegetation=0.7, humidity=0.3)
        terrain[5][5].burned = True
        area = calculate_burn_area(terrain)
        assert area == 1
