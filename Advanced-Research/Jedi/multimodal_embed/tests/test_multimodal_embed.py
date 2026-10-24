from multimodal_embed.encoders import AudioEncoder, ImageEncoder, TextEncoder
from multimodal_embed.mediator import ModalityMediator
from multimodal_embed.models import JointEmbedding, ModalityType


def test_text_encoder_produces_vec() -> None:
    enc = TextEncoder(output_dim=16)
    vec = enc.encode("hello")
    assert len(vec) == 16


def test_image_encoder_produces_vec() -> None:
    enc = ImageEncoder(output_dim=16)
    vec = enc.encode("image_data")
    assert len(vec) == 16


def test_audio_encoder_produces_vec() -> None:
    enc = AudioEncoder(output_dim=16)
    vec = enc.encode("audio_data")
    assert len(vec) == 16


def test_mediator_single_modality() -> None:
    med = ModalityMediator(output_dim=8)
    med.register(ModalityType.TEXT, TextEncoder(output_dim=8))
    emb = med.encode({ModalityType.TEXT: "hello"})
    assert emb.text_vec
    assert emb.dim == 8
    assert not emb.is_multimodal


def test_mediator_multiple_modalities() -> None:
    med = ModalityMediator(output_dim=8)
    med.register(ModalityType.TEXT, TextEncoder(output_dim=8))
    med.register(ModalityType.IMAGE, ImageEncoder(output_dim=8))
    emb = med.encode({ModalityType.TEXT: "cat", ModalityType.IMAGE: "img"})
    assert emb.text_vec
    assert emb.image_vec
    assert emb.is_multimodal


def test_fusion_averages_vectors() -> None:
    med = ModalityMediator(output_dim=4)
    med.register(ModalityType.TEXT, TextEncoder(output_dim=4))
    med.register(ModalityType.IMAGE, ImageEncoder(output_dim=4))
    emb = med.encode({ModalityType.TEXT: "a", ModalityType.IMAGE: "b"})
    assert len(emb.fused_vec) == 4
    for i in range(4):
        expected = (emb.text_vec[i] + emb.image_vec[i]) / 2
        assert abs(emb.fused_vec[i] - expected) < 1e-9


def test_joint_embedding_dim() -> None:
    je = JointEmbedding(fused_vec=[0.1, 0.2, 0.3])
    assert je.dim == 3


def test_joint_embedding_not_multimodal() -> None:
    je = JointEmbedding(modalities=[ModalityType.TEXT])
    assert not je.is_multimodal
