"""Stability AI Plugin - Image generation"""
import os
from typing import Dict

class StabilityAIClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("STABILITY_API_KEY", "")
        self.base_url = "https://api.stability.ai/v1"
    def _headers(self): return {"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"}
    def generate(self, prompt: str, engine: str = "stable-diffusion-xl-1024-v1-0", width: int = 1024, height: int = 1024) -> bytes:
        import requests
        resp = requests.post(f"{self.base_url}/generation/{engine}/text-to-image", headers=self._headers(), json={"text_prompts": [{"text": prompt}], "width": width, "height": height, "cfg_scale": 7, "steps": 30}, timeout=120)
        resp.raise_for_status()
        return resp.content

def register(plugin): plugin.set_resource("client_class", StabilityAIClient)
stabilityai_plugin = {"metadata": {"name": "stabilityai", "version": "1.0.0", "description": "Stability AI - Image generation", "author": "Mito Team", "license": "MIT", "tags": ["stability", "ai", "images", "generation"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
