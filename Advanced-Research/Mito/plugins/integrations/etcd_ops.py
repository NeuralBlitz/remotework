"""
etcd Operations Plugin
Key-value store operations via etcd.
"""
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.etcd_ops")

try:
    import etcd3
    ETCD_AVAILABLE = True
except ImportError:
    ETCD_AVAILABLE = False


def _client(host: str = "localhost", port: int = 2379, ca_cert: str = "", cert_key: str = "", cert_cert: str = ""):
    if not ETCD_AVAILABLE:
        raise ImportError("etcd3 not installed. Run: pip install etcd3")
    if cert_cert:
        import grpc
        credentials = grpc.ssl_channel_credentials(open(ca_cert).read() if ca_cert else None, open(cert_key).read(), open(cert_cert).read())
        return etcd3.client(host=host, port=port, credentials=credentials)
    return etcd3.client(host=host, port=port)


def etcd_get_cmd(key: str = "", host: str = "localhost", port: int = 2379) -> Dict:
    c = _client(host, port)
    value, metadata = c.get(key)
    return {"key": key, "value": value.decode() if value else None, "revision": metadata.version if metadata else None}


def etcd_put_cmd(key: str = "", value: str = "", host: str = "localhost", port: int = 2379) -> Dict:
    c = _client(host, port)
    result = c.put(key, value)
    return {"key": key, "status": "put", "revision": result.mod_revision if result else None}


def etcd_delete_cmd(key: str = "", host: str = "localhost", port: int = 2379) -> Dict:
    c = _client(host, port)
    result = c.delete(key)
    return {"key": key, "deleted": result.deleted if hasattr(result, 'deleted') else True}


def etcd_list_keys_cmd(prefix: str = "/", host: str = "localhost", port: int = 2379) -> Dict:
    c = _client(host, port)
    keys = []
    for k, v in c.get_prefix(prefix):
        keys.append({"key": k.decode() if k else None, "value": v.decode() if v else None})
    return {"keys": keys, "count": len(keys), "prefix": prefix}


def etcd_watch_key_cmd(key: str = "", host: str = "localhost", port: int = 2379, timeout: int = 10) -> Dict:
    c = _client(host, port)
    events = c.watch(key, timeout=timeout)
    result = []
    for event in events:
        result.append({"type": type(event).__name__, "value": event.value.decode() if hasattr(event, 'value') else None})
    return {"watched": key, "events": result, "count": len(result)}


def register(plugin):
    plugin.register_command("get", etcd_get_cmd)
    plugin.register_command("put", etcd_put_cmd)
    plugin.register_command("delete", etcd_delete_cmd)
    plugin.register_command("list_keys", etcd_list_keys_cmd)
    plugin.register_command("watch_key", etcd_watch_key_cmd)


PLUGIN_METADATA = {
    "name": "etcd_ops", "version": "1.0.0",
    "description": "etcd key-value store operations",
    "author": "Mito Team", "license": "MIT",
    "tags": ["etcd", "kv-store", "distributed", "config"],
    "dependencies": ["etcd3"], "permissions": ["etcd_access"],
    "min_mito_version": "1.0.1",
}

etcd_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
