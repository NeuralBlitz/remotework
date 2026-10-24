"""
Zendesk Support Plugin
Tickets, users, organizations via REST API
"""

import os
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.zendesk")


class ZendeskClient:
    def __init__(self, subdomain: str = None, email: str = None, api_token: str = None):
        self.subdomain = subdomain or os.environ.get("ZENDESK_SUBDOMAIN", "")
        self.email = email or os.environ.get("ZENDESK_EMAIL", "")
        self.api_token = api_token or os.environ.get("ZENDESK_API_TOKEN", "")
        self.base_url = f"https://{self.subdomain}.zendesk.com/api/v2"

    def _auth(self):
        return (f"{self.email}/token", self.api_token)

    def list_tickets(self, status: str = None, per_page: int = 50) -> List[Dict]:
        import requests
        params = {"per_page": per_page}
        if status:
            params["status"] = status
        resp = requests.get(f"{self.base_url}/tickets", auth=self._auth(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("tickets", [])

    def create_ticket(self, subject: str, comment: str, requester_email: str = "",
                      priority: str = "normal", ticket_type: str = "question") -> Dict:
        import requests
        payload = {"ticket": {
            "subject": subject,
            "comment": {"body": comment},
            "priority": priority,
            "type": ticket_type,
        }}
        if requester_email:
            payload["ticket"]["requester"] = {"email": requester_email}
        resp = requests.post(f"{self.base_url}/tickets", auth=self._auth(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_ticket(self, ticket_id: int) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/tickets/{ticket_id}", auth=self._auth(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def update_ticket(self, ticket_id: int, data: Dict) -> Dict:
        import requests
        resp = requests.put(f"{self.base_url}/tickets/{ticket_id}", auth=self._auth(),
                             json={"ticket": data}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def add_comment(self, ticket_id: int, body: str, public: bool = True) -> Dict:
        return self.update_ticket(ticket_id, {"comment": {"body": body, "public": public}})

    def search(self, query: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/search", auth=self._auth(),
                             params={"query": query}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("results", [])

    def list_users(self, role: str = None) -> List[Dict]:
        import requests
        params = {}
        if role:
            params["role"] = role
        resp = requests.get(f"{self.base_url}/users", auth=self._auth(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("users", [])


def register(plugin):
    plugin.register_command("zendesk_list_tickets", lambda status="open": ZendeskClient().list_tickets(status=status))
    plugin.register_command("zendesk_create_ticket", lambda subject="", comment="": ZendeskClient().create_ticket(subject, comment))
    plugin.register_command("zendesk_search", lambda query="": ZendeskClient().search(query))
    plugin.set_resource("client_class", ZendeskClient)


zendesk_plugin = {
    "metadata": {"name": "zendesk", "version": "1.0.0", "description": "Zendesk - Tickets, users, search",
                 "author": "Mito Team", "license": "MIT", "tags": ["zendesk", "support", "tickets"],
                 "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"},
    "register": register,
}
