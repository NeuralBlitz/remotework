"""
Mito Validators
Input validation for email, URL, IP, UUID, JSON schema, config
"""

import re
import json
from typing import Any, Dict, List, Optional, Callable


def is_email(value: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value))


def is_url(value: str) -> bool:
    return bool(re.match(r"^https?://[^\s/$.?#].[^\s]*$", value))


def is_ipv4(value: str) -> bool:
    parts = value.split(".")
    if len(parts) != 4:
        return False
    return all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)


def is_ipv6(value: str) -> bool:
    return bool(re.match(r"^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$", value))


def is_uuid(value: str) -> bool:
    return bool(re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", value.lower()))


def is_hex_color(value: str) -> bool:
    return bool(re.match(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", value))


def is_credit_card(value: str) -> bool:
    digits = re.sub(r"\D", "", value)
    if len(digits) < 13 or len(digits) > 19:
        return False
    total = 0
    for i, d in enumerate(reversed(digits)):
        n = int(d)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def is_phone(value: str, country: str = "US") -> bool:
    digits = re.sub(r"\D", "", value)
    if country == "US":
        return len(digits) == 10 or (len(digits) == 11 and digits[0] == "1")
    return 7 <= len(digits) <= 15


def is_json(value: str) -> bool:
    try:
        json.loads(value)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def is_alphanumeric(value: str) -> bool:
    return value.isalnum()


def is_numeric(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_integer(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_positive(value: float) -> bool:
    return value > 0


def in_range(value: float, min_val: float, max_val: float) -> bool:
    return min_val <= value <= max_val


def min_length(value: str, length: int) -> bool:
    return len(value) >= length


def max_length(value: str, length: int) -> bool:
    return len(value) <= length


def matches_pattern(value: str, pattern: str) -> bool:
    return bool(re.match(pattern, value))


def is_slug(value: str) -> bool:
    return bool(re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", value))


def is_semver(value: str) -> bool:
    return bool(re.match(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$", value))


class Validator:
    def __init__(self):
        self.rules: Dict[str, List[Callable]] = {}
        self.errors: Dict[str, List[str]] = {}

    def field(self, name: str) -> "Validator":
        self._current_field = name
        if name not in self.rules:
            self.rules[name] = []
        return self

    def required(self, msg: str = None) -> "Validator":
        self.rules[self._current_field].append(
            (lambda v: v is not None and str(v).strip() != "",
             msg or f"{self._current_field} is required")
        )
        return self

    def email(self, msg: str = None) -> "Validator":
        self.rules[self._current_field].append(
            (lambda v: is_email(str(v)), msg or f"{self._current_field} must be a valid email")
        )
        return self

    def url(self, msg: str = None) -> "Validator":
        self.rules[self._current_field].append(
            (lambda v: is_url(str(v)), msg or f"{self._current_field} must be a valid URL")
        )
        return self

    def min_len(self, length: int, msg: str = None) -> "Validator":
        self.rules[self._current_field].append(
            (lambda v: min_length(str(v), length), msg or f"{self._current_field} must be at least {length} chars")
        )
        return self

    def max_len(self, length: int, msg: str = None) -> "Validator":
        self.rules[self._current_field].append(
            (lambda v: max_length(str(v), length), msg or f"{self._current_field} must be at most {length} chars")
        )
        return self

    def one_of(self, choices: List[Any], msg: str = None) -> "Validator":
        self.rules[self._current_field].append(
            (lambda v: v in choices, msg or f"{self._current_field} must be one of {choices}")
        )
        return self

    def validate(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        self.errors = {}
        for field, rules in self.rules.items():
            value = data.get(field)
            for check, msg in rules:
                if not check(value):
                    if field not in self.errors:
                        self.errors[field] = []
                    self.errors[field].append(msg)
        return self.errors

    def is_valid(self, data: Dict[str, Any]) -> bool:
        return len(self.validate(data)) == 0
