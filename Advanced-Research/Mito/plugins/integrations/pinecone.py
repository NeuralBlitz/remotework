"""Pinecone Vector DB Plugin"""
import os
from typing import Dict, List

class PineconeClient:
    def __init__(self, api_key: str = None, environment: str = None):
        self.api_key = api_key or os.environ.get("PINECONE_API_KEY", "")
        self.environment = environment or os.environ.get("PINECONE_ENV", "us-east-1")
        self.base_url = f"https://controller.{self.environment}.pinecone.io"
    def _headers(self): return {"Api-Key": self.api_key, "Content-Type": "application/json"}
    def list_indexes(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/databases", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def create_index(self, name: str, dimension: int, metric: str = "cosine") -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/databases", headers=self._headers(), json={"name": name, "dimension": dimension, "metric": metric}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def delete_index(self, name: str) -> bool:
        import requests
        resp = requests.delete(f"{self.base_url}/databases/{name}", headers=self._headers(), timeout=30)
        return resp.ok

def register(plugin): plugin.set_resource("client_class", PineconeClient)
pinecone_plugin = {"metadata": {"name": "pinecone", "version": "1.0.0", "description": "Pinecone vector database", "author": "Mito Team", "license": "MIT", "tags": ["pinecone", "vector", "database"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
