import math
from dataclasses import dataclass


@dataclass
class RuinSite:
    site_id: str
    name: str
    latitude: float
    longitude: float
    estimated_period: str

    @property
    def location(self) -> tuple[float, float]:
        return (self.latitude, self.longitude)


@dataclass
class Reconstruction:
    site: RuinSite
    completeness: float
    confidence: float

    @property
    def is_reliable(self) -> bool:
        return self.confidence > 0.7 and self.completeness > 0.5

    @property
    def missing_percentage(self) -> float:
        return (1 - self.completeness) * 100


def reconstruct_site(site: RuinSite) -> Reconstruction:
    completeness = 0.65
    confidence = 0.75
    return Reconstruction(site, completeness, confidence)


def estimate_period(features: dict[str, float]) -> str:
    if features.get("mosaic", 0) > 0.5:
        return "Roman"
    elif features.get("gothic_arch", 0) > 0.5:
        return "Medieval"
    return "Unknown"


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    return R * 2 * math.asin(math.sqrt(a))
