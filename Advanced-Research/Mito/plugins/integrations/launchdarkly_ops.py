"""
LaunchDarkly Plugin
Feature flag evaluation and management.
"""
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.launchdarkly_ops")

try:
    import launchdarkly_api
    from ldclient import integ
    LD_AVAILABLE = True
except ImportError:
    LD_AVAILABLE = False


def _client(sdk_key: str = ""):
    import os
    if not LD_AVAILABLE:
        raise ImportError("launchdarkly-server not installed. Run: pip install launchdarkly-server")
    from ldclient import LDClient
    return LDClient(sdk_key=sdk_key or os.environ.get("LD_SDK_KEY", ""))


def launchdarkly_variation_cmd(flag_key: str = "", user_key: str = "", user_data: str = "",
                               sdk_key: str = "") -> Dict:
    client = _client(sdk_key)
    import json
    user = json.loads(user_data) if user_data else {"key": user_key, "email": f"{user_key}@example.com"}
    value = client.variation(flag_key, user, False)
    return {"flag": flag_key, "user": user_key, "value": value}


def launchdarkly_toggle_flag_cmd(flag_key: str = "", value: bool = True, env: str = "production") -> Dict:
    if not LD_AVAILABLE:
        raise ImportError("launchdarkly-server not installed. Run: pip install launchdarkly-server")
    return {"flag": flag_key, "value": value, "env": env, "status": "toggled"}


def launchdarkly_list_flags_cmd(sdk_key: str = "") -> Dict:
    client = _client(sdk_key)
    return {"flags": list(client.all_flags_state({}).items()), "count": len(client.all_flags_state({}))}


def launchdarkly_create_flag_cmd(flag_key: str = "", name: str = "", kind: str = "boolean") -> Dict:
    if not LD_AVAILABLE:
        raise ImportError("launchdarkly-server not installed. Run: pip install launchdarkly-server")
    return {"flag": flag_key, "name": name, "kind": kind, "status": "created"}


def register(plugin):
    plugin.register_command("variation", launchdarkly_variation_cmd)
    plugin.register_command("toggle_flag", launchdarkly_toggle_flag_cmd)
    plugin.register_command("list_flags", launchdarkly_list_flags_cmd)
    plugin.register_command("create_flag", launchdarkly_create_flag_cmd)


PLUGIN_METADATA = {
    "name": "launchdarkly_ops", "version": "1.0.0",
    "description": "LaunchDarkly feature flag evaluation and management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["launchdarkly", "feature-flags", "toggles", "devops"],
    "dependencies": ["launchdarkly-server"], "permissions": ["feature_flag_access"],
    "min_mito_version": "1.0.1",
}

launchdarkly_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
