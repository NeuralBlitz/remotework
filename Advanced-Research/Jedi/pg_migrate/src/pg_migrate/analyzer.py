from __future__ import annotations

from pg_migrate.models import DDLCommand, LockLevel, MigrationPlan


class LockAnalyzer:
    def analyze_lock_impact(self, command: DDLCommand, table_size_bytes: int) -> str:
        if not command.is_locking:
            return f"Low impact: '{command.command}' uses {command.lock_level.value} lock"
        size_mb = table_size_bytes / (1024 * 1024)
        if table_size_bytes > 100 * 1024 * 1024:
            return (
                f"HIGH impact: '{command.command}' on {size_mb:.0f} MB table "
                f"requires {command.lock_level.value} lock. Consider maintenance window."
            )
        return (
            f"Medium impact: '{command.command}' on {size_mb:.0f} MB table "
            f"with {command.lock_level.value} lock"
        )

    def estimate_lock_wait_time(self, command: DDLCommand, active_queries: int) -> float:
        if not command.is_locking:
            return 0.0
        base = 0.1
        if command.lock_level == LockLevel.ACCESS_EXCLUSIVE:
            base = 2.0
        elif command.lock_level in (LockLevel.SHARE, LockLevel.SHARE_ROW_EXCLUSIVE):
            base = 1.0
        return base + (active_queries * 0.5)

    def suggest_alternatives(self, command: DDLCommand, table_size_bytes: int) -> list[str]:
        suggestions: list[str] = []
        if not command.is_dangerous:
            return suggestions
        if table_size_bytes > 100 * 1024 * 1024:
            suggestions.append("Use pg_repack for online DDL operations")
        if command.command == "ADD COLUMN DEFAULT":
            suggestions.append("Add column without default, then backfill")
        if command.command == "ALTER COLUMN TYPE":
            suggestions.append("Add new column, copy data, drop old column")
        if command.command == "CREATE INDEX":
            suggestions.append("Use CREATE INDEX CONCURRENTLY")
        return suggestions

    def analyze_plan(self, plan: MigrationPlan) -> list[tuple[DDLCommand, str]]:
        return [
            (cmd, self.analyze_lock_impact(cmd, plan.table_size_bytes)) for cmd in plan.commands
        ]
