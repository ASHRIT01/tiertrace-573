"""SC-1 Step 0 inventory: parsing, strata and field checks only. NO agent or silver claim is compared with the reference here.
Reference = filer-declared supplier/component (non-AI, not ground truth). Only names, supplier type and country are kept from the block;
address and telephone lines are never stored or printed.
  python scripts/sc_inventory.py  -> reports/sc/SC_INVENTORY.json and reports/SC_INVENTORY.md"""
import hashlib
import io
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).parent))
from sc_lib import BLOCK_HEAD, FIELD, POINTER, component_records, locate_quote, norm_name, supplier_blocks  # noqa: E402
from tt.agent.run_dev import build_user  # noqa: E402
from tt.data.flat import FIELDS  # noqa: E402
from tt.parse.pdf import extract_text  # noqa: E402
from tt.parse.sections import clean, parse_header  # noqa: E402

SPLITS = {"testA": "data/testA_raw", "testB": "data/testB_raw", "unseen": "data/unseen_raw"}
NAME = {"testA": "Test-A", "testB": "Test-B", "unseen": "unseen-filer"}
FLAT = "data/flat/FLAT_RCL_POST_2010.zip"
STRATA = ["NAMED_SUPPLIER", "OEM_SELF", "OBTAINED_FROM", "MULTIPLE", "BLANK", "PARSE_FAIL"]
DIST = re.compile(r"(?i)distribut|obtained from|supplied by|importer|reseller")


def layout(t):
    return "portal" if "Defect / Noncompliance Description" in t else "older"


def load_flat(camps):
    rows = defaultdict(list)
    with zipfile.ZipFile(FLAT) as z, z.open(z.namelist()[0]) as raw:
        for line in io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline=""):
            f = line.rstrip("\r\n").split("\t")
            if len(f) == 29 and re.fullmatch(r"\d{2}[VECT]\d{6}", f[1].strip()) and f[1][:6] in camps:
                rows[f[1][:6]].append(dict(zip(FIELDS, f)))
    return rows


def stratum(recs, filer_names, literal_oem=False):
    """Precedence: PARSE_FAIL > BLANK > MULTIPLE > OEM_SELF > OBTAINED_FROM > NAMED_SUPPLIER.
    OEM_SELF (primary) = the single declared name normalises to a filer name (flat MFGNAME or the PDF header Manufacturer Name).
    literal_oem=True adds the instruction's literal rule 'Supplier Type OEM' (kept as a sensitivity; see the inventory, section 2)."""
    if not recs or not any(r["has_name_label"] for r in recs):
        return "PARSE_FAIL"
    named = [r for r in recs if r["name"] and not POINTER.search(r["name"])]
    if not named:
        return "BLANK"
    if len({norm_name(r["name"]) for r in named}) >= 2:
        return "MULTIPLE"
    r = named[0]
    fn = {norm_name(x) for x in filer_names if x}
    if norm_name(r["name"]) in fn or (literal_oem and (r["type"] or "").upper() == "OEM"):
        return "OEM_SELF"
    if (r["type"] or "").lower() == "distributor" or DIST.search(r["name"]):
        return "OBTAINED_FROM"
    return "NAMED_SUPPLIER"


def safe_block(text, b):
    """Example rendering: label lines only (Tier/Supplier Type/Name/Country); Address and any other line redacted."""
    out = []
    for ln in text[b["start"]:b["end"]].split("\n"):
        m = FIELD.match(ln)
        if BLOCK_HEAD.match(ln) or re.match(r"(?i)^\s*supplier identification", ln):
            out.append(ln.strip())
        elif m and m[1].lower() == "address":
            out.append("Address: [redacted]")
        elif m:
            out.append(ln.strip())
        elif ln.strip():
            prev = out[-1] if out else ""
            keep = re.match(r"(?i)^(name|country|tier of supplier|supplier type)\s*:$", prev) and not re.search(r"\d{4,}|\(\d{3}\)|@|\bphone\b", ln, re.I)
            out.append(ln.strip()[:80] if keep else "[line redacted]")
    s = " / ".join(out)
    return re.sub(r"\[line redacted\]( / \[line redacted\])+", "[lines redacted]", s)


