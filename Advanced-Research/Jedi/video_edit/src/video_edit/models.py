from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class VideoClip:
    clip_id: str
    duration: float = 0.0
    start_time: float = 0.0
    filters: list[str] = field(default_factory=list)
    path: str = ""


@dataclass
class EditAction:
    action_type: str = ""
    clip_id: str = ""
    parameters: dict[str, str] = field(default_factory=dict)

