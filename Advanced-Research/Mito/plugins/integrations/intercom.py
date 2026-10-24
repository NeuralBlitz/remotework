"""
Intercom Customer Support Plugin
Conversations, contacts, companies, notes via API
"""

import os
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.intercom")


class IntercomClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("INTERCOM_TOKEN", "")
        self.base_url = "https://api.intercom.io"

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}

    def list_contacts(self, per_page: int = 50) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/contacts", headers=self._headers(),
                             params={"per_page": per_page}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", [])

    def create_contact(self, email: str, name: str = "", custom_attrs: Dict = None) -> Dict:
        import requests
        data = {"email": email}
        if name:
            data["name"] = name
        if custom_attrs:
            data["custom_attributes"] = custom_attrs
        resp = requests.post(f"{self.base_url}/contacts", headers=self._headers(), json=data, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_conversations(self, per_page: int = 50) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/conversations", headers=self._headers(),
                             params={"per_page": per_page}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("conversations", [])

    def reply_to_conversation(self, conversation_id: str, message: str, message_type: str = "comment") -> Dict:
        import requests
        data = {"message_type": message_type, "type": "admin", "body": message}
        resp = requests.post(f"{self.base_url}/conversations/{conversation_id}/reply",
                              headers=self._headers(), json=data, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def add_note(self, contact_id: str, body: str) -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/contacts/{contact_id}/notes",
                              headers=self._headers(), json={"body": body}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def search(self, query: str) -> List[Dict]:
        import requests
        resp = requests.post(f"{self.base_url}/contacts/search",
                              headers=self._headers(), json={"query": {"field": "name", "operator": "~", "value": query}}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", [])


def register(plugin):
    plugin.register_command("intercom_list_contacts", lambda: IntercomClient().list_contacts())
    plugin.register_command("intercom_create_contact", lambda email="", name="": IntercomClient().create_contact(email, name))
    plugin.set_resource("client_class", IntercomClient)


intercom_plugin = {
    "metadata": {"name": "intercom", "version": "1.0.0", "description": "Intercom - Conversations, contacts, notes",
                 "author": "Mito Team", "license": "MIT", "tags": ["intercom", "support", "chat"],
                 "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"},
    "register": register,
}
