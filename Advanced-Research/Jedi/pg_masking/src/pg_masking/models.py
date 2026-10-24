from dataclasses import dataclass
from enum import Enum


class MaskingType(Enum):
    FULL = "full"
    PARTIAL = "partial"
    HASH = "hash"
    REDACT = "redact"


@dataclass(frozen=True)
class MaskingRule:
    field_name: str
    masking_type: MaskingType
    roles_exempt: frozenset[str] = frozenset()
    mask_char: str = "*"
