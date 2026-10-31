"""AL-1 Step 0 inventory: Part 573 version counts from the cached listings, a sample plan, and a small URL probe.
Metadata only: no chronology is opened or compared. The default mode makes no network request.
  python scripts/al1_inventory.py          -> reports/al1/AL1_INVENTORY.json, reports/al1/AL1_SAMPLE_PLAN.json
  python scripts/al1_inventory.py --probe  -> fetches 5 earlier-version PDFs into ~/tiertrace_al1_cache/cache, reports/al1/AL1_PROBE.json"""
import argparse
import hashlib
import io
import json
import random
import re
import statistics
import sys
import time
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tt.data.flat import FIELDS, campaign_id  # noqa: E402
from tt.fetch.api import ApiClient, list_573  # noqa: E402
from tt.fetch.nhtsa import UA, Blocked, PoliteFetcher  # noqa: E402

FLAT = "data/flat/FLAT_RCL_POST_2010.zip"
SN1 = Path("~/tiertrace_sn1_cache").expanduser()
AL1 = Path("~/tiertrace_al1_cache").expanduser()
OUT = Path("reports/al1")
EXCLUDE = ["dev_ids", "testA_ids", "testA_labelled_ids", "testB_ids", "unseen_filer_ids"]
RATE_S, N_SAMPLE, SEED = 1.05, 300, 0
PROBE_YEARS = ["2020", "2021", "2023", "2025", "2026"]
MONTHS = "January February March April May June July August September October November December".split()


def flat_campaigns():
    out = {}
    with zipfile.ZipFile(FLAT) as z, z.open(z.namelist()[0]) as raw:
        for line in io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline=""):
            f = line.rstrip("\r\n").split("\t")
            if len(f) != 29:
                continue
            r = dict(zip(FIELDS, f))
            cid = campaign_id(r["CAMPNO"])
            if cid and r["RCDATE"] >= "20200101" and r["RCLTYPECD"] in "VE":
                out.setdefault(cid, {"year": r["RCDATE"][:4], "type": r["RCLTYPECD"]})
    return out


def day(d):
    return date.fromisoformat(d["loadDate"][:10])


def quart(xs):
    q = statistics.quantiles(xs, n=4, method="inclusive")
    return {"n": len(xs), "median": statistics.median(xs), "q1": q[0], "q3": q[2], "iqr": q[2] - q[0], "max": max(xs)}


def label_date(s):
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    try:
        if m:
            return date(int(m[3]), int(m[1]), int(m[2]))
        m = re.search(r"(%s) (\d{1,2}), (\d{4})" % "|".join(MONTHS), s)
        return date(int(m[3]), MONTHS.index(m[1]) + 1, int(m[2])) if m else None
    except ValueError:
        return None


def amendment_no(s):
    m = re.search(r"amendment\s*#?\s*(\d+)", s, re.I)
    return int(m[1]) if m else None


def shares(rows, key):
    n, k = Counter(), Counter()
    for r in rows:
        n[r[key]] += 1
        k[r[key]] += r["n_docs"] >= 2
    return {g: {"campaigns": n[g], "ge2": k[g], "share": round(k[g] / n[g], 4)} for g in sorted(n)}


def load():
    camps = flat_campaigns()
    api = ApiClient(SN1 / "api_cache")
    docs = {}
    for c in sorted(camps):
        if not (SN1 / "api_cache" / f"si_{c}.json").exists():
            raise SystemExit(f"no cached listing for {c}; this script must not fetch listings")
        docs[c] = list_573(api, c)
    assert api.requests_made == 0
    return camps, docs


def dest_name(url):
    return url.replace("https://", "").replace("/", "_")


