"""Tests for batch_scheduler."""
from __future__ import annotations

from src.batch_scheduler import create_job, run_job


def test_create_job():
    job = create_job("my_job", "0 * * * *")
    assert job.name == "my_job"
    assert job.schedule == "0 * * * *"
    assert job.enabled is True

def test_create_job_disabled():
    job = create_job("my_job", "0 * * * *", enabled=False)
    assert job.enabled is False

def test_run_job():
    job = create_job("my_job", "0 * * * *")
    run = run_job(job)
    assert run.job.name == "my_job"
    assert run.status == "running"
    assert run.started_at > 0

def test_run_job_preserves_schedule():
    job = create_job("scheduled", "*/5 * * * *")
    run = run_job(job)
    assert run.job.schedule == "*/5 * * * *"

def test_multiple_jobs():
    job1 = create_job("job1", "0 * * * *")
    job2 = create_job("job2", "*/5 * * * *")
    assert job1.name != job2.name

def test_job_enabled_default():
    job = create_job("test", "0 0 * * *")
    assert hasattr(job, "enabled")
    assert job.enabled is True
