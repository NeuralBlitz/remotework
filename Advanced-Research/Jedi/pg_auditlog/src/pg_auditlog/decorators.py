"""Decorator-based audit wrappers."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from pg_auditlog.logger import AuditLogger
from pg_auditlog.models import AuditAction, AuditEntry

F = TypeVar("F", bound=Callable[..., Any])


class AuditDecorator:
    """Wraps DB operations to automatically create audit log entries."""

    def __init__(self, logger: AuditLogger) -> None:
        self._logger = logger

    def audit_insert(self, table_name: str, user_id: str = "system") -> Callable[[F], F]:
        def decorator(func: F) -> F:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                result = func(*args, **kwargs)
                row_id = str(result) if result is not None else None
                entry = AuditEntry(
                    action=AuditAction.INSERT,
                    table_name=table_name,
                    user_id=user_id,
                    row_id=row_id,
                    new_data=kwargs,
                )
                self._logger.record(entry)
                return result

            return wrapper  # type: ignore[return-value]

        return decorator

    def audit_update(self, table_name: str, user_id: str = "system") -> Callable[[F], F]:
        def decorator(func: F) -> F:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                old_data = kwargs.pop("old_data", None)
                result = func(*args, **kwargs)
                row_id = kwargs.get("row_id", str(args[1]) if len(args) > 1 else None)
                entry = AuditEntry(
                    action=AuditAction.UPDATE,
                    table_name=table_name,
                    user_id=user_id,
                    row_id=str(row_id) if row_id else None,
                    old_data=old_data,
                    new_data=kwargs,
                )
                self._logger.record(entry)
                return result

            return wrapper  # type: ignore[return-value]

        return decorator

    def audit_delete(self, table_name: str, user_id: str = "system") -> Callable[[F], F]:
        def decorator(func: F) -> F:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                result = func(*args, **kwargs)
                row_id = str(args[0]) if len(args) > 0 else kwargs.get("row_id", "unknown")
                entry = AuditEntry(
                    action=AuditAction.DELETE,
                    table_name=table_name,
                    user_id=user_id,
                    row_id=str(row_id),
                    old_data=kwargs.get("old_data"),
                )
                self._logger.record(entry)
                return result

            return wrapper  # type: ignore[return-value]

        return decorator
