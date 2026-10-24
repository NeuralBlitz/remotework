"""Okta Plugin - Users, groups, applications via API"""
import os
from typing import Dict, List

class OktaClient:
    def __init__(self, domain: str = None, token: str = None):
        self.domain = domain or os.environ.get("OKTA_DOMAIN", "")
        self.token = token or os.environ.get("OKTA_TOKEN", "")
        self.base_url = f"https://{self.domain}/api/v1"
    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"SSWS {self.token}", "Content-Type": "application/json"}
    def list_users(self, limit: int = 25) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/users", headers=self._headers(), params={"limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def create_user(self, email: str, first_name: str, last_name: str, login: str = None) -> Dict:
        import requests
        payload = {"profile": {"email": email, "firstName": first_name, "lastName": last_name, "login": login or email}}
        resp = requests.post(f"{self.base_url}/users", headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def deactivate_user(self, user_id: str) -> bool:
        import requests
        resp = requests.post(f"{self.base_url}/users/{user_id}/lifecycle/deactivate", headers=self._headers(), timeout=30)
        return resp.ok
    def list_groups(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/groups", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def add_user_to_group(self, user_id: str, group_id: str) -> bool:
        import requests
        resp = requests.put(f"{self.base_url}/groups/{group_id}/users/{user_id}", headers=self._headers(), timeout=30)
        return resp.ok

def register(plugin): plugin.set_resource("client_class", OktaClient)

okta_plugin = {"metadata": {"name": "okta", "version": "1.0.0", "description": "Okta - Users, groups, applications", "author": "Mito Team", "license": "MIT", "tags": ["okta", "auth", "identity", "sso"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
