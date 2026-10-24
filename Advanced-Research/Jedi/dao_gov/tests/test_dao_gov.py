from dao_gov import Proposal, Vote
from dao_gov.models import create_proposal, quorum_check


class TestVote:
    def test_vote_creation(self) -> None:
        v = Vote("alice", "yes", weight=10.0)
        assert v.voter == "alice"
        assert v.choice == "yes"
        assert v.weight == 10.0

    def test_default_timestamp(self) -> None:
        v = Vote("alice", "yes")
        assert v.timestamp is not None


class TestProposal:
    def test_add_vote(self) -> None:
        p = Proposal("1", "test", "desc", [])
        p.add_vote(Vote("alice", "yes"))
        assert len(p.votes) == 1

    def test_tally(self) -> None:
        p = Proposal("1", "test", "desc", [])
        p.add_vote(Vote("alice", "yes", 100))
        p.add_vote(Vote("bob", "no", 50))
        tallies = p.tally()
        assert tallies["yes"] == 100
        assert tallies["no"] == 50

    def test_passed(self) -> None:
        p = Proposal("1", "test", "desc", [], threshold=0.6)
        p.add_vote(Vote("alice", "yes", 70))
        p.add_vote(Vote("bob", "no", 30))
        assert p.passed() is True

    def test_not_passed(self) -> None:
        p = Proposal("1", "test", "desc", [], threshold=0.8)
        p.add_vote(Vote("alice", "yes", 50))
        p.add_vote(Vote("bob", "no", 50))
        assert p.passed() is False


class TestHelpers:
    def test_create_proposal(self) -> None:
        p = create_proposal("P1", "title", "desc")
        assert p.proposal_id == "P1"

    def test_quorum_check(self) -> None:
        assert quorum_check(100, 1000) is True
        assert quorum_check(5, 1000) is False
