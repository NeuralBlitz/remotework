from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TranslationRequest:
    request_id: str
    text: str = ""
    source_language: str = "en"
    target_language: str = "es"


@dataclass
class TranslationResult:
    request_id: str
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""

