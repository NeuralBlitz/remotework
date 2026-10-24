from __future__ import annotations

import pytest

from pg_extensions.commands import CommandInvoker, DisableExtensionCommand, EnableExtensionCommand
from pg_extensions.models import ExtensionInfo
from pg_extensions.registry import ExtensionRegistry


def test_enable_extension() -> None:
    ext = ExtensionInfo(name="pgcrypto")
    cmd = EnableExtensionCommand(ext)
    result = cmd.execute()
    assert ext.enabled is True
    assert "CREATE EXTENSION" in result.sql
    assert "pgcrypto" in result.sql


def test_disable_extension() -> None:
    ext = ExtensionInfo(name="pgcrypto", enabled=True)
    cmd = DisableExtensionCommand(ext)
    result = cmd.execute()
    assert ext.enabled is False
    assert "DROP EXTENSION" in result.sql


def test_undo_enable() -> None:
    ext = ExtensionInfo(name="pgcrypto")
    cmd = EnableExtensionCommand(ext)
    cmd.execute()
    assert ext.enabled is True
    result = cmd.undo()
    assert ext.enabled is False
    assert "DROP EXTENSION" in result.sql


def test_undo_disable() -> None:
    ext = ExtensionInfo(name="pgcrypto", enabled=True)
    cmd = DisableExtensionCommand(ext)
    cmd.execute()
    assert ext.enabled is False
    result = cmd.undo()
    assert ext.enabled is True
    assert "CREATE EXTENSION" in result.sql


def test_invoker_execute() -> None:
    ext = ExtensionInfo(name="uuid-ossp")
    invoker = CommandInvoker()
    invoker.execute(EnableExtensionCommand(ext))
    assert ext.enabled is True
    assert len(invoker.executed) == 1


def test_invoker_undo() -> None:
    ext = ExtensionInfo(name="uuid-ossp")
    invoker = CommandInvoker()
    invoker.execute(EnableExtensionCommand(ext))
    result = invoker.undo()
    assert ext.enabled is False
    assert "DROP EXTENSION" in result.sql


def test_invoker_undo_empty() -> None:
    invoker = CommandInvoker()
    with pytest.raises(IndexError):
        invoker.undo()


def test_dry_run_enable() -> None:
    ext = ExtensionInfo(name="hstore")
    invoker = CommandInvoker()
    result = invoker.dry_run(EnableExtensionCommand(ext))
    assert ext.enabled is False  # not actually executed
    assert "[DRY RUN]" in result.description
    assert "CREATE EXTENSION" in result.sql


def test_dry_run_disable() -> None:
    ext = ExtensionInfo(name="hstore", enabled=True)
    invoker = CommandInvoker()
    result = invoker.dry_run(DisableExtensionCommand(ext))
    assert ext.enabled is True
    assert "DROP EXTENSION" in result.sql


def test_registry() -> None:
    reg = ExtensionRegistry()
    e1 = ExtensionInfo(name="pgcrypto", enabled=True)
    e2 = ExtensionInfo(name="hstore")
    reg.register(e1)
    reg.register(e2)
    assert reg.get("pgcrypto") is e1
    assert len(reg.list_all()) == 2
    assert len(reg.list_enabled()) == 1
    assert len(reg.list_disabled()) == 1


def test_registry_get_missing() -> None:
    reg = ExtensionRegistry()
    assert reg.get("nope") is None
