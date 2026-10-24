from __future__ import annotations

from abc import ABC, abstractmethod

from .models import VideoClip


class EditCommand(ABC):
    @abstractmethod
    def execute(self, clips: list[VideoClip]) -> list[VideoClip]:
        raise NotImplementedError

    @abstractmethod
    def undo(self, clips: list[VideoClip]) -> list[VideoClip]:
        raise NotImplementedError


class CutCommand(EditCommand):
    def __init__(self, clip_id: str, start: float, end: float) -> None:
        self.clip_id = clip_id
        self.start = start
        self.end = end
        self._original_duration: float = 0.0

    def execute(self, clips: list[VideoClip]) -> list[VideoClip]:
        for clip in clips:
            if clip.clip_id == self.clip_id:
                self._original_duration = clip.duration
                clip.duration = self.end - self.start
                clip.start_time = self.start
        return clips

    def undo(self, clips: list[VideoClip]) -> list[VideoClip]:
        for clip in clips:
            if clip.clip_id == self.clip_id:
                clip.duration = self._original_duration
                clip.start_time = 0.0
        return clips


class MergeCommand(EditCommand):
    def __init__(self, clip_ids: list[str], new_id: str = "merged") -> None:
        self.clip_ids = clip_ids
        self.new_id = new_id
        self._removed: list[VideoClip] = []

    def execute(self, clips: list[VideoClip]) -> list[VideoClip]:
        merged = VideoClip(clip_id=self.new_id, duration=0.0)
        remaining: list[VideoClip] = []
        for clip in clips:
            if clip.clip_id in self.clip_ids:
                merged.duration += clip.duration
                self._removed.append(clip)
            else:
                remaining.append(clip)
        remaining.insert(0, merged)
        return remaining

    def undo(self, clips: list[VideoClip]) -> list[VideoClip]:
        return [c for c in clips if c.clip_id != self.new_id] + self._removed


class FilterCommand(EditCommand):
    def __init__(self, clip_id: str, filter_name: str = "blur") -> None:
        self.clip_id = clip_id
        self.filter_name = filter_name
        self._had_filter = False

    def execute(self, clips: list[VideoClip]) -> list[VideoClip]:
        for clip in clips:
            if clip.clip_id == self.clip_id:
                self._had_filter = self.filter_name in clip.filters
                if self.filter_name not in clip.filters:
                    clip.filters.append(self.filter_name)
        return clips

    def undo(self, clips: list[VideoClip]) -> list[VideoClip]:
        for clip in clips:
            if clip.clip_id == self.clip_id and not self._had_filter:
                clip.filters = [f for f in clip.filters if f != self.filter_name]
        return clips


class EditCommandInvoker:
    def __init__(self) -> None:
        self._history: list[EditCommand] = []

    def execute(self, command: EditCommand, clips: list[VideoClip]) -> list[VideoClip]:
        self._history.append(command)
        return command.execute(clips)

    def undo_last(self, clips: list[VideoClip]) -> list[VideoClip]:
        if self._history:
            return self._history.pop().undo(clips)
        return clips

