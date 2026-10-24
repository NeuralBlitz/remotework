"""
Mito HTTP Client
Production-ready REST client with retries, auth, rate limiting, logging
"""

import json
import time
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlencode

logger = logging.getLogger("mito.httpclient")


@dataclass
class Response:
    status_code: int
    headers: Dict[str, str]
    body: Any
    text: str
    elapsed: float
    url: str
    ok: bool = True

    def json(self) -> Any:
        return self.body

    def raise_for_status(self):
        if not self.ok:
            raise Exception(f"HTTP {self.status_code}: {self.text[:200]}")


class HTTPClient:
    def __init__(self, base_url: str = "", headers: Dict = None, auth: tuple = None,
                 timeout: int = 30, max_retries: int = 0, retry_delay: float = 1.0):
        self.base_url = base_url.rstrip("/")
        self.default_headers = headers or {}
        self.auth = auth
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._session = None

    def _get_session(self):
        if self._session is None:
            import requests
            self._session = requests.Session()
            self._session.headers.update(self.default_headers)
            if self.auth:
                self._session.auth = self.auth
        return self._session

    def _request(self, method: str, path: str, params: Dict = None, data: Any = None,
                 json_data: Any = None, headers: Dict = None, files: Dict = None,
                 stream: bool = False) -> Response:
        import requests
        url = f"{self.base_url}{path}" if self.base_url else path
        session = self._get_session()

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                start = time.time()
                resp = session.request(
                    method, url, params=params, data=data, json=json_data,
                    headers=headers, files=files, timeout=self.timeout, stream=stream,
                )
                elapsed = time.time() - start

                try:
                    body = resp.json()
                except Exception:
                    body = None

                return Response(
                    status_code=resp.status_code,
                    headers=dict(resp.headers),
                    body=body,
                    text=resp.text,
                    elapsed=elapsed,
                    url=url,
                    ok=resp.ok,
                )
            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (attempt + 1))
                    logger.warning(f"Request attempt {attempt + 1} failed: {e}")

        raise last_error

    def get(self, path: str, params: Dict = None, **kwargs) -> Response:
        return self._request("GET", path, params=params, **kwargs)

    def post(self, path: str, json_data: Any = None, data: Any = None, **kwargs) -> Response:
        return self._request("POST", path, json_data=json_data, data=data, **kwargs)

    def put(self, path: str, json_data: Any = None, **kwargs) -> Response:
        return self._request("PUT", path, json_data=json_data, **kwargs)

    def patch(self, path: str, json_data: Any = None, **kwargs) -> Response:
        return self._request("PATCH", path, json_data=json_data, **kwargs)

    def delete(self, path: str, **kwargs) -> Response:
        return self._request("DELETE", path, **kwargs)

    def head(self, path: str, **kwargs) -> Response:
        return self._request("HEAD", path, **kwargs)

    def upload(self, path: str, file_path: str, field_name: str = "file",
               extra_data: Dict = None) -> Response:
        with open(file_path, "rb") as f:
            files = {field_name: f}
            return self._request("POST", path, files=files, data=extra_data)

    def download(self, path: str, dest_path: str) -> str:
        import requests
        url = f"{self.base_url}{path}" if self.base_url else path
        resp = requests.get(url, stream=True, timeout=self.timeout)
        resp.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return dest_path

    def close(self):
        if self._session:
            self._session.close()
            self._session = None


class GraphQLClient:
    def __init__(self, endpoint: str, headers: Dict = None, timeout: int = 30):
        self.endpoint = endpoint
        self.default_headers = headers or {"Content-Type": "application/json"}
        self.timeout = timeout

    def execute(self, query: str, variables: Dict = None, operation_name: str = None) -> Dict:
        import requests
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        if operation_name:
            payload["operationName"] = operation_name
        resp = requests.post(self.endpoint, json=payload, headers=self.default_headers,
                              timeout=self.timeout)
        resp.raise_for_status()
        result = resp.json()
        if "errors" in result:
            raise Exception(f"GraphQL errors: {result['errors']}")
        return result.get("data", {})

    def query(self, query: str, variables: Dict = None) -> Dict:
        return self.execute(query, variables)

    def mutation(self, mutation: str, variables: Dict = None) -> Dict:
        return self.execute(mutation, variables)

    def subscribe(self, query: str, variables: Dict = None):
        raise NotImplementedError("Subscriptions require WebSocket support")


class APIClient:
    """Convenience wrapper for common API patterns."""

    def __init__(self, base_url: str, token: str = "", token_type: str = "Bearer",
                 api_key: str = "", api_key_header: str = "X-API-Key"):
        headers = {}
        if token:
            headers["Authorization"] = f"{token_type} {token}"
        if api_key:
            headers[api_key_header] = api_key
        self.client = HTTPClient(base_url, headers=headers, max_retries=2)

    def list(self, resource: str, params: Dict = None, limit: int = 50) -> List[Dict]:
        p = {"limit": limit}
        if params:
            p.update(params)
        resp = self.client.get(f"/{resource}", params=p)
        resp.raise_for_status()
        return resp.body if isinstance(resp.body, list) else resp.body.get("data", [])

    def get(self, resource: str, id: str) -> Dict:
        resp = self.client.get(f"/{resource}/{id}")
        resp.raise_for_status()
        return resp.body if isinstance(resp.body, dict) else resp.body

    def create(self, resource: str, data: Dict) -> Dict:
        resp = self.client.post(f"/{resource}", json_data=data)
        resp.raise_for_status()
        return resp.body

    def update(self, resource: str, id: str, data: Dict) -> Dict:
        resp = self.client.patch(f"/{resource}/{id}", json_data=data)
        resp.raise_for_status()
        return resp.body

    def delete(self, resource: str, id: str) -> bool:
        resp = self.client.delete(f"/{resource}/{id}")
        return resp.ok
