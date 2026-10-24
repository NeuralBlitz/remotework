import pytest

from llm_judge.evaluator import ConversationEvaluator
from llm_judge.models import ConversationNode, EvalScore, Role
from llm_judge.visitors import CoherenceVisitor, HallucinationVisitor, ToxicityVisitor


def test_hallucination_visitor():
    visitor = HallucinationVisitor()
    node = ConversationNode(role=Role.ASSISTANT, content="This is always correct")
    score = visitor.visit(node)
    assert score.score < 1.0
    assert score.metric == "hallucination"


def test_hallucination_clean():
    visitor = HallucinationVisitor()
    node = ConversationNode(role=Role.ASSISTANT, content="A reasonable response")
    score = visitor.visit(node)
    assert score.score == 1.0


def test_toxicity_visitor():
    visitor = ToxicityVisitor()
    node = ConversationNode(content="This is hate speech and stupid")
    score = visitor.visit(node)
    assert score.score < 1.0


def test_coherence_visitor():
    visitor = CoherenceVisitor()
    node = ConversationNode(content="A sufficiently long and detailed response here")
    score = visitor.visit(node)
    assert score.score >= 0.7


def test_coherence_short():
    visitor = CoherenceVisitor()
    node = ConversationNode(content="Hi")
    score = visitor.visit(node)
    assert score.score == 0.3


def test_evaluator_register():
    evaluator = ConversationEvaluator()
    evaluator.register(HallucinationVisitor()).register(ToxicityVisitor())
    assert len(evaluator.visitor_names()) == 2


def test_evaluator_evaluate_tree():
    root = ConversationNode(role=Role.USER, content="Hello")
    child = ConversationNode(role=Role.ASSISTANT, content="Hi there, always happy to help")
    root.add_child(child)
    evaluator = ConversationEvaluator()
    evaluator.register(HallucinationVisitor())
    scores = evaluator.evaluate(root)
    assert len(scores) == 2


def test_average_score():
    scores = [
        EvalScore(metric="hallucination", score=0.8),
        EvalScore(metric="hallucination", score=0.6),
    ]
    evaluator = ConversationEvaluator()
    assert evaluator.average_score(scores, "hallucination") == 0.7


def test_is_passing():
    score = EvalScore(score=0.7)
    assert score.is_passing(0.5)
    assert not score.is_passing(0.8)


def test_node_depth():
    root = ConversationNode(role=Role.USER)
    child1 = ConversationNode(role=Role.ASSISTANT)
    child2 = ConversationNode(role=Role.USER)
    root.add_child(child1)
    child1.add_child(child2)
    assert child2.depth() == 2
