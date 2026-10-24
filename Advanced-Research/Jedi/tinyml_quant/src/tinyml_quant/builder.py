from __future__ import annotations

from tinyml_quant.models import (
    CalibrationData,
    CalibrationMethod,
    QuantConfig,
    QuantScheme,
)


class QuantizationBuilder:
    def __init__(self) -> None:
        self._config = QuantConfig()

    def with_scheme(self, scheme: QuantScheme) -> QuantizationBuilder:
        self._config.scheme = scheme
        return self

    def with_calibration(
        self,
        min_val: float,
        max_val: float,
        method: CalibrationMethod = CalibrationMethod.MINMAX,
    ) -> QuantizationBuilder:
        self._config.calibration = CalibrationData(min_val=min_val, max_val=max_val)
        self._config.method = method
        return self

    def with_per_channel(self, enabled: bool = True) -> QuantizationBuilder:
        self._config.per_channel = enabled
        return self

    def with_symmetric(self, symmetric: bool = True) -> QuantizationBuilder:
        self._config.symmetric = symmetric
        return self

    def with_granularity(self, granularity: str) -> QuantizationBuilder:
        self._config.granularity = granularity
        return self

    def with_percentile(self, percentile: float) -> QuantizationBuilder:
        self._config.calibration.percentile = percentile
        self._config.method = CalibrationMethod.PERCENTILE
        return self

    def with_num_samples(self, n: int) -> QuantizationBuilder:
        self._config.calibration.num_samples = n
        return self

    def reset(self) -> QuantizationBuilder:
        self._config = QuantConfig()
        return self

    def build(self) -> QuantConfig:
        if not self._config.is_valid():
            raise ValueError("Invalid quantization configuration")
        return self._config
