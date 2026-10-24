from __future__ import annotations

from agentic_tooluse.commands import ToolCommand
from agentic_tooluse.models import Observation, Thought, ToolType


class ReActAgent:
    def __init__(self) -> None:
        self._commands: dict[ToolType, ToolCommand] = {}
        self.history: list[tuple[Thought, Observation]] = []

    def register(self, cmd: ToolCommand) -> None:
        self._commands[cmd.tool_type()] = cmd

    def think(self, query: str) -> Thought:
        if any(c.isdigit() for c in query):
            return Thought("Numbers detected", ToolType.CALCULATOR, query)
        return Thought("Text query", ToolType.SEARCH, query)

    def act(self, thought: Thought) -> Observation:
        if thought.action_needed is None or thought.action_needed not in self._commands:
            return Observation("No tool available", ToolType.SEARCH, False)
        cmd = self._commands[thought.action_needed]
        return cmd.execute(thought.action_input)

    def run(self, query: str) -> Observation:
        thought = self.think(query)
        obs = self.act(thought)
        self.history.append((thought, obs))
        return obs
