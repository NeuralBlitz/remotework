from __future__ import annotations

from neurosym_reasoner.models import Fact, Query, Rule


class RuleEngine:
    def __init__(self) -> None:
        self.facts: list[Fact] = []
        self.rules: list[Rule] = []

    def add_fact(self, fact: Fact) -> None:
        self.facts.append(fact)

    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)

    def query(self, query: Query, max_iterations: int = 10) -> Query:
        results: list[Fact] = []
        current_facts = list(self.facts)
        for _ in range(max_iterations):
            new_facts: list[Fact] = []
            for rule in self.rules:
                if rule.head.predicate != query.predicate:
                    continue
                if all(
                    any(
                        b.predicate == bf.predicate and b.arguments == bf.arguments
                        for bf in current_facts
                    )
                    for b in rule.body
                ):
                    min_conf = min(
                        bf.confidence
                        for b in rule.body
                        for bf in current_facts
                        if b.predicate == bf.predicate and b.arguments == bf.arguments
                    )
                    derived = Fact(rule.head.predicate, rule.head.arguments, min_conf)
                    if derived not in new_facts:
                        new_facts.append(derived)
            added = False
            for nf in new_facts:
                if nf not in current_facts:
                    current_facts.append(nf)
                    added = True
            if not added:
                break
        results = [f for f in current_facts if f.predicate == query.predicate]
        query.results = results
        return query

    def retract(self, fact: Fact) -> bool:
        if fact in self.facts:
            self.facts.remove(fact)
            return True
        return False
