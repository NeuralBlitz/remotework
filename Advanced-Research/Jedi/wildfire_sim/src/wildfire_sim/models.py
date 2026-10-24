from dataclasses import dataclass


@dataclass
class TerrainCell:
    row: int
    col: int
    elevation: float
    vegetation: float
    humidity: float
    on_fire: bool = False
    burned: bool = False

    @property
    def combustibility(self) -> float:
        fuel = self.vegetation * (1 - self.humidity)
        return max(0.0, min(1.0, fuel))


@dataclass
class FireSpread:
    grid: list[list[TerrainCell]]
    wind_speed: float
    wind_direction: float

    def step(self) -> None:
        rows = len(self.grid)
        cols = len(self.grid[0]) if rows > 0 else 0
        new_fires: list[tuple[int, int]] = []
        for r in range(rows):
            for c in range(cols):
                cell = self.grid[r][c]
                if cell.on_fire:
                    cell.burned = True
                    cell.on_fire = False
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            neighbor = self.grid[nr][nc]
                            if not neighbor.burned and neighbor.combustibility > 0.3:
                                new_fires.append((nr, nc))
        for r, c in new_fires:
            self.grid[r][c].on_fire = True


def create_terrain(
    rows: int, cols: int, vegetation: float = 0.5, humidity: float = 0.5
) -> list[list[TerrainCell]]:
    return [
        [TerrainCell(r, c, 100.0, vegetation, humidity) for c in range(cols)] for r in range(rows)
    ]


def simulate_wildfire(terrain: list[list[TerrainCell]], steps: int) -> list[int]:
    spread = FireSpread(terrain, wind_speed=10.0, wind_direction=90.0)
    history = []
    for _ in range(steps):
        spread.step()
        history.append(calculate_burn_area(terrain))
    return history


def calculate_burn_area(terrain: list[list[TerrainCell]]) -> int:
    return sum(1 for row in terrain for cell in row if cell.burned)
