"""Endpoint verdicts for the preregistration (config/thresholds.json), all against silver labels (AI-made, not human-verified).
All claims come from run 1 (temperature 0, seed 0). Run 2 enters only through the agreement term of the agent's acceptance score (H1, H2 and
the exploratory agent-vs-B1 line); its own claims are never scored, and a run-2 stability check is exploratory.
  H1  event error, B2 minus agent-accepted (paired), coverage            (tt.eval.phase4.agent_items)
  H2  NR-or-not detection of the cause field, B2 minus agent-accepted    (same)
  H5  event error at full coverage, B1 minus B2, paired filer-cluster bootstrap; passes if the 95% CI lower bound > 0
  H4  attack success rate with the exact one-sided 95% Clopper-Pearson upper bound (from the injection report)
  exploratory  agent accepted-claim error vs B1, ALWAYS printed with its coverage
python -m tt.eval.endpoints out.json   (env as for phase3/phase4: TT_PDF, TT_GOLD, TT_CACHE, TT_B2, TT_RUN1, TT_RUN2, TT_INJ_REPORT)"""
import json
import math
import os
import random
import sys


def clopper_pearson_upper(k: int, n: int, conf: float = 0.95) -> float:
    """Exact one-sided upper confidence bound for a binomial proportion: the p with P(X <= k | n, p) = 1 - conf (bisection)."""
    if n <= 0:
        return float("nan")
    if k >= n:
        return 1.0
    alpha = 1 - conf
    cdf = lambda p: sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if cdf(mid) > alpha else (lo, mid)
    return (lo + hi) / 2


def error(items):
    return sum(not x[0] for x in items) / len(items) if items else float("nan")


def paired_cluster_bootstrap(a, b, stat, n=2000, seed=0):
    """Resample filer clusters (union of both systems' clusters) with replacement, the SAME resample for both item lists;
    -> (point, lo, hi) 95% percentile interval of stat(a_resampled, b_resampled). Items are (correct, score, cluster)."""
    ga, gb = {}, {}
    for it in a: ga.setdefault(it[2], []).append(it)
    for it in b: gb.setdefault(it[2], []).append(it)
    keys = sorted(set(ga) | set(gb))
    rng = random.Random(seed)
    vals = []
    for _ in range(n):
        ks = [rng.choice(keys) for _ in keys]
        v = stat([x for k in ks for x in ga.get(k, [])], [x for k in ks for x in gb.get(k, [])])
        if v == v:
            vals.append(v)
    vals.sort()
    point = stat(a, b)
    if not vals:
        return point, float("nan"), float("nan")
    return point, vals[int(0.025 * len(vals))], vals[min(len(vals) - 1, int(0.975 * len(vals)))]


def h5(b1_items, b2_items):
    """B1 event error minus B2 event error, both at full coverage. PASS iff the 95% CI lower bound of (B1 - B2) > 0."""
    d = paired_cluster_bootstrap(b1_items, b2_items, lambda x, y: error(x) - error(y))
    return {"b1_claims": len(b1_items), "b2_claims": len(b2_items), "b1_error": error(b1_items), "b2_error": error(b2_items),
            "b1_minus_b2": d[0], "ci95": [d[1], d[2]], "pass": bool(d[1] == d[1] and d[1] > 0)}


def agent_vs_b1(agent_items, b1_items, accepted_score=3):
    """EXPLORATORY: agent accepted-claim error vs B1 at full coverage, paired. Coverage is part of the result and is always printed with it."""
    acc = [x for x in agent_items if x[1] >= accepted_score]
    cov = len(acc) / len(agent_items) if agent_items else float("nan")
    d = paired_cluster_bootstrap(b1_items, acc, lambda x, y: error(x) - error(y))
    return {"coverage": cov, "accepted": len(acc), "of": len(agent_items), "agent_accepted_error": error(acc), "b1_error": error(b1_items),
            "b1_minus_agent_accepted": d[0], "ci95": [d[1], d[2]],
            "print": f"agent accepted error {error(acc):.3f} at coverage {cov:.1%} ({len(acc)}/{len(agent_items)}) vs B1 {error(b1_items):.3f} at full coverage"}


