"""
Notion Integration Plugin
Pages, databases, search via Notion API
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.notion")


class NotionClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("NOTION_TOKEN", "")
        self.base_url = "https://api.notion.com/v1"
        self.version = "2022-06-28"

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.version,
            "Content-Type": "application/json",
        }

    def _request(self, method: str, path: str, data: Dict = None, params: Dict = None) -> Any:
        import requests
        url = f"{self.base_url}{path}"
        resp = requests.request(method, url, headers=self._headers(), json=data, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_page(self, page_id: str) -> Dict:
        return self._request("GET", f"/pages/{page_id}")

    def create_page(self, parent_id: str, title: str, properties: Dict = None,
                    children: List[Dict] = None, parent_type: str = "database_id") -> Dict:
        payload = {
            "parent": {parent_type: parent_id},
            "properties": {
                "title": {"title": [{"text": {"content": title}}]}
            },
        }
        if properties:
            payload["properties"].update(properties)
        if children:
            payload["children"] = children
        return self._request("POST", "/pages", payload)

    def update_page(self, page_id: str, properties: Dict) -> Dict:
        return self._request("PATCH", f"/pages/{page_id}", {"properties": properties})

    def archive_page(self, page_id: str) -> Dict:
        return self._request("PATCH", f"/pages/{page_id}", {"archived": True})

    def get_block_children(self, block_id: str, page_size: int = 100) -> List[Dict]:
        result = self._request("GET", f"/blocks/{block_id}/children",
                                params={"page_size": page_size})
        return result.get("results", [])

    def append_block_children(self, block_id: str, children: List[Dict]) -> Dict:
        return self._request("PATCH", f"/blocks/{block_id}/children", {"children": children})

    def get_database(self, database_id: str) -> Dict:
        return self._request("GET", f"/databases/{database_id}")

    def query_database(self, database_id: str, filter_obj: Dict = None,
                       sorts: List[Dict] = None, page_size: int = 100) -> List[Dict]:
        payload = {"page_size": page_size}
        if filter_obj:
            payload["filter"] = filter_obj
        if sorts:
            payload["sorts"] = sorts
        result = self._request("POST", f"/databases/{database_id}/query", payload)
        return result.get("results", [])

    def create_database(self, parent_id: str, title: str, properties: Dict) -> Dict:
        payload = {
            "parent": {"type": "page_id", "page_id": parent_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties,
        }
        return self._request("POST", "/databases", payload)

    def search(self, query: str, filter_type: str = None, page_size: int = 100) -> List[Dict]:
        payload = {"query": query, "page_size": page_size}
        if filter_type:
            payload["filter"] = {"value": filter_type, "property": "object"}
        result = self._request("POST", "/search", payload)
        return result.get("results", [])

    def get_users(self, page_size: int = 100) -> List[Dict]:
        result = self._request("GET", "/users", params={"page_size": page_size})
        return result.get("results", [])


def notion_get_page_cmd(page_id: str = "") -> Dict:
    """Get a Notion page by ID."""
    client = NotionClient()
    return client.get_page(page_id)


def notion_create_page_cmd(parent_id: str = "", title: str = "") -> Dict:
    """Create a new Notion page."""
    client = NotionClient()
    return client.create_page(parent_id, title)


def notion_search_cmd(query: str = "") -> List[Dict]:
    """Search across Notion workspace."""
    client = NotionClient()
    return client.search(query)


def notion_query_database_cmd(database_id: str = "") -> List[Dict]:
    """Query a Notion database."""
    client = NotionClient()
    return client.query_database(database_id)


def register(plugin):
    plugin.register_command("notion_get_page", notion_get_page_cmd)
    plugin.register_command("notion_create_page", notion_create_page_cmd)
    plugin.register_command("notion_search", notion_search_cmd)
    plugin.register_command("notion_query_database", notion_query_database_cmd)
    plugin.set_resource("client_class", NotionClient)


PLUGIN_METADATA = {
    "name": "notion",
    "version": "1.0.0",
    "description": "Notion integration - Pages, databases, search",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["notion", "docs", "wiki", "databases"],
    "dependencies": [],
    "permissions": ["network_access", "read_env"],
    "min_mito_version": "1.0.0",
}


notion_plugin = {
    "metadata": PLUGIN_METADATA,
    "register": register,
}
