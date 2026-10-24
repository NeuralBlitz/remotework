from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Scene:
    scene_id: str
    objects: list[str] = field(default_factory=list)
    lights: list[str] = field(default_factory=list)
    width: int = 1920
    height: int = 1080


@dataclass
class RenderedFrame:
    frame_id: str
    width: int = 0
    height: int = 0
    pixel_count: int = 0
    render_time_ms: int = 0

