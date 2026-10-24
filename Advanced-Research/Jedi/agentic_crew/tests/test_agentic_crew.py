from agentic_crew.composite import AgentSwarm, ManagerAgent, WorkerAgent
from agentic_crew.models import AgentRole, Task, TaskResult


def test_worker_executes_task() -> None:
    w = WorkerAgent("w1", "coding")
    t = Task("build feature", priority=2)
    result = w.execute(t)
    assert result.success
    assert result.agent_name == "w1"
    assert t.completed


def test_worker_count_is_one() -> None:
    w = WorkerAgent("w1")
    assert w.count() == 1


def test_manager_aggregates_results() -> None:
    m = ManagerAgent("mgr")
    m.add(WorkerAgent("w1"))
    m.add(WorkerAgent("w2"))
    t = Task("process data")
    result = m.execute(t)
    assert result.success
    assert len(result.sub_results) == 2
    assert t.completed


def test_manager_count_includes_children() -> None:
    m = ManagerAgent("mgr")
    m.add(WorkerAgent("w1"))
    m.add(WorkerAgent("w2"))
    assert m.count() == 3


def test_swarm_runs_entire_hierarchy() -> None:
    exec_node = ManagerAgent("exec", AgentRole.EXECUTIVE)
    mgr1 = ManagerAgent("mgr1")
    mgr1.add(WorkerAgent("w1"))
    mgr1.add(WorkerAgent("w2"))
    mgr2 = ManagerAgent("mgr2")
    mgr2.add(WorkerAgent("w3"))
    exec_node.add(mgr1)
    exec_node.add(mgr2)
    swarm = AgentSwarm(exec_node)
    t = Task("full pipeline")
    result = swarm.run(t)
    assert result.success
    assert swarm.agent_count() == 6


def test_remove_child() -> None:
    m = ManagerAgent("mgr")
    w = WorkerAgent("w1")
    m.add(w)
    assert len(m.children) == 1
    m.remove(w)
    assert len(m.children) == 0


def test_manager_children_property_returns_copy() -> None:
    m = ManagerAgent("mgr")
    m.add(WorkerAgent("w1"))
    children = m.children
    children.append(WorkerAgent("w2"))
    assert len(m.children) == 1
