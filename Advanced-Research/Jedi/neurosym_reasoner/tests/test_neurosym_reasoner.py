from neurosym_reasoner.interpreter import (
    ConjunctionExpression,
    DisjunctionExpression,
    PredicateFilter,
)
from neurosym_reasoner.models import Fact, Query, Rule
from neurosym_reasoner.rules import RuleEngine


def test_predicate_filter() -> None:
    facts = [Fact("cat", ["fluffy"]), Fact("dog", ["rex"])]
    expr = PredicateFilter("cat")
    assert expr.evaluate(facts) == [Fact("cat", ["fluffy"])]


def test_conjunction_filters_sequentially() -> None:
    facts = [Fact("mammal", ["fluffy"]), Fact("mammal", ["rex"])]
    expr = ConjunctionExpression(PredicateFilter("mammal"))
    result = expr.evaluate(facts)
    assert len(result) == 2


def test_disjunction_unions_results() -> None:
    facts = [Fact("cat", ["fluffy"]), Fact("dog", ["rex"])]
    expr = DisjunctionExpression(PredicateFilter("cat"), PredicateFilter("dog"))
    result = expr.evaluate(facts)
    assert len(result) == 2


def test_disjunction_deduplicates() -> None:
    facts = [Fact("x", ["a"]), Fact("x", ["a"])]
    expr = DisjunctionExpression(PredicateFilter("x"), PredicateFilter("x"))
    result = expr.evaluate(facts)
    assert len(result) == 1


def test_expression_count() -> None:
    expr = ConjunctionExpression(PredicateFilter("a"), PredicateFilter("b"))
    assert expr.count() == 3


def test_rule_engine_add_and_query() -> None:
    engine = RuleEngine()
    engine.add_fact(Fact("parent", ["alice", "bob"]))
    engine.add_fact(Fact("parent", ["bob", "carol"]))
    engine.add_rule(
        Rule(
            "grandparent",
            Fact("grandparent", ["alice", "carol"]),
            [Fact("parent", ["alice", "bob"]), Fact("parent", ["bob", "carol"])],
        )
    )
    q = engine.query(Query("grandparent", ["alice", "carol"]))
    assert len(q.results) == 1


def test_rule_engine_retract() -> None:
    engine = RuleEngine()
    f = Fact("sunny", [])
    engine.add_fact(f)
    assert len(engine.facts) == 1
    assert engine.retract(f)
    assert len(engine.facts) == 0


def test_rule_engine_query_no_match() -> None:
    engine = RuleEngine()
    q = engine.query(Query("missing", []))
    assert len(q.results) == 0


def test_nested_interpreter() -> None:
    facts = [Fact("a", ["1"]), Fact("b", ["2"]), Fact("c", ["3"])]
    expr = DisjunctionExpression(
        ConjunctionExpression(PredicateFilter("a"), PredicateFilter("b")),
        PredicateFilter("c"),
    )
    result = expr.evaluate(facts)
    assert len(result) == 3


def test_conjunction_empty_if_child_empty() -> None:
    facts = [Fact("a", ["1"])]
    expr = ConjunctionExpression(PredicateFilter("a"), PredicateFilter("z"))
    result = expr.evaluate(facts)
    assert len(result) == 1
    assert result[0].predicate == "a"
