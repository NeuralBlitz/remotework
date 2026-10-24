"""
Mito Date/Time Utilities
Parsing, formatting, relative time, ranges, cron helpers
"""

import time
import calendar
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple


def now() -> datetime:
    return datetime.now()


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def timestamp() -> float:
    return time.time()


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_iso(text: str) -> datetime:
    text = text.replace("Z", "+00:00")
    return datetime.fromisoformat(text)


def parse(text: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    return datetime.strptime(text, fmt)


def format(dt: datetime = None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    return (dt or now()).strftime(fmt)


def to_timestamp(dt: datetime) -> float:
    return dt.timestamp()


def from_timestamp(ts: float) -> datetime:
    return datetime.fromtimestamp(ts)


def relative_time(dt: datetime, now: datetime = None) -> str:
    now = now or datetime.now()
    diff = now - dt if now > dt else dt - now
    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"
    if seconds < 3600:
        m = int(seconds / 60)
        return f"{m} minute{'s' if m != 1 else ''} ago" if now > dt else f"in {m} minutes"
    if seconds < 86400:
        h = int(seconds / 3600)
        return f"{h} hour{'s' if h != 1 else ''} ago" if now > dt else f"in {h} hours"
    if seconds < 2592000:
        d = int(seconds / 86400)
        return f"{d} day{'s' if d != 1 else ''} ago" if now > dt else f"in {d} days"
    if seconds < 31536000:
        m = int(seconds / 2592000)
        return f"{m} month{'s' if m != 1 else ''} ago" if now > dt else f"in {m} months"
    y = int(seconds / 31536000)
    return f"{y} year{'s' if y != 1 else ''} ago" if now > dt else f"in {y} years"


def add_days(dt: datetime, days: int) -> datetime:
    return dt + timedelta(days=days)


def add_hours(dt: datetime, hours: int) -> datetime:
    return dt + timedelta(hours=hours)


def add_minutes(dt: datetime, minutes: int) -> datetime:
    return dt + timedelta(minutes=minutes)


def start_of_day(dt: datetime = None) -> datetime:
    dt = dt or now()
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day(dt: datetime = None) -> datetime:
    dt = dt or now()
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def start_of_week(dt: datetime = None) -> datetime:
    dt = dt or now()
    return start_of_day(dt - timedelta(days=dt.weekday()))


def start_of_month(dt: datetime = None) -> datetime:
    dt = dt or now()
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def days_between(start: datetime, end: datetime) -> int:
    return abs((end - start).days)


def hours_between(start: datetime, end: datetime) -> float:
    return abs((end - start).total_seconds() / 3600)


def is_weekend(dt: datetime) -> bool:
    return dt.weekday() >= 5


def is_leap_year(year: int) -> bool:
    return calendar.isleap(year)


def days_in_month(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]


def date_range(start: datetime, end: datetime, step_days: int = 1) -> List[datetime]:
    result = []
    current = start
    while current <= end:
        result.append(current)
        current += timedelta(days=step_days)
    return result


def business_days_between(start: datetime, end: datetime) -> int:
    days = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            days += 1
        current += timedelta(days=1)
    return days


def to_epoch_ms(dt: datetime = None) -> int:
    return int((dt or now()).timestamp() * 1000)


def from_epoch_ms(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000)


class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()
        return self

    def stop(self) -> float:
        self.end_time = time.perf_counter()
        return self.elapsed

    @property
    def elapsed(self) -> float:
        end = self.end_time or time.perf_counter()
        return end - (self.start_time or end)

    @property
    def elapsed_ms(self) -> float:
        return self.elapsed * 1000

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()
