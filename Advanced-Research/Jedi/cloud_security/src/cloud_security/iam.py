from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    REPLICATION = "replication"
    SUPERUSER = "superuser"


@dataclass
class Role:
    name: str
    permissions: set[Permission] = field(default_factory=set)
    inherits_from: list[str] = field(default_factory=list)

    def has_permission(self, perm: Permission) -> bool:
        return perm in self.permissions


class IAMManager:
    def __init__(self) -> None:
        self._roles: dict[str, Role] = {}
        self._users: dict[str, set[str]] = {}

    def create_role(self, name: str, permissions: set[Permission] | None = None) -> Role:
        if name in self._roles:
            raise ValueError(f"Role {name!r} already exists")
        role = Role(name=name, permissions=permissions or set())
        self._roles[name] = role
        return role

    def get_role(self, name: str) -> Role:
        if name not in self._roles:
            raise KeyError(f"Role {name!r} not found")
        return self._roles[name]

    def grant_permission(self, role_name: str, perm: Permission) -> None:
        role = self.get_role(role_name)
        role.permissions.add(perm)

    def revoke_permission(self, role_name: str, perm: Permission) -> None:
        role = self.get_role(role_name)
        role.permissions.discard(perm)

    def assign_role(self, user: str, role_name: str) -> None:
        if role_name not in self._roles:
            raise KeyError(f"Role {role_name!r} not found")
        self._users.setdefault(user, set()).add(role_name)

    def remove_role(self, user: str, role_name: str) -> None:
        if user in self._users:
            self._users[user].discard(role_name)

    def get_user_roles(self, user: str) -> set[str]:
        return set(self._users.get(user, set()))

    def check_access(self, user: str, required: Permission) -> bool:
        for role_name in self._users.get(user, set()):
            role = self._roles.get(role_name)
            if role and self._has_effective_permission(role, required):
                return True
        return False

    def _has_effective_permission(self, role: Role, perm: Permission) -> bool:
        if role.has_permission(perm):
            return True
        for parent_name in role.inherits_from:
            parent = self._roles.get(parent_name)
            if parent and self._has_effective_permission(parent, perm):
                return True
        return False
