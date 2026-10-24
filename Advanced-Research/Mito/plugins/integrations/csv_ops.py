"""
CSV Operations Plugin
Read, write, filter, merge, and analyze CSV data.
"""
import csv as csv_lib
import io
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.csv_ops")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


def csv_read_cmd(file_path: str = "", limit: int = 1000) -> List[Dict]:
    rows = []
    with open(file_path, newline="") as f:
        reader = csv_lib.DictReader(f)
        for i, row in enumerate(reader):
            if i >= limit:
                break
            rows.append(dict(row))
    return {"rows": rows, "count": len(rows)}


def csv_write_cmd(file_path: str = "", data: str = "", headers: str = "") -> Dict:
    rows = __import__("json").loads(data) if data.startswith("[") else []
    hdrs = headers.split(",") if headers else (list(rows[0].keys()) if rows else [])
    with open(file_path, "w", newline="") as f:
        writer = csv_lib.DictWriter(f, fieldnames=hdrs)
        writer.writeheader()
        writer.writerows(rows)
    return {"status": "written", "rows": len(rows), "path": file_path}


def csv_filter_cmd(file_path: str = "", column: str = "", value: str = "", limit: int = 100) -> List[Dict]:
    results = []
    with open(file_path, newline="") as f:
        reader = csv_lib.DictReader(f)
        for i, row in enumerate(reader):
            if i >= limit:
                break
            if row.get(column, "") == value:
                results.append(dict(row))
    return {"rows": results, "count": len(results)}


def csv_stats_cmd(file_path: str = "") -> Dict:
    if not PANDAS_AVAILABLE:
        rows, cols = 0, 0
        with open(file_path, newline="") as f:
            reader = csv_lib.reader(f)
            for row in reader:
                rows += 1
                cols = max(cols, len(row))
        return {"rows": rows - 1, "columns": cols, "note": "Install pandas for detailed stats"}
    df = pd.read_csv(file_path)
    return {
        "rows": len(df), "columns": len(df.columns),
        "numeric_columns": list(df.select_dtypes(include="number").columns),
        "dtypes": {c: str(d) for c, d in df.dtypes.items()},
        "describe": df.describe().to_dict(),
    }


def csv_merge_cmd(files: str = "", output: str = "") -> Dict:
    file_list = files.split(",") if files else []
    all_rows = []
    for fp in file_list:
        fp = fp.strip()
        with open(fp, newline="") as f:
            reader = csv_lib.DictReader(f)
            all_rows.extend(list(reader))
    with open(output, "w", newline="") as f:
        if all_rows:
            writer = csv_lib.DictWriter(f, fieldnames=list(all_rows[0].keys()))
            writer.writeheader()
            writer.writerows(all_rows)
    return {"status": "merged", "total_rows": len(all_rows), "output": output}


def csv_to_json_cmd(file_path: str = "", output: str = "") -> Dict:
    rows = csv_read_cmd(file_path=file_path)["rows"]
    with open(output, "w") as f:
        __import__("json").dump(rows, f, indent=2)
    return {"status": "converted", "rows": len(rows), "output": output}


def register(plugin):
    plugin.register_command("read", csv_read_cmd)
    plugin.register_command("write", csv_write_cmd)
    plugin.register_command("filter", csv_filter_cmd)
    plugin.register_command("stats", csv_stats_cmd)
    plugin.register_command("merge", csv_merge_cmd)
    plugin.register_command("to_json", csv_to_json_cmd)


PLUGIN_METADATA = {
    "name": "csv_ops", "version": "1.0.0",
    "description": "CSV read, write, filter, merge, and analysis",
    "author": "Mito Team", "license": "MIT",
    "tags": ["csv", "data", "tabular", "utilities"],
    "dependencies": ["pandas"], "permissions": ["read_files", "write_files"],
    "min_mito_version": "1.0.1",
}

csv_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
