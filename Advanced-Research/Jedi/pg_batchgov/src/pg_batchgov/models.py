from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Priority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class ResourceLimits:
    max_memory_mb: int = 512
    max_cpu_percent: float = 50.0
    max_connections: int = 5
    timeout_seconds: float = 300.0


@dataclass(frozen=True)
class BatchConfig:
    name: str
    priority: Priority = Priority.NORMAL
    limits: ResourceLimits = field(default_factory=ResourceLimits)
    retry_count: int = 0
    tags: tuple[str, ...] = ()


@dataclass
class JobResult:
    job_name: str
    success: bool
    result: Any = None
    error: str | None = None
    started_at: datetime = field(default_factory=datetime.now)
    finished_at: datetime | None = None
    duration_ms: float = 0.0
    retries_used: int = 0
