"""
Webhooks Plugin
Receive and send webhooks with signature verification
"""

import os
import json
import hmac
import hashlib
import logging
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

logger = logging.getLogger("mito.plugins.webhooks")


class WebhookHandler:
    def __init__(self, secret: Optional[str] = None):
        self.secret = secret or os.environ.get("WEBHOOK_SECRET", "")
        self.routes: Dict[str, Dict[str, Callable]] = {}
        self.history: List[Dict] = []

    def register(self, path: str, method: str, handler: Callable):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method.upper()] = handler
        logger.info(f"Registered webhook: {method.upper()} {path}")

    def verify_signature(self, payload: bytes, signature: str) -> bool:
        if not self.secret:
            return True
        expected = hmac.new(self.secret.encode(), payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(f"sha256={expected}", signature)

    def handle(self, path: str, method: str, headers: Dict, body: bytes) -> Dict:
        signature = headers.get("X-Hub-Signature-256", headers.get("X-Signature", ""))
        if self.secret and not self.verify_signature(body, signature):
            return {"status": 401, "body": {"error": "Invalid signature"}}

        entry = {
            "path": path,
            "method": method,
            "timestamp": datetime.now().isoformat(),
            "headers": dict(headers),
            "body_size": len(body),
        }
        self.history.append(entry)

        if path in self.routes and method.upper() in self.routes[path]:
            try:
                data = json.loads(body) if body else {}
                result = self.routes[path][method.upper()](data, headers)
                entry["status"] = 200
                return {"status": 200, "body": result or {"ok": True}}
            except Exception as e:
                logger.error(f"Webhook handler error: {e}")
                entry["status"] = 500
                return {"status": 500, "body": {"error": str(e)}}

        entry["status"] = 404
        return {"status": 404, "body": {"error": "Not found"}}

    def get_history(self, limit: int = 50) -> List[Dict]:
        return self.history[-limit:]


class WebhookSender:
    def __init__(self, secret: Optional[str] = None):
        self.secret = secret or os.environ.get("WEBHOOK_SECRET", "")

    def sign_payload(self, payload: bytes) -> str:
        if not self.secret:
            return ""
        sig = hmac.new(self.secret.encode(), payload, hashlib.sha256).hexdigest()
        return f"sha256={sig}"

    def send(self, url: str, data: Dict, headers: Dict = None, method: str = "POST",
             timeout: int = 30) -> Dict:
        import requests
        body = json.dumps(data).encode()
        all_headers = {"Content-Type": "application/json"}
        if headers:
            all_headers.update(headers)
        if self.secret:
            all_headers["X-Hub-Signature-256"] = self.sign_payload(body)

        resp = requests.request(method, url, data=body, headers=all_headers, timeout=timeout)
        return {
            "status": resp.status_code,
            "body": resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text,
        }

    def send_github_style(self, url: str, event: str, data: Dict, delivery_id: str = None) -> Dict:
        import uuid
        headers = {
            "X-GitHub-Event": event,
            "X-GitHub-Delivery": delivery_id or str(uuid.uuid4()),
        }
        return self.send(url, data, headers)

    def send_slack_style(self, url: str, payload: Dict) -> Dict:
        return self.send(url, payload)


def webhooks_register_cmd(path: str = "/", method: str = "POST", callback: Callable = None) -> str:
    """Register a webhook endpoint."""
    handler = WebhookHandler()
    handler.register(path, method, callback or (lambda d, h: d))
    return f"Registered {method} {path}"


def webhooks_send_cmd(url: str = "", event: str = "", data: str = "{}") -> Dict:
    """Send a webhook to a URL."""
    sender = WebhookSender()
    return sender.send_github_style(url, event, json.loads(data) if isinstance(data, str) else data)


def register(plugin):
    plugin.register_command("webhooks_register", webhooks_register_cmd)
    plugin.register_command("webhooks_send", webhooks_send_cmd)
    plugin.set_resource("handler_class", WebhookHandler)
    plugin.set_resource("sender_class", WebhookSender)


PLUGIN_METADATA = {
    "name": "webhooks",
    "version": "1.0.0",
    "description": "Webhook handler and sender with HMAC signature verification",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["webhooks", "http", "events", "notifications"],
    "dependencies": [],
    "permissions": ["network_access"],
    "min_mito_version": "1.0.0",
}


webhooks_plugin = {
    "metadata": PLUGIN_METADATA,
    "register": register,
}
