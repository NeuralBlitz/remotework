"""
RAG (Retrieval Augmented Generation) System
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import numpy as np



class Document:
    def __init__(self, content: str, metadata: Optional[Dict] = None):
        self.content = content
        self.metadata = metadata or {}
        self.embedding: Optional[np.ndarray] = None
    
    def __repr__(self):
        return f"Document(content={self.content[:50]}...)"


class VectorStore:
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding_model = embedding_model
        self.documents: List[Document] = []
        self.embeddings: Optional[np.ndarray] = None
    
    def _get_embedder(self):
        from python.ai.embeddings import Embedder
        return Embedder(model_name=self.embedding_model)
    
    def add_document(self, doc: Document):
        self.documents.append(doc)
    
    def add_documents(self, docs: List[Document]):
        for doc in docs:
            self.add_document(doc)
    
    def build_index(self):
        embedder = self._get_embedder()
        texts = [doc.content for doc in self.documents]
        
        self.embeddings = embedder.embed_batch(texts)
        
        for i, doc in enumerate(self.documents):
            doc.embedding = self.embeddings[i]
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        embedder = self._get_embedder()
        
        query_emb = embedder.embed(query)
        
        if self.embeddings is None:
            self.build_index()
        
        similarities = np.dot(self.embeddings, query_emb) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_emb)
        )
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] >= threshold:
                results.append({
                    "document": self.documents[idx],
                    "score": float(similarities[idx]),
                    "content": self.documents[idx].content,
                    "metadata": self.documents[idx].metadata
                })
        
        return results
    
    def save(self, path: str):
        data = {
            "embedding_model": self.embedding_model,
            "documents": [
                {
                    "content": doc.content,
                    "metadata": doc.metadata
                }
                for doc in self.documents
            ]
        }
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self, path: str):
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.embedding_model = data["embedding_model"]
        self.documents = [
            Document(d["content"], d["metadata"])
            for d in data["documents"]
        ]
        
        self.build_index()


class RAG:
    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        llm_model: str = "gpt2"
    ):
        self.vector_store = vector_store or VectorStore()
        self.llm_model = llm_model
    
    def add_documents(self, docs: List[str], metadata_list: Optional[List[Dict]] = None):
        metadata_list = metadata_list or [{}] * len(docs)
        
        documents = [
            Document(content, meta)
            for content, meta in zip(docs, metadata_list)
        ]
        
        self.vector_store.add_documents(documents)
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        return self.vector_store.search(query, top_k=top_k)
    
    def generate(
        self,
        query: str,
        context: Optional[str] = None,
        max_tokens: int = 200
    ) -> str:
        from python.ai import TextGenerator
        
        if context is None:
            docs = self.retrieve(query)
            context = "\n\n".join([d["content"] for d in docs])
        
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""
        
        gen = TextGenerator(model_name=self.llm_model)
        result = gen.generate_single(prompt, max_length=max_tokens)
        
        return result
    
    def query(self, question: str) -> Dict[str, Any]:
        docs = self.retrieve(question)
        
        answer = self.generate(question)
        
        return {
            "question": question,
            "answer": answer,
            "sources": docs
        }


def create_rag(
    documents: List[str],
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    llm_model: str = "gpt2"
) -> RAG:
    """
    Quick RAG creation from documents.
    
    Args:
        documents: List of text documents.
        embedding_model: Model for embeddings.
        llm_model: Model for generation.
        
    Returns:
        Configured RAG system.
    """
    rag = RAG(llm_model=llm_model)
    rag.add_documents(documents)
    return rag


if __name__ == '__main__':
    docs = [
        "Python is a high-level programming language.",
        "Machine learning is a subset of artificial intelligence.",
        "Transformers are a type of neural network architecture.",
    ]
    
    rag = create_rag(docs)
    
    result = rag.query("What is Python?")
    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {len(result['sources'])}")
