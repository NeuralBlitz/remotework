from quantum_ec import ErrorCode, Qubit
from quantum_ec.models import apply_bit_flip, syndrome_measurement


class TestQubit:
    def test_creation(self) -> None:
        q = Qubit(0)
        assert q.index == 0
        assert q.state == "0"
        assert q.error_rate == 0.0

    def test_flip(self) -> None:
        q = Qubit(0)
        q.flip()
        assert q.state == "1"
        q.flip()
        assert q.state == "0"


class TestErrorCode:
    def test_encode(self) -> None:
        qubits = [Qubit(i) for i in range(5)]
        code = ErrorCode(name="test", distance=3, qubits=qubits)
        encoded = code.encode("1")
        assert len(encoded) == 5
        assert all(b == "1" for b in encoded)

    def test_decode_majority(self) -> None:
        qubits = [Qubit(i) for i in range(3)]
        code = ErrorCode(name="test", distance=3, qubits=qubits)
        decoded = code.decode(["1", "1", "0"])
        assert decoded == "1"


class TestHelpers:
    def test_syndrome_measurement(self) -> None:
        qubits = [Qubit(i) for i in range(3)]
        qubits[1].flip()
        syndrome = syndrome_measurement(qubits)
        assert syndrome[1] == 1

    def test_apply_bit_flip(self) -> None:
        q = Qubit(0)
        apply_bit_flip(q, 0.0)
        assert q.state == "0"
