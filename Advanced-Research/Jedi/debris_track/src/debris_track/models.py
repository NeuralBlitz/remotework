from dataclasses import dataclass


@dataclass
class Debris:
    debris_id: str
    norad_id: int
    size_m: float
    orbit_type: str

    @property
    def collision_risk(self) -> float:
        if self.size_m > 10:
            return 0.8
        elif self.size_m > 1:
            return 0.4
        return 0.1


@dataclass
class OrbitalState:
    debris: Debris
    altitude_km: float
    inclination_deg: float
    eccentricity: float = 0.0

    @property
    def orbital_period_min(self) -> float:
        return 84 + 0.03 * self.altitude_km

    def predict_position(self, minutes: float) -> tuple[float, float]:
        return (self.altitude_km, minutes / self.orbital_period_min * 360)


def catalog_debris() -> list[Debris]:
    return [
        Debris("D1", 10001, 5.0, "LEO"),
        Debris("D2", 10002, 2.0, "LEO"),
        Debris("D3", 10003, 10.0, "MEO"),
    ]


def predict_conjunction(debris1_id: str, debris2_id: str, hours: float) -> dict:
    return {
        "debris1": debris1_id,
        "debris2": debris2_id,
        " TCA_hours": hours,
        "miss_distance_km": 0.5,
    }


def collision_probability(r1: float, r2: float) -> float:
    combined_radius = r1 + r2
    return 0.01 * combined_radius
