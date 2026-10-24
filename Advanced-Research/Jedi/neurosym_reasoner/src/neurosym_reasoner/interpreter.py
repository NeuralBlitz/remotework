from __future__ import annotations

from abc import ABC, abstractmethod

from neurosym_reasoner.models import Fact


class Expression(ABC):
    @abstractmethod
    def evaluate(self, facts: list[Fact]) -> list[Fact]: ...

    @abstractmethod
    def count(self) -> int: ...


class ConjunctionExpression(Expression):
    def __init__(self, *children: Expression) -> None:
        self._children = list(children)

    def evaluate(self, facts: list[Fact]) -> list[Fact]:
        seen: set[tuple[str, tuple[str, ...]]] = set()
        results: list[Fact] = []
        for child in self._children:
            for f in child.evaluate(facts):
                key = (f.predicate, tuple(f.arguments))
                if key not in seen:
                    seen.add(key)
                    results.append(f)
        return results

    def count(self) -> int:
        return 1 + sum(c.count() for c in self._children)


class DisjunctionExpression(Expression):
    def __init__(self, *children: Expression) -> None:
        self._children = list(children)

    def evaluate(self, facts: list[Fact]) -> list[Fact]:
        seen: set[tuple[str, tuple[str, ...]]] = set()
        results: list[Fact] = []
        for child in self._children:
            for f in child.evaluate(facts):
                key = (f.predicate, tuple(f.arguments))
                if key not in seen:
                    seen.add(key)
                    results.append(f)
        return results

    def count(self) -> int:
        return 1 + sum(c.count() for c in self._children)


class PredicateFilter(Expression):
    def __init__(self, predicate: str) -> None:
        self.predicate = predicate

    def evaluate(self, facts: list[Fact]) -> list[Fact]:
        return [f for f in facts if f.predicate == self.predicate]

    def count(self) -> int:
        return 1
