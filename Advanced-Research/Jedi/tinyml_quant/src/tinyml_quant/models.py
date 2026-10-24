from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class QuantScheme(Enum):
    INT8 = "int8"
    FP16 = "fp16"
    DYNAMIC = "dynamic"


class CalibrationMethod(Enum):
    MINMAX = "minmax"
    PERCENTILE = "percentile"
    KL_DIVERGENCE = "kl_divergence"


@dataclass
class CalibrationData:
    min_val: float = 0.0
    max_val: float = 1.0
    percentile: float = 99.9
    num_samples: int = 100

    def validate(self) -> bool:
        if self.min_val >= self.max_val:
            return False
        if not 0 < self.percentile <= 100:
            return False
        return self.num_samples > 0


@dataclass
class QuantConfig:
    scheme: QuantScheme = QuantScheme.INT8
    calibration: CalibrationData = field(default_factory=CalibrationData)
    method: CalibrationMethod = CalibrationMethod.MINMAX
    per_channel: bool = False
    symmetric: bool = True
    granularity: str = "per_tensor"

    def get_bit_width(self) -> int:
        if self.scheme == QuantScheme.INT8:
            return 8
        if self.scheme == QuantScheme.FP16:
            return 16
        return 4

    def is_valid(self) -> bool:
        return self.calibration.validate()
