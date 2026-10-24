"""Automated Data Downsampler - Template Method Pattern."""

from pg_downsampler.models import DownsampleConfig, Resolution
from pg_downsampler.template import DailyDownsampler, DownsampleTemplate, HourlyDownsampler

__all__ = [
    "DownsampleConfig",
    "Resolution",
    "DownsampleTemplate",
    "HourlyDownsampler",
    "DailyDownsampler",
]
