"""AL-1 Step 0b: resample (>= 2 distinct load days), fetch every Part 573 version, order versions by the Submission Date header.
Only the Submission Date line of page 1 is kept; page text is matched and discarded, nothing else is read, stored or printed.
  python scripts/al1_step0b.py plan   -> reports/al1/AL1_SAMPLE_PLAN_v2.json (no network)
  python scripts/al1_step0b.py fetch  -> ~/tiertrace_al1_cache/cache, reports/al1/AL1_FETCH.json; log runs/al1_fetch.log; exit 2 if blocked
  python scripts/al1_step0b.py order  -> reports/al1/AL1_ORDER.json, ~/tiertrace_al1_cache/al1_manifest.json (prints its SHA-256)"""
import argparse
import hashlib
import json
import re
import shutil
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from al1_inventory import AL1, OUT, RATE_S, SN1, dest_name, load, make_inventory, make_plan  # noqa: E402
from tt.fetch.nhtsa import UA, PoliteFetcher  # noqa: E402

PLAN, FETCH, ORDER = OUT / "AL1_SAMPLE_PLAN_v2.json", OUT / "AL1_FETCH.json", OUT / "AL1_ORDER.json"
LOG = Path("runs/al1_fetch.log")
SUB_RE = re.compile(r"Submission\s*Date\s*:\s*([A-Za-z]{3,9})\.?\s+(\d{1,2}),\s*(\d{4})")
BLOCK = (401, 403, 429)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def cmd_plan():
    camps, docs = load()
    rows, _, _ = make_inventory(camps, docs)
    plan = make_plan(rows, docs, min_days=2)
    plan["eligibility"] = ">= 2 Part 573 documents on >= 2 distinct load days, dev/test IDs excluded"
    sampled = sorted(c for v in plan["sample"].values() for c in v)
    plan["documents"] = {c: docs[c] for c in sampled}  # every version, in load order
    PLAN.write_text(json.dumps(plan, indent=1))
    print(json.dumps({k: v for k, v in plan.items() if k not in ("sample", "need", "documents")}, indent=1))


def cmd_fetch():
    plan = json.loads(PLAN.read_text())
    fx = PoliteFetcher(AL1 / "cache", rate_s=RATE_S)  # robots.txt check, honest UA
    sn1_sha = json.loads((SN1 / "sn1_manifest.json").read_text())["files"]
    allv = [d for ds in plan["documents"].values() for d in ds]
    log(f"START documents={len(allv)} campaigns={len(plan['documents'])}")
    last = time.monotonic()  # robots.txt was just requested
    n = Counter()
    recs = []

    def attempt(url):
        nonlocal last
        wait = RATE_S - (time.monotonic() - last)
        if wait > 0:
            time.sleep(wait)
        last = time.monotonic()
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
        except requests.RequestException as e:
            return None, b"", f"{type(e).__name__}: {e}"
        return r.status_code, r.content, None

    for i, d in enumerate(allv, 1):
        name, url = dest_name(d["url"]), d["url"]
        dest = fx.cache / name
        rec = {"campaign": d["campaign"], "fileName": d["fileName"], "url": url}
        if dest.exists():
            b = dest.read_bytes()
            if b[:4] == b"%PDF":
                n["already_in_al1_cache"] += 1
                recs.append({**rec, "outcome": "ALREADY_CACHED", "source": "al1_cache", "sha256": sha(b)})
                continue
            log(f"FAIL existing file is not a PDF: {name}")
            sys.exit(3)
        src = SN1 / "cache" / name
        if src.exists():
            b = src.read_bytes()
            want = sn1_sha.get(f"cache/{name}", {}).get("sha256")
            if sha(b) != want:
                n["sn1_hash_mismatch"] += 1
                log(f"SN-1 hash mismatch {name}; refetching")
            elif b[:4] != b"%PDF":
                n["sn1_copy_not_pdf"] += 1
                log(f"SN-1 copy is not a PDF {name}; refetching")
            else:
                shutil.copyfile(src, dest)
                if sha(dest.read_bytes()) != want:
                    dest.unlink()
                    log(f"FAIL copy hash mismatch {name}")
                    sys.exit(3)
                n["copied_from_sn1"] += 1
                recs.append({**rec, "outcome": "COPIED", "source": "sn1_cache", "sha256": want})
                continue
        if not fx.robots.can_fetch(UA, url):
            n["robots_disallowed"] += 1
            recs.append({**rec, "outcome": "ROBOTS_DISALLOWED"})
            continue
        tries = []
        ok = False
        for k in range(2):  # first try plus one retry
            status, body, err = attempt(url)
            n["requests"] += 1
            if status in BLOCK:
                FETCH.write_text(json.dumps({"stopped": True, "reason": f"{status} from {url}", "counts": dict(n), "records": recs}, indent=1))
                log(f"BLOCKED {status} from {url}; stopping")
                sys.exit(2)
            tries.append({"status": status, "error": err, "bytes": len(body), "first_100_bytes": body[:100].decode("latin-1")})
            if status == 200 and body[:4] == b"%PDF":
                dest.write_bytes(body)
                ok = True
                n["fetched"] += 1
                n["retried_ok"] += k == 1
                recs.append({**rec, "outcome": "FETCHED", "source": "http", "status": status, "tries": k + 1, "sha256": sha(body)})
                break
        if not ok:
            n["NON_PDF"] += 1
            recs.append({**rec, "outcome": "NON_PDF", "tries": tries})
            log(f"NON_PDF {d['campaign']} {name} {[t['status'] for t in tries]}")
        if i % 100 == 0:
            log(f"PROGRESS {i}/{len(allv)} {dict(n)}")
    FETCH.write_text(json.dumps({"stopped": False, "user_agent": UA, "spacing_s": RATE_S, "counts": dict(n), "records": recs}, indent=1))
    log(f"DONE {len(allv)} {dict(n)}")


