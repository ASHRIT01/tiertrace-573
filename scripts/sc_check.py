"""SC-1 supplier check: compute (protocol tag sc-protocol-1, reports/SC_PROTOCOL.md). Pure Python, deterministic, no model run.
Reference = filer-declared supplier (non-AI, not a reference standard). A match measures fidelity to the declaration, not who made the part.
  python scripts/sc_check.py  -> reports/sc/phase_8_supplier_check.json (aggregates only, no per-filer rows, no names)
Runs tests/test_sc_check.py first and writes nothing if any test fails. Needs runs/sc/<split>_agent_suppliers.json (scripts/sc_gate.py)."""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sc_inventory import SPLITS, load_all, stratum  # noqa: E402
from sc_lib import POINTER, inside, locate_quote, match_contain, match_exact, match_fuzzy  # noqa: E402
from ts_lib import wilson  # noqa: E402
from tt.eval.riskcov import cluster_bootstrap  # noqa: E402

POP = ("NAMED_SUPPLIER", "MULTIPLE")
LEVELS = {"exact": match_exact, "containment": match_contain, "fuzzy_tsr90": match_fuzzy}
NOTE = "reference = filer-declared supplier (non-AI, not a reference standard); a match measures fidelity to the filer's declaration, not who made the part"


def loc(quote, f):
    sp = locate_quote(quote, f["text"])
    if sp is None:
        return "not_located"
    return "in_block" if inside(sp, [(b["start"], b["end"]) for b in f["blocks"]]) else "out_of_block"


def silver_name(c):
    """Pass A items: the text of `label` after the first ': '. Pass-C-decided items carry no label; their name is in `name` (amendment SC-A1)."""
    if c.get("name"):
        return c["name"]
    lab = c.get("label") or ""
    return lab.split(": ", 1)[1] if ": " in lab else ""


def attach_claims(F):
    agent = {s: json.load(open(f"runs/sc/{s}_agent_suppliers.json")) for s in SPLITS}
    silver = {s: {x["file"]: x for x in json.load(open(f"data/labels/{s}_silver.json"))} for s in SPLITS}
    for f in F:
        f["declared"] = [r["name"] for r in f["recs"] if r["name"] and not POINTER.search(r["name"])]
        f["agent"] = [{"name": a["name"], "accepted": a["accepted"], "loc": loc(a["quote"], f)} for a in agent[f["split"]][f["file"]]["suppliers"]]
        f["silver"] = [{"name": silver_name(c), "id": c["id"], "loc": loc(c["quote"], f)}
                       for c in silver[f["split"]][f["file"]]["claims"] if c["id"] in ("S1", "S2") and c["status"] == "SUPPORTED"]


def share(items, pred, cluster):
    k, n = sum(1 for x in items if pred(x)), len(items)
    wl, wh = wilson(k, n)
    _, bl, bh = cluster_bootstrap([(x, None, cluster(x)) for x in items], lambda it: sum(1 for y in it if pred(y[0])) / len(it) if it else float("nan"))
    return {"k": k, "n": n, "share": k / n if n else None, "wilson95": [wl, wh], "cluster_boot95": [bl, bh], "unstable": n < 20}


