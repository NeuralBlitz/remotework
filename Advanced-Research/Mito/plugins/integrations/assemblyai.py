"""AssemblyAI Speech Plugin"""
import os
from typing import Dict

class AssemblyAIClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("ASSEMBLYAI_API_KEY", "")
        self.base_url = "https://api.assemblyai.com/v2"
    def _headers(self): return {"authorization": self.api_key, "Content-Type": "application/json"}
    def transcribe(self, audio_url: str) -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/transcript", headers=self._headers(), json={"audio_url": audio_url}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def get_transcript(self, transcript_id: str) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/transcript/{transcript_id}", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

def register(plugin): plugin.set_resource("client_class", AssemblyAIClient)
assemblyai_plugin = {"metadata": {"name": "assemblyai", "version": "1.0.0", "description": "AssemblyAI - Speech transcription", "author": "Mito Team", "license": "MIT", "tags": ["assemblyai", "speech", "transcription"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
