"""
Mito String Utilities
Slugify, truncate, template, random, encoding, validation
"""

import re
import string
import secrets
import unicodedata
from typing import Dict, List, Optional, Any


def slugify(text: str, sep: str = "-") -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", sep, text).strip(sep)


def truncate(text: str, length: int, suffix: str = "...") -> str:
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


def truncate_words(text: str, words: int, suffix: str = "...") -> str:
    parts = text.split()
    if len(parts) <= words:
        return text
    return " ".join(parts[:words]) + suffix


def template(text: str, variables: Dict[str, Any], start: str = "{{", end: str = "}}") -> str:
    result = text
    for key, value in variables.items():
        result = result.replace(f"{start}{key}{end}", str(value))
    return result


def interpolate(text: str, **kwargs) -> str:
    for key, value in kwargs.items():
        text = text.replace(f"{{{key}}}", str(value))
    return text


def snake_case(text: str) -> str:
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    text = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", text)
    return text.replace("-", "_").replace(" ", "_").lower()


def camel_case(text: str) -> str:
    parts = re.split(r"[-_\s]+", text)
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def pascal_case(text: str) -> str:
    return "".join(p.capitalize() for p in re.split(r"[-_\s]+", text))


def kebab_case(text: str) -> str:
    return snake_case(text).replace("_", "-")


def title_case(text: str) -> str:
    return text.title()


def random_string(length: int = 16, chars: str = None) -> str:
    chars = chars or string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def random_hex(length: int = 32) -> str:
    return secrets.token_hex(length // 2 + 1)[:length]


def random_uuid() -> str:
    import uuid
    return str(uuid.uuid4())


def extract_emails(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)


def extract_urls(text: str) -> List[str]:
    return re.findall(r"https?://[^\s<>\"']+", text)


def extract_numbers(text: str) -> List[float]:
    return [float(x) for x in re.findall(r"-?\d+\.?\d*", text)]


def is_email(text: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", text))


def is_url(text: str) -> bool:
    return bool(re.match(r"^https?://[^\s]+$", text))


def is_numeric(text: str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False


def is_empty(text: str) -> bool:
    return not text or text.strip() == ""


def pad_left(text: str, length: int, char: str = " ") -> str:
    return text.rjust(length, char)


def pad_right(text: str, length: int, char: str = " ") -> str:
    return text.ljust(length, char)


def pad_center(text: str, length: int, char: str = " ") -> str:
    return text.center(length, char)


def strip_ansi(text: str) -> str:
    return re.sub(r"\033\[[0-9;]*m", "", text)


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def word_count(text: str) -> int:
    return len(text.split())


def char_count(text: str, include_spaces: bool = True) -> int:
    return len(text) if include_spaces else len(text.replace(" ", ""))


def reverse(text: str) -> str:
    return text[::-1]


def contains_any(text: str, patterns: List[str]) -> bool:
    return any(p in text for p in patterns)


def contains_all(text: str, patterns: List[str]) -> bool:
    return all(p in text for p in patterns)


def levenshtein(a: str, b: str) -> int:
    if len(a) < len(b):
        return levenshtein(b, a)
    if len(b) == 0:
        return len(a)
    prev = range(len(b) + 1)
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (ca != cb)))
        prev = curr
    return prev[-1]


def similarity(a: str, b: str) -> float:
    max_len = max(len(a), len(b))
    if max_len == 0:
        return 1.0
    return 1.0 - levenshtein(a, b) / max_len


def indent(text: str, spaces: int = 2, first_line: bool = True) -> str:
    prefix = " " * spaces
    lines = text.split("\n")
    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(prefix + line)
    return "\n".join(result)


def dedent(text: str) -> str:
    import textwrap
    return textwrap.dedent(text)
