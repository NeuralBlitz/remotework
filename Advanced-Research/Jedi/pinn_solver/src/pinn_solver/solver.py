from __future__ import annotations

from typing import Callable

from pinn_solver.models import PDEConfig


class PINNSolver:
    def __init__(self, config: PDEConfig) -> None:
        self.config = config
        self._loss_fn: Callable[..., float] | None = None
        self._history: list[float] = []

    def set_loss(self, loss_fn: Callable[..., float]) -> None:
        self._loss_fn = loss_fn

    def train_step(self, *args: float, **kwargs: float) -> float:
        if self._loss_fn is None:
            raise ValueError("No loss function set")
        loss = self._loss_fn(*args, **kwargs)
        self._history.append(loss)
        return loss

    def train(self, steps: int, *args: float, **kwargs: float) -> list[float]:
        for _ in range(steps):
            self.train_step(*args, **kwargs)
        return self._history

    @property
    def history(self) -> list[float]:
        return list(self._history)

    def reset(self) -> None:
        self._history.clear()