def load_all():
    F = []
    camps = {}
    for s in SPLITS:
        for x in json.load(open(f"config/{s}_selection.json"))["filings"]:
            camps[re.match(r"RCLRPT-(\w{6})-", x["file"])[1]] = (s, x)
    flat = load_flat(camps)
    for c, (s, x) in camps.items():
        t, _ = extract_text(f"{SPLITS[s]}/{x['file']}")
        cl = clean(t)
        B = supplier_blocks(cl)
        recs = [r for b in B for r in b["records"]]
        mfg = {r["MFGNAME"] for r in flat[c]}
        filer_names = mfg | {parse_header(t)["filer"]}
        found, comps, cspans = component_records(cl)
        F.append({"split": s, "file": x["file"], "campaign": c, "layout": layout(t), "text": cl, "blocks": B, "recs": recs,
                  "filer_names": filer_names, "stratum": stratum(recs, filer_names), "stratum_literal_oem": stratum(recs, filer_names, True),
                  "comp_found": found, "comps": comps, "comp_spans": cspans, "flat": flat[c], "rcltypecd": flat[c][0]["RCLTYPECD"] if flat[c] else None,
                  "cluster": re.sub(r"\s+", " ", x["filer"].lower()).strip()})
    return F


def main():
    F = load_all()
    R = {"note": "reference = filer-declared supplier/component (non-AI, not ground truth); inventory only, no claim compared with the reference"}
    # 1. block parse
    P = Counter(); ex = defaultdict(list)
    for f in F:
        ok = bool(f["blocks"]) and any(r["has_name_label"] for r in f["recs"])
        P[(f["split"], f["layout"], "filings")] += 1
        P[(f["split"], f["layout"], "parsed")] += ok
        P[(f["split"], f["layout"], "blocks found")] += len(f["blocks"])
        if ok and any(r["name"] for r in f["recs"]) and len(ex[f["layout"]]) < 5 and f["split"] not in {e["split"] for e in ex[f["layout"]][:2]} | set():
            ex[f["layout"]].append({"split": f["split"], "block": safe_block(f["text"], f["blocks"][0])})
    for lay in ("portal", "older"):                                              # top up to 5 examples per layout, in file order
        for f in F:
            if len(ex[lay]) >= 5:
                break
            if f["layout"] == lay and any(r["name"] for r in f["recs"]) and safe_block(f["text"], f["blocks"][0]) not in [e["block"] for e in ex[lay]]:
                ex[lay].append({"split": f["split"], "block": safe_block(f["text"], f["blocks"][0])})
    R["1_block_parse"] = {"counts": {"|".join(k): v for k, v in sorted(P.items())}, "examples": ex,
                          "failures": [{"split": f["split"], "layout": f["layout"], "reason": "no block heading" if not f["blocks"] else "no Name label"}
                                       for f in F if not (f["blocks"] and any(r["has_name_label"] for r in f["recs"]))]}
    # 2. strata
    S = Counter((f["split"], f["layout"], f["stratum"]) for f in F)
    SL = Counter((f["split"], f["stratum_literal_oem"]) for f in F)
    typ = Counter((r["type"] or "(blank)", "name = filer" if norm_name(r["name"]) in {norm_name(x) for x in f["filer_names"] if x} else "name ≠ filer")
                  for f in F for r in f["recs"] if r["name"])
    R["2_strata"] = {"primary": {"|".join(k): v for k, v in sorted(S.items())}, "literal_type_oem_rule": {"|".join(k): v for k, v in sorted(SL.items())},
                     "supplier_type_vs_filer_name": {"|".join(k): v for k, v in sorted(typ.items())},
                     "pointer_names_counted_as_blank": sum(1 for f in F for r in f["recs"] if r["name"] and POINTER.search(r["name"])),
                     "declared_names_per_filing": dict(Counter((f["split"], len({norm_name(r["name"]) for r in f["recs"] if r["name"] and not POINTER.search(r["name"])})) for f in F).most_common()) and
                     {f"{k[0]}|{k[1]}": v for k, v in sorted(Counter((f["split"], len({norm_name(r["name"]) for r in f["recs"] if r["name"] and not POINTER.search(r["name"])})) for f in F).items())}}
    # 3. components
    C = Counter()
    for f in F:
        k = (f["split"], f["layout"])
        C[k + ("filings",)] += 1
        st = "PARSE_FAIL" if not f["comp_found"] else ("PRESENT" if any(r["name"] or r["ptno"] for r in f["comps"]) else "BLANK")
        C[k + (st,)] += 1
        C[k + ("with component name",)] += any(r["name"] for r in f["comps"])
        C[k + ("with part number",)] += any(r["ptno"] for r in f["comps"])
        C[k + ("component records",)] += len(f["comps"])
    R["3_components"] = {"|".join(k): v for k, v in sorted(C.items())}
    # 4. flat file
    sha = hashlib.sha256(open(FLAT, "rb").read()).hexdigest()
    with zipfile.ZipFile(FLAT) as z:
        info = z.infolist()[0]
    fl = {}
    for s in SPLITS:
        G = [f for f in F if f["split"] == s]
        d = {"campaigns": len(G), "joined": sum(bool(f["flat"]) for f in G)}
        for fld in ("MFR_COMP_NAME", "MFR_COMP_DESC", "MFR_COMP_PTNO"):
            vals = [{r[fld].strip() for r in f["flat"] if r[fld].strip()} for f in G]
            d[fld] = {"campaigns_with_value": sum(bool(v) for v in vals), "distinct_values_median": median(len(v) for v in vals) if vals else None,
                      "distinct_values_max": max(len(v) for v in vals) if vals else None}
        fl[s] = d
    R["4_flat_file"] = {"file": FLAT, "member": info.filename, "member_date": "%04d-%02d-%02d" % info.date_time[:3], "sha256": sha, "column_names": FIELDS,
                        "mfr_comp_fields_present": all(x in FIELDS for x in ("MFR_COMP_NAME", "MFR_COMP_DESC", "MFR_COMP_PTNO")),
                        "download": "not needed: MFR_COMP_NAME, MFR_COMP_DESC and MFR_COMP_PTNO are present (fields 25-27); nothing downloaded",
                        "join_rule": "campaign id = 6 characters after 'RCLRPT-' in the PDF file name; flat rows whose CAMPNO (\\d{2}[VECT]\\d{6}) starts with it; all rows kept, distinct values per field",
                        "per_split": fl}
    # 5. claims: storage and locatability (no comparison with the reference)
    CL = {}
    for s in SPLITS:
        A = json.load(open(f"runs/sc/{s}_agent_suppliers.json"))
        silver = {x["file"]: x for x in json.load(open(f"data/labels/{s}_silver.json"))}
        c = Counter()
        for f in [f for f in F if f["split"] == s]:
            for a in A[f["file"]]["suppliers"]:
                c["agent supplier claims (all)"] += 1; c["agent supplier claims (gate-accepted)"] += a["accepted"]
                c["agent quote located in parsed text"] += locate_quote(a["quote"], f["text"]) is not None
                c["agent quote contains [MASKED]"] += "[MASKED]" in a["quote"]
            for cl in silver[f["file"]]["claims"]:
                if cl["id"] in ("S1", "S2") and cl["status"] == "SUPPORTED":
                    c[f"silver {cl['id']} SUPPORTED"] += 1
                    c[f"silver {cl['id']} quote located in parsed text"] += locate_quote(cl["quote"], f["text"]) is not None
        CL[s] = dict(c)
    R["5_claims"] = {"agent_stores": "companies[]: name, role (SUPPLIER/SUB_SUPPLIER/DISTRIBUTOR count as supplier claims), status, evidence.section (cause/chronology/components/defect), evidence.quote; NO character offset; gate decision from the frozen agent.decide (scripts/sc_gate.py)",
                     "silver_stores": "claims S1 (block reports a component manufacturer; section 'block') and S2 (the narrative names that supplier; section cause/chronology): id, label (contains the name after ': '), status, quote, section; NO character offset; no gate",
                     "no_component_claims": "neither the frozen agent schema (tt/agent/schemas.py) nor the silver labels contain component claims",
                     "counts": CL}
    # 6. does the agent's input contain the supplier block?
    I = Counter()
    for f in F:
        u = build_user(Path(SPLITS[f["split"]]) / f["file"])
        k = (f["split"], f["layout"])
        I[k + ("filings",)] += 1
        I[k + ("input contains a block heading or block field line",)] += bool(re.search(r"(?im)^\s*(component manufacturer|supplier identification|supplier type\s*:|tier of supplier\s*:)", u))
        I[k + ("input contains [MASKED]",)] += "[MASKED]" in u
        names = [r["name"] for r in f["recs"] if r["name"] and not POINTER.search(r["name"])]
        I[k + ("a declared name appears verbatim (case-insensitive) in the input",)] += any(n.lower() in u.lower() for n in names)
    R["6_agent_input"] = {"how": "the frozen tt.agent.run_dev.build_user rebuilt for every filing (no model call): 'CAUSE:' + cause + 'CHRONOLOGY:' + chronology, block name masked",
                          "counts": {"|".join(k): v for k, v in sorted(I.items())}}
    Path("reports/sc").mkdir(parents=True, exist_ok=True)
    json.dump(R, open("reports/sc/SC_INVENTORY.json", "w"), indent=1, default=str)
    print(json.dumps({k: v for k, v in R.items() if k not in ("1_block_parse",)}, indent=1, default=str)[:6000])
    for lay, es in ex.items():
        for e in es:
            print(lay, e)


if __name__ == "__main__":
    main()
