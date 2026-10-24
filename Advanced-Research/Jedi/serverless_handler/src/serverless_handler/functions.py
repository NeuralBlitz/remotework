from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ServerlessFunction:
    name: str
    handler: Callable[..., Any]
    timeout_ms: int = 30000
    memory_mb: int = 256
    env: dict[str, str] = field(default_factory=dict)
    triggers: list[str] = field(default_factory=list)

    def invoke(self, payload: dict[str, Any]) -> Any:
        return self.handler(payload)


class FunctionRegistry:
    def __init__(self) -> None:
        self._functions: dict[str, ServerlessFunction] = {}

    def register(self, func: ServerlessFunction) -> None:
        if func.name in self._functions:
            raise ValueError(f"Function {func.name!r} already registered")
        self._functions[func.name] = func

    def unregister(self, name: str) -> bool:
        return self._functions.pop(name, None) is not None

    def get(self, name: str) -> ServerlessFunction:
        if name not in self._functions:
            raise KeyError(f"Function {name!r} not found")
        return self._functions[name]

    def list_functions(self, trigger: str | None = None) -> list[ServerlessFunction]:
        funcs = list(self._functions.values())
        if trigger:
            funcs = [f for f in funcs if trigger in f.triggers]
        return funcs

    @property
    def function_count(self) -> int:
        return len(self._functions)
