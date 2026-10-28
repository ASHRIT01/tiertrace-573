"""Live SN-1 progress from the cache directory (not from the log): campaigns with their latest Part 573 PDF present,
campaigns whose listing has no 573 document, campaigns not yet listed, unparsable listings, and the ETA at 2.15 s/campaign.
  python scripts/sn1_progress.py [--cache-dir ~/tiertrace_sn1_cache]"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sn1_fetch import campaigns  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--cache-dir", default="~/tiertrace_sn1_cache")
a = ap.parse_args()
root = Path(a.cache_dir).expanduser()
camps = campaigns("VE")
have = no573 = unlisted = bad = 0
for c in camps:
    f = root / "api_cache" / f"si_{c}.json"
    if not f.exists():
        unlisted += 1; continue
    try:
        d = json.loads(f.read_text())
    except ValueError:
        bad += 1; continue
    docs = sorted((x for r in d.get("results", []) for rec in r.get("recalls", []) for x in rec.get("associatedDocuments", [])
                   if x.get("summary", "").startswith("Recall 573 Report") or x.get("fileName", "").upper().startswith("RCLRPT")),
                  key=lambda x: x["loadDate"])
    if not docs:
        no573 += 1
    elif (root / "cache" / docs[-1]["url"].replace("https://", "").replace("/", "_")).exists():
        have += 1
    else:
        unlisted += 1  # listed but PDF still to fetch / failed
todo = len(camps) - have - no573
fails, no573_logged = set(), set()
fp = Path("runs/sn1_failures.jsonl")
if fp.exists():
    for line in fp.read_text().splitlines():
        r = json.loads(line)
        (no573_logged if "no_573" in r["reason"] else fails).add(r["campaign"])
# files this fetch phase wrote itself (mtime after the last START that used --cache-dir), as opposed to copied-in ones
start = None
for line in Path("runs/sn1_fetch.log").read_text().splitlines():
    if " START " in line and "cache_dir=/" in line:
        start = datetime.fromisoformat(line.split()[0]).timestamp()
new_pdfs = sum(1 for p in (root / "cache").iterdir() if start and p.stat().st_mtime > start)
n_pdf_files, n_listings = len(list((root / "cache").iterdir())), len(list((root / "api_cache").iterdir()))
print(f"{have + no573:,} of {len(camps):,} campaigns done = {have:,} with latest 573 PDF on disk + {no573} with no 573 in listing; "
      f"{todo:,} to go; failures (non-573): {len(fails)}; unparsable listings: {bad}; ETA {todo * 2.15 / 3600:.1f} h")
print(f"on disk: {n_pdf_files:,} PDF files, {n_listings:,} listings; fetched since the cache move: {new_pdfs:,} PDFs "
      f"(rest were copied in); distinct campaigns logged with no 573 document: {len(no573_logged)}")
