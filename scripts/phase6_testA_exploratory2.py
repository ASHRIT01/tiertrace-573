"""EXPLORATORY analyses (d)-(g) on the existing Test-A outputs: scoring only, no model run, nothing frozen changed (frozen agent.decide, amendment-1 wrapper, primary settings).
  python scripts/phase6_testA_exploratory2.py  -> reports/phase_6_exploratory_2.json (+ the table fragments used by reports/phase_6_exploratory_2.md)
Pure Python (the project venv has no numpy/scipy)."""
import json
import math
import zlib
import os
import random
import sys
from collections import Counter, defaultdict

os.environ.setdefault("TT_PDF", "data/testA_raw"); os.environ.setdefault("TT_GOLD", "data/labels/testA_silver.json")
os.environ.setdefault("TT_CACHE", "runs/testA_cache.pkl"); os.environ.setdefault("TT_RUN1", "runs/testA_4b_v2_run1.jsonl")
os.environ.setdefault("TT_RUN2", "runs/testA_4b_v2_run2.jsonl")
import tt.eval.amend1 as AM
AM.install()
from tt.agent import agent as A
from tt.agent.schemas import Extraction
from tt.baselines.rules import b1
from tt.eval import diagnose as D
from tt.labels.agree import wilson
from tt.parse.block import mask_text
from tt.verify.extra import date_errors

NBOOT, SEED = 2000, 0
PLAYERS = ["V1", "E1", "V3_unparseable", "V3_before_1990", "V3_after_filing_date", "V3o_event_order", "V8_injection", "run2_agreement"]
NP = len(PLAYERS); NM = 1 << NP; RUN2_BIT = 1 << (NP - 1); VER_MASK = RUN2_BIT - 1
V3MAP = (("V3 unparseable", "V3_unparseable"), ("V3 date before", "V3_before_1990"), ("V3 event after", "V3_after_filing_date"))
CODEBIT = {"V1": "V1", "E1": "E1", "V3o": "V3o_event_order", "V8": "V8_injection"}


# ---- data ---------------------------------------------------------------------------------------------------------------
def build():
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

    def sf(kind, ex, claim, f):
        x = key[(f, kind, id(claim) if claim is not None else None)]
        if kind != "E":
            return (x["score"], not x["reasons"], bool(x["agree2"]), frozenset(x["reasons"]))
        codes = set()
        errs = date_errors(type("X", (), {"events": [claim]})(), docs[f])
        assert ("V3" in x["reasons"]) == bool(errs)
        for pre, name in V3MAP:
            if any(e.startswith(pre) for e in errs):
                codes.add(name)
        assert not errs or codes, errs
        codes |= {CODEBIT[r] for r in x["reasons"] if r in CODEBIT}
        assert set(x["reasons"]) <= set(CODEBIT) | {"V3"}, x["reasons"]
        return (x["score"], not x["reasons"], bool(x["agree2"]), frozenset(codes))
    items, unl = AM.items_for(gold, docs, ex1, sf)
    return gold, docs, ex1, ex2, items


def code_mask(codes):
    return sum(1 << PLAYERS.index(c) for c in codes)


# ---- (d) leave-one-out and exact Shapley --------------------------------------------------------------------------------
def accepted_in(coalition, fired_mask, agrees):
    return (fired_mask & coalition & VER_MASK) == 0 and (not coalition & RUN2_BIT or agrees)


def shapley_weights():
    f = math.factorial
    return [f(s) * f(NP - s - 1) / f(NP) for s in range(NP)]


