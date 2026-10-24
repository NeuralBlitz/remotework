"""
Prometheus Plugin
Query and manage Prometheus metrics.
"""
from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Any, Dict, List

logger = logging.getLogger("mito.plugins.prometheus")

try:
    from prometheus_api_client import PrometheusConnect
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

if TYPE_CHECKING:
    from prometheus_api_client import PrometheusConnect


def _client(url: str = "http://localhost:9090") -> PrometheusConnect:
    if not PROMETHEUS_AVAILABLE:
        raise ImportError("prometheus-api-client not installed. Run: pip install prometheus-api-client")
    return PrometheusConnect(url=url, disable_ssl_cert_verification=True)


def prometheus_query_cmd(query: str = "", url: str = "http://localhost:9090") -> List[Dict]:
    p = _client(url)
    result = p.custom_query(query=query)
    return {"query": query, "results": result, "count": len(result)}


def prometheus_range_cmd(query: str = "", start: str = "", end: str = "", step: str = "15s",
                          url: str = "http://localhost:9090") -> Dict:
    p = _client(url)
    start_dt = __import__("datetime").datetime.fromisoformat(start) if start else None
    end_dt = __import__("datetime").datetime.fromisoformat(end) if end else None
    result = p.custom_query_range(query=query, start_time=start_dt, end_time=end_dt, step=step)
    return {"query": query, "range": result}


def prometheus_alerts_cmd(url: str = "http://localhost:9090") -> List[Dict]:
    p = _client(url)
    alerts = p.get_alerts()
    return {"alerts": alerts, "count": len(alerts)}


def prometheus_targets_cmd(url: str = "http://localhost:9090") -> List[Dict]:
    p = _client(url)
    targets = p.get_targets()
    return {"active_targets": targets.get("active_targets", []), "dropped": targets.get("dropped_targets", [])}


def prometheus_rules_cmd(url: str = "http://localhost:9090") -> Dict:
    p = _client(url)
    rules = p.get_rules()
    return {"rules": rules, "count": len(rules)}


def register(plugin):
    plugin.register_command("query", prometheus_query_cmd)
    plugin.register_command("range", prometheus_range_cmd)
    plugin.register_command("alerts", prometheus_alerts_cmd)
    plugin.register_command("targets", prometheus_targets_cmd)
    plugin.register_command("rules", prometheus_rules_cmd)


PLUGIN_METADATA = {
    "name": "prometheus", "version": "1.0.0",
    "description": "Prometheus metrics querying and alert management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["monitoring", "metrics", "prometheus"],
    "dependencies": ["prometheus-api-client"], "permissions": ["metrics_read"],
    "min_mito_version": "1.0.1",
}

prometheus_plugin = {"metadata": PLUGIN_METADATA, "register": register}
