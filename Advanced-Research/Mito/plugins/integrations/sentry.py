"""Sentry Error Tracking Plugin - Issues, events, projects via API"""
import os
from typing import Dict, List

class SentryClient:
    def __init__(self, token: str = None, org: str = None):
        self.token = token or os.environ.get("SENTRY_TOKEN", "")
        self.org = org or os.environ.get("SENTRY_ORG", "")
        self.base_url = "https://sentry.io/api/0"
    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}
    def list_projects(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/organizations/{self.org}/projects/", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_issues(self, project: str, query: str = "is:unresolved", limit: int = 25) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/projects/{self.org}/{project}/issues/", headers=self._headers(), params={"query": query, "limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def get_issue(self, issue_id: str) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/issues/{issue_id}/", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def resolve_issue(self, issue_id: str) -> Dict:
        import requests
        resp = requests.put(f"{self.base_url}/issues/{issue_id}/", headers=self._headers(), json={"status": "resolved"}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_events(self, project: str, limit: int = 25) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/projects/{self.org}/{project}/events/", headers=self._headers(), params={"limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json()

def register(plugin):
    plugin.set_resource("client_class", SentryClient)

sentry_plugin = {"metadata": {"name": "sentry", "version": "1.0.0", "description": "Sentry - Issues, events, error tracking", "author": "Mito Team", "license": "MIT", "tags": ["sentry", "errors", "monitoring"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