def cmd_fix_case():
    """URLs differing only in case share one path on this case-insensitive disk, so the later one was never requested. Fetch it now;
    keep it under a separate name only if its bytes differ."""
    plan = json.loads(PLAN.read_text())
    F = json.loads(FETCH.read_text())
    fx = PoliteFetcher(AL1 / "cache", rate_s=RATE_S)
    first = {}
    done = []
    for rec in F["records"]:
        k = rec["url"].lower()
        if k not in first:
            first[k] = rec
            continue
        time.sleep(RATE_S)
        for t in range(2):
            r = requests.get(rec["url"], headers={"User-Agent": UA}, timeout=30)
            F["counts"]["requests"] += 1
            if r.status_code in BLOCK:
                log(f"BLOCKED {r.status_code} from {rec['url']}; stopping")
                sys.exit(2)
            if r.status_code == 200 and r.content[:4] == b"%PDF":
                break
            time.sleep(RATE_S)
        else:
            raise SystemExit(f"non-PDF for {rec['url']}: {r.status_code} {r.content[:100]!r}")
        h, same = sha(r.content), sha(r.content) == first[k].get("sha256")
        rec.update(outcome="FETCHED", source="http", status=r.status_code, tries=t + 1, sha256=h, case_variant_of=first[k]["url"], same_bytes=same)
        if not same:
            rec["local_name"] = dest_name(rec["url"]).rsplit(".", 1)[0] + "__casevariant.PDF"
            (fx.cache / rec["local_name"]).write_bytes(r.content)
        F["counts"]["fetched"] += 1
        F["counts"]["already_in_al1_cache"] -= 1
        F["counts"]["case_variants_refetched"] = F["counts"].get("case_variants_refetched", 0) + 1
        done.append({"url": rec["url"], "status": r.status_code, "same_bytes": same, "bytes": len(r.content)})
    FETCH.write_text(json.dumps(F, indent=1))
    log(f"FIX_CASE {done}")


def submission_dates(path):
    """Dates on the Submission Date line of page 1, and the page's text length (to tell image-only files apart). Page text is discarded."""
    import pymupdf
    with pymupdf.open(path) as pdf:
        text = pdf[0].get_text() if len(pdf) else ""
    out = []
    for m in SUB_RE.finditer(text):
        for f in ("%b %d %Y", "%B %d %Y"):
            try:
                out.append(datetime.strptime(f"{m[1]} {m[2]} {m[3]}", f).date().isoformat())
                break
            except ValueError:
                pass
    return out, bool(text.strip())


def is_amend(summary):
    return bool(re.search(r"amend", summary, re.I))


