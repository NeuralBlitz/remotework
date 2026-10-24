"""
Mito Parsers
Config file parsers, env files, INI, dot notation, query strings
"""

import re
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


def parse_env(text: str) -> Dict[str, str]:
    result = {}
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            result[key] = value
    return result


def load_env(filepath: str = ".env") -> Dict[str, str]:
    if not os.path.exists(filepath):
        return {}
    with open(filepath) as f:
        return parse_env(f.read())


def apply_env(filepath: str = ".env", override: bool = False):
    env = load_env(filepath)
    for key, value in env.items():
        if override or key not in os.environ:
            os.environ[key] = value


def parse_ini(text: str) -> Dict[str, Dict[str, str]]:
    result = {}
    current_section = "DEFAULT"
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith(";") or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1]
            if current_section not in result:
                result[current_section] = {}
        elif "=" in line:
            key, value = line.split("=", 1)
            result.setdefault(current_section, {})[key.strip()] = value.strip()
    return result


def load_ini(filepath: str) -> Dict[str, Dict[str, str]]:
    with open(filepath) as f:
        return parse_ini(f.read())


def parse_dot_notation(data: Dict[str, Any]) -> Dict[str, Any]:
    result = {}
    for key, value in data.items():
        parts = key.split(".")
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result


def flatten_to_dot(data: Dict[str, Any], prefix: str = "") -> Dict[str, str]:
    result = {}
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result.update(flatten_to_dot(value, full_key))
        else:
            result[full_key] = str(value)
    return result


def parse_query_string(query: str) -> Dict[str, str]:
    result = {}
    if "?" in query:
        query = query.split("?", 1)[1]
    for part in query.split("&"):
        if "=" in part:
            key, value = part.split("=", 1)
            from urllib.parse import unquote
            result[unquote(key)] = unquote(value)
        elif part:
            result[part] = ""
    return result


def build_query_string(params: Dict[str, str]) -> str:
    from urllib.parse import quote
    parts = []
    for key, value in params.items():
        parts.append(f"{quote(str(key))}={quote(str(value))}")
    return "&".join(parts)


def parse_headers(raw: str) -> Dict[str, str]:
    result = {}
    for line in raw.strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def parse_cookies(raw: str) -> Dict[str, str]:
    result = {}
    for part in raw.split(";"):
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            result[key.strip()] = value.strip()
    return result


def parse_size(size_str: str) -> int:
    size_str = size_str.strip().upper()
    units = {"TB": 1024**4, "GB": 1024**3, "MB": 1024**2, "KB": 1024, "B": 1}
    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            return int(float(size_str[:-len(unit)].strip()) * multiplier)
    return int(size_str)


def format_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}PB"


def parse_duration(duration_str: str) -> float:
    duration_str = duration_str.strip().lower()
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    for unit, multiplier in units.items():
        if duration_str.endswith(unit):
            return float(duration_str[:-1]) * multiplier
    return float(duration_str)
