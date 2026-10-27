"""TS-1 Step 0 inventory: counts and field checks only. Computes NO gaps and NO date differences.
Reads (read-only): config/<split>_selection.json, the processed PDFs (frozen text extraction), the NHTSA flat file, the version listings,
silver labels, runs/ts/<split>_agent_events.json (frozen gate decisions, from scripts/ts_gate.py).
  python scripts/ts_inventory.py  -> reports/ts/TS_INVENTORY.json (aggregates only; no company names, no recall numbers)"""
import io
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ts_lib import cites_other_recall, date_format  # noqa: E402
from tt.data.flat import FIELDS  # noqa: E402
from tt.parse.pdf import extract_text  # noqa: E402
from tt.parse.sections import parse_header  # noqa: E402

SPLITS = {"testA": "data/testA_raw", "testB": "data/testB_raw", "unseen": "data/unseen_raw"}
LISTINGS = ["data/processed/testA_573.jsonl", "data/processed/testB_573.jsonl", "data/labels/work/unseen/listing.jsonl"]
SUB_RE = re.compile(r"Submission\s*Date\s*:\s*([A-Za-z]{3,9})\.?\s+(\d{1,2}),\s*(\d{4})")
_M = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
TYPE_HDR = re.compile(r"Description of (?:the\s+)?(Defect|Noncompliance)\s*:")
NEW_LAYOUT = "Defect / Noncompliance Description"
REDACT = [(re.compile(r"\d{2}[VECT]-?\d{3}"), "[recall no.]")]


def sub_dates(t: str) -> list[date]:
    out = []
    for m in SUB_RE.finditer(t):
        try:
            out.append(date(int(m[3]), _M[m[1].lower()[:3]], int(m[2])))
        except (KeyError, ValueError):
            out.append(None)
    return out


def campaign_of(fn: str) -> str:
    return re.match(r"RCLRPT-(\d{2}[VECT]\d{3})-", fn)[1]


def header_example(t: str) -> str:
    """The header lines around the Submission Date with every value except the date redacted."""
    m = SUB_RE.search(t)
    lines = t[:m.start()].split("\n")[-3:] + [t[m.start():m.end()]] + t[m.end():].split("\n")[1:3]
    out = []
    for ln in lines:
        if SUB_RE.search(ln):
            out.append(ln.strip())
        elif ":" in ln:
            out.append(ln.split(":")[0].strip() + ": [redacted]")
        elif ln.strip():
            out.append("[redacted line]")
    return " / ".join(out)