def cmd_order():
    plan = json.loads(PLAN.read_text())
    res = {r["url"]: r for r in json.loads(FETCH.read_text())["records"]}
    cache = AL1 / "cache"
    camps = {}
    dcount = Counter()
    for c, ds in plan["documents"].items():
        vers = []
        for d in ds:
            rec = res[d["url"]]
            v = {"fileName": d["fileName"], "loadDate": d["loadDate"], "amendment_label": is_amend(d["summary"]), "outcome": rec["outcome"]}
            if rec["outcome"] in ("NON_PDF", "ROBOTS_DISALLOWED"):
                v["usable"] = False
            else:
                dates, has_text = submission_dates(cache / rec.get("local_name", dest_name(d["url"])))
                v.update(usable=True, sha256=rec["sha256"], submission_date=dates[0] if len(set(dates)) == 1 else None,
                         n_submission_lines=len(dates), has_text=has_text)
                dcount["one_date" if len(set(dates)) == 1 else "conflicting_dates" if dates else "no_date_text" if has_text else "no_text_layer"] += 1
            vers.append(v)
        use = [v for v in vers if v["usable"]]
        no_date = [v for v in use if not v["submission_date"]]
        use.sort(key=lambda v: (v["submission_date"] or "", v["loadDate"]))
        keys = [(v["submission_date"], v["loadDate"]) for v in use]
        tied = len(set(keys)) < len(keys)
        reason = "no_submission_date" if no_date else "same_date_and_load_timestamp" if tied else None
        identical = tied and not no_date and all(
            len({v["sha256"] for v in use if (v["submission_date"], v["loadDate"]) == k}) == 1 for k in keys if keys.count(k) > 1)
        # earliest group: all versions sharing the first key; the original is missing only if every one of them is labelled an amendment
        if no_date or not use:
            early = [v for v in vers if v["loadDate"] == vers[0]["loadDate"]]  # load order is the only order available
            basis = "load_timestamp"
        else:
            early = [v for v in use if (v["submission_date"], v["loadDate"]) == keys[0]]
            basis = "submission_date"
        load_early = [v for v in vers if v["loadDate"] == vers[0]["loadDate"]]
        dates_only = [v["submission_date"] for v in use if v["submission_date"]]
        load_seq = [v["submission_date"] for v in sorted(use, key=lambda v: v["loadDate"]) if v["submission_date"]]
        camps[c] = {
            "order_status": "ORDER_AMBIGUOUS" if reason else "ORDERED", "ambiguous_reason": reason, "tied_files_byte_identical": bool(identical),
            "ORIGINAL_MISSING": all(v["amendment_label"] for v in early), "original_missing_basis": basis,
            "original_missing_by_load_order": all(v["amendment_label"] for v in load_early),
            "NON_PDF_docs": sum(v["outcome"] == "NON_PDF" for v in vers), "usable_docs": len(use),
            "same_date_broken_by_load": len(set(dates_only)) < len(dates_only) and not tied,
            "date_order_differs_from_load": load_seq != sorted(load_seq),
            "versions_in_order": [v["fileName"] for v in use], "submission_dates": [v.get("submission_date") for v in use],
            "versions": vers,
        }
    V = camps.values()
    summary = {
        "campaigns": len(camps), "documents": sum(len(c["versions"]) for c in V), "documents_by_date_result": dict(dcount),
        "ORDERED": sum(c["order_status"] == "ORDERED" for c in V), "ORDER_AMBIGUOUS": sum(c["order_status"] == "ORDER_AMBIGUOUS" for c in V),
        "ambiguous_reasons": dict(Counter(c["ambiguous_reason"] for c in V if c["ambiguous_reason"])),
        "ambiguous_tied_byte_identical": sum(c["tied_files_byte_identical"] for c in V),
        "ORIGINAL_MISSING": sum(c["ORIGINAL_MISSING"] for c in V),
        "ORIGINAL_MISSING_by_load_order": sum(c["original_missing_by_load_order"] for c in V),
        "ORIGINAL_MISSING_and_ORDERED": sum(c["ORIGINAL_MISSING"] and c["order_status"] == "ORDERED" for c in V),
        "NON_PDF_documents": sum(c["NON_PDF_docs"] for c in V), "NON_PDF_campaigns": sum(c["NON_PDF_docs"] > 0 for c in V),
        "ordered_with_2plus_usable": sum(c["order_status"] == "ORDERED" and c["usable_docs"] >= 2 for c in V),
        "ordered_needing_load_tiebreak": sum(c["same_date_broken_by_load"] and c["order_status"] == "ORDERED" for c in V),
        "date_order_differs_from_load": sum(c["date_order_differs_from_load"] for c in V),
        "ids": {k: sorted(x for x, c in camps.items() if p(c)) for k, p in (
            ("ORDER_AMBIGUOUS", lambda c: c["order_status"] == "ORDER_AMBIGUOUS"), ("ORIGINAL_MISSING", lambda c: c["ORIGINAL_MISSING"]),
            ("NON_PDF", lambda c: c["NON_PDF_docs"] > 0))},
    }
    ORDER.write_text(json.dumps({"summary": summary, "campaigns": camps}, indent=1))

    planned = {res[d["url"]].get("local_name", dest_name(d["url"])) for ds in plan["documents"].values() for d in ds}
    files = {}
    for p in sorted(cache.iterdir()):
        if p.name.startswith("._"):
            continue
        b = p.read_bytes()
        files[f"cache/{p.name}"] = {"sha256": sha(b), "bytes": len(b), "in_sample": p.name in planned}
    manifest = {"n_files": len(files), "n_in_sample": sum(f["in_sample"] for f in files.values()),
                "total_bytes": sum(f["bytes"] for f in files.values()), "files": files}
    mp = AL1 / "al1_manifest.json"
    mp.write_text(json.dumps(manifest, indent=1))
    print(json.dumps(summary, indent=1))
    print("manifest", {k: v for k, v in manifest.items() if k != "files"}, sha(mp.read_bytes()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "fetch", "fix-case", "order"])
    {"plan": cmd_plan, "fetch": cmd_fetch, "fix-case": cmd_fix_case, "order": cmd_order}[ap.parse_args().cmd]()
