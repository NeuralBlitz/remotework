"""
Embeddings using sentence-transformers
"""

from typing import Optional, List, Union
import numpy as np



class Embedder:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: Optional[str] = None
    ):
        """
        Initialize embedder.
        
        Args:
            model_name: HuggingFace model name.
            device: Device to use.
        """
        self.model_name = model_name
        self.device = device
        self.model = None
    
    def _get_model(self):
        """Lazy load embedding model."""
        if self.model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(
                    self.model_name,
                    device=self.device
                )
            except ImportError:
                raise ImportError(
                    "sentence-transformers not installed. Install with:\n"
                    "  pip install sentence-transformers"
                )
        return self.model
    
    def embed(self, text: str) -> np.ndarray:
        """
        Get embedding for single text.
        
        Args:
            text: Input text.
            
        Returns:
            Embedding vector.
        """
        model = self._get_model()
        return model.encode(text)
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """
        Get embeddings for multiple texts.
        
        Args:
            texts: List of input texts.
            
        Returns:
            Array of embedding vectors.
        """
        model = self._get_model()
        return model.encode(texts)
    
    def similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity between two texts.
        
        Args:
            text1: First text.
            text2: Second text.
            
        Returns:
            Similarity score (0-1).
        """
        emb1 = self.embed(text1)
        emb2 = self.embed(text2)
        
        cos_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return float(cos_sim)
    
    def semantic_search(
        self,
        query: str,
        corpus: List[str],
        top_k: int = 5
    ) -> List[dict]:
        """
        Semantic search over a corpus.
        
        Args:
            query: Search query.
            corpus: List of texts to search.
            top_k: Number of results.
            
        Returns:
            List of results with scores.
        """
        model = self._get_model()
        
        query_emb = model.encode(query)
        corpus_emb = model.encode(corpus)
        
        similarities = np.dot(corpus_emb, query_emb) / (
            np.linalg.norm(corpus_emb, axis=1) * np.linalg.norm(query_emb)
        )
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "text": corpus[idx],
                "score": float(similarities[idx]),
                "index": int(idx)
            })
        
        return results


def quick_embed(text: str, model: str = "sentence-transformers/all-MiniLM-L6-v2") -> List[float]:
    """
    Quick embedding.
    
    Args:
        text: Input text.
        model: Model name.
        
    Returns:
        Embedding as list.
    """
    embedder = Embedder(model_name=model)
    return embedder.embed(text).tolist()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m ai.embeddings <text>")
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    
    embedder = Embedder()
    emb = embedder.embed(text)
    print(f"Embedding shape: {emb.shape}")
    print(f"First 5 values: {emb[:5]}")