def main():
    R = {"note": "silver reference (AI-generated, not human-verified); counts and field checks only; no gap or date difference computed"}
    sel = {s: json.load(open(f"config/{s}_selection.json")) for s in SPLITS}
    R["1_filings"] = {s: {"processed_readable": len(sel[s]["filings"]), "unreadable_listed_in_selection": len(sel[s]["unreadable"])} for s in SPLITS}
    # ---- 2. submission date + layout + type header
    texts, layout, sub, examples, fails = {}, Counter(), Counter(), [], []
    hdr_agree = Counter()
    silver = {s: {x["file"]: x for x in json.load(open(f"data/labels/{s}_silver.json"))} for s in SPLITS}
    ex_seen = Counter()
    for s, d in SPLITS.items():
        for x in sel[s]["filings"]:
            t, _ = extract_text(f"{d}/{x['file']}")
            texts[x["file"]] = (s, t)
            lay = "2025+ form (label and value on separate lines)" if NEW_LAYOUT in t else "pre-2025 form (label : value on one line)"
            layout[(s, lay)] += 1
            ds = sub_dates(t)
            if not ds:
                sub[(s, "no match")] += 1; fails.append(lay); continue
            if any(v is None for v in ds):
                sub[(s, "matched but not a valid date")] += 1; fails.append(lay); continue
            sub[(s, "parsed")] += 1
            sub[(s, "occurrences>1 all equal" if len(ds) > 1 and len(set(ds)) == 1 else "occurrences>1 DIFFER" if len(ds) > 1 else "single occurrence")] += 1
            sub[(s, "one-digit day in text")] += bool(re.search(r"Submission\s*Date\s*:\s*[A-Za-z]{3,9}\.?\s+\d,", t))
            fh = parse_header(t)["filing_date"]
            hdr_agree[(s, "equals frozen parse_header filing_date" if fh == ds[0] else "differs from frozen parse_header")] += 1
            sl = silver[s][x["file"]].get("filing_date")
            hdr_agree[(s, "equals silver label filing_date" if sl == ds[0].isoformat() else "differs from silver label filing_date")] += 1
            if ex_seen[(s, lay)] < 1:                       # one example per split and layout (5 combinations exist)
                ex_seen[(s, lay)] += 1
                examples.append({"split": s, "layout": lay, "header": header_example(t)})
    R["2_submission_date"] = {"regex": SUB_RE.pattern, "layouts": {f"{k[0]} | {k[1]}": v for k, v in sorted(layout.items())},
                              "parse": {f"{k[0]} | {k[1]}": v for k, v in sorted(sub.items())},
                              "cross_checks": {f"{k[0]} | {k[1]}": v for k, v in sorted(hdr_agree.items())},
                              "failing_layouts": dict(Counter(fails)), "examples": examples}
    # ---- 3. flat file
    camps = {campaign_of(f): (s, f) for f, (s, _) in texts.items()}
    rows, shapes = defaultdict(list), Counter()
    with zipfile.ZipFile("data/flat/FLAT_RCL_POST_2010.zip") as z, z.open(z.namelist()[0]) as raw:
        member = z.namelist()[0]
        for line in io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline=""):
            f = line.rstrip("\r\n").split("\t")
            if len(f) != 29:
                shapes["lines with != 29 fields"] += 1; continue
            r = dict(zip(FIELDS, f)); c = r["CAMPNO"].strip()
            shapes[re.sub(r"\d", "9", re.sub(r"[A-Z]", "A", c))] += 1
            if re.fullmatch(r"\d{2}[VECT]\d{6}", c) and c[:6] in camps:
                rows[c[:6]].append(r)
    flat = {}
    consist = Counter()
    for c, rs in rows.items():
        for fld in ("RCDATE", "RCLTYPECD", "INFLUENCED_BY", "FMVSS", "RPNO"):
            consist[f"{fld}: campaigns with more than one distinct value across rows"] += len({r[fld] for r in rs}) > 1
        flat[c] = rs[0]
    R["3_flat_file"] = {
        "file": "data/flat/FLAT_RCL_POST_2010.zip", "member": member, "layout_doc": "data/flat/RCL.txt (TAB-delimited, 29 fields, dates YYYYMMDD; last updated May 2025)",
        "column_names": FIELDS, "campno_shapes_all_rows": dict(shapes.most_common()),
        "join_rule": "campaign id = the 6 characters after 'RCLRPT-' in the processed PDF file name (e.g. YYTNNN); flat-file rows with CAMPNO matching \\d{2}[VECT]\\d{6} whose first 6 characters equal it; one campaign has many rows (one per make/model/year), the first row by file order is used after checking the fields below are constant across rows",
        "joined": {s: f"{sum(1 for c, (ss, _) in camps.items() if ss == s and c in flat)}/{sum(1 for ss, _ in camps.values() if ss == s)}" for s in SPLITS},
        "row_consistency": dict(consist),
        "RCDATE": {"present_and_8_digits": sum(bool(re.fullmatch(r"\d{8}", r["RCDATE"])) for r in flat.values()), "of": len(flat), "meaning (RCL.txt)": "Part 573 Defect/Noncompliance Report Received Date"},
        "INFLUENCED_BY": {"exists": True, "meaning (RCL.txt)": "Recall Initiated By (MFR/OVSC/ODI)", "values": dict(Counter(r["INFLUENCED_BY"] or "(empty)" for r in flat.values()))},
        "RCLTYPECD": {"exists": True, "meaning (RCL.txt)": "Vehicle, Equipment, Child Restraint, Or Tire Part 573 Defect/Noncompliance Report", "values": dict(Counter(r["RCLTYPECD"] or "(empty)" for r in flat.values())),
                      "note": "codes the product type (V/E/C/T), NOT defect vs noncompliance"},
        "FMVSS": {"exists": True, "meaning (RCL.txt)": "Federal Motor Vehicle Safety Standard Number", "non_empty": sum(bool(r["FMVSS"].strip()) for r in flat.values()), "of": len(flat)},
        "RPNO": {"exists": True, "meaning (RCL.txt)": "Regulation Part Number", "non_empty": sum(bool(r["RPNO"].strip()) for r in flat.values()), "of": len(flat)},
        "explicit_noncompliance_indicator": "none: no flat-file column states defect vs noncompliance (FMVSS gives a standard number, which defect reports can also carry)"}
    # ---- 4. defect vs noncompliance
    listing = defaultdict(list)
    for p in LISTINGS:
        for l in open(p):
            r = json.loads(l); listing[r["campaign"]].append(r)
    T = Counter(); cross = Counter()
    for f, (s, t) in texts.items():
        c = campaign_of(f)
        hd = sorted(set(TYPE_HDR.findall(t)))
        h = hd[0].upper() if len(hd) == 1 else ("BOTH" if hd else None)
        titles = {"DEFECT" if "defect notice" in r["summary"].lower() else "NONCOMPLIANCE" for r in listing[c]
                  if "defect notice" in r["summary"].lower() or "noncompliance notice" in r["summary"].lower()}
        ti = titles.pop() if len(titles) == 1 else ("CONFLICT" if titles else None)
        fl = "NONCOMPLIANCE" if flat[c]["FMVSS"].strip() else "DEFECT"
        T[(s, "report text header", h or "absent")] += 1
        T[(s, "NHTSA document title (any version)", ti or "absent")] += 1
        T[(s, "flat-file FMVSS empty=DEFECT / non-empty=NONCOMPLIANCE", fl)] += 1
        if h in ("DEFECT", "NONCOMPLIANCE"):
            if ti in ("DEFECT", "NONCOMPLIANCE"):
                cross[f"header vs title: {'agree' if h == ti else 'DISAGREE'}"] += 1
            cross[f"header {h} vs flat FMVSS proxy {fl}"] += 1
        elif ti in ("DEFECT", "NONCOMPLIANCE"):
            cross[f"no header; title {ti} vs flat FMVSS proxy {fl}"] += 1
        src = "report text header" if h in ("DEFECT", "NONCOMPLIANCE") else "NHTSA document title" if ti in ("DEFECT", "NONCOMPLIANCE") else "flat-file FMVSS proxy"
        val = h if src == "report text header" else ti if src == "NHTSA document title" else fl
        T[(s, "DECIDED BY (hierarchy)", f"{src}: {val}")] += 1
    R["4_defect_vs_noncompliance"] = {"counts": {f"{k[0]} | {k[1]} | {k[2]}": v for k, v in sorted(T.items())}, "cross_checks": dict(sorted(cross.items()))}
    # ---- 5. what events store
    E = {}
    for s in SPLITS:
        C = Counter()
        for x in silver[s].values():
            for e in x["events"]:
                C["silver events (all)"] += 1
                if e.get("contested"):
                    C["silver events contested (dropped)"] += 1; continue
                dt = (e.get("date_text") or "").strip()
                C["silver non-contested"] += 1
                C["  with raw date text"] += bool(dt)
                C["  with stored ISO span"] += bool(e.get("span"))
                C["  ISO span only (no raw date text)"] += bool(e.get("span")) and not dt
                C["  raw date text but no stored span"] += bool(dt) and not e.get("span")
                C["  undated (no date text, no span)"] += (not dt and not e.get("span"))
                C["  with evidence quote"] += bool((e.get("quote") or "").strip())
                if e["type"] == "DECISION":
                    C["  DECISION (all)"] += 1; C["  DECISION with raw date text"] += bool(dt)
                    C["  DECISION quote cites a different recall number"] += cites_other_recall(e.get("quote"), campaign_of(x["file"]))
        A = json.load(open(f"runs/ts/{s}_agent_events.json"))
        for f, v in A.items():
            C["agent filings with valid run-1 output"] += v["run1_valid"]
            C["agent filings with valid run-2 output"] += v.get("run2_valid", False)
            for e in v["events"]:
                C["agent run-1 events"] += 1; C["agent run-1 events with raw date text"] += bool(e["date_text"].strip())
                C["agent run-1 events with evidence quote"] += bool(e["quote"].strip())
                if e["accepted"]:
                    C["agent accepted events"] += 1
                    if e["type"] == "DECISION":
                        C["agent accepted DECISION"] += 1; C["agent accepted DECISION with raw date text"] += bool(e["date_text"].strip())
                        C["agent accepted DECISION quote cites a different recall number"] += cites_other_recall(e["quote"], campaign_of(f))
                if e["type"] == "DECISION":
                    C["agent run-1 DECISION (any gate outcome)"] += 1
        E[s] = dict(C)
    R["5_event_fields"] = {"silver_stores": "date_text (raw, as written; for an entry-header date the header text), span (ISO start/end; stored only for Pass A items), quote, type, flags inherited_date/date_inferred/contested",
                           "agent_stores": "date_text (raw), type, status, evidence.quote, evidence.section; no ISO date; acceptance from the frozen gate (score >= 3)",
                           "counts": E}
    # ---- 6. version
    V = Counter()
    for f, (s, _) in texts.items():
        rs = [r for r in listing[campaign_of(f)] if r["fileName"] == f]
        if not rs:
            V[(s, "processed PDF not in listing")] += 1; continue
        r = rs[0]
        V[(s, "processed = original (only version)" if r["is_original"] else "processed = later (amended) version")] += 1
        V[(s, "processed is the latest version")] += r["is_latest"]
    R["6_version"] = {"counts": {f"{k[0]} | {k[1]}": v for k, v in sorted(V.items())},
                      "original_pdfs_of_multi_version_campaigns_cached": 0,
                      "note": "knowable from the NHTSA version listing (is_original, n_versions); only the latest version was downloaded, so the original's own Submission Date is not available"}
    # ---- 7. date-text formats
    F = {}
    for s in SPLITS:
        cs, cd, ca, cad = Counter(), Counter(), Counter(), Counter()
        for x in silver[s].values():
            for e in x["events"]:
                dt = (e.get("date_text") or "").strip()
                if e.get("contested") or not dt:
                    continue
                k = date_format(dt); cs[k] += 1
                if e["type"] == "DECISION":
                    cd[k] += 1
        for v in json.load(open(f"runs/ts/{s}_agent_events.json")).values():
            for e in v["events"]:
                if e["accepted"] and e["date_text"].strip():
                    k = date_format(e["date_text"]); ca[k] += 1
                    if e["type"] == "DECISION":
                        cad[k] += 1
        F[s] = {"silver_all": dict(cs), "silver_DECISION": dict(cd), "agent_accepted_all": dict(ca), "agent_accepted_DECISION": dict(cad)}
    R["7_date_formats"] = F
    Path("reports/ts").mkdir(parents=True, exist_ok=True)
    json.dump(R, open("reports/ts/TS_INVENTORY.json", "w"), indent=1, default=str)
    print(json.dumps(R, indent=1, default=str))


if __name__ == "__main__":
    main()
