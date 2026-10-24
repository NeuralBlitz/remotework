from __future__ import annotations

import re
import time
from abc import ABC, abstractmethod

from adv_defense.models import ThreatAlert, ThreatLevel


class Observer(ABC):
    @abstractmethod
    def scan(self, text: str) -> ThreatAlert | None: ...

    @abstractmethod
    def name(self) -> str: ...


class KeywordSentinel(Observer):
    def __init__(self, keywords: list[str] | None = None) -> None:
        self._keywords = keywords or [
            "ignore previous",
            "disregard instructions",
            "system prompt",
            "jailbreak",
            "DAN mode",
        ]

    def scan(self, text: str) -> ThreatAlert | None:
        lower = text.lower()
        for kw in self._keywords:
            if kw in lower:
                return ThreatAlert(
                    level=ThreatLevel.HIGH,
                    source=self.name(),
                    message=f"Injection keyword detected: {kw}",
                    input_snippet=text[:100],
                    timestamp=time.time(),
                )
        return None

    def name(self) -> str:
        return "keyword_sentinel"


class BertSentinel(Observer):
    def __init__(self) -> None:
        self._suspicious_patterns = [
            r"pretend you are",
            r"act as if",
            r"you are now",
            r"new persona",
        ]

    def scan(self, text: str) -> ThreatAlert | None:
        lower = text.lower()
        for pattern in self._suspicious_patterns:
            if re.search(pattern, lower):
                return ThreatAlert(
                    level=ThreatLevel.MEDIUM,
                    source=self.name(),
                    message=f"Persona injection pattern: {pattern}",
                    input_snippet=text[:100],
                    timestamp=time.time(),
                )
        return None

    def name(self) -> str:
        return "bert_sentinel"


class PIISentinel(Observer):
    def __init__(self) -> None:
        self._patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        }

    def scan(self, text: str) -> ThreatAlert | None:
        for pii_type, pattern in self._patterns.items():
            if re.search(pattern, text):
                return ThreatAlert(
                    level=ThreatLevel.HIGH,
                    source=self.name(),
                    message=f"PII detected: {pii_type}",
                    input_snippet=text[:100],
                    timestamp=time.time(),
                )
        return None

    def name(self) -> str:
        return "pii_sentinel"
