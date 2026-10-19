"""Phase 4: agent (4B v2 run 1 + run 2 agreement + B1 agreement + verifiers) on the 100 dev filings vs SILVER labels. Dev only.
python -m tt.eval.phase4 out.json"""
import json
import sys
from collections import Counter

from tt.agent import agent as A
from tt.agent.schemas import Extraction
from tt.baselines.rules import b1
from tt.eval import diagnose as D
from tt.eval.phase3 import items_for, summarise
from tt.eval.riskcov import aurc, cluster_bootstrap, risk_at
from tt.parse.block import mask_text

RUN1, RUN2 = "runs/dev_bench_4b_silver_v2.jsonl", "runs/dev_bench_4b_silver_v2_run2.jsonl"


def run():
    gold, docs, raw, blocks = D.load_world()
    P1, P2 = D.load_preds(RUN1), D.load_preds(RUN2)
    ex1 = {f: Extraction.model_validate(p["extraction"]) for f, p in P1.items()}
    ex2 = {f: Extraction.model_validate(p["extraction"]) if p.get("extraction") else None for f, p in P2.items()}
    dec, reason_count, v8_fp = {}, Counter(), 0
    for l in gold:
        f = l["file"]; d = docs[f]
        c, ch = (mask_text(d.sections.get(k, ""), blocks[f]) for k in ("cause", "chronology"))
        base = Extraction.model_validate(b1(c, ch, d.filer))
        dec[f] = A.decide(ex1[f], ex2[f], base, d, blocks[f])
        for x in dec[f]:
            for r in x["reasons"]: reason_count[(x["kind"], r)] += 1
    key = {(f, x["kind"], id(x["ref"]) if x["ref"] is not None else None): x for f, xs in dec.items() for x in xs}

    def score_fn(kind, ex, claim, f):
        return key[(f, kind, id(claim) if claim is not None else None)]["score"]

    items, unl = items_for(gold, docs, ex1, score_fn)
    R = {"unlabelled_excluded": unl, "reason_counts": {f"{k}:{r}": v for (k, r), v in sorted(reason_count.items())}, "run2_valid": sum(v is not None for v in ex2.values())}
    err = lambda it: sum(not x[0] for x in it) / len(it) if it else float("nan")
    for t, its in items.items():
        row = {"candidates": len(its)}
        for name, thr in (("B2 (no verifiers)", 0), ("verifiers only", 1), ("verifiers + two-run agreement (accepted)", 3)):
            acc = [x for x in its if x[2] is not None and x[1] >= thr]
            row[name] = {"accepted": len(acc), "coverage": len(acc) / len(its) if its else None, "error": cluster_bootstrap(acc, err) if acc else None,
                         "right_claims": sum(x[0] for x in acc)}
        row["ranked"] = summarise(its)
        R[t] = row
    return R


if __name__ == "__main__":
    A.STRICT_E1 = len(sys.argv) > 2 and sys.argv[2] == "strict"
    R = run(); json.dump(R, open(sys.argv[1], "w"), indent=1, default=str)
    f = lambda x: "n/a" if not x else f"{x[0]:.3f} [{x[1]:.3f},{x[2]:.3f}]"
    for t in ("S2", "E", "C"):
        print(t, "candidates", R[t]["candidates"])
        for k, v in R[t].items():
            if isinstance(v, dict) and "accepted" in v: print("  ", k, "accepted", v["accepted"], "cov", None if v["coverage"] is None else round(v["coverage"], 3), "err", f(v["error"]), "right", v["right_claims"])
        s = R[t]["ranked"]; print("   ranked AURC", f(s["AURC"]), "risk@90/70/50", [round(s[f"risk@{c}%"][0], 3) for c in (90, 70, 50)])
    print(R["reason_counts"])
