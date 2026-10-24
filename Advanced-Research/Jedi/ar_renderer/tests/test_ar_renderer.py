from __future__ import annotations

from ar_renderer.models import RenderedFrame, Scene
from ar_renderer.pipeline import ARPipeline, Compositor, RenderEngine, SceneParser


def _make_scene() -> Scene:
    return Scene(scene_id="s1", objects=["cube", "sphere"], lights=["sun"], width=800, height=600)


def test_scene_parser() -> None:
    stats = SceneParser().parse(_make_scene())
    assert stats["objects"] == 2
    assert stats["lights"] == 1


def test_render_engine() -> None:
    engine = RenderEngine()
    frame = engine.render(_make_scene(), {"objects": 2, "lights": 1})
    assert frame.pixel_count == 480000


def test_compositor() -> None:
    frame = RenderedFrame(frame_id="f1", render_time_ms=10)
    overlay = RenderedFrame(frame_id="f2", render_time_ms=5)
    result = Compositor().composite(frame, overlay)
    assert result.render_time_ms == 15


def test_pipeline() -> None:
    pipeline = ARPipeline()
    frame = pipeline.run(_make_scene())
    assert frame.frame_id == "s1_rendered"
    assert frame.render_time_ms > 0


def test_no_overlay() -> None:
    frame = RenderedFrame(frame_id="f1", render_time_ms=10)
    result = Compositor().composite(frame)
    assert result.frame_id == "f1"

