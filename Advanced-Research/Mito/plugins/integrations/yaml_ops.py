"""
YAML Operations Plugin
Read, write, merge, and validate YAML files.
"""
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.yaml_ops")

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def _check():
    if not YAML_AVAILABLE:
        raise ImportError("pyyaml not installed. Run: pip install pyyaml")


def yaml_read_cmd(file_path: str = "") -> Dict:
    _check()
    with open(file_path) as f:
        data = yaml.safe_load(f)
    return {"data": data, "type": type(data).__name__}


def yaml_write_cmd(file_path: str = "", data: str = "") -> Dict:
    _check()
    import json
    obj = json.loads(data) if data.startswith("{") or data.startswith("[") else data
    with open(file_path, "w") as f:
        yaml.dump(obj, f, default_flow_style=False, sort_keys=False)
    return {"status": "written", "path": file_path}


def yaml_validate_cmd(file_path: str = "") -> Dict:
    _check()
    try:
        with open(file_path) as f:
            yaml.safe_load(f)
        return {"valid": True, "path": file_path}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def yaml_merge_cmd(files: str = "", output: str = "") -> Dict:
    _check()
    file_list = [f.strip() for f in files.split(",")]
    merged = {}
    for fp in file_list:
        with open(fp) as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict):
                merged.update(data)
            elif isinstance(data, list):
                merged = merged.get("items", []).extend(data) if merged.get("items") else data
    with open(output, "w") as f:
        yaml.dump(merged, f, default_flow_style=False)
    return {"status": "merged", "output": output}


def yaml_to_json_cmd(file_path: str = "", output: str = "") -> Dict:
    _check()
    with open(file_path) as f:
        data = yaml.safe_load(f)
    import json
    with open(output, "w") as f:
        json.dump(data, f, indent=2)
    return {"status": "converted", "output": output}


def register(plugin):
    plugin.register_command("read", yaml_read_cmd)
    plugin.register_command("write", yaml_write_cmd)
    plugin.register_command("validate", yaml_validate_cmd)
    plugin.register_command("merge", yaml_merge_cmd)
    plugin.register_command("to_json", yaml_to_json_cmd)


PLUGIN_METADATA = {
    "name": "yaml_ops", "version": "1.0.0",
    "description": "YAML read, write, merge, validate, and convert",
    "author": "Mito Team", "license": "MIT",
    "tags": ["yaml", "data", "config", "utilities"],
    "dependencies": ["pyyaml"], "permissions": ["read_files", "write_files"],
    "min_mito_version": "1.0.1",
}

yaml_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
