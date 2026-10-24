"""Circuit breaker pattern."""
from __future__ import annotations

from .models import CircuitState

__all__ = ["CircuitState", "create_state", "record_failure", "reset_state"]

def create_state(name: str, threshold: int = 5) -> CircuitState:
    return CircuitState(name=name, failures=0, threshold=threshold)

def record_failure(state: CircuitState) -> CircuitState:
    return CircuitState(
        name=state.name,
        failures=state.failures + 1,
        threshold=state.threshold,
    )

def reset_state(state: CircuitState) -> CircuitState:
    return CircuitState(name=state.name, failures=0, threshold=state.threshold)
