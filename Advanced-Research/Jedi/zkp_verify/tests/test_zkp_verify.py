from zkp_verify import Proof, Verifier
from zkp_verify.models import Prover


class TestProof:
    def test_creation(self) -> None:
        proof = Proof("test", "comm", "resp", ["sig1"])
        assert proof.statement == "test"

    def test_to_bytes(self) -> None:
        proof = Proof("test", "abc", "def", [])
        b = proof.to_bytes()
        assert b == b"abcdef"


class TestVerifier:
    def test_verify_valid(self) -> None:
        v = Verifier("bob")
        proof = Proof("test", "comm", "resp", [])
        assert v.verify(proof) is True

    def test_verify_invalid(self) -> None:
        v = Verifier("bob")
        proof = Proof("test", "", "", [])
        assert v.verify(proof) is False

    def test_generate_challenge(self) -> None:
        v = Verifier("bob")
        c = v.generate_challenge()
        assert len(c) == 32


class TestProver:
    def test_create_proof(self) -> None:
        p = Prover("alice")
        proof = p.create_proof("x = 10")
        assert proof.statement == "x = 10"
