from __future__ import annotations

from llm_judge.models import ConversationNode, EvalScore
from llm_judge.visitors import Visitor


class ConversationEvaluator:
    def __init__(self) -> None:
        self._visitors: list[Visitor] = []

    def register(self, visitor: Visitor) -> ConversationEvaluator:
        self._visitors.append(visitor)
        return self

    def evaluate(self, root: ConversationNode) -> list[EvalScore]:
        scores: list[EvalScore] = []
        nodes = self._collect_nodes(root)
        for node in nodes:
            for visitor in self._visitors:
                score = visitor.visit(node)
                scores.append(score)
        return scores

    def evaluate_single(self, node: ConversationNode) -> list[EvalScore]:
        return [v.visit(node) for v in self._visitors]

    def average_score(self, scores: list[EvalScore], metric: str) -> float:
        filtered = [s for s in scores if s.metric == metric]
        if not filtered:
            return 0.0
        return sum(s.score for s in filtered) / len(filtered)

    def _collect_nodes(self, root: ConversationNode) -> list[ConversationNode]:
        result = [root]
        for child in root.children:
            result.extend(self._collect_nodes(child))
        return result

    def visitor_names(self) -> list[str]:
        return [v.name() for v in self._visitors]
