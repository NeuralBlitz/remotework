import pytest

from causal_inference.estimators import IVEstimator, PropensityScoreEstimator
from causal_inference.facade import CausalFacade
from causal_inference.models import CausalGraph, Outcome, Treatment


def test_causal_graph_add_edge() -> None:
    g = CausalGraph()
    g.add_edge("X", "Y")
    assert "X" in g.nodes
    assert "Y" in g.nodes
    assert ("X", "Y") in g.edges


def test_causal_graph_parents() -> None:
    g = CausalGraph(nodes=["A", "B", "C"], edges=[("A", "C"), ("B", "C")])
    assert sorted(g.parents("C")) == ["A", "B"]


def test_causal_graph_children() -> None:
    g = CausalGraph(nodes=["A", "B"], edges=[("A", "B")])
    assert g.children("A") == ["B"]


def test_facade_identify() -> None:
    g = CausalGraph(nodes=["drug", "recovery"], edges=[("drug", "recovery")])
    facade = CausalFacade(g)
    t = Treatment("drug")
    o = Outcome("recovery")
    assert facade.identify(t, o)


def test_propensity_score_estimates_ate() -> None:
    g = CausalGraph()
    est = PropensityScoreEstimator()
    t = Treatment("t", [0, 1])
    o = Outcome("y", [1.0, 2.0, 3.0, 4.0])
    ate = est.estimate(g, t, o)
    assert ate == pytest.approx(-2.0)


def test_iv_estimator() -> None:
    g = CausalGraph()
    est = IVEstimator("z")
    t = Treatment("x", [1.0, 2.0, 3.0])
    o = Outcome("y", [2.0, 4.0, 6.0])
    ate = est.estimate(g, t, o)
    assert ate > 0


def test_facade_run_returns_result() -> None:
    g = CausalGraph(nodes=["drug", "outcome"], edges=[("drug", "outcome")])
    facade = CausalFacade(g)
    t = Treatment("drug")
    o = Outcome("outcome", [1.0, 2.0, 3.0, 4.0])
    result = facade.run(t, o)
    assert result.refuted
    assert result.estimator_used == "PropensityScoreEstimator"


def test_facade_unidentified_returns_zero() -> None:
    g = CausalGraph(nodes=["X"])
    facade = CausalFacade(g)
    t = Treatment("missing")
    o = Outcome("outcome")
    result = facade.run(t, o)
    assert result.ate == 0.0


def test_empty_outcome_gives_zero() -> None:
    g = CausalGraph()
    est = PropensityScoreEstimator()
    ate = est.estimate(g, Treatment("x"), Outcome("y"))
    assert ate == 0.0
