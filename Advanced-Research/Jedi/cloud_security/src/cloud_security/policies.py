from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PolicyEffect(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass
class SecurityPolicy:
    name: str
    effect: PolicyEffect
    actions: list[str] = field(default_factory=list)
    resources: list[str] = field(default_factory=list)
    conditions: dict[str, Any] = field(default_factory=dict)

    def matches(self, action: str, resource: str) -> bool:
        action_ok = "*" in self.actions or action in self.actions
        resource_ok = "*" in self.resources or resource in self.resources
        return action_ok and resource_ok


class PolicyEngine:
    def __init__(self) -> None:
        self._policies: list[SecurityPolicy] = []

    def add_policy(self, policy: SecurityPolicy) -> None:
        self._policies.append(policy)

    def remove_policy(self, name: str) -> bool:
        before = len(self._policies)
        self._policies = [p for p in self._policies if p.name != name]
        return len(self._policies) < before

    def evaluate(self, action: str, resource: str) -> bool:
        for policy in self._policies:
            if policy.matches(action, resource):
                return policy.effect == PolicyEffect.ALLOW
        return False

    @property
    def policy_count(self) -> int:
        return len(self._policies)
