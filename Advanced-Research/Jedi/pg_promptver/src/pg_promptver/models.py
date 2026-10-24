from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class PromptTemplate:
    name: str
    system_prompt: str
    user_template: str
    variables: list[str] = field(default_factory=list)
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1024

    def render(self, **kwargs: Any) -> str:
        result = self.user_template
        for var in self.variables:
            if var in kwargs:
                result = result.replace(f"{{{var}}}", str(kwargs[var]))
        return result


@dataclass(frozen=True)
class PromptVersion:
    version_id: str
    template: PromptTemplate
    created_at: datetime
    message: str = ""
    tags: tuple[str, ...] = ()
