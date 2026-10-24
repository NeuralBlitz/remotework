from __future__ import annotations

from dataclasses import dataclass


@dataclass
class QualityRule:
    name: str
    expression: str

@dataclass
class QualityResult:
    rule: QualityRule
    passed: bool
    message: str