def make_inventory(camps, docs):
    rows = []
    for c, ds in docs.items():
        days = sorted({day(d) for d in ds})
        rows.append({"campaign": c, **camps[c], "n_docs": len(ds), "n_stamps": len({d["loadDate"] for d in ds}), "n_days": len(days),
                     "gap": (days[-1] - days[0]).days if ds else None,
                     "latest_tied": sum(d["loadDate"] == ds[-1]["loadDate"] for d in ds) > 1 if ds else False})
    ge2 = [r for r in rows if r["n_docs"] >= 2]

    # how far the listing's load dates can be trusted as version dates
    label_diff, load_days = [], Counter()
    order_bad = order_n = first_is_amend = 0
    for c, ds in docs.items():
        for d in ds:
            load_days[d["loadDate"][:10]] += 1
            ld = label_date(d["summary"])
            if ld:
                label_diff.append(abs((day(d) - ld).days))
        am = [(d["loadDate"], amendment_no(d["summary"])) for d in ds if amendment_no(d["summary"]) is not None]
        if len(am) >= 2:
            order_n += 1
            order_bad += any(la < lb and na > nb for la, na in am for lb, nb in am)  # tied stamps have no order, so they never count
        first_is_amend += bool(ds) and amendment_no(ds[0]["summary"]) is not None
    return rows, ge2, {
        "n_campaigns": len(rows),
        "n_docs": sum(r["n_docs"] for r in rows),
        "docs_per_campaign": {str(k): v for k, v in sorted(Counter(r["n_docs"] for r in rows).items())},
        "distinct_load_days_per_campaign": {str(k): v for k, v in sorted(Counter(r["n_days"] for r in rows).items())},
        "ge2_docs": len(ge2),
        "ge2_distinct_stamps": sum(r["n_stamps"] >= 2 for r in rows),
        "ge2_distinct_days": sum(r["n_days"] >= 2 for r in rows),
        "ge2_docs_all_one_day": sum(r["n_docs"] >= 2 and r["n_days"] == 1 for r in rows),
        "campaigns_with_tied_stamps": sum(r["n_stamps"] < r["n_docs"] for r in rows),
        "campaigns_latest_stamp_tied": sum(r["latest_tied"] for r in rows),
        "by_year": shares(rows, "year"),
        "by_type": shares(rows, "type"),
        "by_year_type": {y: shares([r for r in rows if r["year"] == y], "type") for y in sorted({r["year"] for r in rows})},
        "gap_days_ge2_docs": quart([r["gap"] for r in ge2]),
        "gap_days_ge2_days": quart([r["gap"] for r in ge2 if r["n_days"] >= 2]),
        "label_vs_load": {"docs_with_date_in_label": len(label_diff), "abs_diff_days": quart(label_diff),
                          "within_7_days": sum(x <= 7 for x in label_diff)},
        "amendment_labels": {"campaigns_with_2plus_numbered": order_n, "numbers_out_of_load_order": order_bad,
                             "earliest_doc_labelled_amendment": first_is_amend},
        "busiest_load_days": load_days.most_common(5),
    }


