from __future__ import annotations

from abc import ABC, abstractmethod

from .models import Item, Rating, User


class RecommendationStrategy(ABC):
    @abstractmethod
    def recommend(self, user: User, items: list[Item], ratings: list[Rating]) -> list[Item]:
        raise NotImplementedError


class CollaborativeFiltering(RecommendationStrategy):
    def recommend(self, user: User, items: list[Item], ratings: list[Rating]) -> list[Item]:
        user_ratings = {r.item_id: r.score for r in ratings if r.user_id == user.user_id}
        similar_users = self._find_similar(user, ratings)
        candidates: dict[str, float] = {}
        for su in similar_users:
            for r in ratings:
                if r.user_id == su and r.item_id not in user_ratings:
                    candidates[r.item_id] = candidates.get(r.item_id, 0.0) + r.score
        ranked = sorted(candidates, key=lambda k: candidates[k], reverse=True)
        return [i for i in items if i.item_id in ranked[:10]]

    def _find_similar(self, user: User, ratings: list[Rating]) -> list[str]:
        return [r.user_id for r in ratings if r.user_id != user.user_id][:5]


class ContentBasedFiltering(RecommendationStrategy):
    def recommend(self, user: User, items: list[Item], ratings: list[Rating]) -> list[Item]:
        liked = {r.item_id for r in ratings if r.user_id == user.user_id and r.score >= 4.0}
        liked_tags: set[str] = set()
        for item in items:
            if item.item_id in liked:
                liked_tags.update(item.tags)
        scored = []
        for item in items:
            if item.item_id not in liked:
                overlap = len(set(item.tags) & liked_tags)
                scored.append((overlap, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored[:10]]


class HybridFiltering(RecommendationStrategy):
    def __init__(self) -> None:
        self._collab = CollaborativeFiltering()
        self._content = ContentBasedFiltering()

    def recommend(self, user: User, items: list[Item], ratings: list[Rating]) -> list[Item]:
        collab_recs = self._collab.recommend(user, items, ratings)
        content_recs = self._content.recommend(user, items, ratings)
        seen: set[str] = set()
        merged: list[Item] = []
        for item in collab_recs + content_recs:
            if item.item_id not in seen:
                seen.add(item.item_id)
                merged.append(item)
        return merged[:10]
