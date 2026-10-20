"""EXPLORATORY Test-A analyses from the existing outputs (scoring only, no model run). Uses the frozen agent.decide, the frozen risk-coverage code and the same
paired filer-cluster bootstrap as H1 (tt.eval.riskcov.cluster_bootstrap, 2000 resamples, seed 0), through the amendment-1 wrapper (primary settings).
  python scripts/phase6_testA_exploratory.py   -> reports/phase_6_testA_exploratory.{json,md}, reports/phase_6_testA_riskcoverage_events.svg"""
import json
import os
import sys

os.environ.setdefault("TT_PDF", "data/testA_raw"); os.environ.setdefault("TT_GOLD", "data/labels/testA_silver.json")
os.environ.setdefault("TT_CACHE", "runs/testA_cache.pkl"); os.environ.setdefault("TT_RUN1", "runs/testA_4b_v2_run1.jsonl")
os.environ.setdefault("TT_RUN2", "runs/testA_4b_v2_run2.jsonl")
from collections import Counter

import tt.eval.amend1 as AM
AM.install()
from tt.agent import agent as A
from tt.agent.schemas import Extraction
from tt.baselines.rules import b1
from tt.eval import diagnose as D
from tt.eval.phase3 import summarise
from tt.eval.riskcov import aurc, cluster_bootstrap, curve, risk_at
from tt.parse.block import mask_text

err = lambda it: sum(not x[0] for x in it) / len(it) if it else float("nan")


def build():
    """items per claim type with score = (frozen score, no verifier reason, run-2 agrees); same construction as tt.eval.phase4.agent_items."""
    gold, docs, raw, blocks = D.load_world()
    P1, P2 = D.load_preds(os.environ["TT_RUN1"]), D.load_preds(os.environ["TT_RUN2"])
    ex1 = {f: Extraction.model_validate(p["extraction"]) for f, p in P1.items()}
    ex2 = {f: Extraction.model_validate(p["extraction"]) if p.get("extraction") else None for f, p in P2.items()}
    dec = {}
    for l in gold:
        f = l["file"]; d = docs[f]
        c, ch = (mask_text(d.sections.get(k, ""), blocks[f]) for k in ("cause", "chronology"))
        dec[f] = A.decide(ex1[f], ex2[f], Extraction.model_validate(b1(c, ch, d.filer)), d, blocks[f])
    key = {(f, x["kind"], id(x["ref"]) if x["ref"] is not None else None): x for f, xs in dec.items() for x in xs}
    sf = lambda kind, ex, claim, f: (lambda x: (x["score"], not x["reasons"], bool(x["agree2"])))(key[(f, kind, id(claim) if claim is not None else None)])
    items, unl = AM.items_for(gold, docs, ex1, sf)
    return items, unl


def delta(items, keep):
    sub = lambda it: [x for x in it if keep(x[1])]
    return cluster_bootstrap(items, lambda it: (err(it) - err(sub(it))) if sub(it) else float("nan"))


def fmt(c):
    return f"{c[0]:.3f} [{c[1]:.3f}, {c[2]:.3f}]"


