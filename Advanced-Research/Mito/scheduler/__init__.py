"""
Mito Task Scheduler
Cron-based scheduling, interval tasks, one-shot scheduling
"""

import asyncio
import json
import logging
import time
import uuid
import re
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
import threading

logger = logging.getLogger("mito.scheduler")


class ScheduleType(Enum):
    CRON = "cron"
    INTERVAL = "interval"
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


class TaskState(Enum):
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


@dataclass
class CronExpression:
    minute: str = "*"
    hour: str = "*"
    day: str = "*"
    month: str = "*"
    weekday: str = "*"

    @classmethod
    def parse(cls, expr: str) -> "CronExpression":
        parts = expr.strip().split()
        if len(parts) != 5:
            raise ValueError(f"Invalid cron expression: {expr}")
        return cls(minute=parts[0], hour=parts[1], day=parts[2],
                   month=parts[3], weekday=parts[4])

    def matches(self, dt: datetime) -> bool:
        return (
            self._match_field(dt.minute, self.minute) and
            self._match_field(dt.hour, self.hour) and
            self._match_field(dt.day, self.day) and
            self._match_field(dt.month, self.month) and
            self._match_field(dt.weekday(), self.weekday)
        )

    def _match_field(self, value: int, spec: str) -> bool:
        if spec == "*":
            return True
        if "," in spec:
            return any(self._match_field(value, s.strip()) for s in spec.split(","))
        if "/" in spec:
            base, step = spec.split("/")
            step = int(step)
            if base == "*":
                return value % step == 0
            return value >= int(base) and (value - int(base)) % step == 0
        if "-" in spec:
            start, end = spec.split("-")
            return int(start) <= value <= int(end)
        return value == int(spec)

    def next_run(self, after: datetime = None) -> datetime:
        dt = after or datetime.now()
        dt = dt.replace(second=0, microsecond=0) + timedelta(minutes=1)

        for _ in range(525600):  # max 1 year
            if self.matches(dt):
                return dt
            dt += timedelta(minutes=1)

        raise ValueError("Could not find next run time within 1 year")


@dataclass
class ScheduledTask:
    id: str
    name: str
    func: Callable
    schedule_type: ScheduleType
    state: TaskState = TaskState.SCHEDULED
    cron_expr: Optional[CronExpression] = None
    interval_seconds: float = 0
    run_at: Optional[float] = None
    next_run: float = 0
    last_run: float = 0
    run_count: int = 0
    max_runs: int = 0  # 0 = unlimited
    last_error: str = ""
    args: List[Any] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    timeout: float = 0
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


