from zkp_verify import Verifier
from zkp_verify.models import Prover


def main() -> None:
    prover = Prover("alice")
    verifier = Verifier("bob")
    proof = prover.create_proof("x > 5")
    valid = verifier.verify(proof)
    print(f"Proof valid: {valid}")


if __name__ == "__main__":
    main()
