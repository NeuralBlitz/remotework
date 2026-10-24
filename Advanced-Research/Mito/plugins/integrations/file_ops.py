"""
File Operations Plugin
Read, write, search, glob, and stat operations on local files.
"""

import os
import re
import json
import glob as _glob
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.file_ops")


class FileOpsClient:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path).resolve()
        self._deny_paths = {"/etc", "/root", "/.git", "/proc", "/sys", "/dev"}

    def _safe_path(self, path: str) -> Path:
        p = (self.base_path / path).resolve()
        for deny in self._deny_paths:
            if str(p).startswith(deny):
                raise PermissionError(f"Access denied: {path}")
        return p

    def read_file(self, path: str, encoding: str = "utf-8") -> Dict:
        p = self._safe_path(path)
        content = p.read_text(encoding=encoding)
        return {"path": str(p), "content": content, "size": len(content), "lines": content.count("\n") + 1}

    def read_lines(self, path: str, start: int = 1, end: int = None, encoding: str = "utf-8") -> Dict:
        p = self._safe_path(path)
        lines = p.read_text(encoding=encoding).splitlines()
        end = end or len(lines)
        return {"path": str(p), "lines": lines[start-1:end], "total": len(lines)}

    def write_file(self, path: str, content: str, encoding: str = "utf-8", append: bool = False) -> Dict:
        p = self._safe_path(path)
        mode = "a" if append else "w"
        with open(p, mode, encoding=encoding) as f:
            f.write(content)
        return {"path": str(p), "written": len(content), "mode": mode}

    def glob(self, pattern: str, recursive: bool = False) -> List[str]:
        matches = _glob.glob(str(self.base_path / pattern), recursive=recursive)
        return [str(Path(m).relative_to(self.base_path)) for m in matches]

    def search(self, pattern: str, path: str = ".", regex: bool = False,
               case_sensitive: bool = False, max_results: int = 100) -> List[Dict]:
        p = self._safe_path(path)
        if p.is_file():
            paths = [p]
        else:
            paths = list(p.rglob("*")) if p.is_dir() else []

        results = []
        flags = 0 if regex else re.IGNORECASE if not case_sensitive else 0

        for fp in paths:
            if not fp.is_file():
                continue
            try:
                content = fp.read_text(errors="ignore")
                if regex:
                    matches = re.finditer(pattern, content, flags)
                else:
                    needle = pattern if case_sensitive else pattern.lower()
                    for i, line in enumerate(content.splitlines(), 1):
                        hay = line if case_sensitive else line.lower()
                        if needle in hay:
                            matches = [(i, line)]
                            for m in matches:
                                results.append({
                                    "file": str(fp.relative_to(self.base_path)),
                                    "line": m[0],
                                    "text": m[1],
                                })
                                if len(results) >= max_results:
                                    return results
                            continue
                    continue

                for i, line in enumerate(content.splitlines(), 1):
                    if (regex and re.search(pattern, line, flags)) or (not regex and pattern in (line if case_sensitive else line.lower())):
                        results.append({"file": str(fp.relative_path(self.base_path)), "line": i, "text": line.rstrip()})
                        if len(results) >= max_results:
                            return results
            except (PermissionError, OSError):
                pass

        return results

    def stat(self, path: str) -> Dict:
        p = self._safe_path(path)
        s = p.stat()
        return {
            "path": str(p),
            "size": s.st_size,
            "modified": s.st_mtime,
            "created": s.st_ctime,
            "is_file": p.is_file(),
            "is_dir": p.is_dir(),
            "is_symlink": p.is_symlink(),
            "permissions": oct(s.st_mode)[-3:],
        }

    def list_dir(self, path: str = ".") -> Dict:
        p = self._safe_path(path)
        items = list(p.iterdir())
        return {
            "path": str(p),
            "dirs": [i.name for i in items if i.is_dir()],
            "files": [i.name for i in items if i.is_file()],
            "total": len(items),
        }

    def exists(self, path: str) -> bool:
        return self._safe_path(path).exists()

    def line_count(self, path: str) -> int:
        p = self._safe_path(path)
        return len(p.read_text(errors="ignore").splitlines())

    def tree(self, path: str = ".", max_depth: int = 3) -> List[str]:
        p = self._safe_path(path)
        lines = []

        def _walk(current: Path, prefix: str = "", depth: int = 0):
            if depth >= max_depth:
                return
            items = sorted(current.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{item.name}")
                if item.is_dir():
                    _walk(item, prefix + ("    " if is_last else "│   "), depth + 1)

        lines.append(p.name)
        _walk(p)
        return lines


def file_read_cmd(path: str = "") -> Dict:
    """Read the full contents of a file."""
    return FileOpsClient().read_file(path)


def file_write_cmd(path: str = "", content: str = "") -> Dict:
    """Write content to a file. Creates or overwrites."""
    return FileOpsClient().write_file(path, content)


def file_append_cmd(path: str = "", content: str = "") -> Dict:
    """Append content to a file."""
    return FileOpsClient().write_file(path, content, append=True)


def file_search_cmd(pattern: str = "", path: str = ".", regex: bool = False) -> List[Dict]:
    """Search for text or regex pattern in files."""
    return FileOpsClient().search(pattern, path=path, regex=regex)


def file_glob_cmd(pattern: str = "") -> List[str]:
    """Glob pattern matching for files."""
    return FileOpsClient().glob(pattern, recursive=True)


def file_stat_cmd(path: str = "") -> Dict:
    """Get file/directory statistics."""
    return FileOpsClient().stat(path)


def file_tree_cmd(path: str = ".", max_depth: int = 3) -> List[str]:
    """List directory as a tree structure."""
    return FileOpsClient().tree(path=path, max_depth=max_depth)


def file_list_cmd(path: str = ".") -> Dict:
    """List directory contents."""
    return FileOpsClient().list_dir(path)


def file_exists_cmd(path: str = "") -> bool:
    """Check if a file or directory exists."""
    return FileOpsClient().exists(path)


def file_lines_cmd(path: str = "", start: int = 1, end: int = None) -> Dict:
    """Read specific lines from a file (1-indexed)."""
    return FileOpsClient().read_lines(path, start=start, end=end)


def register(plugin):
    plugin.register_command("file_read", file_read_cmd)
    plugin.register_command("file_write", file_write_cmd)
    plugin.register_command("file_append", file_append_cmd)
    plugin.register_command("file_search", file_search_cmd)
    plugin.register_command("file_glob", file_glob_cmd)
    plugin.register_command("file_stat", file_stat_cmd)
    plugin.register_command("file_tree", file_tree_cmd)
    plugin.register_command("file_list", file_list_cmd)
    plugin.register_command("file_exists", file_exists_cmd)
    plugin.register_command("file_lines", file_lines_cmd)
    plugin.set_resource("client_class", FileOpsClient)


PLUGIN_METADATA = {
    "name": "file_ops",
    "version": "1.0.0",
    "description": "File operations - read, write, search, glob, stat, tree, list",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["file", "read", "write", "search", "glob", "filesystem"],
    "dependencies": [],
    "permissions": ["read_files", "write_files"],
    "min_mito_version": "1.0.1",
}


file_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
