from stablecoin_cb import Collateral, Reserve


def main() -> None:
    reserve = Reserve("USDC Reserve", [], 100_000_000)
    reserve.add_collateral(Collateral("ETH", 50000, 150_000_000))
    print(f"Reserve: {reserve.name}")
    print(f"Health factor: {reserve.health_factor:.2f}")


if __name__ == "__main__":
    main()
