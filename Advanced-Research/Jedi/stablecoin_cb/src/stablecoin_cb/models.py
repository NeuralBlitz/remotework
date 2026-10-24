from dataclasses import dataclass


@dataclass
class Collateral:
    asset: str
    amount: float
    value_usd: float
    locked: bool = False

    @property
    def ratio(self) -> float:
        return self.amount / self.value_usd if self.value_usd > 0 else 0.0


@dataclass
class Reserve:
    name: str
    collaterals: list[Collateral]
    total_debt: float

    def add_collateral(self, collateral: Collateral) -> None:
        self.collaterals.append(collateral)

    @property
    def total_value(self) -> float:
        return sum(c.value_usd for c in self.collaterals)

    @property
    def health_factor(self) -> float:
        return self.total_value / self.total_debt if self.total_debt > 0 else float("inf")

    @property
    def is_healthy(self) -> bool:
        return self.health_factor >= 1.5


def rebalance_reserve(reserve: Reserve, target: float = 1.5) -> float:
    if reserve.health_factor > target:
        return reserve.health_factor - target
    return 0.0


def liquidation_check(reserve: Reserve) -> bool:
    return reserve.health_factor < 1.0


def target_ratio(strategy: str) -> float:
    ratios = {"conservative": 2.0, "moderate": 1.75, "aggressive": 1.5}
    return ratios.get(strategy, 1.5)
