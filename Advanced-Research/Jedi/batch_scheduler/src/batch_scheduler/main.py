"""Batch job scheduling."""
from __future__ import annotations

import time

from .models import Job, JobRun

__all__ = ["Job", "JobRun", "create_job", "run_job"]

def create_job(name: str, schedule: str, enabled: bool = True) -> Job:
    return Job(name=name, schedule=schedule, enabled=enabled)

def run_job(job: Job) -> JobRun:
    return JobRun(job=job, status="running", started_at=time.time())
