from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Content:
    content_id: str
    text: str = ""
    image_url: str = ""
    video_url: str = ""
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class ModerationDecision:
    content_id: str
    approved: bool
    violations: list[str] = field(default_factory=list)
    score: float = 0.0

