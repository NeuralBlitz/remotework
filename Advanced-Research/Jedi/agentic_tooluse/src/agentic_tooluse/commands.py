from __future__ import annotations

from abc import ABC, abstractmethod

from agentic_tooluse.models import Observation, ToolType


class ToolCommand(ABC):
    @abstractmethod
    def execute(self, query: str) -> Observation: ...

    @abstractmethod
    def tool_type(self) -> ToolType: ...


class SearchCommand(ToolCommand):
    def execute(self, query: str) -> Observation:
        return Observation(
            content=f"Search results for: {query}",
            tool_type=ToolType.SEARCH,
        )

    def tool_type(self) -> ToolType:
        return ToolType.SEARCH


class CalculatorCommand(ToolCommand):
    def execute(self, query: str) -> Observation:
        try:
            allowed = {"__builtins__": {}}
            result = eval(query, allowed, {})
            return Observation(
                content=str(result),
                tool_type=ToolType.CALCULATOR,
            )
        except Exception as e:
            return Observation(
                content=f"Error: {e}",
                tool_type=ToolType.CALCULATOR,
                success=False,
            )

    def tool_type(self) -> ToolType:
        return ToolType.CALCULATOR
