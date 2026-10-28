"""SN-1: SHA-256 manifest of every fetched file (PDFs and API listings) in the SN-1 cache dir.
  python scripts/sn1_manifest.py [--cache-dir ~/tiertrace_sn1_cache] -> <cache-dir>/sn1_manifest.json (+ prints its SHA-256)"""
import argparse
import hashlib
import json
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--cache-dir", default="~/tiertrace_sn1_cache")
a = ap.parse_args()
root = Path(a.cache_dir).expanduser()
files = {}
for sub in ("cache", "api_cache"):
    for p in sorted((root / sub).iterdir()):
        files[f"{sub}/{p.name}"] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size}
out = root / "sn1_manifest.json"
out.write_text(json.dumps({"n_files": len(files), "n_pdfs": sum(k.startswith("cache/") for k in files),
                           "n_listings": sum(k.startswith("api_cache/") for k in files),
                           "total_bytes": sum(v["bytes"] for v in files.values()), "files": files}, indent=1))
print(len(files), "files;", hashlib.sha256(out.read_bytes()).hexdigest(), out)
