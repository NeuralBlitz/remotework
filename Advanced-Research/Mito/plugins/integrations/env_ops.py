"""
Environment Variables Plugin
Read, list, set, and search environment variables.
"""

import os
import logging
from typing import Dict, List, Optional

logger = logging.getLogger("mito.plugins.env_ops")


class EnvOpsClient:
    def __init__(self, prefix: str = ""):
        self.prefix = prefix

    def get(self, key: str, default: str = None) -> Optional[str]:
        return os.environ.get(key, default)

    def set(self, key: str, value: str) -> Dict:
        os.environ[key] = value
        return {"key": key, "value": value, "set": True}

    def unset(self, key: str) -> Dict:
        if key in os.environ:
            del os.environ[key]
            return {"key": key, "removed": True}
        return {"key": key, "removed": False, "note": "key not found"}

    def list_all(self) -> Dict:
        env = dict(os.environ)
        if self.prefix:
            filtered = {k: v for k, v in env.items() if k.startswith(self.prefix)}
        else:
            filtered = env
        return {
            "count": len(filtered),
            "vars": filtered,
        }

    def search(self, pattern: str) -> Dict:
        import re
        needle = pattern.lower()
        results = {}
        for k, v in os.environ.items():
            if needle in k.lower() or needle in v.lower():
                results[k] = v
        return {"count": len(results), "matches": results}

    def masked(self, keys: List[str] = None) -> Dict:
        safe_keys = {"PATH", "HOME", "USER", "PWD", "SHELL", "TERM", "LANG"}
        if keys:
            safe_keys.update(keys)
        result = {}
        for k, v in os.environ.items():
            if k in safe_keys:
                result[k] = v
            else:
                result[k] = "***" if v else ""
        return {"count": len(result), "vars": result}


def env_get_cmd(key: str = "") -> Optional[str]:
    """Get an environment variable value."""
    return EnvOpsClient().get(key)


def env_set_cmd(key: str = "", value: str = "") -> Dict:
    """Set an environment variable."""
    return EnvOpsClient().set(key, value)


def env_unset_cmd(key: str = "") -> Dict:
    """Unset (remove) an environment variable."""
    return EnvOpsClient().unset(key)


def env_list_cmd(prefix: str = "") -> Dict:
    """List all environment variables, optionally filtered by prefix."""
    return EnvOpsClient(prefix=prefix).list_all()


def env_search_cmd(pattern: str = "") -> Dict:
    """Search environment variables by key or value."""
    return EnvOpsClient().search(pattern)


def env_masked_cmd() -> Dict:
    """List environment variables with sensitive values masked."""
    return EnvOpsClient().masked()


def register(plugin):
    plugin.register_command("env_get", env_get_cmd)
    plugin.register_command("env_set", env_set_cmd)
    plugin.register_command("env_unset", env_unset_cmd)
    plugin.register_command("env_list", env_list_cmd)
    plugin.register_command("env_search", env_search_cmd)
    plugin.register_command("env_masked", env_masked_cmd)
    plugin.set_resource("client_class", EnvOpsClient)


PLUGIN_METADATA = {
    "name": "env_ops",
    "version": "1.0.0",
    "description": "Environment variables - read, set, unset, list, search",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["env", "environment", "variables", "config"],
    "dependencies": [],
    "permissions": ["read_env"],
    "min_mito_version": "1.0.1",
}


env_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
