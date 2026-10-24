from __future__ import annotations

from ad_bidding.models import Auction, BidRequest, BidResponse
from ad_bidding.strategies import (
    AuctionEngine,
    BudgetAwareBidStrategy,
    DynamicBidStrategy,
    FixedBidStrategy,
)


def test_fixed_bid() -> None:
    strategy = FixedBidStrategy(amount=2.5)
    req = BidRequest(request_id="r1")
    resp = strategy.bid(req)
    assert resp.amount == 2.5


def test_dynamic_bid() -> None:
    strategy = DynamicBidStrategy(base=1.0, multiplier=2.0)
    req = BidRequest(request_id="r2", quality_score=1.5)
    resp = strategy.bid(req)
    assert resp.amount == 3.0


def test_budget_aware_bid() -> None:
    strategy = BudgetAwareBidStrategy(budget=100.0)
    req = BidRequest(request_id="r3", max_bid=5.0)
    resp = strategy.bid(req)
    assert resp.amount <= 5.0


def test_auction_winner() -> None:
    engine = AuctionEngine()
    bids = [BidResponse(request_id="r1", amount=1.0), BidResponse(request_id="r2", amount=2.0)]
    auction = Auction(auction_id="a1", bids=bids)
    winner = engine.run_auction(auction)
    assert winner is not None
    assert winner.request_id == "r2"


def test_empty_auction() -> None:
    engine = AuctionEngine()
    auction = Auction(auction_id="a2")
    assert engine.run_auction(auction) is None

