from quantum_ec import ErrorCode, Qubit


def main() -> None:
    qubits = [Qubit(i) for i in range(9)]
    code = ErrorCode(name="surface", distance=3, qubits=qubits)
    encoded = code.encode("1")
    print(f"Encoded: {encoded}")
    decoded = code.decode(encoded)
    print(f"Decoded: {decoded}")


if __name__ == "__main__":
    main()