def d_attribution(E):
    clusters = defaultdict(list)
    for ok, sc, cl in E:
        clusters[cl].append((ok, code_mask(sc[3]), sc[2]))
    keys = sorted(clusters)
    W = 16
    pack_a, pack_w, n_g, w_g = {}, {}, {}, {}
    for k in keys:
        pa = pw = 0
        for ok, fm, ag in clusters[k]:
            row = sum(1 << (W * m) for m in range(NM) if accepted_in(m, fm, ag))
            pa += row
            if not ok:
                pw += row
        pack_a[k], pack_w[k] = pa, pw
        n_g[k] = len(clusters[k]); w_g[k] = sum(1 for ok, _, _ in clusters[k] if not ok)
    sw = shapley_weights()

    def stats(sample_keys):
        N = sum(n_g[k] for k in sample_keys); Wr = sum(w_g[k] for k in sample_keys)
        PA = sum(pack_a[k] for k in sample_keys); PW = sum(pack_w[k] for k in sample_keys)
        v = []
        for m in range(NM):
            na = (PA >> (W * m)) & 0xFFFF; wa = (PW >> (W * m)) & 0xFFFF
            v.append(Wr / N - wa / na if na else float("nan"))
        full = v[NM - 1]
        loo = [full - v[(NM - 1) & ~(1 << i)] for i in range(NP)]
        sh = []
        for i in range(NP):
            s = 0.0
            for m in range(NM):
                if not m & (1 << i):
                    s += sw[bin(m).count("1")] * (v[m | (1 << i)] - v[m])
            sh.append(s)
        return full, loo, sh, v
    point = stats(keys)
    assert abs(point[3][0]) < 1e-15                        # no rule active = nothing filtered = delta 0
    assert abs(sum(point[2]) - point[0]) < 1e-12           # Shapley values sum to the full delta
    rng = random.Random(SEED)
    draws = {"full": [], "loo": [[] for _ in range(NP)], "shap": [[] for _ in range(NP)]}
    for _ in range(NBOOT):
        ks = [rng.choice(keys) for _ in keys]              # the same resampling scheme as tt.eval.riskcov.cluster_bootstrap (seed 0)
        full, loo, sh, _ = stats(ks)
        if full == full:
            draws["full"].append(full)
        for i in range(NP):
            if loo[i] == loo[i]: draws["loo"][i].append(loo[i])
            if sh[i] == sh[i]: draws["shap"][i].append(sh[i])
    ci = lambda xs: (sorted(xs)[int(0.025 * len(xs))], sorted(xs)[min(len(xs) - 1, int(0.975 * len(xs)))]) if xs else (float("nan"),) * 2
    fires = Counter()
    for ok, sc, cl in E:
        for c in sc[3]: fires[c] += 1
    out = {"full_delta": point[0], "full_delta_ci": ci(draws["full"]), "claims": len(E), "fires_on_claims": {p: fires.get(p, 0) for p in PLAYERS[:-1]},
           "run2_disagrees_on_claims": sum(1 for _, sc, _ in E if not sc[2]),
           "players": {p: {"loo": point[1][i], "loo_ci": ci(draws["loo"][i]), "shapley": point[2][i], "shapley_ci": ci(draws["shap"][i])} for i, p in enumerate(PLAYERS)},
           "v_single": {p: point[3][1 << i] for i, p in enumerate(PLAYERS)}, "shapley_sum": sum(point[2])}
    return out


# ---- (e) tipping point for silver-label noise ---------------------------------------------------------------------------------
def e_tipping(E):
    by = defaultdict(lambda: [0, 0, 0, 0, 0])               # n, wrong, accepted, accepted wrong, accepted correct
    for ok, sc, cl in E:
        b = by[cl]; b[0] += 1; b[1] += (not ok)
        if sc[0] >= 3:
            b[2] += 1; b[3] += (not ok); b[4] += ok
    keys = sorted(by); rng = random.Random(SEED)
    res = []
    for _ in range(NBOOT):
        ks = [rng.choice(keys) for _ in keys]
        res.append(tuple(sum(by[k][j] for k in ks) for j in range(5)))
    tot = tuple(sum(by[k][j] for k in keys) for j in range(5))
    N, Wr, NA, WA, CA = tot

    def delta(t, f):
        n, w, na, wa, ca = t
        return (w + f * ca) / n - (wa + f * ca) / na if na else float("nan")

    def lower(f):
        v = sorted(x for x in (delta(t, f) for t in res) if x == x)
        return v[int(0.025 * len(v))]
    d0 = delta(tot, 0.0)
    f_point = d0 / (CA * (1 / NA - 1 / N))
    lo0 = lower(0.0)
    f_ci = None
    if lower(1.0) <= 0:
        a, b = 0.0, 1.0
        for _ in range(60):
            mid = (a + b) / 2
            a, b = (mid, b) if lower(mid) > 0 else (a, mid)
        f_ci = (a + b) / 2
    row = lambda f: None if f is None else {"fraction_of_accepted_correct_claims_wrong": f, "claims_flipped": f * CA, "share_of_all_event_labels": f * CA / N,
                                           "share_of_accepted_labels": f * CA / NA, "accepted_error_after": (WA + f * CA) / NA, "unfiltered_error_after": (Wr + f * CA) / N,
                                           "delta_after": delta(tot, f), "ci_lower_after": lower(f)}
    return {"claims": N, "accepted": NA, "accepted_correct": CA, "delta": d0, "ci_lower": lo0, "point_estimate_tipping": row(f_point), "ci_lower_bound_tipping": row(f_ci),
            "ci_lower_bound_reaches_0_only_if_all_accepted_correct_wrong": f_ci is None}