def metrics(P, m):
    """P = population filings. Returns recall/precision for agent (all, accepted) and silver, overall and by evidence location."""
    hit = lambda c, f: any(m(c["name"], d) for d in f["declared"])
    out = {"n_filings": len(P)}
    fc = lambda f: f["cluster"]
    for side, sel in (("agent_all", lambda c: True), ("agent_accepted", lambda c: c["accepted"])):
        cl = [(c, f) for f in P for c in f["agent"] if sel(c)]
        out[side] = {"recall": share(P, lambda f: any(hit(c, f) for c in f["agent"] if sel(c)), fc),
                     "recall_in_block": share(P, lambda f: any(hit(c, f) and c["loc"] == "in_block" for c in f["agent"] if sel(c)), fc),
                     "recall_out_of_block": share(P, lambda f: any(hit(c, f) and c["loc"] == "out_of_block" for c in f["agent"] if sel(c)), fc),
                     "precision": share(cl, lambda x: hit(*x), lambda x: x[1]["cluster"]),
                     "claims_by_location": dict(Counter(c["loc"] for c, _ in cl)),
                     "precision_by_location": {L: share([x for x in cl if x[0]["loc"] == L], lambda x: hit(*x), lambda x: x[1]["cluster"])
                                               for L in ("in_block", "out_of_block", "not_located")}}
    for side, ids in (("silver_S1_S2", ("S1", "S2")), ("silver_S1", ("S1",)), ("silver_S2", ("S2",))):
        cl = [(c, f) for f in P for c in f["silver"] if c["id"] in ids]
        out[side] = {"recall": share(P, lambda f: any(hit(c, f) for c in f["silver"] if c["id"] in ids), fc),
                     "recall_in_block": share(P, lambda f: any(hit(c, f) and c["loc"] == "in_block" for c in f["silver"] if c["id"] in ids), fc),
                     "recall_out_of_block": share(P, lambda f: any(hit(c, f) and c["loc"] == "out_of_block" for c in f["silver"] if c["id"] in ids), fc),
                     "precision": share(cl, lambda x: hit(*x), lambda x: x[1]["cluster"]),
                     "claims_by_location": dict(Counter(c["loc"] for c, _ in cl)),
                     "precision_by_location": {L: share([x for x in cl if x[0]["loc"] == L], lambda x: hit(*x), lambda x: x[1]["cluster"])
                                               for L in ("in_block", "out_of_block", "not_located")}}
    # (d) agent vs silver, per filing
    d = {}
    for a_lab, a_sel in (("agent_all", lambda c: True), ("agent_accepted", lambda c: c["accepted"])):
        for s_lab, ids in (("silver_S1_S2", ("S1", "S2")), ("silver_S2", ("S2",))):
            t = Counter()
            for f in P:
                am = any(hit(c, f) for c in f["agent"] if a_sel(c))
                sm = any(hit(c, f) for c in f["silver"] if c["id"] in ids)
                t[("agent match" if am else "agent no match") + " / " + ("silver match" if sm else "silver no match")] += 1
            d[f"{a_lab} vs {s_lab}"] = dict(t)
    out["d_agent_vs_silver"] = d
    return out


def main():
    t = subprocess.run([sys.executable, "-m", "pytest", "tests/test_sc_check.py", "-q"], capture_output=True, text=True)
    last = [l for l in t.stdout.strip().splitlines() if "passed" in l or "failed" in l]
    print(last[-1] if last else t.stdout[-500:])
    if t.returncode != 0:
        print(t.stdout); sys.exit("unit tests failed: no result written")
    F = load_all()
    attach_claims(F)
    groups = {"testA": lambda f: f["split"] == "testA", "testB": lambda f: f["split"] == "testB", "unseen": lambda f: f["split"] == "unseen",
              "layout_portal": lambda f: f["layout"] == "portal", "layout_older": lambda f: f["layout"] == "older",
              "rcltypecd_V": lambda f: f["rcltypecd"] == "V", "rcltypecd_E": lambda f: f["rcltypecd"] == "E", "pooled": lambda f: True}
    R = {"note": NOTE, "protocol": "sc-protocol-1", "tests": last[-1] if last else None, "levels": {}, "literal_oem_sensitivity": {},
         "other_strata_claim_counts": {}, "components": "not run: neither the frozen agent schema nor the silver labels contain component claims (protocol E)"}
    for lev, m in LEVELS.items():
        R["levels"][lev] = {g: metrics([f for f in F if sel(f) and f["stratum"] in POP], m) for g, sel in groups.items()}
    R["literal_oem_sensitivity"] = {g: metrics([f for f in F if sel(f) and f["stratum_literal_oem"] in POP], match_exact)
                                    for g, sel in groups.items() if g in ("testA", "testB", "unseen", "pooled")}
    for g in ("testA", "testB", "unseen", "pooled"):
        c = Counter()
        for f in F:
            if groups[g](f):
                c[(f["stratum"], "filings")] += 1
                c[(f["stratum"], "agent claims (all)")] += len(f["agent"])
                c[(f["stratum"], "agent claims (accepted)")] += sum(a["accepted"] for a in f["agent"])
                c[(f["stratum"], "silver S1+S2 claims")] += len(f["silver"])
        R["other_strata_claim_counts"][g] = {f"{k[0]}|{k[1]}": v for k, v in sorted(c.items())}
    Path("reports/sc").mkdir(parents=True, exist_ok=True)
    json.dump(R, open("reports/sc/phase_8_supplier_check.json", "w"), indent=1, default=str)
    print("written reports/sc/phase_8_supplier_check.json")


if __name__ == "__main__":
    main()
