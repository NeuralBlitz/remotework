from __future__ import annotations

from pg_extensions.models import ExtensionInfo


class ExtensionRegistry:
    def __init__(self) -> None:
        self._extensions: dict[str, ExtensionInfo] = {}

    def register(self, ext: ExtensionInfo) -> None:
        self._extensions[ext.name] = ext

    def get(self, name: str) -> ExtensionInfo | None:
        return self._extensions.get(name)

    def list_all(self) -> list[ExtensionInfo]:
        return list(self._extensions.values())

    def list_enabled(self) -> list[ExtensionInfo]:
        return [e for e in self._extensions.values() if e.enabled]

    def list_disabled(self) -> list[ExtensionInfo]:
        return [e for e in self._extensions.values() if not e.enabled]
