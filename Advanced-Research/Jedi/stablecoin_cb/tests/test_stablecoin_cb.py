from stablecoin_cb import Collateral, Reserve
from stablecoin_cb.models import liquidation_check, rebalance_reserve, target_ratio


class TestCollateral:
    def test_creation(self) -> None:
        c = Collateral("ETH", 100, 200000)
        assert c.asset == "ETH"

    def test_ratio(self) -> None:
        c = Collateral("ETH", 100, 200000)
        assert c.ratio == 0.0005


class TestReserve:
    def test_add_collateral(self) -> None:
        r = Reserve("Test", [], 1000)
        r.add_collateral(Collateral("BTC", 1, 50000))
        assert len(r.collaterals) == 1

    def test_total_value(self) -> None:
        r = Reserve("Test", [Collateral("ETH", 10, 20000)], 10000)
        assert r.total_value == 20000

    def test_health_factor_healthy(self) -> None:
        r = Reserve("Test", [Collateral("ETH", 100, 200000)], 100000)
        assert r.health_factor == 2.0
        assert r.is_healthy is True

    def test_health_factor_unhealthy(self) -> None:
        r = Reserve("Test", [Collateral("ETH", 50, 100000)], 100000)
        assert r.health_factor == 1.0
        assert r.is_healthy is False


class TestHelpers:
    def test_rebalance_reserve(self) -> None:
        r = Reserve("Test", [Collateral("ETH", 100, 200000)], 100000)
        result = rebalance_reserve(r, target=1.5)
        assert result >= 0

    def test_liquidation_check(self) -> None:
        r = Reserve("Test", [Collateral("ETH", 100, 200000)], 100000)
        assert liquidation_check(r) is False

    def test_target_ratio(self) -> None:
        assert target_ratio("conservative") == 2.0
        assert target_ratio("aggressive") == 1.5
