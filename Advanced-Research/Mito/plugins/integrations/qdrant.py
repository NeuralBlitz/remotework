"""Qdrant Vector DB Plugin"""
import os
from typing import Dict, List
class QdrantClient:
    def __init__(self, url: str = None, api_key: str = None):
        self.url = (url or os.environ.get("QDRANT_URL", "http://localhost:6333")).rstrip("/")
        self.api_key = api_key or os.environ.get("QDRANT_API_KEY", "")
    def _headers(self):
        h = {"Content-Type": "application/json"}
        if self.api_key: h["api-key"] = self.api_key
        return h
    def list_collections(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.url}/collections", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("result", {}).get("collections", [])
    def create_collection(self, name: str, vector_size: int, distance: str = "Cosine") -> bool:
        import requests
        resp = requests.put(f"{self.url}/collections/{name}", headers=self._headers(), json={"vectors": {"size": vector_size, "distance": distance}}, timeout=30)
        return resp.ok
    def search(self, collection: str, vector: List[float], top_k: int = 5) -> List[Dict]:
        import requests
        resp = requests.post(f"{self.url}/collections/{collection}/points/search", headers=self._headers(), json={"vector": vector, "limit": top_k}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("result", [])
def register(plugin): plugin.set_resource("client_class", QdrantClient)
qdrant_plugin = {"metadata": {"name": "qdrant", "version": "1.0.0", "description": "Qdrant vector database", "author": "Mito Team", "license": "MIT", "tags": ["qdrant", "vector", "database"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
