from __future__ import annotations

from enum import Enum

from .models import Composition, Note


class CompositionState(Enum):
    DRAFT = "draft"
    COMPOSING = "composing"
    ARRANGING = "arranging"
    MIXING = "mixing"
    MASTERING = "mastering"
    COMPLETE = "complete"


class CompositionStateMachine:
    TRANSITIONS = {
        CompositionState.DRAFT: CompositionState.COMPOSING,
        CompositionState.COMPOSING: CompositionState.ARRANGING,
        CompositionState.ARRANGING: CompositionState.MIXING,
        CompositionState.MIXING: CompositionState.MASTERING,
        CompositionState.MASTERING: CompositionState.COMPLETE,
    }

    def __init__(self) -> None:
        self.state = CompositionState.DRAFT

    def advance(self) -> CompositionState:
        next_state = self.TRANSITIONS.get(self.state)
        if next_state:
            self.state = next_state
        return self.state

    def can_add_tracks(self) -> bool:
        return self.state in (CompositionState.DRAFT, CompositionState.COMPOSING)

    def process(self, composition: Composition) -> Composition:
        while self.state != CompositionState.COMPLETE:
            if self.state == CompositionState.COMPOSING:
                for track in composition.tracks:
                    if not track.notes:
                        track.notes = [
                            Note(pitch="C4", duration=1.0),
                            Note(pitch="E4", duration=1.0),
                        ]
            self.advance()
        composition.state = self.state.value
        return composition

