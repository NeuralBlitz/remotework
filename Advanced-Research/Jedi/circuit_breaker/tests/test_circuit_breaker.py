"""Tests for circuit_breaker."""
from __future__ import annotations

from src.circuit_breaker import create_state, record_failure, reset_state


def test_create_state():
    state = create_state("service1")
    assert state.name == "service1"
    assert state.failures == 0
    assert state.threshold == 5

def test_create_state_custom_threshold():
    state = create_state("service2", threshold=3)
    assert state.threshold == 3

def test_record_failure():
    state = create_state("service1")
    new_state = record_failure(state)
    assert new_state.failures == 1
    assert new_state.name == "service1"

def test_record_multiple_failures():
    state = create_state("service1")
    for _ in range(3):
        state = record_failure(state)
    assert state.failures == 3

def test_reset_state():
    state = create_state("service1")
    state = record_failure(state)
    state = record_failure(state)
    new_state = reset_state(state)
    assert new_state.failures == 0

def test_is_open():
    state = create_state("service1", threshold=2)
    assert state.is_open() is False
    state = record_failure(state)
    assert state.is_open() is False
    state = record_failure(state)
    assert state.is_open() is True
