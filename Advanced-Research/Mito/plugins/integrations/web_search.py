"""
Web Search Plugin
Search the web via DuckDuckGo or SerpAPI.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.web_search")


class WebSearchClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("SERPAPI_KEY", "")
        self.ddg_fallback = True

    def _ddg_search(self, query: str, num_results: int = 10) -> List[Dict]:
        try:
            import requests
            params = {"q": query, "kl": "us-en", "ia": "web"}
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(
                "https://duckduckgo.com/html/",
                params=params,
                headers=headers,
                timeout=15,
            )
            resp.raise_for_status()
            results = []
            text = resp.text
            import re
            links = re.findall(r'href="(https?://[^"]+)"', text)
            titles = re.findall(r'<a class="result__a"[^>]*>([^<]+)</a>', text)
            snippets = re.findall(r'<a class="result__snippet"[^>]*>([^<]+)</a>', text)

            for i in range(min(len(links), num_results)):
                results.append({
                    "title": titles[i] if i < len(titles) else f"Result {i+1}",
                    "url": links[i] if i < len(links) else "",
                    "snippet": snippets[i] if i < len(snippets) else "",
                    "source": "duckduckgo",
                })
            return results
        except Exception as e:
            return [{"error": str(e), "source": "duckduckgo"}]

    def _serpapi_search(self, query: str, num_results: int = 10) -> List[Dict]:
        try:
            import requests
            params = {
                "q": query,
                "api_key": self.api_key,
                "num": num_results,
                "engine": "google",
            }
            resp = requests.get("https://serpapi.com/search", params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            results = []
            for item in data.get("organic_results", [])[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "serpapi",
                })
            return results
        except Exception as e:
            return [{"error": str(e), "source": "serpapi"}]

    def search(self, query: str, num_results: int = 10, engine: str = "auto") -> List[Dict]:
        if engine == "serpapi" or (engine == "auto" and self.api_key):
            return self._serpapi_search(query, num_results)
        return self._ddg_search(query, num_results)

    def summarize_results(self, results: List[Dict]) -> str:
        if not results:
            return "No results found."
        lines = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            url = r.get("url", "")
            snippet = r.get("snippet", "")
            lines.append(f"{i}. {title}\n   {url}\n   {snippet[:150]}...")
        return "\n".join(lines)


def web_search_cmd(query: str = "", num_results: int = 10) -> List[Dict]:
    """Search the web and return results with titles, URLs, and snippets."""
    return WebSearchClient().search(query, num_results=num_results)


def web_search_summarize_cmd(query: str = "", num_results: int = 5) -> str:
    """Search the web and return a human-readable summary."""
    results = WebSearchClient().search(query, num_results=num_results)
    return WebSearchClient().summarize_results(results)


def register(plugin):
    plugin.register_command("web_search", web_search_cmd)
    plugin.register_command("web_search_summarize", web_search_summarize_cmd)
    plugin.set_resource("client_class", WebSearchClient)


PLUGIN_METADATA = {
    "name": "web_search",
    "version": "1.0.0",
    "description": "Web search via DuckDuckGo or SerpAPI",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["web", "search", "duckduckgo", "serpapi"],
    "dependencies": [],
    "permissions": ["network_access"],
    "min_mito_version": "1.0.1",
}


web_search_plugin = {"metadata": PLUGIN_METADATA, "register": register}
