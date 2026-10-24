from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .models import Content, ModerationDecision


class ModerationStage(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"


@dataclass
class ModerationChain:
    stages: list[ModerationStage] = field(
        default_factory=lambda: [ModerationStage.TEXT, ModerationStage.IMAGE, ModerationStage.VIDEO]
    )

    def process(self, content: Content) -> ModerationDecision:
        violations: list[str] = []
        for stage in self.stages:
            if stage == ModerationStage.TEXT and content.text:
                if self._check_text(content.text):
                    violations.append("text_violation")
            elif stage == ModerationStage.IMAGE and content.image_url:
                if self._check_image(content.image_url):
                    violations.append("image_violation")
            elif stage == ModerationStage.VIDEO and content.video_url:
                if self._check_video(content.video_url):
                    violations.append("video_violation")
        approved = len(violations) == 0
        return ModerationDecision(
            content_id=content.content_id, approved=approved, violations=violations
        )

    def _check_text(self, text: str) -> bool:
        blocked = {"spam", "abuse", "harmful"}
        return any(word in text.lower() for word in blocked)

    def _check_image(self, url: str) -> bool:
        return "nsfw" in url.lower()

    def _check_video(self, url: str) -> bool:
        return "explicit" in url.lower()

