# cache.py

import json
from pathlib import Path

def file_mtime(path: Path) -> float:
    """Get modification time as a float timestamp, or 0 if missing."""
    return path.stat().st_mtime if path.exists() else 0

def should_download(df_file: Path, parquet_file: Path, meta_file: Path) -> bool:
    """Check whether cache files are missing or outdated compared to meta."""
    if not meta_file.exists():
        return True
    with open(meta_file) as f:
        meta = json.load(f)
    return (
        file_mtime(df_file) < meta.get("df_chembl.csv", 0) or
        file_mtime(parquet_file) < meta.get("sql_chembl_cache.parquet", 0)
    )
