from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Document:
    document_id: str
    title: str = ""
    content: str = ""


@dataclass
class Summary:
    document_id: str
    text: str = ""
    method: str = ""

