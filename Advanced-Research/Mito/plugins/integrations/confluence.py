"""
Confluence Wiki Plugin
Pages, spaces, search via REST API
"""
import os
from typing import Dict, List

class ConfluenceClient:
    def __init__(self, base_url: str = None, email: str = None, api_token: str = None):
        self.base_url = (base_url or os.environ.get("CONFLUENCE_URL", "")).rstrip("/")
        self.email = email or os.environ.get("CONFLUENCE_EMAIL", "")
        self.api_token = api_token or os.environ.get("CONFLUENCE_TOKEN", "")

    def _auth(self):
        return (self.email, self.api_token)

    def search(self, cql: str, limit: int = 25) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/wiki/rest/api/search", auth=self._auth(),
                             params={"cql": cql, "limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("results", [])

    def get_page(self, page_id: str) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/wiki/rest/api/content/{page_id}",
                             auth=self._auth(), params={"expand": "body.storage,version"}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def create_page(self, space_key: str, title: str, body: str, parent_id: str = None) -> Dict:
        import requests
        payload = {"type": "page", "title": title, "space": {"key": space_key},
                   "body": {"storage": {"value": body, "representation": "storage"}}}
        if parent_id:
            payload["ancestors"] = [{"id": parent_id}]
        resp = requests.post(f"{self.base_url}/wiki/rest/api/content",
                              auth=self._auth(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def update_page(self, page_id: str, title: str, body: str, version: int) -> Dict:
        import requests
        payload = {"type": "page", "title": title,
                   "body": {"storage": {"value": body, "representation": "storage"}},
                   "version": {"number": version + 1}}
        resp = requests.put(f"{self.base_url}/wiki/rest/api/content/{page_id}",
                             auth=self._auth(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_spaces(self, limit: int = 50) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/wiki/rest/api/space",
                             auth=self._auth(), params={"limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("results", [])

def register(plugin):
    plugin.set_resource("client_class", ConfluenceClient)

confluence_plugin = {
    "metadata": {"name": "confluence", "version": "1.0.0", "description": "Confluence - Pages, spaces, search",
                 "author": "Mito Team", "license": "MIT", "tags": ["confluence", "wiki", "docs"],
                 "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"},
    "register": register,
}
