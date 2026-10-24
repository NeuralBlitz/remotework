"""Deepgram Speech Plugin"""
import os
from typing import Dict

class DeepgramClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("DEEPGRAM_API_KEY", "")
        self.base_url = "https://api.deepgram.com/v1"
    def _headers(self): return {"Authorization": f"Token {self.api_key}", "Content-Type": "application/json"}
    def transcribe_url(self, audio_url: str, model: str = "nova-2") -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/listen", headers=self._headers(), json={"url": audio_url, "model": model}, timeout=60)
        resp.raise_for_status()
        return resp.json()

def register(plugin): plugin.set_resource("client_class", DeepgramClient)
deepgram_plugin = {"metadata": {"name": "deepgram", "version": "1.0.0", "description": "Deepgram - Speech recognition", "author": "Mito Team", "license": "MIT", "tags": ["deepgram", "speech", "stt"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
