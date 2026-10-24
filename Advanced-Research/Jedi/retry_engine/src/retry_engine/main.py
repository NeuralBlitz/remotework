"""Retry logic engine."""
from __future__ import annotations

from .models import RetryAttempt, RetryPolicy

__all__ = ["RetryPolicy", "RetryAttempt", "create_policy", "calculate_delay"]

def create_policy(max_attempts: int = 3, backoff_multiplier: float = 2.0) -> RetryPolicy:
    return RetryPolicy(max_attempts=max_attempts, backoff_multiplier=backoff_multiplier)

def calculate_delay(attempt: RetryAttempt, policy: RetryPolicy) -> float:
    return 1.0 * (policy.backoff_multiplier ** (attempt.attempt - 1))
