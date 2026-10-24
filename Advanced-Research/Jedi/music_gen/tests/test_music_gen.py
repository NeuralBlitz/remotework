from __future__ import annotations

from music_gen.models import Composition, Track
from music_gen.states import CompositionState, CompositionStateMachine


def test_state_transitions() -> None:
    sm = CompositionStateMachine()
    assert sm.state == CompositionState.DRAFT
    sm.advance()
    assert sm.state == CompositionState.COMPOSING
    sm.advance()
    assert sm.state == CompositionState.ARRANGING


def test_can_add_tracks() -> None:
    sm = CompositionStateMachine()
    assert sm.can_add_tracks()
    sm.advance()
    assert sm.can_add_tracks()
    sm.advance()
    assert not sm.can_add_tracks()


def test_process_composition() -> None:
    sm = CompositionStateMachine()
    comp = Composition(composition_id="c1", tracks=[Track(track_id="t1")])
    result = sm.process(comp)
    assert result.state == "complete"
    assert len(result.tracks[0].notes) > 0


def test_full_lifecycle() -> None:
    sm = CompositionStateMachine()
    states = []
    while sm.state != CompositionState.COMPLETE:
        sm.advance()
        states.append(sm.state)
    assert len(states) == 5


def test_complete_state_stays() -> None:
    sm = CompositionStateMachine()
    while sm.state != CompositionState.COMPLETE:
        sm.advance()
    sm.advance()
    assert sm.state == CompositionState.COMPLETE
