import hashlib

from zkp_verify import Proof


class Prover:
    def __init__(self, name: str) -> None:
        self.name = name

    def create_proof(self, statement: str) -> Proof:
        import secrets

        commitment = secrets.token_hex(16)
        response = secrets.token_hex(32)
        return Proof(statement, commitment, response, [statement])


def create_schnorr_proof(witness: str, statement: str) -> Proof:
    import secrets

    return Proof(statement, secrets.token_hex(16), secrets.token_hex(32), [witness])


def hash_proof(proof: Proof) -> str:
    h = hashlib.sha256()
    h.update(proof.to_bytes())
    return h.hexdigest()
