from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from serverless_handler.events import TriggerEvent
from serverless_handler.functions import FunctionRegistry


@dataclass
class InvocationResult:
    function_name: str
    success: bool
    result: Any = None
    error: str = ""
    duration_ms: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class FunctionRuntime:
    def __init__(self, registry: FunctionRegistry) -> None:
        self._registry = registry
        self._invocations: list[InvocationResult] = []

    def invoke(self, function_name: str, payload: dict[str, Any]) -> InvocationResult:
        func = self._registry.get(function_name)
        start = datetime.now(timezone.utc)
        try:
            result = func.invoke(payload)
            end = datetime.now(timezone.utc)
            duration = (end - start).total_seconds() * 1000
            inv = InvocationResult(
                function_name=function_name,
                success=True,
                result=result,
                duration_ms=duration,
            )
        except Exception as e:
            end = datetime.now(timezone.utc)
            duration = (end - start).total_seconds() * 1000
            inv = InvocationResult(
                function_name=function_name,
                success=False,
                error=str(e),
                duration_ms=duration,
            )
        self._invocations.append(inv)
        return inv

    def dispatch_event(self, event: TriggerEvent, targets: list[str]) -> list[InvocationResult]:
        results: list[InvocationResult] = []
        for func_name in targets:
            results.append(self.invoke(func_name, event.payload))
        return results

    def get_invocations(self, function_name: str | None = None) -> list[InvocationResult]:
        if function_name is None:
            return list(self._invocations)
        return [i for i in self._invocations if i.function_name == function_name]

    def get_failed_invocations(self) -> list[InvocationResult]:
        return [i for i in self._invocations if not i.success]

    @property
    def invocation_count(self) -> int:
        return len(self._invocations)

    @property
    def success_rate(self) -> float:
        if not self._invocations:
            return 0.0
        successful = sum(1 for i in self._invocations if i.success)
        return successful / len(self._invocations)
