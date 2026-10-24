"""Log aggregation utilities."""
from __future__ import annotations

import time

from .models import LogEntry

__all__ = ["LogEntry", "create_log", "filter_logs"]

def create_log(level: str, message: str) -> LogEntry:
    return LogEntry(level=level, message=message, timestamp=time.time())

def filter_logs(logs: list[LogEntry], level: str) -> list[LogEntry]:
    return [log for log in logs if log.level == level]
