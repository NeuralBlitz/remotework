from __future__ import annotations

from abc import ABC, abstractmethod

from .models import Document, Summary


class SummarizationStrategy(ABC):
    @abstractmethod
    def summarize(self, document: Document, max_sentences: int = 3) -> Summary:
        raise NotImplementedError


class ExtractiveSummarizer(SummarizationStrategy):
    def summarize(self, document: Document, max_sentences: int = 3) -> Summary:
        sentences = [s.strip() for s in document.content.split(".") if s.strip()]
        if not sentences:
            return Summary(document_id=document.document_id, text="")
        scored = []
        words = document.content.lower().split()
        for sentence in sentences:
            s_words = sentence.lower().split()
            score = sum(1 for w in s_words if w in words) / max(len(s_words), 1)
            scored.append((score, sentence))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = [s for _, s in scored[:max_sentences]]
        return Summary(document_id=document.document_id, text=". ".join(top) + ".")


class AbstractiveSummarizer(SummarizationStrategy):
    def summarize(self, document: Document, max_sentences: int = 3) -> Summary:
        sentences = [s.strip() for s in document.content.split(".") if s.strip()]
        if not sentences:
            return Summary(document_id=document.document_id, text="")
        shortened = []
        for sentence in sentences[:max_sentences]:
            words = sentence.split()
            if len(words) > 5:
                shortened.append(" ".join(words[:5]) + "...")
            else:
                shortened.append(sentence)
        return Summary(document_id=document.document_id, text=" ".join(shortened))

