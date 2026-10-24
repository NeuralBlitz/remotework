from dataclasses import dataclass, field
from enum import Enum


class StageType(Enum):
    RAW = "raw"
    CLEANING = "cleaning"
    AGGREGATION = "aggregation"
    TRANSFORM = "transform"


@dataclass(frozen=True)
class TransformResult:
    stage_name: str
    rows_in: int
    rows_out: int
    errors: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.errors) == 0


@dataclass
class PipelineStage:
    name: str
    stage_type: StageType
    description: str = ""
