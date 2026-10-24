from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Any

from pg_etl.models import PipelineStage, StageType, TransformResult


class Stage(ABC):
    """Abstract base for a pipeline stage."""

    def __init__(self, name: str, stage_type: StageType) -> None:
        self.meta = PipelineStage(name=name, stage_type=stage_type)

    @abstractmethod
    def execute(
        self, data: list[dict[str, Any]]
    ) -> tuple[list[dict[str, Any]], TransformResult]: ...


class RawIngestStage(Stage):
    """Simulates ingesting raw data (identity passthrough with validation)."""

    def __init__(self, name: str = "raw_ingest") -> None:
        super().__init__(name, StageType.RAW)

    def execute(self, data: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], TransformResult]:
        errors: list[str] = []
        for i, row in enumerate(data):
            if not isinstance(row, dict):
                errors.append(f"Row {i}: expected dict, got {type(row).__name__}")
        valid = [r for r in data if isinstance(r, dict)]
        return valid, TransformResult(
            stage_name=self.meta.name, rows_in=len(data), rows_out=len(valid), errors=errors
        )


class CleaningStage(Stage):
    """Removes rows with None values in required fields and strips whitespace."""

    def __init__(self, required_fields: list[str], name: str = "cleaning") -> None:
        super().__init__(name, StageType.CLEANING)
        self.required_fields = required_fields

    def execute(self, data: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], TransformResult]:
        errors: list[str] = []
        cleaned: list[dict[str, Any]] = []
        for i, row in enumerate(data):
            missing = [f for f in self.required_fields if f not in row or row[f] is None]
            if missing:
                errors.append(f"Row {i}: missing fields {missing}")
                continue
            stripped = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
            cleaned.append(stripped)
        return cleaned, TransformResult(
            stage_name=self.meta.name, rows_in=len(data), rows_out=len(cleaned), errors=errors
        )


class AggregationStage(Stage):
    """Groups rows by a key and counts occurrences."""

    def __init__(self, group_by: str, name: str = "aggregation") -> None:
        super().__init__(name, StageType.AGGREGATION)
        self.group_by = group_by

    def execute(self, data: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], TransformResult]:
        counts: dict[Any, int] = {}
        for row in data:
            key = row.get(self.group_by, "__missing__")
            counts[key] = counts.get(key, 0) + 1
        result_rows = [{self.group_by: k, "count": v} for k, v in sorted(counts.items(), key=str)]
        return result_rows, TransformResult(
            stage_name=self.meta.name, rows_in=len(data), rows_out=len(result_rows)
        )


class RegexTransformStage(Stage):
    """Applies a regex substitution to a given field."""

    def __init__(
        self, field_name: str, pattern: str, replacement: str, name: str = "regex_transform"
    ) -> None:
        super().__init__(name, StageType.TRANSFORM)
        self.field_name = field_name
        self.regex = re.compile(pattern)
        self.replacement = replacement

    def execute(self, data: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], TransformResult]:
        errors: list[str] = []
        transformed: list[dict[str, Any]] = []
        for i, row in enumerate(data):
            new_row = dict(row)
            if self.field_name in new_row and isinstance(new_row[self.field_name], str):
                new_row[self.field_name] = self.regex.sub(
                    self.replacement, new_row[self.field_name]
                )
            else:
                errors.append(f"Row {i}: field '{self.field_name}' missing or not a string")
            transformed.append(new_row)
        return transformed, TransformResult(
            stage_name=self.meta.name, rows_in=len(data), rows_out=len(transformed), errors=errors
        )


class Pipeline:
    """Chains stages and executes them in order."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._stages: list[Stage] = []

    def add_stage(self, stage: Stage) -> Pipeline:
        self._stages.append(stage)
        return self

    @property
    def stages(self) -> list[Stage]:
        return list(self._stages)

    def run(self, data: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[TransformResult]]:
        current = data
        results: list[TransformResult] = []
        for stage in self._stages:
            current, result = stage.execute(current)
            results.append(result)
        return current, results
