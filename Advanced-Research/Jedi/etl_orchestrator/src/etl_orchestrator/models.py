from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    id: str
    operation: str
    config: dict[str, str]

@dataclass
class Pipeline:
    tasks: list[Task] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "tasks": [
                {
                    "id": t.id,
                    "operation": t.operation,
                    "config": t.config,
                }
                for t in self.tasks
            ]
        }
