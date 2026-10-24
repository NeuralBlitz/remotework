from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum


class ScheduleType(str, Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    CRON = "cron"


@dataclass
class Schedule:
    name: str
    config_name: str
    schedule_type: ScheduleType
    cron_expression: str = ""
    enabled: bool = True
    last_run: datetime | None = None
    next_run: datetime | None = None

    def compute_next_run(self, from_time: datetime | None = None) -> datetime:
        base = from_time or datetime.now(timezone.utc)
        if self.schedule_type == ScheduleType.HOURLY:
            return base + timedelta(hours=1)
        elif self.schedule_type == ScheduleType.DAILY:
            return base + timedelta(days=1)
        elif self.schedule_type == ScheduleType.WEEKLY:
            return base + timedelta(weeks=1)
        return base + timedelta(hours=1)


class BackupScheduler:
    def __init__(self) -> None:
        self._schedules: dict[str, Schedule] = {}

    def add_schedule(self, schedule: Schedule) -> None:
        if schedule.name in self._schedules:
            raise ValueError(f"Schedule {schedule.name!r} already exists")
        self._schedules[schedule.name] = schedule

    def remove_schedule(self, name: str) -> bool:
        return self._schedules.pop(name, None) is not None

    def get_schedule(self, name: str) -> Schedule:
        if name not in self._schedules:
            raise KeyError(f"Schedule {name!r} not found")
        return self._schedules[name]

    def enable_schedule(self, name: str) -> None:
        self.get_schedule(name).enabled = True

    def disable_schedule(self, name: str) -> None:
        self.get_schedule(name).enabled = False

    def get_due_schedules(self) -> list[Schedule]:
        now = datetime.now(timezone.utc)
        return [
            s
            for s in self._schedules.values()
            if s.enabled and (s.next_run is None or s.next_run <= now)
        ]

    @property
    def schedule_count(self) -> int:
        return len(self._schedules)
