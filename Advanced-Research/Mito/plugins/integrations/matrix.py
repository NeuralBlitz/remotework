"""
Matrix/Element Chat Plugin
Rooms, messages, sync via Matrix Client-Server API
"""
import os
from typing import Dict, List

class MatrixClient:
    def __init__(self, homeserver: str = None, token: str = None):
        self.homeserver = (homeserver or os.environ.get("MATRIX_HOMESERVER", "https://matrix.org")).rstrip("/")
        self.token = token or os.environ.get("MATRIX_TOKEN", "")
        self.base_url = f"{self.homeserver}/_matrix/client/v3"

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def send_message(self, room_id: str, text: str, msgtype: str = "m.text") -> Dict:
        import requests, uuid
        txn_id = str(uuid.uuid4())
        payload = {"msgtype": msgtype, "body": text}
        resp = requests.put(f"{self.base_url}/rooms/{room_id}/send/m.room.message/{txn_id}",
                             headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_messages(self, room_id: str, limit: int = 50) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/rooms/{room_id}/messages",
                             headers=self._headers(), params={"limit": limit, "dir": "b"}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("chunk", [])

    def join_room(self, room_id_or_alias: str) -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/join/{room_id_or_alias}", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_joined_rooms(self) -> List[str]:
        import requests
        resp = requests.get(f"{self.base_url}/joined_rooms", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("joined_rooms", [])

    def create_room(self, name: str, topic: str = "", is_public: bool = False) -> Dict:
        import requests
        payload = {"name": name, "topic": topic, "preset": "public_chat" if is_public else "private_chat"}
        resp = requests.post(f"{self.base_url}/createRoom", headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def sync(self, since: str = None, timeout: int = 30000) -> Dict:
        import requests
        params = {"timeout": timeout}
        if since:
            params["since"] = since
        resp = requests.get(f"{self.base_url}/sync", headers=self._headers(), params=params, timeout=timeout/1000 + 5)
        resp.raise_for_status()
        return resp.json()

    def upload_file(self, file_path: str, content_type: str = "application/octet-stream") -> str:
        import requests
        url = f"{self.homeserver}/_matrix/media/v3/upload"
        with open(file_path, "rb") as f:
            resp = requests.post(url, headers={"Authorization": f"Bearer {self.token}"},
                                  data=f, params={"filename": os.path.basename(file_path)},
                                  headers_override={"Content-Type": content_type}, timeout=60)
        resp.raise_for_status()
        return resp.json().get("content_uri", "")

def register(plugin):
    plugin.set_resource("client_class", MatrixClient)

matrix_plugin = {
    "metadata": {"name": "matrix", "version": "1.0.0", "description": "Matrix/Element chat - Rooms, messages, sync",
                 "author": "Mito Team", "license": "MIT", "tags": ["matrix", "element", "chat", "decentralized"],
                 "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"},
    "register": register,
}
