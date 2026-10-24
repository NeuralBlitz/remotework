"""Data quality checks."""
from __future__ import annotations

from .models import QualityResult, QualityRule

__all__ = ["QualityRule", "QualityResult", "create_rule", "check_rule"]

def create_rule(name: str, expression: str) -> QualityRule:
    return QualityRule(name=name, expression=expression)

def check_rule(rule: QualityRule, data: dict[str, object]) -> QualityResult:
    passed = "value" in data and isinstance(data.get("value"), (int, float))
    return QualityResult(
        rule=rule,
        passed=passed,
        message="OK" if passed else "Validation failed",
    )
