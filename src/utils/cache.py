import json
import os
import subprocess
from pathlib import Path
from datetime import datetime

def file_mtime(path: Path) -> int:
    """Get modification time as an integer timestamp, or 0 if missing."""
    return int(path.stat().st_mtime) if path.exists() else 0

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

def load_meta(meta_file: Path) -> dict:
    """Load .cache_meta.json if it exists, otherwise return empty dict."""
    if meta_file.exists():
        with open(meta_file) as f:
            return json.load(f)
    return {}

def save_meta(df_file: Path, parquet_file: Path, meta_file: Path):
    """Save modification times and UTC timestamp to .cache_meta.json."""
    meta = {
        "df_chembl.csv": file_mtime(df_file),
        "sql_chembl_cache.parquet": file_mtime(parquet_file),
        "updated_at": datetime.utcnow().isoformat()
    }
    with open(meta_file, "w") as f:
        json.dump(meta, f, indent=2)

def run_update_script(script_path: Path):
    """Run the cache update shell script."""
    print("Running update_cache.sh to upload changed cache files...")
    subprocess.run(["bash", str(script_path)], check=True)
