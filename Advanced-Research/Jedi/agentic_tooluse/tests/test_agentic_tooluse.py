from agentic_tooluse.agent import ReActAgent
from agentic_tooluse.commands import CalculatorCommand, SearchCommand
from agentic_tooluse.models import ToolType


def test_search_command_returns_results() -> None:
    cmd = SearchCommand()
    obs = cmd.execute("python")
    assert obs.success
    assert "python" in obs.content


def test_calculator_command_evaluates() -> None:
    cmd = CalculatorCommand()
    obs = cmd.execute("2 + 3")
    assert obs.success
    assert obs.content == "5"


def test_calculator_handles_error() -> None:
    cmd = CalculatorCommand()
    obs = cmd.execute("undefined_var")
    assert not obs.success


def test_agent_routes_to_search() -> None:
    agent = ReActAgent()
    agent.register(SearchCommand())
    obs = agent.run("what is python")
    assert obs.tool_type == ToolType.SEARCH


def test_agent_routes_to_calculator() -> None:
    agent = ReActAgent()
    agent.register(CalculatorCommand())
    obs = agent.run("10 * 5")
    assert obs.tool_type == ToolType.CALCULATOR
    assert obs.content == "50"


def test_agent_maintains_history() -> None:
    agent = ReActAgent()
    agent.register(SearchCommand())
    agent.register(CalculatorCommand())
    agent.run("hello")
    agent.run("1+1")
    assert len(agent.history) == 2


def test_agent_returns_failure_without_tool() -> None:
    agent = ReActAgent()
    obs = agent.run("1+1")
    assert not obs.success


def test_tool_type_enum() -> None:
    cmd = SearchCommand()
    assert cmd.tool_type() == ToolType.SEARCH
    cmd2 = CalculatorCommand()
    assert cmd2.tool_type() == ToolType.CALCULATOR
