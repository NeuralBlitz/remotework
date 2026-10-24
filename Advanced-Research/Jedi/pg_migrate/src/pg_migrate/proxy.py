from __future__ import annotations

from pg_migrate.models import DDLCommand, MigrationPlan

LARGE_TABLE_THRESHOLD_BYTES = 100 * 1024 * 1024


class DDLBlockedError(Exception):
    pass


class LockGuardProxy:
    def __init__(
        self,
        table_size_bytes: int = 0,
        large_table_threshold: int = LARGE_TABLE_THRESHOLD_BYTES,
    ) -> None:
        self._table_size_bytes = table_size_bytes
        self._large_table_threshold = large_table_threshold
        self._blocked: list[DDLCommand] = []
        self._executed: list[DDLCommand] = []

    @property
    def is_large_table(self) -> bool:
        return self._table_size_bytes >= self._large_table_threshold

    def check(self, command: DDLCommand) -> tuple[bool, str]:
        if not command.is_dangerous:
            return True, "Command is safe to execute"
        if self.is_large_table:
            msg = (
                f"DDL command '{command.command}' on large table "
                f"({self._table_size_bytes / (1024 * 1024):.0f} MB) requires ACCESS EXCLUSIVE lock"
            )
            if command.requires_repack_suggestion:
                msg += ". Consider using pg_repack to avoid long locks."
            return False, msg
        return True, "Command accepted for small table"

    def execute(self, command: DDLCommand) -> tuple[bool, str]:
        allowed, reason = self.check(command)
        if allowed:
            self._executed.append(command)
            return True, reason
        self._blocked.append(command)
        return False, reason

    def execute_safe(self, command: DDLCommand) -> tuple[bool, str]:
        allowed, reason = self.execute(command)
        if not allowed:
            raise DDLBlockedError(reason)
        return allowed, reason

    def review_plan(self, plan: MigrationPlan) -> list[tuple[DDLCommand, bool, str]]:
        results: list[tuple[DDLCommand, bool, str]] = []
        for cmd in plan.commands:
            allowed, reason = self.check(cmd)
            results.append((cmd, allowed, reason))
        return results

    @property
    def blocked_commands(self) -> list[DDLCommand]:
        return list(self._blocked)

    @property
    def executed_commands(self) -> list[DDLCommand]:
        return list(self._executed)
