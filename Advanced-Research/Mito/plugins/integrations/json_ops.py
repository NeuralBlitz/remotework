"""
JSON Operations Plugin
Parse, query, transform, and validate JSON data.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger("mito.plugins.json_ops")


class JSONOpsClient:
    def parse(self, data: str) -> Any:
        return json.loads(data)

    def stringify(self, data: Any, indent: int = 2) -> str:
        return json.dumps(data, indent=indent, default=str)

    def query(self, data: Any, path: str) -> Any:
        parts = path.strip("/").split("/")
        current = data
        for part in parts:
            if not part:
                continue
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list):
                try:
                    idx = int(part)
                    current = current[idx]
                except (ValueError, IndexError):
                    return None
            else:
                return None
        return current

    def set_value(self, data: Dict, path: str, value: Any) -> Dict:
        parts = path.strip("/").split("/")
        current = data
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
        return data

    def merge(self, *dicts: Dict, deep: bool = False) -> Dict:
        result = {}
        for d in dicts:
            if deep:
                self._deep_merge(result, d)
            else:
                result.update(d)
        return result

    def _deep_merge(self, base: Dict, overlay: Dict):
        for key, value in overlay.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def flatten(self, data: Dict, parent_key: str = "", sep: str = ".") -> Dict:
        items = {}
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self.flatten(v, new_key, sep))
            else:
                items[new_key] = v
        return items

    def unflatten(self, data: Dict, sep: str = ".") -> Dict:
        result = {}
        for key, value in data.items():
            self.set_value(result, key.replace(".", "/"), value)
        return result

    def diff(self, a: Any, b: Any, path: str = "") -> List[Dict]:
        differences = []
        if type(a) != type(b):
            differences.append({"path": path, "type": "type_change", "a": type(a).__name__, "b": type(b).__name__})
            return differences
        if isinstance(a, dict):
            all_keys = set(a.keys()) | set(b.keys())
            for key in all_keys:
                new_path = f"{path}/{key}" if path else key
                if key not in a:
                    differences.append({"path": new_path, "type": "added", "value": b[key]})
                elif key not in b:
                    differences.append({"path": new_path, "type": "removed", "value": a[key]})
                else:
                    differences.extend(self.diff(a[key], b[key], new_path))
        elif isinstance(a, list):
            for i in range(max(len(a), len(b))):
                new_path = f"{path}[{i}]"
                if i >= len(a):
                    differences.append({"path": new_path, "type": "added", "value": b[i]})
                elif i >= len(b):
                    differences.append({"path": new_path, "type": "removed", "value": a[i]})
                else:
                    differences.extend(self.diff(a[i], b[i], new_path))
        else:
            if a != b:
                differences.append({"path": path, "type": "value_change", "a": a, "b": b})
        return differences

    def validate(self, data: Any, schema: Dict) -> Dict:
        errors = []

        def check(value, sch, path):
            if "type" in sch:
                expected = sch["type"]
                if expected == "string" and not isinstance(value, str):
                    errors.append(f"{path}: expected string, got {type(value).__name__}")
                elif expected == "number" and not isinstance(value, (int, float)):
                    errors.append(f"{path}: expected number")
                elif expected == "boolean" and not isinstance(value, bool):
                    errors.append(f"{path}: expected boolean")
                elif expected == "array" and not isinstance(value, list):
                    errors.append(f"{path}: expected array")
                elif expected == "object" and not isinstance(value, dict):
                    errors.append(f"{path}: expected object")

            if "required" in sch and isinstance(value, dict):
                for req in sch["required"]:
                    if req not in value:
                        errors.append(f"{path}: missing required field '{req}'")

            if "properties" in sch and isinstance(value, dict):
                for prop, prop_schema in sch["properties"].items():
                    if prop in value:
                        check(value[prop], prop_schema, f"{path}.{prop}")

        check(data, schema, "$")
        return {"valid": len(errors) == 0, "errors": errors}


def json_parse_cmd(data: str = "{}") -> Any:
    """Parse a JSON string and return the Python object."""
    return JSONOpsClient().parse(data)


def json_stringify_cmd(data: str = "{}", indent: int = 2) -> str:
    """Convert a Python object to a JSON string."""
    return JSONOpsClient().stringify(json.loads(data), indent=indent)


def json_query_cmd(data: str = "{}", path: str = "") -> Any:
    """Query a JSON object with a path like /users/0/name."""
    return JSONOpsClient().query(json.loads(data), path)


def json_flatten_cmd(data: str = "{}") -> Dict:
    """Flatten a nested JSON object."""
    return JSONOpsClient().flatten(json.loads(data))


def json_diff_cmd(a: str = "{}", b: str = "{}") -> List[Dict]:
    """Find differences between two JSON objects."""
    return JSONOpsClient().diff(json.loads(a), json.loads(b))


def json_merge_cmd(*dicts: str, deep: bool = False) -> Dict:
    """Merge multiple JSON objects."""
    return JSONOpsClient().merge(*[json.loads(d) for d in dicts], deep=deep)


def register(plugin):
    plugin.register_command("json_parse", json_parse_cmd)
    plugin.register_command("json_stringify", json_stringify_cmd)
    plugin.register_command("json_query", json_query_cmd)
    plugin.register_command("json_flatten", json_flatten_cmd)
    plugin.register_command("json_diff", json_diff_cmd)
    plugin.register_command("json_merge", json_merge_cmd)
    plugin.set_resource("client_class", JSONOpsClient)


PLUGIN_METADATA = {
    "name": "json_ops",
    "version": "1.0.0",
    "description": "JSON operations - parse, query, flatten, diff, merge, validate",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["json", "parse", "query", "transform"],
    "dependencies": [],
    "permissions": [],
    "min_mito_version": "1.0.1",
}


json_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
