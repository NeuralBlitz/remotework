from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pg_downsampler.models import DownsampleConfig


class DownsampleTemplate(ABC):
    def __init__(self, config: DownsampleConfig) -> None:
        self.config = config
        self._processed_rows = 0

    def execute(self) -> dict[str, Any]:
        if not self.config.validate():
            raise ValueError("Invalid downsampler config")
        self._pre_hook()
        chunks = self._partition_data()
        for chunk in chunks:
            aggregated = self._aggregate(chunk)
            self._write_target(aggregated)
        self._post_hook()
        return {"processed": self._processed_rows, "resolution": self.config.resolution.value}

    def _pre_hook(self) -> None:
        self._processed_rows = 0

    @abstractmethod
    def _partition_data(self) -> list[list[dict[str, Any]]]: ...

    @abstractmethod
    def _aggregate(self, chunk: list[dict[str, Any]]) -> list[dict[str, Any]]: ...

    def _write_target(self, rows: list[dict[str, Any]]) -> None:
        self._processed_rows += len(rows)

    def _post_hook(self) -> None:
        pass


class HourlyDownsampler(DownsampleTemplate):
    def _partition_data(self) -> list[list[dict[str, Any]]]:
        return [[{"ts": f"2024-01-01 {h:02d}:00", "value": h} for h in range(24)]]

    def _aggregate(self, chunk: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not chunk:
            return []
        avg_val = sum(r["value"] for r in chunk) / len(chunk)
        return [{"ts": chunk[0]["ts"], "value": round(avg_val, 2), "count": len(chunk)}]


class DailyDownsampler(DownsampleTemplate):
    def _partition_data(self) -> list[list[dict[str, Any]]]:
        return [
            [{"ts": f"2024-01-{d:02d}", "value": d * 10} for d in range(1, 32)],
        ]

    def _aggregate(self, chunk: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not chunk:
            return []
        total = sum(r["value"] for r in chunk)
        return [{"ts": chunk[0]["ts"], "value": total, "count": len(chunk)}]
