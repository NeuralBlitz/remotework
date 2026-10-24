"""
Regex Operations Plugin
Pattern matching, validation, extraction, and replacement.
"""
import re
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.regex_ops")


def regex_match_cmd(pattern: str = "", text: str = "", flags: str = "") -> Dict:
    flag_val = sum(
        getattr(re, f.upper(), 0) for f in flags.split(",") if f
    ) if flags else 0
    match = re.search(pattern, text, flag_val)
    if match:
        return {
            "matched": True, "group": match.group(),
            "span": list(match.span()),
            "groups": list(match.groups()),
            "named_groups": match.groupdict(),
        }
    return {"matched": False, "pattern": pattern}


def regex_find_all_cmd(pattern: str = "", text: str = "", flags: str = "") -> List[Dict]:
    flag_val = sum(getattr(re, f.upper(), 0) for f in (flags.split(",") if flags else [])) if flags else 0
    matches = re.finditer(pattern, text, flag_val)
    return [{"match": m.group(), "span": list(m.span()), "groups": list(m.groups())} for m in matches]


def regex_replace_cmd(pattern: str = "", text: str = "", replacement: str = "", count: int = 0) -> Dict:
    if count:
        new_text = re.sub(pattern, replacement, text, count=count)
    else:
        new_text = re.sub(pattern, replacement, text)
    return {"original": text, "result": new_text, "count": text.count(replacement) if not count else count}


def regex_validate_email_cmd(email: str = "") -> Dict:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    matched = bool(re.match(pattern, email))
    return {"valid": matched, "email": email}


def regex_validate_url_cmd(url: str = "") -> Dict:
    pattern = r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$"
    matched = bool(re.match(pattern, url))
    return {"valid": matched, "url": url}


def regex_validate_phone_cmd(phone: str = "", country: str = "US") -> Dict:
    patterns = {
        "US": r"^\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$",
        "UK": r"^\+?44?[-\s]?[0-9]{4}[-\s]?[0-9]{6}$",
        "INTL": r"^\+?[0-9]{1,4}[-\s]?[0-9]{1,4}[-\s]?[0-9]{1,4}[-\s]?[0-9]{1,9}$",
    }
    pattern = patterns.get(country, patterns["INTL"])
    matched = bool(re.match(pattern, phone))
    return {"valid": matched, "phone": phone, "country": country}


def regex_split_cmd(pattern: str = "", text: str = "", maxsplit: int = 0) -> List[str]:
    parts = re.split(pattern, text, maxsplit=maxsplit or 0)
    return {"parts": parts, "count": len(parts)}


def regex_extract_cmd(pattern: str = "", text: str = "", group: int = 0) -> Dict:
    match = re.search(pattern, text)
    if match:
        return {"extracted": match.group(group or 0), "all_groups": list(match.groups()), "named": match.groupdict()}
    return {"extracted": None}


def regex_is_match_cmd(pattern: str = "", text: str = "") -> Dict:
    return {"is_match": bool(re.match(pattern, text)), "pattern": pattern}


def register(plugin):
    plugin.register_command("match", regex_match_cmd)
    plugin.register_command("find_all", regex_find_all_cmd)
    plugin.register_command("replace", regex_replace_cmd)
    plugin.register_command("validate_email", regex_validate_email_cmd)
    plugin.register_command("validate_url", regex_validate_url_cmd)
    plugin.register_command("validate_phone", regex_validate_phone_cmd)
    plugin.register_command("split", regex_split_cmd)
    plugin.register_command("extract", regex_extract_cmd)
    plugin.register_command("is_match", regex_is_match_cmd)


PLUGIN_METADATA = {
    "name": "regex_ops", "version": "1.0.0",
    "description": "Regex pattern matching, validation, extraction, and replacement",
    "author": "Mito Team", "license": "MIT",
    "tags": ["regex", "pattern", "validation", "utilities"],
    "dependencies": [], "permissions": [],
    "min_mito_version": "1.0.1",
}

regex_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
