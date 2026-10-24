from __future__ import annotations

from video_edit.commands import CutCommand, EditCommandInvoker, FilterCommand, MergeCommand
from video_edit.models import VideoClip


def _make_clips() -> list[VideoClip]:
    return [
        VideoClip(clip_id="c1", duration=10.0),
        VideoClip(clip_id="c2", duration=20.0),
    ]


def test_cut_command() -> None:
    clips = _make_clips()
    cmd = CutCommand(clip_id="c1", start=2.0, end=8.0)
    result = cmd.execute(clips)
    assert result[0].duration == 6.0


def test_merge_command() -> None:
    clips = _make_clips()
    cmd = MergeCommand(clip_ids=["c1", "c2"])
    result = cmd.execute(clips)
    assert len(result) == 1
    assert result[0].duration == 30.0


def test_filter_command() -> None:
    clips = _make_clips()
    cmd = FilterCommand(clip_id="c1", filter_name="sepia")
    result = cmd.execute(clips)
    assert "sepia" in result[0].filters


def test_undo_cut() -> None:
    clips = _make_clips()
    cmd = CutCommand(clip_id="c1", start=2.0, end=8.0)
    cmd.execute(clips)
    cmd.undo(clips)
    assert clips[0].duration == 10.0


def test_invoker_undo() -> None:
    invoker = EditCommandInvoker()
    clips = _make_clips()
    invoker.execute(CutCommand(clip_id="c1", start=0.0, end=5.0), clips)
    invoker.undo_last(clips)
    assert clips[0].duration == 10.0

