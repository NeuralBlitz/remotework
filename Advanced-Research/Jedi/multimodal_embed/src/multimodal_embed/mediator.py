from __future__ import annotations

from multimodal_embed.encoders import ModalityEncoder
from multimodal_embed.models import JointEmbedding, ModalityType


class ModalityMediator:
    def __init__(self, output_dim: int = 64) -> None:
        self.output_dim = output_dim
        self._encoders: dict[ModalityType, ModalityEncoder] = {}

    def register(self, modality: ModalityType, encoder: ModalityEncoder) -> None:
        self._encoders[modality] = encoder

    def encode(self, inputs: dict[ModalityType, str]) -> JointEmbedding:
        embedding = JointEmbedding(modalities=list(inputs.keys()))
        for modality, data in inputs.items():
            if modality not in self._encoders:
                continue
            vec = self._encoders[modality].encode(data)
            if modality == ModalityType.TEXT:
                embedding.text_vec = vec
            elif modality == ModalityType.IMAGE:
                embedding.image_vec = vec
            elif modality == ModalityType.AUDIO:
                embedding.audio_vec = vec
        embedding.fused_vec = self._fuse(embedding)
        return embedding

    def _fuse(self, embedding: JointEmbedding) -> list[float]:
        all_vecs = [v for v in (embedding.text_vec, embedding.image_vec, embedding.audio_vec) if v]
        if not all_vecs:
            return []
        n = len(all_vecs[0])
        fused = [0.0] * n
        for vec in all_vecs:
            for i in range(min(n, len(vec))):
                fused[i] += vec[i]
        count = len(all_vecs)
        return [x / count for x in fused]
