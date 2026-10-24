from __future__ import annotations

from abc import ABC, abstractmethod


class ModalityEncoder(ABC):
    def __init__(self, output_dim: int = 64) -> None:
        self.output_dim = output_dim

    @abstractmethod
    def encode(self, data: str) -> list[float]: ...


class TextEncoder(ModalityEncoder):
    def encode(self, data: str) -> list[float]:
        seed = sum(ord(c) for c in data)
        return [((seed * (i + 1)) % 97) / 97.0 for i in range(self.output_dim)]


class ImageEncoder(ModalityEncoder):
    def encode(self, data: str) -> list[float]:
        seed = len(data)
        return [((seed * (i + 3)) % 89) / 89.0 for i in range(self.output_dim)]


class AudioEncoder(ModalityEncoder):
    def encode(self, data: str) -> list[float]:
        seed = hash(data) % 1000
        return [((seed * (i + 5)) % 83) / 83.0 for i in range(self.output_dim)]
