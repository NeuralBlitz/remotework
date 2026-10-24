from pinn_solver.decorators import NavierStokesResidual, PhysicsResidualDecorator
from pinn_solver.models import BoundaryCondition, BoundaryType, PDEConfig
from pinn_solver.solver import PINNSolver


def base_loss(*args: float, **kwargs: float) -> float:
    return 0.5


def test_pde_config_domain_size() -> None:
    cfg = PDEConfig("heat", domain=(0.0, 2.0))
    assert cfg.domain_size == 2.0


def test_boundary_condition_defaults() -> None:
    bc = BoundaryCondition(BoundaryType.DIRICHLET)
    assert bc.value == 0.0
    assert bc.location == "x=0"


def test_physics_residual_adds_term() -> None:
    decorated = PhysicsResidualDecorator(base_loss, weight=1.0)
    result = decorated(1.0, 0.5)
    assert result > 0.5


def test_physics_residual_weight_zero() -> None:
    decorated = PhysicsResidualDecorator(base_loss, weight=0.0)
    assert decorated(1.0, 0.5) == 0.5


def test_navier_stokes_residual() -> None:
    decorated = NavierStokesResidual(base_loss, viscosity=0.01, weight=2.0)
    result = decorated(1.0, 0.5, 0.3, 0.1)
    assert result > 0.5


def test_solver_train_step() -> None:
    solver = PINNSolver(PDEConfig("test"))
    solver.set_loss(base_loss)
    loss = solver.train_step()
    assert loss == 0.5
    assert len(solver.history) == 1


def test_solver_train_multiple_steps() -> None:
    solver = PINNSolver(PDEConfig("test"))
    solver.set_loss(base_loss)
    history = solver.train(10)
    assert len(history) == 10


def test_solver_reset() -> None:
    solver = PINNSolver(PDEConfig("test"))
    solver.set_loss(base_loss)
    solver.train(5)
    solver.reset()
    assert len(solver.history) == 0


def test_solver_raises_without_loss() -> None:
    solver = PINNSolver(PDEConfig("test"))
    try:
        solver.train_step()
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_pde_config_params() -> None:
    cfg = PDEConfig("navier_stokes", params={"nu": 0.01, "rho": 1.0})
    assert cfg.params["nu"] == 0.01
