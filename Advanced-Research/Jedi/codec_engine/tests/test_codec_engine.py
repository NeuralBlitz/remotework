from __future__ import annotations

from codec_engine.models import Frame
from codec_engine.strategies import AV1Encoder, CodecEngine, H264Encoder, H265Encoder


def _make_frame() -> Frame:
    return Frame(frame_id="f1", width=1920, height=1080, data=b"\xff" * 10000)


def test_h264_encode() -> None:
    encoder = H264Encoder()
    chunk = encoder.encode(_make_frame())
    assert chunk.codec == "h264"
    assert chunk.size_bytes < 10000


def test_h265_encode() -> None:
    encoder = H265Encoder()
    chunk = encoder.encode(_make_frame())
    assert chunk.codec == "h265"
    assert chunk.size_bytes < 10000


def test_av1_encode() -> None:
    encoder = AV1Encoder()
    chunk = encoder.encode(_make_frame())
    assert chunk.codec == "av1"
    assert chunk.size_bytes < 10000


def test_roundtrip() -> None:
    engine = CodecEngine(H264Encoder())
    frame = _make_frame()
    chunk = engine.encode_frame(frame)
    decoded = engine.decode_chunk(chunk)
    assert decoded.frame_id == chunk.chunk_id


def test_encode_batch() -> None:
    engine = CodecEngine(H265Encoder())
    frames = [_make_frame() for _ in range(3)]
    chunks = engine.encode_batch(frames)
    assert len(chunks) == 3

