from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Job:
    name: str
    schedule: str
    enabled: bool

@dataclass
class JobRun:
    job: Job
    status: str
    started_at: float
