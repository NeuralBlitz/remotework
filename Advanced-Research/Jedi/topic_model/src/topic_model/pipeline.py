from __future__ import annotations

import re
from collections import Counter

from .models import Document, Topic


class Preprocessor:
    def process(self, doc: Document) -> list[str]:
        text = doc.content.lower()
        text = re.sub(r"[^a-z\s]", "", text)
        stopwords = {"the", "a", "an", "is", "are", "was", "in", "of", "to", "and"}
        return [w for w in text.split() if w not in stopwords and len(w) > 2]


class LDAModel:
    def __init__(self, num_topics: int = 3) -> None:
        self.num_topics = num_topics

    def fit(self, tokenized_docs: list[list[str]]) -> list[Topic]:
        all_words = [w for doc in tokenized_docs for w in doc]
        common = Counter(all_words).most_common(self.num_topics * 5)
        topics: list[Topic] = []
        words_per_topic = max(len(common) // self.num_topics, 1)
        for i in range(self.num_topics):
            start = i * words_per_topic
            chunk = common[start : start + words_per_topic]
            topics.append(
                Topic(
                    topic_id=f"topic_{i}",
                    keywords=[w for w, _ in chunk],
                    weight=sum(c for _, c in chunk),
                )
            )
        return topics


class TopicPipeline:
    def __init__(self, num_topics: int = 3) -> None:
        self.preprocessor = Preprocessor()
        self.model = LDAModel(num_topics=num_topics)

    def run(self, documents: list[Document]) -> list[Topic]:
        tokenized = [self.preprocessor.process(doc) for doc in documents]
        return self.model.fit(tokenized)

