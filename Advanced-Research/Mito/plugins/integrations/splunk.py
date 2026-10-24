"""
Splunk Plugin
Search and manage Splunk logs and events.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.splunk")

try:
    from splunklib import client
    SPLUNK_AVAILABLE = True
except ImportError:
    SPLUNK_AVAILABLE = False


def _splunk(host: str = "localhost", port: int = 8089, username: str = "admin", password: str = ""):
    if not SPLUNK_AVAILABLE:
        raise ImportError("splunk-sdk not installed. Run: pip install splunk-sdk")
    import os
    return client.connect(
        host=host, port=port,
        username=username, password=password or os.environ.get("SPLUNK_PASSWORD", ""),
    )


def splunk_search_cmd(query: str = "", earliest: str = "-24h", latest: str = "now",
                       host: str = "localhost", port: int = 8089, username: str = "admin",
                       password: str = "") -> List[Dict]:
    s = _splunk(host, port, username, password)
    job = s.jobs.create(query, earliest_time=earliest, latest_time=latest)
    results = job.results()
    events = []
    for result in results:
        events.append(dict(result))
    return {"query": query, "events": events, "count": len(events), "sid": job.sid}


def splunk_submit_cmd(source: str = "", sourcetype: str = "mito", event: str = "",
                       host: str = "localhost", port: int = 8089, username: str = "admin",
                       password: str = "") -> Dict:
    s = _splunk(host, port, username, password)
    s.indexes[source or "main"].submit(event, sourcetype=sourcetype)
    return {"status": "ok", "source": source, "sourcetype": sourcetype}


def splunk_health_cmd(host: str = "localhost", port: int = 8089, username: str = "admin",
                       password: str = "") -> Dict:
    s = _splunk(host, port, username, password)
    return {"version": s.info.get("version"), "build": s.info.get("build"), "server": host}


def splunk_saved_searches_cmd(host: str = "localhost", port: int = 8089, username: str = "admin",
                               password: str = "") -> List[Dict]:
    s = _splunk(host, port, username, password)
    return [{"name": s.name, "search": s["search"]} for s in s.saved_searches]


def register(plugin):
    plugin.register_command("search", splunk_search_cmd)
    plugin.register_command("submit", splunk_submit_cmd)
    plugin.register_command("health", splunk_health_cmd)
    plugin.register_command("saved_searches", splunk_saved_searches_cmd)


PLUGIN_METADATA = {
    "name": "splunk", "version": "1.0.0",
    "description": "Splunk log search, submission, and management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["logging", "splunk", "search", "events"],
    "dependencies": ["splunk-sdk"], "permissions": ["splunk_write"],
    "min_mito_version": "1.0.1",
}

splunk_plugin = {"metadata": PLUGIN_METADATA, "register": register}
