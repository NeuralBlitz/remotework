"""
WhatsApp Business API Plugin
Messages, templates, media via WhatsApp Cloud API
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.whatsapp")


class WhatsAppClient:
    def __init__(self, token: Optional[str] = None, phone_id: Optional[str] = None):
        self.token = token or os.environ.get("WHATSAPP_TOKEN", "")
        self.phone_id = phone_id or os.environ.get("WHATSAPP_PHONE_ID", "")
        self.base_url = f"https://graph.facebook.com/v18.0/{self.phone_id}"

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _request(self, data: Dict) -> Any:
        import requests
        resp = requests.post(f"{self.base_url}/messages",
                              headers=self._headers(), json=data, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def send_text(self, to: str, text: str, preview_url: bool = False) -> Dict:
        return self._request({
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text, "preview_url": preview_url},
        })

    def send_template(self, to: str, template_name: str, language: str = "en",
                      components: List[Dict] = None) -> Dict:
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language},
            },
        }
        if components:
            payload["template"]["components"] = components
        return self._request(payload)

    def send_image(self, to: str, image_url: str, caption: str = "") -> Dict:
        return self._request({
            "messaging_product": "whatsapp",
            "to": to,
            "type": "image",
            "image": {"link": image_url, "caption": caption},
        })

    def send_document(self, to: str, doc_url: str, filename: str = "",
                      caption: str = "") -> Dict:
        return self._request({
            "messaging_product": "whatsapp",
            "to": to,
            "type": "document",
            "document": {"link": doc_url, "filename": filename, "caption": caption},
        })

    def send_location(self, to: str, latitude: float, longitude: float,
                      name: str = "", address: str = "") -> Dict:
        return self._request({
            "messaging_product": "whatsapp",
            "to": to,
            "type": "location",
            "location": {
                "latitude": latitude, "longitude": longitude,
                "name": name, "address": address,
            },
        })

    def send_interactive(self, to: str, body: str, buttons: List[Dict]) -> Dict:
        return self._request({
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body},
                "action": {"buttons": buttons},
            },
        })

    def mark_read(self, message_id: str) -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/messages",
                              headers=self._headers(),
                              json={"messaging_product": "whatsapp", "status": "read",
                                    "message_id": message_id},
                              timeout=10)
        return resp.json()


def whatsapp_send_cmd(to: str = "", text: str = "") -> Dict:
    """Send a WhatsApp message."""
    client = WhatsAppClient()
    return client.send_text(to, text)


def whatsapp_template_cmd(to: str = "", template: str = "") -> Dict:
    """Send a WhatsApp template message."""
    client = WhatsAppClient()
    return client.send_template(to, template)


def register(plugin):
    plugin.register_command("whatsapp_send", whatsapp_send_cmd)
    plugin.register_command("whatsapp_template", whatsapp_template_cmd)
    plugin.set_resource("client_class", WhatsAppClient)


PLUGIN_METADATA = {
    "name": "whatsapp",
    "version": "1.0.0",
    "description": "WhatsApp Business API - Messages, templates, media",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["whatsapp", "messaging", "business"],
    "dependencies": [],
    "permissions": ["network_access", "read_env"],
    "min_mito_version": "1.0.0",
}


whatsapp_plugin = {"metadata": PLUGIN_METADATA, "register": register}
