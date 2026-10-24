from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RetryPolicy:
    max_attempts: int
    backoff_multiplier: float

@dataclass
class RetryAttempt:
    attempt: int
    delay: float
    success: bool