def main():
    items, unl = build()
    R = {"note": "EXPLORATORY; silver labels (AI-made, not human-verified); run-1 claims, run 2 as agreement filter; primary amendment-1 settings; no model run", "unlabelled_company_claims_excluded": unl}
    # (a) decomposition of the H1 gain (events)
    E = items["E"]
    rules = {"verifiers only (no verifier reason fired)": lambda s: s[1], "run-2 agreement only (ignoring verifiers)": lambda s: s[2],
             "both (= the accepted set of H1)": lambda s: s[1] and s[2]}
    dec = {}
    for name, keep in rules.items():
        acc = [x for x in E if keep(x[1])]
        dec[name] = {"accepted": len(acc), "of": len(E), "coverage": len(acc) / len(E), "accepted_error": err(acc), "unfiltered_error": err(E),
                     "delta_unfiltered_minus_accepted": list(delta(E, keep))}
    R["a_decomposition_events"] = dec
    both = dec["both (= the accepted set of H1)"]
    ep = json.load(open("reports/phase_6_testA_endpoints.json"))["H1"]
    assert abs(both["delta_unfiltered_minus_accepted"][0] - ep["delta"]) < 1e-12 and both["delta_unfiltered_minus_accepted"][1:] == ep["ci95"], "does not reproduce the committed H1"
    # (b) risk-coverage with the frozen ordering
    Es = [(x[0], x[1][0], x[2]) for x in E]
    cv = curve(Es)
    R["b_risk_coverage_events"] = {"ordering": "frozen tt.eval.phase4 score: 0 if any verifier fired, else 1 + 2*[run 2 agrees] + [B1 agrees]; higher score accepted first; ties included fractionally (expected value under random tie-breaking); no model confidence",
                                   "score_counts": dict(sorted(Counter(s for _, s, _ in Es).items())), "N": len(Es), "overall_error_no_ranking": err(Es),
                                   "AURC": list(cluster_bootstrap(Es, aurc)), "risk@90": list(cluster_bootstrap(Es, lambda it: risk_at(it, .9))),
                                   "risk@70": list(cluster_bootstrap(Es, lambda it: risk_at(it, .7))), "risk@50": list(cluster_bootstrap(Es, lambda it: risk_at(it, .5))),
                                   "curve_at_coverage": {f"{c:.2f}": cv[max(0, round(c * len(cv)) - 1)] for c in (0.05, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0)}}
    svg(cv, R["b_risk_coverage_events"]["overall_error_no_ranking"], "reports/phase_6_testA_riskcoverage_events.svg")
    # (c) accepted vs unfiltered, cause and supplier claims
    R["c_cause_and_supplier"] = {}
    for t, label in (("C", "cause (NR-or-not detection)"), ("S2", "supplier claims")):
        its = items[t]; acc = [x for x in its if x[1][0] >= 3]
        R["c_cause_and_supplier"][t] = {"label": label, "candidates": len(its), "accepted": len(acc), "coverage": len(acc) / len(its) if its else None,
                                        "unfiltered_errors": sum(not x[0] for x in its), "accepted_errors": sum(not x[0] for x in acc),
                                        "unfiltered_error": cluster_bootstrap(its, err) if its else None, "accepted_error": cluster_bootstrap(acc, err) if acc else None,
                                        "delta_unfiltered_minus_accepted": list(delta(its, lambda s: s[0] >= 3)) if acc else None}
    json.dump(R, open("reports/phase_6_testA_exploratory.json", "w"), indent=1, default=str)
    write_md(R)


def svg(cv, flat, path):
    W, H, m = 480, 320, 44
    x = lambda i: m + (W - 2 * m) * (i + 1) / len(cv)
    y = lambda r: H - m - (H - 2 * m) * r / 0.6
    pts = " ".join(f"{x(i):.1f},{y(r):.1f}" for i, r in enumerate(cv))
    ticks = "".join(f'<text x="{m - 6}" y="{y(v) + 4:.0f}" text-anchor="end" font-size="10">{v:.1f}</text><line x1="{m}" x2="{W - m}" y1="{y(v):.0f}" y2="{y(v):.0f}" stroke="#ddd"/>' for v in (0, .2, .4, .6))
    xt = "".join(f'<text x="{m + (W - 2 * m) * c:.0f}" y="{H - m + 14}" text-anchor="middle" font-size="10">{c:.1f}</text>' for c in (0, .2, .4, .6, .8, 1))
    open(path, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="sans-serif"><rect width="{W}" height="{H}" fill="white"/>{ticks}{xt}'
                          f'<line x1="{m}" x2="{W - m}" y1="{y(flat):.1f}" y2="{y(flat):.1f}" stroke="#888" stroke-dasharray="4 3"/>'
                          f'<polyline points="{pts}" fill="none" stroke="#1f77b4" stroke-width="1.6"/>'
                          f'<text x="{W / 2}" y="{H - 8}" text-anchor="middle" font-size="11">coverage (fraction of event claims accepted, highest frozen score first)</text>'
                          f'<text x="12" y="{H / 2}" font-size="11" transform="rotate(-90 12 {H / 2})" text-anchor="middle">error among accepted</text>'
                          f'<text x="{W - m}" y="{y(flat) - 5:.0f}" text-anchor="end" font-size="10" fill="#555">no ranking (B2 error {flat:.3f})</text>'
                          f'<title>Test-A events, risk-coverage with the frozen phase-4 ordering (silver labels, exploratory)</title></svg>')


