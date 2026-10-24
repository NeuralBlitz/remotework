from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class ModalityType(Enum):
    TEXT = auto()
    IMAGE = auto()
    AUDIO = auto()


@dataclass
class JointEmbedding:
    text_vec: list[float] = field(default_factory=list)
    image_vec: list[float] = field(default_factory=list)
    audio_vec: list[float] = field(default_factory=list)
    fused_vec: list[float] = field(default_factory=list)
    modalities: list[ModalityType] = field(default_factory=list)

    @property
    def dim(self) -> int:
        return len(self.fused_vec)

    @property
    def is_multimodal(self) -> bool:
        return len(self.modalities) > 1
