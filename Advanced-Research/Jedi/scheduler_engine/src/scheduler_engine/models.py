from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScheduledTask:
    id: str
    cron: str
    callback: str

@dataclass
class TaskExecution:
    task: ScheduledTask
    executed_at: float
