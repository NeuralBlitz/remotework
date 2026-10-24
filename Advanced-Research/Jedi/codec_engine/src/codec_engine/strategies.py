from __future__ import annotations

from abc import ABC, abstractmethod

from .models import EncodedChunk, Frame


class EncodingStrategy(ABC):
    @abstractmethod
    def encode(self, frame: Frame) -> EncodedChunk:
        raise NotImplementedError

    @abstractmethod
    def decode(self, chunk: EncodedChunk) -> Frame:
        raise NotImplementedError


class H264Encoder(EncodingStrategy):
    def encode(self, frame: Frame) -> EncodedChunk:
        compressed_size = len(frame.data) // 10
        return EncodedChunk(
            chunk_id=f"{frame.frame_id}_h264",
            codec="h264",
            size_bytes=compressed_size,
            frame_number=frame.frame_number,
            data=b"\x00" * compressed_size,
        )

    def decode(self, chunk: EncodedChunk) -> Frame:
        return Frame(
            frame_id=chunk.chunk_id,
            width=1920,
            height=1080,
            frame_number=chunk.frame_number,
            data=b"\xff" * (chunk.size_bytes * 10),
        )


class H265Encoder(EncodingStrategy):
    def encode(self, frame: Frame) -> EncodedChunk:
        compressed_size = len(frame.data) // 15
        return EncodedChunk(
            chunk_id=f"{frame.frame_id}_h265",
            codec="h265",
            size_bytes=compressed_size,
            frame_number=frame.frame_number,
            data=b"\x00" * compressed_size,
        )

    def decode(self, chunk: EncodedChunk) -> Frame:
        return Frame(
            frame_id=chunk.chunk_id,
            width=3840,
            height=2160,
            frame_number=chunk.frame_number,
            data=b"\xff" * (chunk.size_bytes * 15),
        )


class AV1Encoder(EncodingStrategy):
    def encode(self, frame: Frame) -> EncodedChunk:
        compressed_size = len(frame.data) // 20
        return EncodedChunk(
            chunk_id=f"{frame.frame_id}_av1",
            codec="av1",
            size_bytes=compressed_size,
            frame_number=frame.frame_number,
            data=b"\x00" * compressed_size,
        )

    def decode(self, chunk: EncodedChunk) -> Frame:
        return Frame(
            frame_id=chunk.chunk_id,
            width=7680,
            height=4320,
            frame_number=chunk.frame_number,
            data=b"\xff" * (chunk.size_bytes * 20),
        )


class CodecEngine:
    def __init__(self, strategy: EncodingStrategy | None = None) -> None:
        self.strategy = strategy or H264Encoder()

    def encode_frame(self, frame: Frame) -> EncodedChunk:
        return self.strategy.encode(frame)

    def decode_chunk(self, chunk: EncodedChunk) -> Frame:
        return self.strategy.decode(chunk)

    def encode_batch(self, frames: list[Frame]) -> list[EncodedChunk]:
        return [self.encode_frame(f) for f in frames]

