"""Task scheduling engine."""
from __future__ import annotations

import time

from .models import ScheduledTask, TaskExecution

__all__ = ["ScheduledTask", "TaskExecution", "create_scheduled_task", "execute_task"]

def create_scheduled_task(task_id: str, cron: str, callback: str) -> ScheduledTask:
    return ScheduledTask(id=task_id, cron=cron, callback=callback)

def execute_task(task: ScheduledTask) -> TaskExecution:
    return TaskExecution(task=task, executed_at=time.time())