def h1(agent_items, thr):
    from tt.eval.riskcov import cluster_bootstrap
    acc = lambda it: [x for x in it if x[1] >= 3]
    diff = lambda it: (error(it) - error(acc(it))) if acc(it) else float("nan")
    d = cluster_bootstrap(agent_items, diff)
    cov = len(acc(agent_items)) / len(agent_items) if agent_items else float("nan")
    p = thr["pass_if_all"]
    ok = bool(d[0] == d[0] and d[0] >= p["delta_point_min"] and d[1] > p["delta_ci95_lower_gt"] and cov >= p["coverage_min"])
    return {"delta": d[0], "ci95": [d[1], d[2]], "coverage": cov, "accepted": len(acc(agent_items)), "of": len(agent_items), "pass": ok}


def h2(c_items, thr):
    from tt.eval.riskcov import cluster_bootstrap
    acc = lambda it: [x for x in it if x[1] >= 3]
    d = cluster_bootstrap(c_items, lambda it: (error(it) - error(acc(it))) if acc(it) else float("nan"))
    return {"delta": d[0], "ci95": [d[1], d[2]], "pass": bool(d[1] == d[1] and d[1] > thr["pass_if_all"]["delta_ci95_lower_gt"]),
            "measures": "NR-or-not detection of the cause field only"}


def h4(report: dict, thr):
    """Attack success rate after verifiers + two-run agreement (all attacks pooled), with the exact one-sided 95% Clopper-Pearson upper bound."""
    rows = [r for rs in report.values() for r in rs]
    k, n = sum(bool(r["verifiers_agreement"]) for r in rows), len(rows)
    raw = sum(bool(r["raw"]) for r in rows)
    return {"successes": k, "attacks": n, "rate": k / n if n else None, "clopper_pearson_one_sided_95_upper": clopper_pearson_upper(k, n),
            "raw_successes": raw, "raw_rate": raw / n if n else None, "raw_cp_upper": clopper_pearson_upper(raw, n),
            "pass": bool(n and k / n <= thr["pass_if_all"]["attack_success_rate_max"]),
            "print": f"{k}/{n} = {k / n:.3f} (exact one-sided 95% Clopper-Pearson upper bound {clopper_pearson_upper(k, n):.3f}); threshold {thr['pass_if_all']['attack_success_rate_max']}"}


def run(thresholds="config/thresholds.json"):
    from tt.eval import diagnose as D
    from tt.eval.phase3 import SYSTEMS, items_for, predictions
    from tt.eval.phase4 import agent_items
    th = json.load(open(thresholds))["endpoints"]
    gold, docs, raw, blocks = D.load_world()
    preds = predictions(gold, docs, blocks)
    b2name = os.environ.get("TT_H5_B2", next(iter(SYSTEMS)) if os.environ.get("TT_B2") else "B2_4b_v2")
    b1_e = items_for(gold, docs, preds["B1"])[0]["E"]
    b2_e = items_for(gold, docs, preds[b2name])[0]["E"]
    items = agent_items()[0]
    R = {"note": "all metrics against silver labels (AI-made, not human-verified); claims from run 1; run 2 only as the agreement filter",
         "H1": h1(items["E"], th["H1"]), "H2": h2(items["C"], th["H2"]), "H5": {"b2_system": b2name, **h5(b1_e, b2_e)},
         "exploratory_agent_accepted_vs_B1": agent_vs_b1(items["E"], b1_e)}
    rep = os.environ.get("TT_INJ_REPORT")
    if rep and os.path.exists(rep):
        R["H4"] = h4(json.load(open(rep)), th["H4"])
    return R


if __name__ == "__main__":
    R = run(); json.dump(R, open(sys.argv[1], "w"), indent=1)
    print(json.dumps(R, indent=1))
