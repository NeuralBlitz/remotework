"""LaunchDarkly Feature Flags Plugin - Flags, segments, users via API"""
import os
from typing import Dict, List

class LaunchDarklyClient:
    def __init__(self, token: str = None):
        self.token = token or os.environ.get("LAUNCHDARKLY_TOKEN", "")
        self.base_url = "https://app.launchdarkly.com/api/v2"
    def _headers(self) -> Dict[str, str]:
        return {"Authorization": self.token, "Content-Type": "application/json"}
    def list_flags(self, project: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/flags/{project}", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("items", [])
    def get_flag(self, project: str, flag_key: str) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/flags/{project}/{flag_key}", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def toggle_flag(self, project: str, flag_key: str, env: str, on: bool) -> Dict:
        import requests
        resp = requests.patch(f"{self.base_url}/flags/{project}/{flag_key}", headers=self._headers(),
                               json={"patch": [{"op": "replace", "path": f"/environments/{env}/on", "value": on}]}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_projects(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/projects", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("items", [])

def register(plugin):
    plugin.set_resource("client_class", LaunchDarklyClient)

launchdarkly_plugin = {"metadata": {"name": "launchdarkly", "version": "1.0.0", "description": "LaunchDarkly - Feature flags, segments", "author": "Mito Team", "license": "MIT", "tags": ["launchdarkly", "feature-flags"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
