"""Trello Plugin - Boards, lists, cards via REST API"""
import os
from typing import Dict, List

class TrelloClient:
    def __init__(self, api_key: str = None, token: str = None):
        self.api_key = api_key or os.environ.get("TRELLO_API_KEY", "")
        self.token = token or os.environ.get("TRELLO_TOKEN", "")
        self.base_url = "https://api.trello.com/1"
    def _params(self):
        return {"key": self.api_key, "token": self.token}
    def list_boards(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/members/me/boards", params=self._params(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_lists(self, board_id: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/boards/{board_id}/lists", params=self._params(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_cards(self, board_id: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/boards/{board_id}/cards", params=self._params(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def create_card(self, list_id: str, name: str, desc: str = "") -> Dict:
        import requests
        params = {**self._params(), "idList": list_id, "name": name, "desc": desc}
        resp = requests.post(f"{self.base_url}/cards", params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def update_card(self, card_id: str, **kwargs) -> Dict:
        import requests
        params = {**self._params(), **kwargs}
        resp = requests.put(f"{self.base_url}/cards/{card_id}", params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def delete_card(self, card_id: str) -> bool:
        import requests
        resp = requests.delete(f"{self.base_url}/cards/{card_id}", params=self._params(), timeout=30)
        return resp.ok

def register(plugin):
    plugin.set_resource("client_class", TrelloClient)

trello_plugin = {"metadata": {"name": "trello", "version": "1.0.0", "description": "Trello - Boards, lists, cards", "author": "Mito Team", "license": "MIT", "tags": ["trello", "project-management", "kanban"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
