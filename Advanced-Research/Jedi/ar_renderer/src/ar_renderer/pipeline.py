from __future__ import annotations

from .models import RenderedFrame, Scene


class SceneParser:
    def parse(self, scene: Scene) -> dict[str, int]:
        return {
            "objects": len(scene.objects),
            "lights": len(scene.lights),
            "cameras": 1,
        }


class RenderEngine:
    def render(self, scene: Scene, stats: dict[str, int]) -> RenderedFrame:
        object_count = stats.get("objects", 0)
        light_count = stats.get("lights", 0)
        render_time_ms = object_count * 10 + light_count * 5
        pixel_count = scene.width * scene.height
        return RenderedFrame(
            frame_id=f"{scene.scene_id}_rendered",
            width=scene.width,
            height=scene.height,
            pixel_count=pixel_count,
            render_time_ms=render_time_ms,
        )


class Compositor:
    def composite(
        self, frame: RenderedFrame, overlay: RenderedFrame | None = None
    ) -> RenderedFrame:
        if overlay is None:
            return frame
        return RenderedFrame(
            frame_id=f"{frame.frame_id}_composited",
            width=frame.width,
            height=frame.height,
            pixel_count=frame.pixel_count,
            render_time_ms=frame.render_time_ms + overlay.render_time_ms,
        )


class ARPipeline:
    def __init__(self) -> None:
        self.parser = SceneParser()
        self.renderer = RenderEngine()
        self.compositor = Compositor()

    def run(self, scene: Scene) -> RenderedFrame:
        stats = self.parser.parse(scene)
        frame = self.renderer.render(scene, stats)
        return self.compositor.composite(frame)
