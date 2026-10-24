import pytest

from pg_downsampler.models import DownsampleConfig, Resolution
from pg_downsampler.template import DailyDownsampler, HourlyDownsampler


def _config(**overrides: object) -> DownsampleConfig:
    defaults: dict[str, object] = {
        "source_table": "raw_metrics",
        "target_table": "metrics_hourly",
        "resolution": Resolution.HOURLY,
    }
    defaults.update(overrides)
    return DownsampleConfig(**defaults)


class TestDownsampleConfig:
    def test_create_config(self) -> None:
        cfg = _config()
        assert cfg.source_table == "raw_metrics"
        assert cfg.resolution == Resolution.HOURLY

    def test_validate_valid(self) -> None:
        assert _config().validate() is True

    def test_validate_same_table(self) -> None:
        cfg = _config(target_table="raw_metrics")
        assert cfg.validate() is False

    def test_validate_empty_source(self) -> None:
        cfg = _config(source_table="")
        assert cfg.validate() is False


class TestHourlyDownsampler:
    def test_execute(self) -> None:
        ds = HourlyDownsampler(_config())
        result = ds.execute()
        assert result["processed"] == 1
        assert result["resolution"] == "hourly"

    def test_aggregate_averages(self) -> None:
        ds = HourlyDownsampler(_config())
        chunk = [{"ts": "2024-01-01 00:00", "value": 10}, {"ts": "2024-01-01 01:00", "value": 20}]
        agg = ds._aggregate(chunk)
        assert agg[0]["value"] == 15.0


class TestDailyDownsampler:
    def test_execute(self) -> None:
        ds = DailyDownsampler(_config(resolution=Resolution.DAILY))
        result = ds.execute()
        assert result["processed"] == 1
        assert result["resolution"] == "daily"

    def test_aggregate_sums(self) -> None:
        ds = DailyDownsampler(_config())
        chunk = [{"ts": "2024-01-01", "value": 10}, {"ts": "2024-01-02", "value": 20}]
        agg = ds._aggregate(chunk)
        assert agg[0]["value"] == 30

    def test_invalid_config_raises(self) -> None:
        ds = HourlyDownsampler(_config(source_table=""))
        with pytest.raises(ValueError, match="Invalid"):
            ds.execute()

    def test_partition_data_not_empty(self) -> None:
        ds = HourlyDownsampler(_config())
        chunks = ds._partition_data()
        assert len(chunks) > 0
        assert len(chunks[0]) == 24