class TaskScheduler:
    def __init__(self, max_workers: int = 4):
        self.tasks: Dict[str, ScheduledTask] = {}
        self.max_workers = max_workers
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._executor = None

    def schedule_cron(self, name: str, func: Callable, cron: str,
                      args: List = None, kwargs: Dict = None, **opts) -> ScheduledTask:
        cron_expr = CronExpression.parse(cron)
        task = ScheduledTask(
            id=str(uuid.uuid4()),
            name=name,
            func=func,
            schedule_type=ScheduleType.CRON,
            cron_expr=cron_expr,
            next_run=cron_expr.next_run().timestamp(),
            args=args or [],
            kwargs=kwargs or {},
            timeout=opts.get("timeout", 0),
            max_runs=opts.get("max_runs", 0),
            tags=opts.get("tags", []),
        )
        with self._lock:
            self.tasks[task.id] = task
        logger.info(f"Scheduled cron task '{name}': {cron}")
        return task

    def schedule_interval(self, name: str, func: Callable, seconds: float,
                          args: List = None, kwargs: Dict = None, **opts) -> ScheduledTask:
        task = ScheduledTask(
            id=str(uuid.uuid4()),
            name=name,
            func=func,
            schedule_type=ScheduleType.INTERVAL,
            interval_seconds=seconds,
            next_run=time.time() + seconds,
            args=args or [],
            kwargs=kwargs or {},
            timeout=opts.get("timeout", 0),
            max_runs=opts.get("max_runs", 0),
            tags=opts.get("tags", []),
        )
        with self._lock:
            self.tasks[task.id] = task
        logger.info(f"Scheduled interval task '{name}': every {seconds}s")
        return task

    def schedule_once(self, name: str, func: Callable, run_at: float,
                      args: List = None, kwargs: Dict = None, **opts) -> ScheduledTask:
        task = ScheduledTask(
            id=str(uuid.uuid4()),
            name=name,
            func=func,
            schedule_type=ScheduleType.ONCE,
            run_at=run_at,
            next_run=run_at,
            args=args or [],
            kwargs=kwargs or {},
            timeout=opts.get("timeout", 0),
            tags=opts.get("tags", []),
        )
        with self._lock:
            self.tasks[task.id] = task
        logger.info(f"Scheduled one-shot task '{name}' at {datetime.fromtimestamp(run_at)}")
        return task

    def schedule_daily(self, name: str, func: Callable, hour: int, minute: int = 0,
                       args: List = None, kwargs: Dict = None, **opts) -> ScheduledTask:
        cron = f"{minute} {hour} * * *"
        return self.schedule_cron(name, func, cron, args, kwargs, **opts)

    def schedule_weekly(self, name: str, func: Callable, weekday: int, hour: int,
                        minute: int = 0, args: List = None, kwargs: Dict = None,
                        **opts) -> ScheduledTask:
        cron = f"{minute} {hour} * * {weekday}"
        return self.schedule_cron(name, func, cron, args, kwargs, **opts)

    def cancel(self, task_id: str):
        with self._lock:
            if task_id in self.tasks:
                self.tasks[task_id].state = TaskState.CANCELLED
                logger.info(f"Cancelled task '{self.tasks[task_id].name}'")

    def pause(self, task_id: str):
        with self._lock:
            if task_id in self.tasks:
                self.tasks[task_id].state = TaskState.PAUSED

    def resume(self, task_id: str):
        with self._lock:
            if task_id in self.tasks:
                self.tasks[task_id].state = TaskState.SCHEDULED

    def remove(self, task_id: str):
        with self._lock:
            if task_id in self.tasks:
                del self.tasks[task_id]

    def run_pending(self) -> List[Dict]:
        now = time.time()
        results = []

        with self._lock:
            pending = [
                t for t in self.tasks.values()
                if t.state == TaskState.SCHEDULED and t.next_run <= now
            ]

        for task in pending:
            result = self._run_task(task)
            results.append(result)

        return results

    def _run_task(self, task: ScheduledTask) -> Dict:
        task.state = TaskState.RUNNING
        task.last_run = time.time()
        task.run_count += 1

        try:
            if task.timeout > 0:
                from concurrent.futures import ThreadPoolExecutor, TimeoutError as FETimeout
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(task.func, *task.args, **task.kwargs)
                    result = future.result(timeout=task.timeout)
            else:
                result = task.func(*task.args, **task.kwargs)

            task.state = TaskState.SCHEDULED
            task.last_error = ""

            if task.schedule_type == ScheduleType.ONCE:
                task.state = TaskState.COMPLETED
            elif task.schedule_type == ScheduleType.CRON and task.cron_expr:
                task.next_run = task.cron_expr.next_run(
                    datetime.fromtimestamp(time.time())
                ).timestamp()
            elif task.schedule_type == ScheduleType.INTERVAL:
                task.next_run = time.time() + task.interval_seconds

            if task.max_runs > 0 and task.run_count >= task.max_runs:
                task.state = TaskState.COMPLETED

            return {"task_id": task.id, "name": task.name, "status": "success", "result": result}

        except Exception as e:
            task.state = TaskState.FAILED
            task.last_error = str(e)
            logger.error(f"Task '{task.name}' failed: {e}")
            return {"task_id": task.id, "name": task.name, "status": "failed", "error": str(e)}

    def start(self, check_interval: float = 1.0):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, args=(check_interval,), daemon=True)
        self._thread.start()
        logger.info("Task scheduler started")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Task scheduler stopped")

    def _loop(self, check_interval: float):
        while self._running:
            self.run_pending()
            time.sleep(check_interval)

    def get_tasks(self, state: TaskState = None) -> List[ScheduledTask]:
        with self._lock:
            tasks = list(self.tasks.values())
        if state:
            tasks = [t for t in tasks if t.state == state]
        return tasks

    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        return self.tasks.get(task_id)
