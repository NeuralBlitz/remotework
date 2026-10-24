from __future__ import annotations

from abc import ABC, abstractmethod

from lnn_solver.models import ODEConfig, Trajectory


class SolverStrategy(ABC):
    @abstractmethod
    def solve(self, config: ODEConfig) -> Trajectory: ...

    @abstractmethod
    def name(self) -> str: ...


class Dopri5Strategy(SolverStrategy):
    def solve(self, config: ODEConfig) -> Trajectory:
        if not config.validate():
            raise ValueError("Invalid ODE config")
        times: list[float] = []
        states: list[list[float]] = []
        t = 0.0
        state = list(config.initial_state)
        while t <= config.t_max:
            times.append(t)
            states.append(list(state))
            for i in range(len(state)):
                state[i] = state[i] + config.dt * (-state[i] / config.tau)
            t += config.dt
        return Trajectory(times=times, states=states)

    def name(self) -> str:
        return "dopri5"


class EulerStrategy(SolverStrategy):
    def solve(self, config: ODEConfig) -> Trajectory:
        if not config.validate():
            raise ValueError("Invalid ODE config")
        times: list[float] = []
        states: list[list[float]] = []
        t = 0.0
        state = list(config.initial_state)
        while t <= config.t_max:
            times.append(t)
            states.append(list(state))
            for i in range(len(state)):
                state[i] = state[i] - config.dt * state[i] / config.tau
            t += config.dt
        return Trajectory(times=times, states=states)

    def name(self) -> str:
        return "euler"


class RungeKuttaStrategy(SolverStrategy):
    def solve(self, config: ODEConfig) -> Trajectory:
        if not config.validate():
            raise ValueError("Invalid ODE config")
        times: list[float] = []
        states: list[list[float]] = []
        t = 0.0
        state = list(config.initial_state)
        while t <= config.t_max:
            times.append(t)
            states.append(list(state))
            k1 = [-s / config.tau for s in state]
            k2 = [-(s + config.dt / 2 * k1[i]) / config.tau for i, s in enumerate(state)]
            k3 = [-(s + config.dt / 2 * k2[i]) / config.tau for i, s in enumerate(state)]
            k4 = [-(s + config.dt * k3[i]) / config.tau for i, s in enumerate(state)]
            for i in range(len(state)):
                state[i] += config.dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
            t += config.dt
        return Trajectory(times=times, states=states)

    def name(self) -> str:
        return "runge_kutta"
