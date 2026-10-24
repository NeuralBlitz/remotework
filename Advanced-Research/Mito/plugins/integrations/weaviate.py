"""Weaviate Vector DB Plugin"""
import os
from typing import Dict, List

class WeaviateClient:
    def __init__(self, url: str = None, api_key: str = None):
        self.url = (url or os.environ.get("WEAVIATE_URL", "http://localhost:8080")).rstrip("/")
        self.api_key = api_key or os.environ.get("WEAVIATE_API_KEY", "")
    def _headers(self):
        h = {"Content-Type": "application/json"}
        if self.api_key: h["Authorization"] = f"Bearer {self.api_key}"
        return h
    def list_classes(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.url}/v1/schema", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("classes", [])
    def create_class(self, name: str, properties: List[Dict] = None) -> Dict:
        import requests
        payload = {"class": name, "properties": properties or []}
        resp = requests.post(f"{self.url}/v1/schema", headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def query(self, class_name: str, fields: str = "*", limit: int = 10) -> List[Dict]:
        import requests
        gql = f'{{ Get {{ {class_name}({fields}) }} }}'
        resp = requests.post(f"{self.url}/v1/graphql", headers=self._headers(), json={"query": gql}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", {}).get("Get", {}).get(class_name, [])

def register(plugin): plugin.set_resource("client_class", WeaviateClient)
weaviate_plugin = {"metadata": {"name": "weaviate", "version": "1.0.0", "description": "Weaviate vector database", "author": "Mito Team", "license": "MIT", "tags": ["weaviate", "vector", "database"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
