"""
Microsoft Teams Integration Plugin
Messages, channels, adaptive cards via Graph API and webhooks
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.teams")


class TeamsClient:
    def __init__(self, webhook_url: Optional[str] = None, token: Optional[str] = None):
        self.webhook_url = webhook_url or os.environ.get("TEAMS_WEBHOOK_URL", "")
        self.token = token or os.environ.get("TEAMS_TOKEN", "")
        self.graph_url = "https://graph.microsoft.com/v1.0"

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def send_webhook(self, title: str, text: str, sections: List[Dict] = None,
                     actions: List[Dict] = None) -> bool:
        import requests
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "summary": title,
            "themeColor": "0076D7",
            "title": title,
            "text": text,
        }
        if sections:
            payload["sections"] = sections
        if actions:
            payload["potentialAction"] = actions
        resp = requests.post(self.webhook_url, json=payload, timeout=10)
        return resp.status_code == 200

    def send_adaptive_card(self, card: Dict) -> bool:
        import requests
        payload = {"type": "message", "attachments": [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card,
        }]}
        resp = requests.post(self.webhook_url, json=payload, timeout=10)
        return resp.status_code == 200

    def get_teams(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.graph_url}/me/joinedTeams", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("value", [])

    def get_channels(self, team_id: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.graph_url}/teams/{team_id}/channels",
                             headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("value", [])

    def send_message(self, team_id: str, channel_id: str, content: str) -> Dict:
        import requests
        url = f"{self.graph_url}/teams/{team_id}/channels/{channel_id}/messages"
        resp = requests.post(url, headers=self._headers(),
                              json={"body": {"content": content}}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_messages(self, team_id: str, channel_id: str, limit: int = 50) -> List[Dict]:
        import requests
        url = f"{self.graph_url}/teams/{team_id}/channels/{channel_id}/messages"
        resp = requests.get(url, headers=self._headers(),
                             params={"$top": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("value", [])

    def create_adaptive_card_simple(self, title: str, body: str,
                                     actions: List[Dict] = None) -> Dict:
        card = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.4",
            "body": [
                {"type": "TextBlock", "text": title, "weight": "Bolder", "size": "Medium"},
                {"type": "TextBlock", "text": body, "wrap": True},
            ],
        }
        if actions:
            card["actions"] = actions
        return card


def teams_webhook_cmd(title: str = "", text: str = "") -> bool:
    """Send a message via Teams webhook."""
    client = TeamsClient()
    return client.send_webhook(title, text)


def teams_get_teams_cmd() -> List[Dict]:
    """List Teams."""
    client = TeamsClient()
    return client.get_teams()


def register(plugin):
    plugin.register_command("teams_webhook", teams_webhook_cmd)
    plugin.register_command("teams_get_teams", teams_get_teams_cmd)
    plugin.set_resource("client_class", TeamsClient)


PLUGIN_METADATA = {
    "name": "teams",
    "version": "1.0.0",
    "description": "Microsoft Teams - Messages, channels, adaptive cards",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["teams", "microsoft", "chat", "messaging"],
    "dependencies": [],
    "permissions": ["network_access", "read_env"],
    "min_mito_version": "1.0.0",
}


teams_plugin = {"metadata": PLUGIN_METADATA, "register": register}
