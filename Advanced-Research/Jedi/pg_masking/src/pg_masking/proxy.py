from __future__ import annotations

from typing import Any

from pg_masking.models import MaskingRule
from pg_masking.rules import Masker, create_masker


class MaskingProxy:
    """Intercepts query result sets and masks PII based on user role."""

    def __init__(self, rules: list[MaskingRule] | None = None) -> None:
        self._rules: list[MaskingRule] = rules or []
        self._maskers: dict[str, Masker] = {}

    def add_rule(self, rule: MaskingRule) -> None:
        self._rules.append(rule)

    def remove_rule(self, field_name: str) -> None:
        self._rules = [r for r in self._rules if r.field_name != field_name]

    def _get_masker(self, rule: MaskingRule) -> Masker:
        key = f"{rule.field_name}:{rule.masking_type.value}"
        if key not in self._maskers:
            self._maskers[key] = create_masker(rule.masking_type, rule.mask_char)
        return self._maskers[key]

    def apply(self, rows: list[dict[str, Any]], role: str) -> list[dict[str, Any]]:
        """Apply masking rules to a result set based on the caller's role."""
        if not self._rules:
            return rows
        masked: list[dict[str, Any]] = []
        for row in rows:
            new_row: dict[str, Any] = {}
            for key, value in row.items():
                rule = self._find_rule(key)
                if rule and role not in rule.roles_exempt:
                    masker = self._get_masker(rule)
                    new_row[key] = masker.mask(value)
                else:
                    new_row[key] = value
            masked.append(new_row)
        return masked

    def _find_rule(self, field_name: str) -> MaskingRule | None:
        for rule in self._rules:
            if rule.field_name == field_name:
                return rule
        return None

    @property
    def rule_count(self) -> int:
        return len(self._rules)
