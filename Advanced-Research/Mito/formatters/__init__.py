"""
Mito Formatters
Output formatting: tables, trees, progress bars, colors, markdown
"""

import sys
import json
from typing import Dict, List, Any, Optional


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

    @classmethod
    def disable(cls):
        for attr in ["RESET", "BOLD", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE", "GRAY"]:
            setattr(cls, attr, "")


def colored(text: str, color: str = "white", bold: bool = False) -> str:
    prefix = ""
    if bold:
        prefix += Colors.BOLD
    prefix += getattr(Colors, color.upper(), "")
    return f"{prefix}{text}{Colors.RESET}" if prefix else text


def red(text: str) -> str: return colored(text, "red")
def green(text: str) -> str: return colored(text, "green")
def yellow(text: str) -> str: return colored(text, "yellow")
def blue(text: str) -> str: return colored(text, "blue")
def cyan(text: str) -> str: return colored(text, "cyan")


def table(data: List[Dict], columns: List[str] = None, max_width: int = 30) -> str:
    if not data:
        return ""
    if not columns:
        columns = list(data[0].keys())

    widths = {col: len(col) for col in columns}
    for row in data:
        for col in columns:
            val = str(row.get(col, ""))
            if len(val) > max_width:
                val = val[:max_width - 3] + "..."
            widths[col] = max(widths[col], len(val))

    header = " | ".join(col.ljust(widths[col]) for col in columns)
    separator = "-+-".join("-" * widths[col] for col in columns)
    rows = []
    for row in data:
        line = " | ".join(
            str(row.get(col, "")).ljust(widths[col])[:max_width]
            for col in columns
        )
        rows.append(line)

    return f"{header}\n{separator}\n" + "\n".join(rows)


def tree(data: Dict, indent: int = 0, prefix: str = "") -> str:
    lines = []
    items = list(data.items())
    for i, (key, value) in enumerate(items):
        is_last = i == len(items) - 1
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "

        if isinstance(value, dict):
            lines.append(f"{prefix}{connector}{key}/")
            lines.append(tree(value, indent + 1, prefix + extension))
        elif isinstance(value, list):
            lines.append(f"{prefix}{connector}{key} [{len(value)}]")
        else:
            lines.append(f"{prefix}{connector}{key}: {value}")

    return "\n".join(lines)


def progress_bar(current: int, total: int, width: int = 40, fill: str = "█", empty: str = "░") -> str:
    if total == 0:
        return f"[{fill * width}] 100%"
    pct = current / total
    filled = int(width * pct)
    bar = fill * filled + empty * (width - filled)
    return f"[{bar}] {pct * 100:.1f}% ({current}/{total})"


def spinner(frame: int = 0) -> str:
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    return frames[frame % len(frames)]


def box(text: str, title: str = "", padding: int = 1) -> str:
    lines = text.split("\n")
    width = max(len(line) for line in lines) + padding * 2
    if title:
        width = max(width, len(title) + 4)

    result = ["┌" + "─" * (width + 2) + "┐"]
    if title:
        result.append("│ " + title.center(width) + " │")
        result.append("├" + "─" * (width + 2) + "┤")

    for line in lines:
        result.append("│ " + " " * padding + line.ljust(width - padding) + " │")

    result.append("└" + "─" * (width + 2) + "┘")
    return "\n".join(result)


def json_pretty(data: Any, indent: int = 2) -> str:
    return json.dumps(data, indent=indent, default=str, ensure_ascii=False)


def markdown_table(data: List[Dict], columns: List[str] = None) -> str:
    if not data:
        return ""
    if not columns:
        columns = list(data[0].keys())

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    rows = []
    for row in data:
        line = "| " + " | ".join(str(row.get(col, "")) for col in columns) + " |"
        rows.append(line)

    return f"{header}\n{separator}\n" + "\n".join(rows)


def bullet_list(items: List[str], bullet: str = "•") -> str:
    return "\n".join(f"  {bullet} {item}" for item in items)


def numbered_list(items: List[str]) -> str:
    width = len(str(len(items)))
    return "\n".join(f"  {i+1:>{width}}. {item}" for i, item in enumerate(items))


def header(text: str, level: int = 1) -> str:
    if level == 1:
        return f"\n{'=' * len(text)}\n{text}\n{'=' * len(text)}"
    elif level == 2:
        return f"\n{text}\n{'-' * len(text)}"
    else:
        return f"\n### {text}"


def diff_table(before: Dict, after: Dict) -> str:
    all_keys = set(before.keys()) | set(after.keys())
    rows = []
    for key in sorted(all_keys):
        b = before.get(key, "(missing)")
        a = after.get(key, "(missing)")
        if b != a:
            rows.append({"field": key, "before": str(b), "after": str(a), "changed": "✓"})
        else:
            rows.append({"field": key, "before": str(b), "after": str(a), "changed": ""})
    return table(rows, ["field", "before", "after", "changed"])


def success(text: str) -> str:
    return f"✓ {green(text)}"


def error(text: str) -> str:
    return f"✗ {red(text)}"


def warning(text: str) -> str:
    return f"⚠ {yellow(text)}"


def info(text: str) -> str:
    return f"ℹ {blue(text)}"
