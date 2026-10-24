from __future__ import annotations

from agentic_healer.models import CodeArtifact, CodePhase
from agentic_healer.states import CodeState, CodeStateMachine


class CodeGenerator(CodeStateMachine):
    def __init__(self, specification: str = "hello") -> None:
        super().__init__()
        self.specification = specification
        self.artifact = CodeArtifact()
        self.done = False

    def set_state(self, state: CodeState) -> None:
        self.state = state

    def step(self) -> CodePhase:
        self.state.handle(self)
        return self.state.phase()

    def run(self, max_steps: int = 20) -> CodeArtifact:
        for _ in range(max_steps):
            if self.done:
                break
            self.step()
        return self.artifact

    def inject_error(self, error: str) -> None:
        self.artifact.errors.append(error)
