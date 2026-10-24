import pytest

from tinyml_quant.builder import QuantizationBuilder
from tinyml_quant.models import CalibrationMethod, QuantScheme


def test_default_config():
    config = QuantizationBuilder().build()
    assert config.scheme == QuantScheme.INT8
    assert config.symmetric is True
    assert config.per_channel is False
    assert config.get_bit_width() == 8


def test_build_int8_per_channel():
    config = (
        QuantizationBuilder()
        .with_scheme(QuantScheme.INT8)
        .with_per_channel(True)
        .with_calibration(0.0, 1.0)
        .build()
    )
    assert config.scheme == QuantScheme.INT8
    assert config.per_channel is True
    assert config.get_bit_width() == 8


def test_build_fp16():
    config = QuantizationBuilder().with_scheme(QuantScheme.FP16).with_symmetric(False).build()
    assert config.scheme == QuantScheme.FP16
    assert config.get_bit_width() == 16
    assert config.symmetric is False


def test_percentile_calibration():
    config = (
        QuantizationBuilder()
        .with_calibration(-1.0, 1.0, CalibrationMethod.PERCENTILE)
        .with_percentile(99.5)
        .build()
    )
    assert config.method == CalibrationMethod.PERCENTILE
    assert config.calibration.percentile == 99.5


def test_invalid_calibration_raises():
    with pytest.raises(ValueError, match="Invalid"):
        QuantizationBuilder().with_calibration(1.0, 0.0).build()


def test_reset():
    builder = QuantizationBuilder()
    builder.with_scheme(QuantScheme.FP16).with_per_channel(True)
    builder.reset()
    config = builder.build()
    assert config.scheme == QuantScheme.INT8
    assert config.per_channel is False


def test_granularity():
    config = QuantizationBuilder().with_granularity("per_channel").build()
    assert config.granularity == "per_channel"


def test_num_samples():
    config = QuantizationBuilder().with_num_samples(500).build()
    assert config.calibration.num_samples == 500


def test_chained_builder():
    config = (
        QuantizationBuilder()
        .with_scheme(QuantScheme.DYNAMIC)
        .with_symmetric(False)
        .with_per_channel(True)
        .with_granularity("per_group")
        .with_num_samples(256)
        .with_calibration(-2.0, 2.0, CalibrationMethod.KL_DIVERGENCE)
        .build()
    )
    assert config.scheme == QuantScheme.DYNAMIC
    assert config.symmetric is False
    assert config.method == CalibrationMethod.KL_DIVERGENCE


def test_invalid_percentile():
    builder = QuantizationBuilder().with_num_samples(-1)
    with pytest.raises(ValueError):
        builder.build()
