from dao_gov import Vote
from dao_gov.models import create_proposal


def main() -> None:
    proposal = create_proposal("P1", "Increase treasury", "Vote to increase")
    proposal.add_vote(Vote("alice", "yes", weight=100))
    proposal.add_vote(Vote("bob", "no", weight=50))
    print(f"Proposal: {proposal.title}")
    print(f"Result: {'Passed' if proposal.passed() else 'Failed'}")


if __name__ == "__main__":
    main()