# ---- (f) cluster-sum t-bound and its validity check ----------------------------------------------------------------------------
def _betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-300 else 1e-300); h = d
    for m in range(1, 400):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-300 else 1e-300); c = 1 + aa / c; c = c if abs(c) > 1e-300 else 1e-300; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-300 else 1e-300); c = 1 + aa / c; c = c if abs(c) > 1e-300 else 1e-300
        de = d * c; h *= de
        if abs(de - 1) < 3e-16:
            break
    return h


def _ibeta(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    return bt * _betacf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1 - bt * _betacf(b, a, 1 - x) / b


def t_cdf(t, df):
    p = 0.5 * _ibeta(df / 2, 0.5, df / (df + t * t))
    return 1 - p if t > 0 else p


def t_quantile(q, df):
    lo, hi = 0.0, 200.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if t_cdf(mid, df) < q else (lo, mid)
    return (lo + hi) / 2


def ucb(sizes, errors, delta=0.01):
    """Cluster-sum t-bound: ratio estimate r = sum e / sum n; linearised residuals d_g = e_g - r n_g; SE = sqrt(G/(G-1) sum d_g^2) / sum n; UCB = r + t_{1-delta,G-1} SE."""
    G = len(sizes); n = sum(sizes); r = sum(errors) / n
    if G < 2:
        return 1.0
    se = math.sqrt(G / (G - 1) * sum((e - r * s) ** 2 for s, e in zip(sizes, errors))) / n
    return min(1.0, r + t_quantile(1 - delta, G - 1) * se)


def capped(items, kind_filter, cap=10, seed=0):
    by = defaultdict(list)
    for ok, sc, cl in items:
        if kind_filter(sc): by[cl].append(not ok)
    out = {}
    for cl in sorted(by):
        errs = by[cl]
        if len(errs) > cap:
            errs = random.Random(f"{seed}:{cl}").sample(errs, cap)
        out[cl] = errs
    return out


def icc(sizes_errors):
    """One-way ANOVA estimator of the intra-cluster correlation of the 0/1 error indicator (clusters with >= 2 claims), clipped to [0, 0.99]."""
    cl = [e for e in sizes_errors if len(e) >= 2]
    N = sum(len(e) for e in cl); k = len(cl); p = sum(sum(e) for e in cl) / N
    ssb = sum(len(e) * (sum(e) / len(e) - p) ** 2 for e in cl); ssw = sum(sum((x - sum(e) / len(e)) ** 2 for x in e) for e in cl)
    msb, msw = ssb / (k - 1), ssw / (N - k); n0 = (N - sum(len(e) ** 2 for e in cl) / N) / (k - 1)
    r = (msb - msw) / (msb + (n0 - 1) * msw) if (msb + (n0 - 1) * msw) > 0 else 0.0
    return max(0.0, min(0.99, r))


def simulate(sizes, p, rho, nsim, seed):
    rng = random.Random(seed); G = len(sizes); bad = 0
    if rho > 0:
        s = 1 / rho - 1; a, b = p * s, (1 - p) * s
    for _ in range(nsim):
        if rho > 0:
            errs = [rng.binomialvariate(n, rng.betavariate(a, b)) for n in sizes]
        else:
            errs = [rng.binomialvariate(n, p) for n in sizes]
        if ucb(sizes, errs) < p:
            bad += 1
    return bad


def f_bound(items, nsim=20000):
    out = {}
    for name, flt, kind in (("events", lambda sc: sc[0] >= 3, "E"), ("cause", lambda sc: sc[0] >= 3, "C")):
        cl = capped(items[kind], flt)
        sizes = [len(e) for e in cl.values()]; errs = [sum(e) for e in cl.values()]
        u = ucb(sizes, errs); rhat = sum(errs) / sum(sizes)
        rho_hat = icc(list(cl.values()))
        row = {"accepted_claims_in_bound": sum(sizes), "clusters": len(sizes), "errors": sum(errs), "point_error": rhat, "ucb_99_one_sided": u, "icc_estimate": rho_hat,
               "accepted_total_before_cap": sum(1 for x in items[kind] if flt(x[1])), "cluster_sizes_after_cap": dict(sorted(Counter(sizes).items())), "validity": []}
        for tname, target in (("target = the observed bound", u), ("target = the observed point estimate", rhat)):
            for sname, rho in (("independent claims (rho = 0)", 0.0), (f"rho = estimated {rho_hat:.3f}", rho_hat), ("stress rho = 0.1", 0.1), ("stress rho = 0.3", 0.3), ("stress rho = 0.5", 0.5)):
                if target <= 0 or target >= 1:
                    continue
                bad = simulate(sizes, target, rho, nsim, seed=zlib.crc32(f'{name}|{tname}|{sname}'.encode()))
                lo, hi = wilson(bad, nsim)
                row["validity"].append({"target": tname, "target_value": target, "scenario": sname, "rho": rho, "sims": nsim, "false_certifications": bad, "rate": bad / nsim,
                                        "rate_ci95": [lo, hi], "valid_rate_le_0.01": bad / nsim <= 0.01})
        out[name] = row
    return out


# ---- (g) empty event lists --------------------------------------------------------------------------------------------------
def g_empty(gold, docs, ex1, ex2):
    host = lambda l: l["cause"]["status"] == "SUPPORTED" and len(docs[l["file"]].sections.get("chronology", "")) > 300 and len(l["events"]) >= 2
    scored = lambda l: sum(1 for e in l["events"] if e.get("span") and not e.get("date_inferred"))
    rows = {}
    for nm, ex in (("run1", ex1), ("run2", ex2)):
        valid = {f: x for f, x in ex.items() if x is not None}
        emp = [f for f, x in valid.items() if not x.events]
        g = {l["file"]: l for l in gold}
        rows[nm] = {"filings_with_valid_output": len(valid), "empty_event_lists": len(emp), "share": len(emp) / len(valid),
                    "empty_with_gold_scored_events": sum(1 for f in emp if scored(g[f]) > 0), "empty_with_any_gold_event": sum(1 for f in emp if g[f]["events"]),
                    "files": sorted(f.replace("RCLRPT-", "").rsplit(".", 1)[0] for f in emp)}
        h = [f for f in valid if host(g[f])]
        he = [f for f in h if not valid[f].events]
        rows[nm]["attack_host_like_filings(criteria of tt.agent.inject.fixtures)"] = {"n": len(h), "empty": len(he), "share": len(he) / len(h) if h else None}
    rows["filings_with_scored_gold_events"] = sum(1 for l in gold if scored(l) > 0)
    rows["total_gold_filings"] = len(gold)
    inj = {}
    for t in ("runA", "runB"):
        L = [json.loads(x) for x in open(f"runs/testA_inject_{t}.jsonl")]
        inj[t] = {"outputs": len(L), "empty_event_lists_by_attack": dict(Counter(x["id"].split(":")[0] for x in L if x["extraction"] is not None and not x["extraction"]["events"]))}
    rows["injection_runs_empty_event_lists"] = inj
    return rows


def main():
    gold, docs, ex1, ex2, items = build()
    E = items["E"]
    R = {"note": "EXPLORATORY; silver labels (AI-made, not human-verified); run-1 claims, run 2 only as the agreement filter; amendment-1 primary settings; no model run"}
    R["d_attribution"] = d_attribution(E)
    ep = json.load(open("reports/phase_6_testA_endpoints.json"))["H1"]
    d = R["d_attribution"]
    assert abs(d["full_delta"] - ep["delta"]) < 1e-12 and all(abs(a - b) < 1e-9 for a, b in zip(d["full_delta_ci"], ep["ci95"])), (d["full_delta"], d["full_delta_ci"], ep)
    assert abs(d["full_delta"] - 0.1352) < 5e-5
    R["e_tipping"] = e_tipping(E)
    assert abs(R["e_tipping"]["ci_lower"] - ep["ci95"][0]) < 1e-9 and abs(R["e_tipping"]["delta"] - ep["delta"]) < 1e-12
    R["f_bound"] = f_bound(items)
    R["g_empty"] = g_empty(gold, docs, ex1, ex2)
    json.dump(R, open("reports/phase_6_exploratory_2.json", "w"), indent=1, default=str)
    print("done; full delta", d["full_delta"], d["full_delta_ci"])


if __name__ == "__main__":
    main()
