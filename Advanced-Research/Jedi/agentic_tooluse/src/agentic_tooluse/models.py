from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class ToolType(Enum):
    SEARCH = auto()
    CALCULATOR = auto()
    API = auto()


@dataclass
class Observation:
    content: str
    tool_type: ToolType
    success: bool = True


@dataclass
class Thought:
    reasoning: str
    action_needed: ToolType | None = None
    action_input: str = ""
