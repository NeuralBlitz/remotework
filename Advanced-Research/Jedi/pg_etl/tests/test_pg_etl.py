from typing import Any

from pg_etl.models import TransformResult
from pg_etl.pipeline import (
    AggregationStage,
    CleaningStage,
    Pipeline,
    RawIngestStage,
    RegexTransformStage,
)


class TestTransformResult:
    def test_success_with_no_errors(self) -> None:
        r = TransformResult(stage_name="s", rows_in=5, rows_out=5)
        assert r.success

    def test_failure_with_errors(self) -> None:
        r = TransformResult(stage_name="s", rows_in=5, rows_out=3, errors=["oops"])
        assert not r.success


class TestRawIngestStage:
    def test_passes_valid_dicts(self) -> None:
        stage = RawIngestStage()
        data: list[dict[str, Any]] = [{"a": 1}, {"b": 2}]
        out, result = stage.execute(data)
        assert len(out) == 2
        assert result.rows_out == 2

    def test_rejects_non_dicts(self) -> None:
        stage = RawIngestStage()
        data: list[Any] = [{"a": 1}, "bad", {"b": 2}]
        out, result = stage.execute(data)
        assert len(out) == 2
        assert len(result.errors) == 1


class TestCleaningStage:
    def test_removes_rows_missing_required(self) -> None:
        stage = CleaningStage(required_fields=["name"])
        data: list[dict[str, Any]] = [{"name": "Alice"}, {"age": 30}, {"name": None}]
        out, result = stage.execute(data)
        assert len(out) == 1
        assert result.rows_out == 1

    def test_strips_whitespace(self) -> None:
        stage = CleaningStage(required_fields=["name"])
        data: list[dict[str, Any]] = [{"name": "  Bob  "}]
        out, _ = stage.execute(data)
        assert out[0]["name"] == "Bob"


class TestAggregationStage:
    def test_groups_by_key(self) -> None:
        stage = AggregationStage(group_by="category")
        data: list[dict[str, Any]] = [
            {"category": "A", "val": 1},
            {"category": "B", "val": 2},
            {"category": "A", "val": 3},
        ]
        out, result = stage.execute(data)
        assert result.rows_out == 2
        counts = {r["category"]: r["count"] for r in out}
        assert counts["A"] == 2
        assert counts["B"] == 1


class TestRegexTransformStage:
    def test_applies_regex(self) -> None:
        stage = RegexTransformStage(field_name="email", pattern=r"@.+", replacement="@example.com")
        data: list[dict[str, Any]] = [{"email": "user@old.com"}]
        out, result = stage.execute(data)
        assert out[0]["email"] == "user@example.com"
        assert result.rows_out == 1

    def test_error_on_missing_field(self) -> None:
        stage = RegexTransformStage(field_name="email", pattern=r".*", replacement="x")
        data: list[dict[str, Any]] = [{"name": "no email"}]
        _, result = stage.execute(data)
        assert len(result.errors) == 1


class TestPipeline:
    def test_full_pipeline(self) -> None:
        pipe = Pipeline("test")
        pipe.add_stage(RawIngestStage()).add_stage(
            CleaningStage(required_fields=["name"])
        ).add_stage(AggregationStage(group_by="name"))
        data: list[dict[str, Any]] = [
            {"name": "Alice", "val": 1},
            {"name": "Alice", "val": 2},
            {"val": 3},
        ]
        out, results = pipe.run(data)
        assert len(results) == 3
        assert len(out) == 1  # aggregated to one Alice row

    def test_empty_pipeline(self) -> None:
        pipe = Pipeline("empty")
        data: list[dict[str, Any]] = [{"a": 1}]
        out, results = pipe.run(data)
        assert out == data
        assert results == []

    def test_chaining_returns_self(self) -> None:
        pipe = Pipeline("chain")
        returned = pipe.add_stage(RawIngestStage())
        assert returned is pipe