def make_plan(rows, docs):
    excl = {name: set((Path("data/splits") / f"{name}.txt").read_text().split()) for name in EXCLUDE}
    union = set().union(*excl.values())
    pool = defaultdict(list)
    for r in rows:
        if r["n_docs"] >= 2 and r["campaign"] not in union:
            pool[r["year"]].append(r["campaign"])
    total = sum(map(len, pool.values()))
    raw = {y: N_SAMPLE * len(v) / total for y, v in pool.items()}
    alloc = {y: int(x) for y, x in raw.items()}
    for y in sorted(raw, key=lambda y: (-(raw[y] - alloc[y]), y))[: N_SAMPLE - sum(alloc.values())]:  # largest remainder
        alloc[y] += 1
    rng = random.Random(SEED)
    sample = {y: sorted(rng.sample(sorted(pool[y]), alloc[y])) for y in sorted(pool)}

    cached = SN1 / "cache"
    byc = {r["campaign"]: r for r in rows}
    need, have, cases = [], 0, []
    for y, cs in sample.items():
        for c in cs:
            for d in docs[c]:
                if (cached / dest_name(d["url"])).exists():
                    have += 1
                else:
                    need.append({"campaign": c, "fileName": d["fileName"], "loadDate": d["loadDate"], "url": d["url"],
                                 "strictly_earlier": d["loadDate"] < docs[c][-1]["loadDate"]})
            cases.append(c)
    pdfs = json.loads((SN1 / "sn1_manifest.json").read_text())["files"]
    sizes = [v["bytes"] for k, v in pdfs.items() if k.startswith("cache/")]
    mean_b = sum(sizes) / len(sizes)
    in_frame = [c for v in pool.values() for c in v]
    plan = {
        "seed": SEED, "n": N_SAMPLE, "stratum": "RCDATE year, proportional allocation (largest remainder)",
        "excluded_files": {k: len(v) for k, v in excl.items()},
        "excluded_union": len(union),
        "ge2_removed_by_exclusion": sum(r["n_docs"] >= 2 and r["campaign"] in union for r in rows),
        "frame": total, "frame_by_year": {y: len(pool[y]) for y in sorted(pool)}, "alloc": dict(sorted(alloc.items())),
        "sample": sample,
        "sample_overlap_with_exclusions": len(set(cases) & union),
        "sample_by_type": dict(Counter(byc[c]["type"] for c in cases)),
        "frame_all_one_day": sum(byc[c]["n_days"] == 1 for c in in_frame),
        "sample_all_one_day": sum(byc[c]["n_days"] == 1 for c in cases),
        "sample_docs_per_campaign": quart([byc[c]["n_docs"] for c in cases]),
        "sample_latest_stamp_tied": sum(byc[c]["latest_tied"] for c in cases),
        "to_fetch_strictly_earlier": sum(d["strictly_earlier"] for d in need),
        "docs_total": have + len(need), "already_cached": have, "pdfs_to_fetch": len(need),
        "estimate": {"rate_s": RATE_S, "seconds": round(len(need) * RATE_S), "minutes": round(len(need) * RATE_S / 60, 1),
                     "mean_pdf_bytes_from_sn1": round(mean_b), "disk_mb": round(len(need) * mean_b / 1e6)},
        "need": need,
    }
    return plan


def probe(plan):
    rng = random.Random(SEED)
    picks = []
    for y in PROBE_YEARS:
        c = rng.choice(sorted({d["campaign"] for d in plan["need"] if d["strictly_earlier"] and d["campaign"] in plan["sample"][y]}))
        picks.append(next(d for d in plan["need"] if d["campaign"] == c and d["strictly_earlier"]))  # need is in load order: earliest version
    fx = PoliteFetcher(AL1 / "cache", rate_s=RATE_S)  # robots.txt check, honest UA
    res = []
    for i, d in enumerate(picks):
        if not fx.robots.can_fetch(UA, d["url"]):
            res.append({**d, "status": "robots-disallowed"})
            continue
        if i:
            time.sleep(RATE_S)
        r = requests.get(d["url"], headers={"User-Agent": UA}, timeout=30)
        if r.status_code in (401, 403, 429):
            raise Blocked(f"{r.status_code} from {d['url']}; stopping")
        is_pdf = r.content[:4] == b"%PDF"  # header bytes only; the PDF is not parsed
        if r.status_code == 200 and is_pdf:
            (fx.cache / dest_name(d["url"])).write_bytes(r.content)
        res.append({**d, "status": r.status_code, "content_type": r.headers.get("Content-Type"), "bytes": len(r.content),
                    "pdf_header": is_pdf, "sha256": hashlib.sha256(r.content).hexdigest(),
                    "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    return {"user_agent": UA, "spacing_s": RATE_S, "results": res}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.probe:
        (OUT / "AL1_PROBE.json").write_text(json.dumps(probe(json.loads((OUT / "AL1_SAMPLE_PLAN.json").read_text())), indent=1))
        print((OUT / "AL1_PROBE.json").read_text())
        return
    camps, docs = load()
    rows, _, inv = make_inventory(camps, docs)
    plan = make_plan(rows, docs)
    (OUT / "AL1_INVENTORY.json").write_text(json.dumps(inv, indent=1, default=str))
    (OUT / "AL1_SAMPLE_PLAN.json").write_text(json.dumps(plan, indent=1))
    print(json.dumps(inv, indent=1, default=str))
    print(json.dumps({k: v for k, v in plan.items() if k not in ("sample", "need")}, indent=1))


if __name__ == "__main__":
    main()
