"""Elasticsearch Plugin"""
import os
from typing import Dict, List
class ElasticsearchClient:
    def __init__(self, url: str = None, api_key: str = None):
        self.url = (url or os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200")).rstrip("/")
        self.api_key = api_key or os.environ.get("ELASTICSEARCH_API_KEY", "")
    def _headers(self):
        h = {"Content-Type": "application/json"}
        if self.api_key: h["Authorization"] = f"ApiKey {self.api_key}"
        return h
    def search(self, index: str, query: Dict, size: int = 10) -> List[Dict]:
        import requests
        resp = requests.post(f"{self.url}/{index}/_search", headers=self._headers(), json={"query": query, "size": size}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("hits", {}).get("hits", [])
    def index(self, index: str, document: Dict, doc_id: str = None) -> Dict:
        import requests
        url = f"{self.url}/{index}/_doc"
        if doc_id: url += f"/{doc_id}"
        resp = requests.post(url, headers=self._headers(), json=document, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def delete_by_query(self, index: str, query: Dict) -> Dict:
        import requests
        resp = requests.post(f"{self.url}/{index}/_delete_by_query", headers=self._headers(), json={"query": query}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_indices(self) -> List[str]:
        import requests
        resp = requests.get(f"{self.url}/_cat/indices?format=json", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return [i["index"] for i in resp.json()]
def register(plugin): plugin.set_resource("client_class", ElasticsearchClient)
elasticsearch_plugin = {"metadata": {"name": "elasticsearch", "version": "1.0.0", "description": "Elasticsearch - Full-text search", "author": "Mito Team", "license": "MIT", "tags": ["elasticsearch", "search", "database"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