def write_md(R):
    a, b, c = R["a_decomposition_events"], R["b_risk_coverage_events"], R["c_cause_and_supplier"]
    L = ["# Phase 6 Test-A: EXPLORATORY analyses (not preregistered endpoints; silver labels, AI-made, not human-verified)", "",
         "From the existing Test-A outputs, scoring only, no model run. Primary amendment-1 settings; run-1 claims; run 2 only as the agreement filter (4 run-2 timeouts missing). "
         "Same paired filer-cluster bootstrap as H1 (2000 resamples, seed 0). The 'both' row reproduces the committed H1 exactly (checked by the script).", "",
         "## (a) Decomposition of the H1 gain (events; unfiltered error " + f"{next(iter(a.values()))['unfiltered_error']:.3f}, {next(iter(a.values()))['of']} claims)", "",
         "| accepted set | accepted | coverage | accepted error | delta = unfiltered - accepted [95% CI] |", "|---|---|---|---|---|"]
    for k, v in a.items():
        L.append(f"| {k} | {v['accepted']} | {v['coverage']:.3f} | {v['accepted_error']:.3f} | {fmt(v['delta_unfiltered_minus_accepted'])} |")
    L += ["", "The deltas are not additive: the two filters overlap, and the table says how much each does alone on this data, not a causal split.", "",
          "## (b) Risk-coverage curve and AURC, events", "", f"Ordering (the frozen one, nothing new): {b['ordering']}.", "",
          f"Score counts (0..4): {b['score_counts']}; N = {b['N']}; error with no ranking = {b['overall_error_no_ranking']:.3f}.", "",
          f"* AURC {fmt(b['AURC'])}", f"* risk@90% {fmt(b['risk@90'])}; risk@70% {fmt(b['risk@70'])}; risk@50% {fmt(b['risk@50'])}", "",
          "| coverage | " + " | ".join(b["curve_at_coverage"]) + " |", "|---|" + "---|" * len(b["curve_at_coverage"]),
          "| error among accepted | " + " | ".join(f"{v:.3f}" for v in b["curve_at_coverage"].values()) + " |", "",
          "Plot: `reports/phase_6_testA_riskcoverage_events.svg` (dashed line = no ranking). Because the score has only five values, ties are large and the curve is a few linear stretches.", "",
          "## (c) Accepted vs unfiltered error, cause and supplier claims", "",
          "| claim type | candidates | accepted (coverage) | unfiltered error [CI] | accepted error [CI] | delta [CI] |", "|---|---|---|---|---|---|"]
    for t, v in c.items():
        L.append(f"| {v['label']} | {v['candidates']} | {v['accepted']} ({v['coverage']:.3f}) | {fmt(v['unfiltered_error'])} ({v['unfiltered_errors']} errors) | "
                 f"{fmt(v['accepted_error']) if v['accepted_error'] else 'n/a'} ({v['accepted_errors']} errors) | {fmt(v['delta_unfiltered_minus_accepted']) if v['delta_unfiltered_minus_accepted'] else 'n/a'} |")
    L += ["", f"Supplier claims are few (the interval is wide); {R['unlabelled_company_claims_excluded']} company claims were excluded as unlabelled (named in the text, no silver claim). "
          "Cause = detecting NR-or-not only, never cause correctness."]
    open("reports/phase_6_testA_exploratory.md", "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
