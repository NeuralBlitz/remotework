from dataclasses import dataclass, field
from enum import Enum


class LockLevel(Enum):
    ACCESS_SHARE = "ACCESS SHARE"
    ROW_SHARE = "ROW SHARE"
    ROW_EXCLUSIVE = "ROW EXCLUSIVE"
    SHARE_UPDATE_EXCLUSIVE = "SHARE UPDATE EXCLUSIVE"
    SHARE = "SHARE"
    SHARE_ROW_EXCLUSIVE = "SHARE ROW EXCLUSIVE"
    ACCESS_EXCLUSIVE = "ACCESS EXCLUSIVE"


@dataclass(frozen=True)
class DDLCommand:
    command: str
    table_name: str
    schema_name: str = "public"
    lock_level: LockLevel = LockLevel.ACCESS_EXCLUSIVE
    raw_sql: str = ""

    @property
    def is_locking(self) -> bool:
        heavy_locks = {
            LockLevel.ACCESS_EXCLUSIVE,
            LockLevel.SHARE_ROW_EXCLUSIVE,
            LockLevel.SHARE,
        }
        return self.lock_level in heavy_locks

    @property
    def is_dangerous(self) -> bool:
        return self.lock_level == LockLevel.ACCESS_EXCLUSIVE

    @property
    def requires_repack_suggestion(self) -> bool:
        return self.command in {"ADD COLUMN DEFAULT", "ALTER COLUMN TYPE", "DROP COLUMN"}


@dataclass(frozen=True)
class MigrationPlan:
    schema_name: str
    commands: list[DDLCommand] = field(default_factory=list)
    table_size_bytes: int = 0
    approved: bool = False

    @property
    def has_dangerous_commands(self) -> bool:
        return any(cmd.is_dangerous for cmd in self.commands)

    @property
    def total_commands(self) -> int:
        return len(self.commands)

    @property
    def table_size_mb(self) -> float:
        return self.table_size_bytes / (1024 * 1024)
