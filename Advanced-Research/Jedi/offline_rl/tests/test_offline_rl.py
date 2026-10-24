import pytest

from offline_rl.buffer import ReplayBuffer
from offline_rl.models import Trajectory, Transition
from offline_rl.prototype import HindsightPrototype, TrajectoryPrototype


def _make_trajectory(n: int = 5) -> Trajectory:
    transitions = [
        Transition(state=[float(i)], action=[1.0], reward=float(i), next_state=[float(i + 1)])
        for i in range(n)
    ]
    return Trajectory(transitions=transitions, episode_id="ep1", total_reward=sum(range(n)))


def test_clone_trajectory():
    traj = _make_trajectory()
    proto = TrajectoryPrototype(traj)
    cloned = proto.clone("ep2")
    assert cloned.episode_id == "ep2"
    assert cloned.length() == traj.length()


def test_mutate_rewards():
    traj = _make_trajectory()
    proto = TrajectoryPrototype(traj)
    mutated = proto.mutate_rewards(2.0, 1.0)
    assert mutated.transitions[0].reward == 1.0


def test_truncate():
    traj = _make_trajectory(10)
    proto = TrajectoryPrototype(traj)
    truncated = proto.truncate(3)
    assert truncated.length() == 3
    assert truncated.last().done is True


def test_hindsight_relabel():
    traj = _make_trajectory()
    proto = HindsightPrototype(traj)
    relabeled = proto.relabel_goals([100.0])
    assert relabeled.transitions[0].next_state == [100.0]


def test_hindsight_reward_relabel():
    traj = _make_trajectory()
    proto = HindsightPrototype(traj)
    relabeled = proto.relabel_rewards([5.0], threshold=10.0)
    assert all(t.reward == 1.0 for t in relabeled.transitions)


def test_buffer_add():
    buf = ReplayBuffer(capacity=100)
    buf.add_trajectory(_make_trajectory())
    assert buf.trajectory_count() == 1


def test_buffer_sample():
    buf = ReplayBuffer()
    for i in range(5):
        buf.add_trajectory(_make_trajectory())
    samples = buf.sample_trajectories(3)
    assert len(samples) == 3


def test_buffer_from_prototype():
    buf = ReplayBuffer()
    proto = TrajectoryPrototype(_make_trajectory())
    buf.add_from_prototype(proto, scale=2.0)
    assert buf.trajectory_count() == 1


def test_buffer_clear():
    buf = ReplayBuffer()
    buf.add_trajectory(_make_trajectory())
    buf.clear()
    assert buf.trajectory_count() == 0
    assert buf.transition_count() == 0


def test_truncate_zero():
    proto = TrajectoryPrototype(_make_trajectory())
    t = proto.truncate(0)
    assert t.length() == 0
