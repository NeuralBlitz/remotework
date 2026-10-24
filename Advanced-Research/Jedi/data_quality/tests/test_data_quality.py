"""Tests for data_quality."""
from __future__ import annotations

from src.data_quality import check_rule, create_rule


def test_create_rule():
    rule = create_rule("not_null", "value is not null")
    assert rule.name == "not_null"
    assert rule.expression == "value is not null"

def test_check_rule_passed():
    rule = create_rule("has_value", "value exists")
    result = check_rule(rule, {"value": 42})
    assert result.passed is True

def test_check_rule_failed():
    rule = create_rule("has_value", "value exists")
    result = check_rule(rule, {})
    assert result.passed is False

def test_check_rule_wrong_type():
    rule = create_rule("is_number", "value is number")
    result = check_rule(rule, {"value": "not a number"})
    assert result.passed is False

def test_check_rule_with_none():
    rule = create_rule("has_value", "value exists")
    result = check_rule(rule, {"value": None})
    assert result.passed is False

def test_quality_result_message():
    rule = create_rule("test", "test expression")
    result = check_rule(rule, {"value": 1})
    assert result.message == "OK"
