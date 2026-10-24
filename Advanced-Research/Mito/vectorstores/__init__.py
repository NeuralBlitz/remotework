"""
Mito Vector Stores
In-memory, file-backed, and cosine similarity vector search
"""

import json
import math
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger("mito.vectorstores")


@dataclass
class VectorDocument:
    id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def cosine_similarity(self, other: List[float]) -> float:
        if len(self.embedding) != len(other):
            return 0.0
        dot = sum(a * b for a, b in zip(self.embedding, other))
        norm_a = math.sqrt(sum(a * a for a in self.embedding))
        norm_b = math.sqrt(sum(b * b for b in other))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)


class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.documents: Dict[str, VectorDocument] = {}

    def add(self, doc: VectorDocument) -> str:
        self.documents[doc.id] = doc
        return doc.id

    def add_batch(self, docs: List[VectorDocument]) -> List[str]:
        ids = []
        for doc in docs:
            self.documents[doc.id] = doc
            ids.append(doc.id)
        return ids

    def get(self, doc_id: str) -> Optional[VectorDocument]:
        return self.documents.get(doc_id)

    def delete(self, doc_id: str) -> bool:
        if doc_id in self.documents:
            del self.documents[doc_id]
            return True
        return False

    def search(self, query_embedding: List[float], top_k: int = 5,
               filter_func=None) -> List[Tuple[VectorDocument, float]]:
        results = []
        for doc in self.documents.values():
            if filter_func and not filter_func(doc):
                continue
            score = doc.cosine_similarity(query_embedding)
            results.append((doc, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def search_by_text(self, query_embedding: List[float], top_k: int = 5,
                       min_score: float = 0.0) -> List[Dict]:
        results = self.search(query_embedding, top_k)
        return [{"id": doc.id, "content": doc.content, "score": score, "metadata": doc.metadata}
                for doc, score in results if score >= min_score]

    def count(self) -> int:
        return len(self.documents)

    def clear(self):
        self.documents.clear()

    def save(self, filepath: str):
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        data = []
        for doc in self.documents.values():
            data.append({
                "id": doc.id, "content": doc.content,
                "embedding": doc.embedding, "metadata": doc.metadata,
                "created_at": doc.created_at,
            })
        with open(filepath, "w") as f:
            json.dump(data, f)

    def load(self, filepath: str):
        with open(filepath) as f:
            data = json.load(f)
        for item in data:
            doc = VectorDocument(
                id=item["id"], content=item["content"],
                embedding=item["embedding"], metadata=item.get("metadata", {}),
                created_at=item.get("created_at", time.time()),
            )
            self.documents[doc.id] = doc

    def upsert(self, doc: VectorDocument) -> str:
        self.documents[doc.id] = doc
        return doc.id

    def list_all(self, limit: int = 100) -> List[VectorDocument]:
        return list(self.documents.values())[:limit]

    def get_stats(self) -> Dict:
        if not self.documents:
            return {"count": 0, "dimension": self.dimension}
        embeddings = list(self.documents.values())
        return {
            "count": len(self.documents),
            "dimension": self.dimension,
            "avg_content_length": sum(len(d.content) for d in embeddings) / len(embeddings),
        }


class FAISSVectorStore:
    """FAISS-backed vector store for large-scale search."""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = None
        self.id_map: Dict[int, str] = {}
        self.documents: Dict[str, VectorDocument] = {}
        self._next_id = 0

    def _ensure_index(self):
        if self.index is None:
            try:
                import faiss
                self.index = faiss.IndexFlatIP(self.dimension)
            except ImportError:
                raise ImportError("faiss not installed. Install with: pip install faiss-cpu")

    def add(self, doc: VectorDocument) -> str:
        import numpy as np
        self._ensure_index()
        vec = np.array([doc.embedding], dtype=np.float32)
        faiss.normalize_L2(vec)
        self.index.add(vec)
        self.id_map[self._next_id] = doc.id
        self.documents[doc.id] = doc
        self._next_id += 1
        return doc.id

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[VectorDocument, float]]:
        import numpy as np
        self._ensure_index()
        vec = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(vec)
        scores, indices = self.index.search(vec, top_k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0 and idx in self.id_map:
                doc_id = self.id_map[idx]
                results.append((self.documents[doc_id], float(score)))
        return results

    def count(self) -> int:
        return len(self.documents)
