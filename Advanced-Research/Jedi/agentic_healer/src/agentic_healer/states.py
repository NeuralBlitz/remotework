from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from agentic_healer.models import CodeArtifact, CodePhase

if TYPE_CHECKING:
    from agentic_healer.generator import CodeGenerator


class CodeState(ABC):
    @abstractmethod
    def phase(self) -> CodePhase: ...

    @abstractmethod
    def handle(self, ctx: CodeGenerator) -> None: ...


class DraftingState(CodeState):
    def phase(self) -> CodePhase:
        return CodePhase.DRAFTING

    def handle(self, ctx: CodeGenerator) -> None:
        ctx.artifact.source = f"def {ctx.specification}():\n    pass\n"
        ctx.artifact.tests = f"def test_{ctx.specification}():\n    assert True\n"
        ctx.set_state(TestingState())


class TestingState(CodeState):
    def phase(self) -> CodePhase:
        return CodePhase.TESTING

    def handle(self, ctx: CodeGenerator) -> None:
        if ctx.artifact.errors:
            ctx.set_state(RefactoringState())
        else:
            ctx.set_state(FinalizingState())


class RefactoringState(CodeState):
    def phase(self) -> CodePhase:
        return CodePhase.REFACTORING

    def handle(self, ctx: CodeGenerator) -> None:
        ctx.artifact.errors.clear()
        ctx.artifact.refactors_applied += 1
        ctx.set_state(TestingState())


class FinalizingState(CodeState):
    def phase(self) -> CodePhase:
        return CodePhase.FINALIZING

    def handle(self, ctx: CodeGenerator) -> None:
        ctx.done = True


class CodeStateMachine:
    def __init__(self) -> None:
        self.state: CodeState = DraftingState()

    def set_state(self, state: CodeState) -> None:
        self.state = state
