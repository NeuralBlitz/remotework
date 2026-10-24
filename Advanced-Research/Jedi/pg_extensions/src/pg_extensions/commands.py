from __future__ import annotations

from abc import ABC, abstractmethod

from pg_extensions.models import ExtensionCommand, ExtensionInfo


class Command(ABC):
    @abstractmethod
    def execute(self) -> ExtensionCommand: ...

    @abstractmethod
    def undo(self) -> ExtensionCommand: ...


class EnableExtensionCommand(Command):
    def __init__(self, ext: ExtensionInfo) -> None:
        self._ext = ext
        self._was_enabled = ext.enabled

    def execute(self) -> ExtensionCommand:
        self._ext.enabled = True
        return ExtensionCommand(
            sql=f"CREATE EXTENSION IF NOT EXISTS {self._ext.name};",
            rollback_sql=f"DROP EXTENSION IF EXISTS {self._ext.name};",
            description=f"Enable {self._ext.name}",
        )

    def undo(self) -> ExtensionCommand:
        self._ext.enabled = self._was_enabled
        return ExtensionCommand(
            sql=f"DROP EXTENSION IF EXISTS {self._ext.name};",
            rollback_sql=f"CREATE EXTENSION IF NOT EXISTS {self._ext.name};",
            description=f"Undo enable {self._ext.name}",
        )


class DisableExtensionCommand(Command):
    def __init__(self, ext: ExtensionInfo) -> None:
        self._ext = ext
        self._was_enabled = ext.enabled

    def execute(self) -> ExtensionCommand:
        self._ext.enabled = False
        return ExtensionCommand(
            sql=f"DROP EXTENSION IF EXISTS {self._ext.name};",
            rollback_sql=f"CREATE EXTENSION IF NOT EXISTS {self._ext.name};",
            description=f"Disable {self._ext.name}",
        )

    def undo(self) -> ExtensionCommand:
        self._ext.enabled = self._was_enabled
        return ExtensionCommand(
            sql=f"CREATE EXTENSION IF NOT EXISTS {self._ext.name};",
            rollback_sql=f"DROP EXTENSION IF EXISTS {self._ext.name};",
            description=f"Undo disable {self._ext.name}",
        )


class CommandInvoker:
    def __init__(self) -> None:
        self._history: list[Command] = []
        self._executed: list[ExtensionCommand] = []

    def execute(self, cmd: Command) -> ExtensionCommand:
        result = cmd.execute()
        self._history.append(cmd)
        self._executed.append(result)
        return result

    def undo(self) -> ExtensionCommand:
        if not self._history:
            raise IndexError("Nothing to undo")
        cmd = self._history.pop()
        result = cmd.undo()
        self._executed.append(result)
        return result

    def dry_run(self, cmd: Command) -> ExtensionCommand:
        if isinstance(cmd, EnableExtensionCommand):
            return ExtensionCommand(
                sql=f"CREATE EXTENSION IF NOT EXISTS {cmd._ext.name};",
                rollback_sql=f"DROP EXTENSION IF EXISTS {cmd._ext.name};",
                description=f"[DRY RUN] Enable {cmd._ext.name}",
            )
        elif isinstance(cmd, DisableExtensionCommand):
            return ExtensionCommand(
                sql=f"DROP EXTENSION IF EXISTS {cmd._ext.name};",
                rollback_sql=f"CREATE EXTENSION IF NOT EXISTS {cmd._ext.name};",
                description=f"[DRY RUN] Disable {cmd._ext.name}",
            )
        return ExtensionCommand(sql="-- noop", rollback_sql="-- noop", description="[DRY RUN]")

    @property
    def executed(self) -> list[ExtensionCommand]:
        return list(self._executed)
