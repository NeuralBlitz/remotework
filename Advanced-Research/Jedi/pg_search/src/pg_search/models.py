from dataclasses import dataclass, field
from enum import Enum


class SearchMode(Enum):
    FULLTEXT = "fulltext"
    FUZZY = "fuzzy"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"


@dataclass(frozen=True)
class SearchResult:
    doc_id: str
    score: float
    snippet: str = ""
    mode: SearchMode = SearchMode.FULLTEXT
    metadata: dict[str, str] = field(default_factory=dict)
