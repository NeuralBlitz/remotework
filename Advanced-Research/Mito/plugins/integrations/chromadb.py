"""ChromaDB Vector DB Plugin"""
import os
from typing import Dict, List
class ChromaDBClient:
    def __init__(self, host: str = None, port: int = None):
        self.host = host or os.environ.get("CHROMA_HOST", "localhost")
        self.port = port or int(os.environ.get("CHROMA_PORT", "8000"))
        self.base_url = f"http://{self.host}:{self.port}/api/v1"
    def list_collections(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/collections", timeout=30)
        resp.raise_for_status()
        return resp.json()
    def create_collection(self, name: str, metadata: Dict = None) -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/collections", json={"name": name, "metadata": metadata or {}}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def query(self, collection: str, query_embeddings: List[List[float]], n_results: int = 5) -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/collections/{collection}/query", json={"query_embeddings": query_embeddings, "n_results": n_results}, timeout=30)
        resp.raise_for_status()
        return resp.json()
def register(plugin): plugin.set_resource("client_class", ChromaDBClient)
chromadb_plugin = {"metadata": {"name": "chromadb", "version": "1.0.0", "description": "ChromaDB vector database", "author": "Mito Team", "license": "MIT", "tags": ["chromadb", "vector", "database"], "permissions": ["network_access"], "min_mito_version": "1.0.0"}, "register": register}
