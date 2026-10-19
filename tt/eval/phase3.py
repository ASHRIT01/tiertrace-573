"""Phase 3: baselines + B2 (single LLM pass, no verifier, no abstention) through the risk-coverage harness, on the 100 dev filings vs
SILVER labels. python -m tt.eval.phase3 out.json"""
import json
import os
import sys
from pathlib import Path

from tt.agent.schemas import Extraction
from tt.baselines.rules import b0, b1
from tt.eval import diagnose as D
from tt.eval.devscore import SUPPLIER_ROLES
from tt.eval.riskcov import aurc, cluster_bootstrap, risk_at
from tt.kind import load_groups
from tt.parse.block import mask_text

SYSTEMS = {"B2_4b_v1": "runs/dev_bench_4b_silver.jsonl", "B2_2b_v1": "runs/dev_bench_2b_silver.jsonl", "B2_4b_v2": "runs/dev_bench_4b_silver_v2.jsonl"}
if os.environ.get("TT_B2"):   # Phase 6: "name=path;name=path"
    SYSTEMS = dict(kv.split("=", 1) for kv in os.environ["TT_B2"].split(";"))
LEVELS = (0.5, 0.7, 0.9)


def predictions(gold, docs, blocks):
    from collections import Counter
    maj = Counter(l["cause"]["status"] == "SUPPORTED" for l in gold).most_common(1)[0][0]
    out = {"B0": {}, "B1": {}}
    for l in gold:
        d = docs[l["file"]]
        c, ch = (mask_text(d.sections.get(k, ""), blocks[l["file"]]) for k in ("cause", "chronology"))
        out["B0"][l["file"]] = Extraction.model_validate(b0(maj))
        out["B1"][l["file"]] = Extraction.model_validate(b1(c, ch, d.filer))
    for name, path in SYSTEMS.items():
        P = D.load_preds(path)
        out[name] = {f: Extraction.model_validate(p["extraction"]) for f, p in P.items()}
    return out


def items_for(gold, docs, preds, score_fn=None):
    """-> {claim type: (items [(correct, score, filer)], excluded_unlabelled)}. score_fn(kind, ex, claim, file) -> float; default 0 (no ranking)."""
    groups = load_groups()
    res = {"S2": [], "E": [], "C": []}; unl = 0
    for l in gold:
        f = l["file"]; ex = preds[f]; doc = docs[f]; years = D.years_of(ex); cl = doc.filer.lower().strip()
        for c in ex.companies:
            if c.role in SUPPLIER_ROLES and c.status == "SUPPORTED":
                k = D.company_class(c, l, doc, groups)
                if k == "unlabelled": unl += 1; continue
                res["S2"].append((k == "right", score_fn("S2", ex, c, f) if score_fn else 0, cl))
        for e in ex.events:
            res["E"].append((D.event_class(e, l, doc, years) == "right", score_fn("E", ex, e, f) if score_fn else 0, cl))
        res["C"].append((ex.cause_reported == (l["cause"]["status"] == "SUPPORTED"), score_fn("C", ex, None, f) if score_fn else 0, cl))
    return res, unl


def summarise(items):
    err = lambda it: sum(not x[0] for x in it) / len(it) if it else float("nan")
    out = {"n": len(items), "error": cluster_bootstrap(items, err), "AURC": cluster_bootstrap(items, aurc)}
    for c in LEVELS:
        out[f"risk@{int(c * 100)}%"] = cluster_bootstrap(items, lambda it, c=c: risk_at(it, c))
    return out


def run():
    gold, docs, raw, blocks = D.load_world()
    preds = predictions(gold, docs, blocks)
    R = {}
    for name, ex in preds.items():
        res, unl = items_for(gold, docs, ex)
        R[name] = {"unlabelled_company_claims_excluded": unl, **{t: summarise(v) for t, v in res.items()}}
    return R


if __name__ == "__main__":
    R = run(); json.dump(R, open(sys.argv[1], "w"), indent=1)
    for name, r in R.items():
        for t in ("S2", "E", "C"):
            s = r[t]; f = lambda x: f"{x[0]:.3f} [{x[1]:.3f},{x[2]:.3f}]"
            print(name, t, "n=", s["n"], "error", f(s["error"]) if s["n"] else "n/a", "AURC", f(s["AURC"]) if s["n"] else "n/a")
