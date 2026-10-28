"""SN-1 Step 0: fetch the latest Part 573 report PDF for every flat-file campaign with RCDATE >= 2020-01-01.
Reuses tt.fetch (identifying UA, robots check, on-disk cache) and list_573 (API doc listing, cached).
Resumable: anything already in data/api_cache or data/cache is skipped without a request.
Combined rate across API + PDF calls stays under 1 request/s. Stops on 401/403/429 (project rule).
  python scripts/sn1_fetch.py [--types VE] [--limit N] [--cache-dir DIR]   appends to runs/sn1_fetch.log; failures -> runs/sn1_failures.jsonl"""
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tt.data.flat import FIELDS, campaign_id  # noqa: E402
from tt.fetch.api import ApiClient, list_573  # noqa: E402
from tt.fetch.nhtsa import Blocked, PoliteFetcher  # noqa: E402

import io, zipfile  # noqa: E402,E401

FLAT = "data/flat/FLAT_RCL_POST_2010.zip"
LOG, FAIL = Path("runs/sn1_fetch.log"), Path("runs/sn1_failures.jsonl")


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def campaigns(types):
    out = {}
    with zipfile.ZipFile(FLAT) as z, z.open(z.namelist()[0]) as raw:
        for line in io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline=""):
            f = line.rstrip("\r\n").split("\t")
            if len(f) != 29:
                continue
            r = dict(zip(FIELDS, f))
            cid = campaign_id(r["CAMPNO"])
            if cid and r["RCDATE"] >= "20200101" and r["RCLTYPECD"] in types:
                out.setdefault(cid, r["RCDATE"])
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--types", default="VE")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--cache-dir", default=None,
                    help="root holding cache/ (PDFs) and api_cache/ (listings); default: data/cache and data/api_cache")
    a = ap.parse_args()
    camps = campaigns(a.types)
    if a.limit:
        camps = camps[:a.limit]
    log(f"START campaigns={len(camps)} types={a.types} cache_dir={a.cache_dir or 'data (default)'}")
    if a.cache_dir:
        root = Path(a.cache_dir).expanduser()
        api, fx = ApiClient(root / "api_cache", rate_s=1.05), PoliteFetcher(root / "cache", rate_s=1.05)
    else:
        api, fx = ApiClient(rate_s=1.05), PoliteFetcher(Path("data/cache"), rate_s=1.05)

    def sync():  # one shared clock so API + PDF calls together stay <= 1/s
        t = max(api._last, fx._last)
        api._last = fx._last = t

    n = dict(pdf_cached=0, pdf_new=0, no_573=0, fail=0)
    for i, c in enumerate(camps, 1):
        try:
            sync()
            docs = list_573(api, c)
            if not docs:
                n["no_573"] += 1
                with open(FAIL, "a") as f:
                    f.write(json.dumps({"campaign": c, "reason": "no_573_in_api_listing_or_api_non200"}) + "\n")
                continue
            url = docs[-1]["url"]
            dest = fx.cache / url.replace("https://", "").replace("/", "_")
            if dest.exists():
                n["pdf_cached"] += 1
                continue
            sync()
            if fx.get(url) is None:
                raise RuntimeError("pdf non-200 or robots-disallowed")
            n["pdf_new"] += 1
        except Blocked as e:
            log(f"BLOCKED {e}; stopping at {c}")
            sys.exit(2)
        except (requests.RequestException, RuntimeError) as e:
            n["fail"] += 1
            log(f"FAIL {c} {type(e).__name__}: {e}")
            with open(FAIL, "a") as f:
                f.write(json.dumps({"campaign": c, "reason": f"{type(e).__name__}: {e}"}) + "\n")
            time.sleep(2)
        if i % 100 == 0:
            log(f"PROGRESS {i}/{len(camps)} {n}")
    log(f"DONE {len(camps)} {n}")


if __name__ == "__main__":
    main()
