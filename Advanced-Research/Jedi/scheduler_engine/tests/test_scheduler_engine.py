"""Tests for scheduler_engine."""
from __future__ import annotations

from src.scheduler_engine import create_scheduled_task, execute_task


def test_create_scheduled_task():
    task = create_scheduled_task("task1", "0 * * * *", "my_callback")
    assert task.id == "task1"
    assert task.cron == "0 * * * *"
    assert task.callback == "my_callback"

def test_execute_task():
    task = create_scheduled_task("task1", "0 * * * *", "cb")
    execution = execute_task(task)
    assert execution.task.id == "task1"
    assert execution.executed_at > 0

def test_execute_preserves_task_info():
    task = create_scheduled_task("my_task", "*/5 * * * *", "my_callback")
    execution = execute_task(task)
    assert execution.task.cron == "*/5 * * * *"
    assert execution.task.callback == "my_callback"

def test_multiple_tasks():
    t1 = create_scheduled_task("a", "0 * * * *", "cb1")
    t2 = create_scheduled_task("b", "*/5 * * * *", "cb2")
    assert t1.id != t2.id

def test_task_execution_has_timestamp():
    task = create_scheduled_task("t1", "* * * * *", "cb")
    execution = execute_task(task)
    assert hasattr(execution, "executed_at")
    assert isinstance(execution.executed_at, float)

def test_different_crons():
    task = create_scheduled_task("t1", "0 0 * * *", "cb")
    assert task.cron == "0 0 * * *"
    task2 = create_scheduled_task("t2", "*/15 * * * *", "cb")
    assert task2.cron == "*/15 * * * *"
