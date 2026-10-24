from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PlanType(Enum):
    SEQ_SCAN = "SeqScan"
    INDEX_SCAN = "IndexScan"
    HASH_JOIN = "HashJoin"
    MERGE_JOIN = "MergeJoin"
    NESTED_LOOP = "NestedLoop"
    SORT = "Sort"
    AGGREGATE = "Aggregate"
    LIMIT = "Limit"


@dataclass
class PlanNode:
    node_type: PlanType
    table: str = ""
    index_name: str = ""
    estimated_rows: int = 0
    actual_rows: int = 0
    cost: float = 0.0
    children: list[PlanNode] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> PlanNode:
        children_raw = data.get("children", [])
        children = (
            [cls.from_dict(c) for c in children_raw] if isinstance(children_raw, list) else []
        )
        raw_est = data.get("estimated_rows", 0)
        raw_act = data.get("actual_rows", 0)
        raw_cost = data.get("cost", 0.0)
        return cls(
            node_type=PlanType(data["node_type"]),
            table=str(data.get("table", "")),
            index_name=str(data.get("index_name", "")),
            estimated_rows=int(raw_est) if isinstance(raw_est, (int, float, str)) else 0,
            actual_rows=int(raw_act) if isinstance(raw_act, (int, float, str)) else 0,
            cost=float(raw_cost) if isinstance(raw_cost, (int, float, str)) else 0.0,
            children=children,
        )
        return cls(
            node_type=PlanType(data["node_type"]),
            table=str(data.get("table", "")),
            index_name=str(data.get("index_name", "")),
            estimated_rows=int(data.get("estimated_rows", 0)),
            actual_rows=int(data.get("actual_rows", 0)),
            cost=float(data.get("cost", 0.0)),
            children=children,
        )


@dataclass
class AuditReport:
    total_cost: float = 0.0
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)

    def add_suggestion(self, msg: str) -> None:
        self.suggestions.append(msg)

    @property
    def has_issues(self) -> bool:
        return len(self.warnings) > 0 or len(self.suggestions) > 0
