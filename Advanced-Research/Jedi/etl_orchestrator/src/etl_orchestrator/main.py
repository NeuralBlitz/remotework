"""ETL pipeline orchestration."""
from __future__ import annotations

from .models import Pipeline, Task

__all__ = ["Task", "Pipeline", "create_task", "create_pipeline", "validate_pipeline"]

def create_task(task_id: str, operation: str, config: dict[str, str]) -> Task:
    return Task(id=task_id, operation=operation, config=config)

def create_pipeline(tasks: list[Task]) -> Pipeline:
    return Pipeline(tasks=tasks)

def validate_pipeline(pipeline: Pipeline) -> bool:
    return len(pipeline.tasks) > 0
