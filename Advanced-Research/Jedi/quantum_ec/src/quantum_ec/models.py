from dataclasses import dataclass


@dataclass
class Qubit:
    index: int
    state: str = "0"
    error_rate: float = 0.0

    def flip(self) -> None:
        self.state = "1" if self.state == "0" else "0"


@dataclass
class ErrorCode:
    name: str
    distance: int
    qubits: list[Qubit]

    def encode(self, logical_bit: str) -> list[str]:
        return [logical_bit] * len(self.qubits)

    def decode(self, physical_bits: list[str]) -> str:
        if not physical_bits:
            return "0"
        counts: dict[str, int] = {}
        for b in physical_bits:
            counts[b] = counts.get(b, 0) + 1
        return max(counts, key=counts.get)  # type: ignore


def create_surface_code(size: int) -> ErrorCode:
    qubits = [Qubit(i) for i in range(size * size)]
    return ErrorCode(name="surface", distance=size, qubits=qubits)


def syndrome_measurement(qubits: list[Qubit]) -> list[int]:
    syndrome: list[int] = []
    for q in qubits:
        syndrome.append(1 if q.state != "0" else 0)
    return syndrome


def apply_bit_flip(qubit: Qubit, probability: float) -> None:
    import random

    if random.random() < probability:
        qubit.flip()
