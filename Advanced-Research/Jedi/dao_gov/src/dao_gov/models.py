from dataclasses import dataclass
from datetime import datetime


@dataclass
class Vote:
    voter: str
    choice: str
    weight: float = 1.0
    timestamp: datetime | None = None

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class Proposal:
    proposal_id: str
    title: str
    description: str
    votes: list[Vote]
    threshold: float = 0.5

    def add_vote(self, vote: Vote) -> None:
        self.votes.append(vote)

    def tally(self) -> dict[str, float]:
        tally_dict: dict[str, float] = {}
        for vote in self.votes:
            tally_dict[vote.choice] = tally_dict.get(vote.choice, 0.0) + vote.weight
        return tally_dict

    def passed(self) -> bool:
        total = sum(v.weight for v in self.votes)
        if total == 0:
            return False
        tallies = self.tally()
        if not tallies:
            return False
        max_choice = max(tallies, key=tallies.get)
        return tallies[max_choice] / total >= self.threshold


def create_proposal(proposal_id: str, title: str, description: str) -> Proposal:
    return Proposal(proposal_id, title, description, [])


def execute_governance(proposal: Proposal) -> str:
    if proposal.passed():
        return "executed"
    return "rejected"


def quorum_check(votes: float, total_tokens: float) -> bool:
    return (votes / total_tokens) >= 0.1 if total_tokens > 0 else False
