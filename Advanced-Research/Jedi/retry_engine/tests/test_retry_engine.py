"""Tests for retry_engine."""
from __future__ import annotations

from src.retry_engine import calculate_delay, create_policy
from src.retry_engine.models import RetryAttempt


def test_create_policy():
    policy = create_policy()
    assert policy.max_attempts == 3
    assert policy.backoff_multiplier == 2.0

def test_create_policy_custom():
    policy = create_policy(max_attempts=5, backoff_multiplier=1.5)
    assert policy.max_attempts == 5
    assert policy.backoff_multiplier == 1.5

def test_calculate_delay_first_attempt():
    policy = create_policy()
    attempt = RetryAttempt(attempt=1, delay=0.0, success=False)
    assert calculate_delay(attempt, policy) == 1.0

def test_calculate_delay_second_attempt():
    policy = create_policy()
    attempt = RetryAttempt(attempt=2, delay=0.0, success=False)
    assert calculate_delay(attempt, policy) == 2.0

def test_calculate_delay_third_attempt():
    policy = create_policy()
    attempt = RetryAttempt(attempt=3, delay=0.0, success=False)
    assert calculate_delay(attempt, policy) == 4.0

def test_calculate_delay_custom_multiplier():
    policy = create_policy(backoff_multiplier=3.0)
    attempt = RetryAttempt(attempt=2, delay=0.0, success=False)
    assert calculate_delay(attempt, policy) == 3.0
