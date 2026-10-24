from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Frame:
    frame_id: str
    width: int = 1920
    height: int = 1080
    frame_number: int = 0
    data: bytes = b""


@dataclass
class EncodedChunk:
    chunk_id: str
    codec: str = ""
    size_bytes: int = 0
    frame_number: int = 0
    data: bytes = b""

