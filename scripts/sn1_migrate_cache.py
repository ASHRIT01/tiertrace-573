"""SN-1: copy already-cached API listings and latest-version Part 573 PDFs for the SN-1 campaign set from the
old (external-drive) caches to a new cache dir. Old dirs are opened read-only; nothing there is modified or deleted.
Every copy is verified by SHA-256 against its source. A PDF whose size differs from the API's fileSize (bytes or KB) is NOT
copied (possible truncation from an interrupted write) and is reported.
  python scripts/sn1_migrate_cache.py --cache-dir ~/tiertrace_sn1_cache"""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sn1_fetch import campaigns  # noqa: E402

OLD_PDF, OLD_API = Path("data/cache"), Path("data/api_cache")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def size_ok(actual, listed):
    """API fileSize is in bytes for older documents and in KB (rounded) for newer ones."""
    return actual == listed or abs(actual / 1024 - listed) <= 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-dir", required=True)
    a = ap.parse_args()
    root = Path(a.cache_dir).expanduser()
    (root / "cache").mkdir(parents=True, exist_ok=True)
    (root / "api_cache").mkdir(parents=True, exist_ok=True)
    stats = dict(campaigns=0, api_copied=0, api_unparsable=0, pdf_copied=0, pdf_absent=0, pdf_size_mismatch=0,
                 verify_fail=0, no_573=0)
    problems = []
    for cid in campaigns("VE"):
        stats["campaigns"] += 1
        src = OLD_API / f"si_{cid}.json"
        if not src.exists():
            continue
        try:
            d = json.loads(src.read_text())
        except ValueError:
            stats["api_unparsable"] += 1; problems.append(("api_unparsable", cid)); continue
        docs = [x for r in d.get("results", []) for rec in r.get("recalls", []) for x in rec.get("associatedDocuments", [])
                if x.get("summary", "").startswith("Recall 573 Report") or x.get("fileName", "").upper().startswith("RCLRPT")]
        docs.sort(key=lambda x: x["loadDate"])
        pairs = [(src, root / "api_cache" / src.name)]
        if not docs:
            stats["no_573"] += 1
        else:
            url = docs[-1]["url"]
            name = url.replace("https://", "").replace("/", "_")
            psrc = OLD_PDF / name
            if not psrc.exists():
                stats["pdf_absent"] += 1
            elif docs[-1].get("fileSize") and not size_ok(psrc.stat().st_size, docs[-1]["fileSize"]):
                stats["pdf_size_mismatch"] += 1; problems.append(("pdf_size_mismatch", cid, psrc.stat().st_size, docs[-1]["fileSize"]))
            else:
                pairs.append((psrc, root / "cache" / name))
        for s, dst in pairs:
            if not dst.exists():
                shutil.copyfile(s, dst)
            if sha(s) != sha(dst):
                stats["verify_fail"] += 1; problems.append(("verify_fail", str(s)))
            elif s.suffix == ".json":
                stats["api_copied"] += 1
            else:
                stats["pdf_copied"] += 1
    print(json.dumps(stats, indent=1)); print(problems[:20])
    (root / "migrate_report.json").write_text(json.dumps({"stats": stats, "problems": problems}, indent=1))


if __name__ == "__main__":
    main()
