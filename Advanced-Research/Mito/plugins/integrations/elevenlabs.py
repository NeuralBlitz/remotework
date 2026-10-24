"""ElevenLabs TTS Plugin"""
import os
from typing import Dict, List

class ElevenLabsClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("ELEVENLABS_API_KEY", "")
        self.base_url = "https://api.elevenlabs.io/v1"
    def _headers(self): return {"xi-api-key": self.api_key, "Content-Type": "application/json"}
    def list_voices(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/voices", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("voices", [])
    def synthesize(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM", model: str = "eleven_monolingual_v1") -> bytes:
        import requests
        resp = requests.post(f"{self.base_url}/text-to-speech/{voice_id}", headers=self._headers(), json={"text": text, "model_id": model}, timeout=60)
        resp.raise_for_status()
        return resp.content

def register(plugin): plugin.set_resource("client_class", ElevenLabsClient)
elevenlabs_plugin = {"metadata": {"name": "elevenlabs", "version": "1.0.0", "description": "ElevenLabs - Text-to-speech", "author": "Mito Team", "license": "MIT", "tags": ["elevenlabs", "tts", "audio", "ai"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
