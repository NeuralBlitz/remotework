"""Meilisearch Plugin"""
import os
from typing import Dict, List
class MeilisearchClient:
    def __init__(self, url: str = None, api_key: str = None):
        self.url = (url or os.environ.get("MEILISEARCH_URL", "http://localhost:7700")).rstrip("/")
        self.api_key = api_key or os.environ.get("MEILISEARCH_API_KEY", "")
    def _headers(self):
        h = {"Content-Type": "application/json"}
        if self.api_key: h["Authorization"] = f"Bearer {self.api_key}"
        return h
    def search(self, index: str, query: str, limit: int = 20) -> Dict:
        import requests
        resp = requests.post(f"{self.url}/indexes/{index}/search", headers=self._headers(), json={"q": query, "limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def add_documents(self, index: str, documents: List[Dict]) -> Dict:
        import requests
        resp = requests.post(f"{self.url}/indexes/{index}/documents", headers=self._headers(), json=documents, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_indexes(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.url}/indexes", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("results", [])
def register(plugin): plugin.set_resource("client_class", MeilisearchClient)
meilisearch_plugin = {"metadata": {"name": "meilisearch", "version": "1.0.0", "description": "Meilisearch - Fast full-text search", "author": "Mito Team", "license": "MIT", "tags": ["meilisearch", "search"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
