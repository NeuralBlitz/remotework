"""
HubSpot CRM Plugin
Contacts, deals, companies, engagements via API
"""

import os
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.hubspot")


class HubSpotClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("HUBSPOT_TOKEN", "")
        self.base_url = "https://api.hubapi.com"

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def list_contacts(self, limit: int = 100, after: str = None) -> Dict:
        import requests
        params = {"limit": limit}
        if after:
            params["after"] = after
        resp = requests.get(f"{self.base_url}/crm/v3/objects/contacts",
                             headers=self._headers(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def create_contact(self, properties: Dict) -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/crm/v3/objects/contacts",
                              headers=self._headers(), json={"properties": properties}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_contact(self, contact_id: str) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/crm/v3/objects/contacts/{contact_id}",
                             headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def search_contacts(self, query: str, limit: int = 20) -> List[Dict]:
        import requests
        payload = {"query": query, "limit": limit}
        resp = requests.post(f"{self.base_url}/crm/v3/objects/contacts/search",
                              headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json().get("results", [])

    def list_deals(self, limit: int = 100) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/crm/v3/objects/deals",
                             headers=self._headers(), params={"limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("results", [])

    def create_deal(self, properties: Dict) -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/crm/v3/objects/deals",
                              headers=self._headers(), json={"properties": properties}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_companies(self, limit: int = 100) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/crm/v3/objects/companies",
                             headers=self._headers(), params={"limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("results", [])

    def create_company(self, properties: Dict) -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/crm/v3/objects/companies",
                              headers=self._headers(), json={"properties": properties}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def send_email(self, contact_id: str, subject: str, body: str) -> Dict:
        import requests
        payload = {
            "email": {"subject": subject, "body": body, "to": contact_id}
        }
        resp = requests.post(f"{self.base_url}/crm/v3/objects/emails",
                              headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()


def register(plugin):
    plugin.register_command("hubspot_list_contacts", lambda limit=50: HubSpotClient().list_contacts(limit=limit))
    plugin.register_command("hubspot_create_contact", lambda props="{}": HubSpotClient().create_contact({}))
    plugin.set_resource("client_class", HubSpotClient)


hubspot_plugin = {
    "metadata": {"name": "hubspot", "version": "1.0.0", "description": "HubSpot CRM - Contacts, deals, companies",
                 "author": "Mito Team", "license": "MIT", "tags": ["hubspot", "crm", "marketing"],
                 "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"},
    "register": register,
}
