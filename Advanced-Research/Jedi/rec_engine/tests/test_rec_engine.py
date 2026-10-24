from __future__ import annotations

from rec_engine.models import Item, Rating, User
from rec_engine.strategies import CollaborativeFiltering, ContentBasedFiltering, HybridFiltering


def _make_data() -> tuple[User, list[Item], list[Rating]]:
    user = User(user_id="u1")
    items = [Item(item_id=f"i{i}", title=f"Item {i}", tags=[f"tag{i}"]) for i in range(5)]
    ratings = [
        Rating(user_id="u1", item_id="i0", score=5.0),
        Rating(user_id="u2", item_id="i1", score=4.0),
    ]
    return user, items, ratings


def test_collaborative() -> None:
    user, items, ratings = _make_data()
    strategy = CollaborativeFiltering()
    recs = strategy.recommend(user, items, ratings)
    assert isinstance(recs, list)


def test_content_based() -> None:
    user, items, ratings = _make_data()
    strategy = ContentBasedFiltering()
    recs = strategy.recommend(user, items, ratings)
    assert isinstance(recs, list)


def test_hybrid() -> None:
    user, items, ratings = _make_data()
    strategy = HybridFiltering()
    recs = strategy.recommend(user, items, ratings)
    assert isinstance(recs, list)


def test_no_duplicates_in_hybrid() -> None:
    user, items, ratings = _make_data()
    strategy = HybridFiltering()
    recs = strategy.recommend(user, items, ratings)
    ids = [i.item_id for i in recs]
    assert len(ids) == len(set(ids))


def test_empty_items() -> None:
    user = User(user_id="u1")
    strategy = CollaborativeFiltering()
    recs = strategy.recommend(user, [], [])
    assert recs == []
