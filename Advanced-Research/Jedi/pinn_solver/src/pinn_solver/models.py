from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class BoundaryType(Enum):
    DIRICHLET = auto()
    NEUMANN = auto()
    PERIODIC = auto()


@dataclass
class BoundaryCondition:
    boundary_type: BoundaryType
    value: float = 0.0
    location: str = "x=0"


@dataclass
class PDEConfig:
    pde_name: str
    domain: tuple[float, float] = (0.0, 1.0)
    num_collocation: int = 100
    boundaries: list[BoundaryCondition] = field(default_factory=list)
    params: dict[str, float] = field(default_factory=dict)

    @property
    def domain_size(self) -> float:
        return self.domain[1] - self.domain[0]
