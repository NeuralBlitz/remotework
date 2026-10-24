from dataclasses import dataclass
from enum import Enum


class VacuumStrategy(Enum):
    AGGRESSIVE = "aggressive"
    BALANCED = "balanced"


@dataclass(frozen=True)
class TableStats:
    schema_name: str
    table_name: str
    dead_tuples: int
    live_tuples: int
    table_size_bytes: int
    last_autovacuum_age_hours: float
    write_rate_per_second: float

    @property
    def dead_tuple_ratio(self) -> float:
        total = self.live_tuples + self.dead_tuples
        if total == 0:
            return 0.0
        return self.dead_tuples / total


@dataclass(frozen=True)
class VacuumConfig:
    vacuum_cost_delay: int
    vacuum_cost_limit: int
    autovacuum_vacuum_threshold: int
    autovacuum_vacuum_scale_factor: float
    autovacuum_analyze_threshold: int
    autovacuum_analyze_scale_factor: float
    strategy: VacuumStrategy

    @classmethod
    def default(cls) -> "VacuumConfig":
        return cls(
            vacuum_cost_delay=2,
            vacuum_cost_limit=200,
            autovacuum_vacuum_threshold=50,
            autovacuum_vacuum_scale_factor=0.2,
            autovacuum_analyze_threshold=50,
            autovacuum_analyze_scale_factor=0.1,
            strategy=VacuumStrategy.BALANCED,
        )
