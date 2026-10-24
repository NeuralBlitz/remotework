import pytest

from lnn_solver.models import ODEConfig, Trajectory
from lnn_solver.solver import LNNSolver
from lnn_solver.strategies import Dopri5Strategy, EulerStrategy, RungeKuttaStrategy


def test_dopri5_solve():
    config = ODEConfig(dt=0.1, t_max=0.5, tau=1.0, initial_state=[1.0])
    solver = LNNSolver(Dopri5Strategy())
    traj = solver.solve(config)
    assert traj.length() > 0
    assert traj.states[0] == [1.0]


def test_euler_solve():
    config = ODEConfig(dt=0.1, t_max=0.5, tau=1.0, initial_state=[1.0])
    solver = LNNSolver(EulerStrategy())
    traj = solver.solve(config)
    assert traj.length() > 0
    assert solver.current_method() == "euler"


def test_rk4_solve():
    config = ODEConfig(dt=0.1, t_max=0.3, tau=1.0, initial_state=[2.0])
    solver = LNNSolver(RungeKuttaStrategy())
    traj = solver.solve(config)
    assert solver.current_method() == "runge_kutta"
    assert traj.final_state()[0] < 2.0


def test_strategy_switch():
    solver = LNNSolver()
    assert solver.current_method() == "dopri5"
    solver.set_strategy(EulerStrategy())
    assert solver.current_method() == "euler"


def test_compare_strategies():
    config = ODEConfig(dt=0.1, t_max=0.5, tau=1.0, initial_state=[1.0])
    solver = LNNSolver()
    results = solver.compare(config, [Dopri5Strategy(), EulerStrategy(), RungeKuttaStrategy()])
    assert len(results) == 3
    assert "dopri5" in results
    assert "euler" in results
    assert "runge_kutta" in results


def test_invalid_config():
    config = ODEConfig(dt=-1, t_max=0.5, tau=1.0, initial_state=[1.0])
    solver = LNNSolver(Dopri5Strategy())
    with pytest.raises(ValueError, match="Invalid"):
        solver.solve(config)


def test_trajectory_state_at():
    traj = Trajectory(
        times=[0.0, 0.1, 0.2],
        states=[[1.0], [0.9], [0.8]],
    )
    assert traj.state_at(0.1) == [0.9]
    assert traj.state_at(0.5) == [0.8]


def test_multi_dim_state():
    config = ODEConfig(dt=0.1, t_max=0.3, tau=2.0, initial_state=[1.0, 2.0])
    solver = LNNSolver(RungeKuttaStrategy())
    traj = solver.solve(config)
    assert len(traj.final_state()) == 2


def test_decay_behavior():
    config = ODEConfig(dt=0.01, t_max=1.0, tau=1.0, initial_state=[1.0])
    solver = LNNSolver(Dopri5Strategy())
    traj = solver.solve(config)
    assert traj.final_state()[0] < 0.5


def test_default_solver():
    solver = LNNSolver()
    assert solver.current_method() == "dopri5"
