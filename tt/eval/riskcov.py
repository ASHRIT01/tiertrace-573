"""Risk-coverage tools. An item = (correct: bool, score: float, cluster: str). Items accepted first are those with the highest score;
tied items are included fractionally (expected value under random tie-breaking), so a system with no ranking has risk(c) = overall risk."""
import random


def curve(items):
    """-> list risk[k-1] = expected error rate among the k highest-scored items, k = 1..N."""
    n = len(items)
    if n == 0:
        return []
    groups = {}
    for ok, sc, _ in items:
        g = groups.setdefault(sc, [0, 0]); g[0] += 1; g[1] += (not ok)
    risk, seen, errs = [], 0, 0.0
    for sc in sorted(groups, reverse=True):
        size, e = groups[sc]
        for j in range(1, size + 1):
            risk.append((errs + e * j / size) / (seen + j))
        seen += size; errs += e
    return risk


def aurc(items):
    r = curve(items)
    return sum(r) / len(r) if r else float("nan")


def risk_at(items, c):
    r = curve(items)
    if not r:
        return float("nan")
    return r[max(0, round(c * len(r)) - 1)]


def cluster_bootstrap(items, stat, n=2000, seed=0):
    """Resample clusters (filers) with replacement; -> (point, lo, hi) 95% percentile interval."""
    by = {}
    for it in items:
        by.setdefault(it[2], []).append(it)
    keys = sorted(by)
    rng = random.Random(seed)
    vals = []
    for _ in range(n):
        samp = [it for k in (rng.choice(keys) for _ in keys) for it in by[k]]
        v = stat(samp)
        if v == v:
            vals.append(v)
    vals.sort()
    if not vals:
        return stat(items), float("nan"), float("nan")
    return stat(items), vals[int(0.025 * len(vals))], vals[min(len(vals) - 1, int(0.975 * len(vals)))]
