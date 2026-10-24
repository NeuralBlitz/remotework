from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable


class LossDecorator(ABC):
    def __init__(self, base_loss: Callable[..., float]) -> None:
        self.base_loss = base_loss

    @abstractmethod
    def __call__(self, *args: float, **kwargs: float) -> float: ...


class PhysicsResidualDecorator(LossDecorator):
    def __init__(self, base_loss: Callable[..., float], weight: float = 1.0) -> None:
        super().__init__(base_loss)
        self.weight = weight

    def __call__(self, *args: float, **kwargs: float) -> float:
        base = self.base_loss(*args, **kwargs)
        residual = self._compute_residual(*args, **kwargs)
        return base + self.weight * residual

    def _compute_residual(self, *args: float, **kwargs: float) -> float:
        if len(args) < 2:
            return 0.0
        u, u_xx = args[0], args[1]
        return (u_xx + u) ** 2


class NavierStokesResidual(LossDecorator):
    def __init__(
        self,
        base_loss: Callable[..., float],
        viscosity: float = 0.01,
        weight: float = 1.0,
    ) -> None:
        super().__init__(base_loss)
        self.viscosity = viscosity
        self.weight = weight

    def __call__(self, *args: float, **kwargs: float) -> float:
        base = self.base_loss(*args, **kwargs)
        residual = self._compute_residual(*args, **kwargs)
        return base + self.weight * residual

    def _compute_residual(self, *args: float, **kwargs: float) -> float:
        if len(args) < 4:
            return 0.0
        u, u_t, u_x, u_xx = args[:4]
        convective = u * u_x
        diffusive = self.viscosity * u_xx
        return (u_t + convective - diffusive) ** 2
