from agentic_healer.generator import CodeGenerator
from agentic_healer.models import CodePhase
from agentic_healer.states import DraftingState, RefactoringState, TestingState


def test_initial_state_is_drafting() -> None:
    gen = CodeGenerator()
    assert gen.state.phase() == CodePhase.DRAFTING


def test_step_advances_from_drafting_to_testing() -> None:
    gen = CodeGenerator()
    gen.step()
    assert gen.state.phase() == CodePhase.TESTING


def test_generator_produces_code() -> None:
    gen = CodeGenerator("greet")
    gen.run()
    assert "def greet" in gen.artifact.source
    assert gen.done


def test_error_triggers_refactoring() -> None:
    gen = CodeGenerator()
    gen.step()  # drafting -> testing
    gen.inject_error("syntax error")
    gen.step()  # testing -> refactoring
    assert gen.state.phase() == CodePhase.REFACTORING


def test_refactoring_clears_errors() -> None:
    gen = CodeGenerator()
    gen.step()
    gen.inject_error("bug")
    gen.step()  # to refactoring
    gen.step()  # refactoring -> testing
    assert len(gen.artifact.errors) == 0
    assert gen.artifact.refactors_applied == 1


def test_run_with_errors_converges() -> None:
    gen = CodeGenerator("my_func")
    gen.inject_error("initial bug")
    gen.run()
    assert gen.done
    assert gen.artifact.refactors_applied >= 1


def test_phase_enum_values() -> None:
    assert CodePhase.DRAFTING.value < CodePhase.TESTING.value
    assert CodePhase.TESTING.value < CodePhase.FINALIZING.value


def test_code_artifact_is_valid() -> None:
    gen = CodeGenerator("calc")
    gen.run()
    assert gen.artifact.is_valid
