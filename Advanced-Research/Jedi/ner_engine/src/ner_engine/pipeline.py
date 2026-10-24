from __future__ import annotations

import re

from .models import Entity, Token


class Tokenizer:
    def tokenize(self, text: str) -> list[Token]:
        words = text.split()
        pos = 0
        tokens: list[Token] = []
        for word in words:
            start = text.index(word, pos)
            tokens.append(Token(text=word, start=start, end=start + len(word)))
            pos = start + len(word)
        return tokens


class NERModel:
    KNOWN_ORGS = {"Google", "Microsoft", "Apple", "Amazon", "Meta"}
    KNOWN_LOCS = {"New", "York", "London", "Tokyo", "Paris", "Berlin"}
    PATTERNS: dict[str, re.Pattern[str]] = {
        "ORG": re.compile(r"^(?:Google|Microsoft|Apple|Amazon|Meta)$"),
        "LOCATION": re.compile(r"^(?:New|York|London|Tokyo|Paris|Berlin)$"),
        "DATE": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
        "PERSON": re.compile(r"^[A-Z][a-z]+$"),
    }

    def extract(self, tokens: list[Token]) -> list[Entity]:
        entities: list[Entity] = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            for label, pattern in self.PATTERNS.items():
                if pattern.match(token.text):
                    if label == "PERSON" and token.text in self.KNOWN_ORGS:
                        label = "ORG"
                    elif label == "PERSON" and token.text in self.KNOWN_LOCS:
                        label = "LOCATION"
                    entities.append(
                        Entity(text=token.text, label=label, start=token.start, end=token.end)
                    )
                    break
            i += 1
        return entities


class PostProcessor:
    def process(self, entities: list[Entity]) -> list[Entity]:
        seen: set[tuple[str, str]] = set()
        result: list[Entity] = []
        for e in entities:
            key = (e.text, e.label)
            if key not in seen:
                seen.add(key)
                result.append(e)
        return result


class NERPipeline:
    def __init__(self) -> None:
        self.tokenizer = Tokenizer()
        self.model = NERModel()
        self.post_processor = PostProcessor()

    def run(self, text: str) -> list[Entity]:
        tokens = self.tokenizer.tokenize(text)
        entities = self.model.extract(tokens)
        return self.post_processor.process(entities)
