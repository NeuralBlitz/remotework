"""
Salesforce CRM Plugin
Leads, contacts, opportunities, queries via REST API
"""

import os
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.salesforce")


class SalesforceClient:
    def __init__(self, instance_url: str = None, token: str = None):
        self.instance_url = (instance_url or os.environ.get("SF_INSTANCE_URL", "")).rstrip("/")
        self.token = token or os.environ.get("SF_TOKEN", "")

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def query(self, soql: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.instance_url}/services/data/v58.0/query",
                             headers=self._headers(), params={"q": soql}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("records", [])

    def create(self, obj_type: str, data: Dict) -> Dict:
        import requests
        resp = requests.post(f"{self.instance_url}/services/data/v58.0/sobjects/{obj_type}",
                              headers=self._headers(), json=data, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def update(self, obj_type: str, obj_id: str, data: Dict) -> bool:
        import requests
        resp = requests.patch(f"{self.instance_url}/services/data/v58.0/sobjects/{obj_type}/{obj_id}",
                               headers=self._headers(), json=data, timeout=30)
        return resp.status_code == 204

    def get(self, obj_type: str, obj_id: str) -> Dict:
        import requests
        resp = requests.get(f"{self.instance_url}/services/data/v58.0/sobjects/{obj_type}/{obj_id}",
                             headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def delete(self, obj_type: str, obj_id: str) -> bool:
        import requests
        resp = requests.delete(f"{self.instance_url}/services/data/v58.0/sobjects/{obj_type}/{obj_id}",
                                headers=self._headers(), timeout=30)
        return resp.status_code == 204

    def search(self, sosl: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.instance_url}/services/data/v58.0/search",
                             headers=self._headers(), params={"q": sosl}, timeout=30)
        resp.raise_for_status()
        return resp.json()


def register(plugin):
    plugin.register_command("sf_query", lambda soql="": SalesforceClient().query(soql))
    plugin.register_command("sf_create", lambda obj_type="", data="{}": SalesforceClient().create(obj_type, {}))
    plugin.set_resource("client_class", SalesforceClient)


salesforce_plugin = {
    "metadata": {"name": "salesforce", "version": "1.0.0", "description": "Salesforce CRM - Leads, contacts, opportunities",
                 "author": "Mito Team", "license": "MIT", "tags": ["salesforce", "crm", "sales"],
                 "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"},
    "register": register,
}
