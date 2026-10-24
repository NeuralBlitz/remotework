from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"
    PANIC = "PANIC"


@dataclass(frozen=True)
class LogEntry:
    timestamp: datetime
    level: LogLevel
    message: str
    query: str | None = None
    duration_ms: float | None = None
    pid: int | None = None
    source_file: str = "postgresql.log"
    line_number: int = 0


@dataclass(frozen=True)
class AlertEvent:
    alert_id: str
    source_entry: LogEntry
    alert_type: str
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    severity: LogLevel = LogLevel.WARNING
