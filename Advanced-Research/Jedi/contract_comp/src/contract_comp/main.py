from contract_comp import Contract


def main() -> None:
    token = Contract("Token", "0x123", ["transfer", "balanceOf"], [])
    vault = Contract("Vault", "0x456", ["deposit", "withdraw"], ["Token"])
    token.add_dependency("Vault")
    print(f"Token functions: {token.functions}")
    print(f"Vault dependencies: {vault.dependencies}")


if __name__ == "__main__":
    main()
