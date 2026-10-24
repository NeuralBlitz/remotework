"""Tests for etl_orchestrator."""
from __future__ import annotations

from src.etl_orchestrator import create_pipeline, create_task, validate_pipeline
from src.etl_orchestrator.models import Pipeline


def test_create_task():
    task = create_task("t1", "load", {"source": "db"})
    assert task.id == "t1"
    assert task.operation == "load"

def test_create_pipeline():
    pipeline = create_pipeline([])
    assert isinstance(pipeline, Pipeline)

def test_create_pipeline_with_tasks():
    tasks = [
        create_task("t1", "extract", {}),
        create_task("t2", "transform", {}),
    ]
    pipeline = create_pipeline(tasks)
    assert len(pipeline.tasks) == 2

def test_validate_pipeline_empty():
    pipeline = create_pipeline([])
    assert validate_pipeline(pipeline) is False

def test_validate_pipeline_with_tasks():
    pipeline = create_pipeline([create_task("t1", "load", {})])
    assert validate_pipeline(pipeline) is True

def test_pipeline_to_dict():
    pipeline = create_pipeline([
        create_task("t1", "extract", {"key": "val"}),
    ])
    d = pipeline.to_dict()
    assert "tasks" in d
    assert len(d["tasks"]) == 1
