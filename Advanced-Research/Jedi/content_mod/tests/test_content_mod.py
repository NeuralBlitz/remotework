from __future__ import annotations

from content_mod.chain import ModerationChain, ModerationStage
from content_mod.models import Content


def test_clean_content() -> None:
    chain = ModerationChain()
    content = Content(content_id="1", text="Hello world")
    decision = chain.process(content)
    assert decision.approved
    assert decision.violations == []


def test_text_violation() -> None:
    chain = ModerationChain()
    content = Content(content_id="2", text="This is spam content")
    decision = chain.process(content)
    assert not decision.approved
    assert "text_violation" in decision.violations


def test_image_violation() -> None:
    chain = ModerationChain()
    content = Content(content_id="3", image_url="http://example.com/nsfw.jpg")
    decision = chain.process(content)
    assert not decision.approved
    assert "image_violation" in decision.violations


def test_video_violation() -> None:
    chain = ModerationChain()
    content = Content(content_id="4", video_url="http://example.com/explicit.mp4")
    decision = chain.process(content)
    assert not decision.approved
    assert "video_violation" in decision.violations


def test_multiple_violations() -> None:
    chain = ModerationChain()
    content = Content(content_id="5", text="spam", image_url="nsfw.jpg")
    decision = chain.process(content)
    assert not decision.approved
    assert len(decision.violations) == 2


def test_custom_stages() -> None:
    chain = ModerationChain(stages=[ModerationStage.TEXT])
    content = Content(content_id="6", text="spam", image_url="nsfw.jpg")
    decision = chain.process(content)
    assert len(decision.violations) == 1

