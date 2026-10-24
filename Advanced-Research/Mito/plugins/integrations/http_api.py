"""
HTTP API Plugin
Generic HTTP client for REST APIs - GET, POST, PUT, DELETE, PATCH.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.http_api")


class HTTPAPIClient:
    def __init__(self, base_url: str = None, headers: Dict = None, auth_token: str = None):
        self.base_url = (base_url or "").rstrip("/")
        self.default_headers = headers or {}
        self.auth_token = auth_token or os.environ.get("API_TOKEN", "")

    def _headers(self, extra: Dict = None) -> Dict:
        h = dict(self.default_headers)
        if self.auth_token:
            h["Authorization"] = f"Bearer {self.auth_token}"
        if extra:
            h.update(extra)
        return h

    def _url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(self, method: str, url: str, data: Any = None,
                 params: Dict = None, headers: Dict = None) -> Dict:
        import requests
        url = self._url(url)
        kwargs = {"headers": self._headers(headers), "params": params or {}, "timeout": 30}

        if data is not None:
            if isinstance(data, dict):
                kwargs["json"] = data
            else:
                kwargs["data"] = data

        try:
            resp = requests.request(method.upper(), url, **kwargs)
            content_type = resp.headers.get("Content-Type", "")
            try:
                if "application/json" in content_type:
                    body = resp.json()
                else:
                    body = resp.text
            except Exception:
                body = resp.text

            return {
                "status_code": resp.status_code,
                "ok": resp.ok,
                "headers": dict(resp.headers),
                "body": body,
                "text": resp.text[:500] if hasattr(resp, "text") else "",
            }
        except requests.exceptions.Timeout:
            return {"status_code": 0, "ok": False, "error": "Request timed out", "body": None}
        except requests.exceptions.ConnectionError as e:
            return {"status_code": 0, "ok": False, "error": f"Connection error: {e}", "body": None}
        except Exception as e:
            return {"status_code": 0, "ok": False, "error": str(e), "body": None}

    def get(self, path: str, params: Dict = None, headers: Dict = None) -> Dict:
        return self._request("GET", path, params=params, headers=headers)

    def post(self, path: str, data: Any = None, params: Dict = None, headers: Dict = None) -> Dict:
        return self._request("POST", path, data=data, params=params, headers=headers)

    def put(self, path: str, data: Any = None, params: Dict = None, headers: Dict = None) -> Dict:
        return self._request("PUT", path, data=data, params=params, headers=headers)

    def patch(self, path: str, data: Any = None, params: Dict = None, headers: Dict = None) -> Dict:
        return self._request("PATCH", path, data=data, params=params, headers=headers)

    def delete(self, path: str, params: Dict = None, headers: Dict = None) -> Dict:
        return self._request("DELETE", path, params=params, headers=headers)

    def head(self, path: str, params: Dict = None, headers: Dict = None) -> Dict:
        return self._request("HEAD", path, params=params, headers=headers)

    def batch(self, requests: List[Dict]) -> List[Dict]:
        results = []
        for req in requests:
            method = req.get("method", "GET").upper()
            path = req.get("path", "")
            data = req.get("data")
            params = req.get("params")
            headers = req.get("headers")
            results.append(self._request(method, path, data=data, params=params, headers=headers))
        return results


def http_get_cmd(url: str = "", params: str = "{}") -> Dict:
    """Send a GET request."""
    client = HTTPAPIClient()
    return client.get(url, params=json.loads(params) if params else None)


def http_post_cmd(url: str = "", data: str = "{}", params: str = "{}") -> Dict:
    """Send a POST request with JSON body."""
    client = HTTPAPIClient()
    return client.post(url, data=json.loads(data), params=json.loads(params) if params else None)


def http_put_cmd(url: str = "", data: str = "{}") -> Dict:
    """Send a PUT request with JSON body."""
    client = HTTPAPIClient()
    return client.put(url, data=json.loads(data))


def http_delete_cmd(url: str = "") -> Dict:
    """Send a DELETE request."""
    return HTTPAPIClient().delete(url)


def http_head_cmd(url: str = "") -> Dict:
    """Send a HEAD request to check resource availability."""
    return HTTPAPIClient().head(url)


def register(plugin):
    plugin.register_command("http_get", http_get_cmd)
    plugin.register_command("http_post", http_post_cmd)
    plugin.register_command("http_put", http_put_cmd)
    plugin.register_command("http_delete", http_delete_cmd)
    plugin.register_command("http_head", http_head_cmd)
    plugin.set_resource("client_class", HTTPAPIClient)


PLUGIN_METADATA = {
    "name": "http_api",
    "version": "1.0.0",
    "description": "HTTP client - GET, POST, PUT, DELETE, PATCH for REST APIs",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["http", "rest", "api", "client", "request"],
    "dependencies": [],
    "permissions": ["network_access"],
    "min_mito_version": "1.0.1",
}


http_api_plugin = {"metadata": PLUGIN_METADATA, "register": register}
