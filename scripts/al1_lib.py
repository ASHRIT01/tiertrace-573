"""AL-1 amendment lineage: deterministic matchers, baselines and label draw (protocol al1-protocol-1, amendment al1-amendment-1). Pure Python; no model
call, no file access. match_global is the primary matcher (amendment 1); match_versions is the greedy nearest-match baseline, as tagged in al1-protocol-1.
An event is a dict {"quote": str, "type": str, "lo": date, "hi": date}: a gate-accepted run-1 claim whose date was resolved by ts_lib.resolve.
Pairs compare two successive versions of one filing; classes are defined in docs/AL1_CODEBOOK.md."""
import random
import re

THETA, N_DAYS = 0.6, 30
MIN_TOKENS = 3
NEW, UNCHANGED, DATE_CORRECTION, TYPE_CHANGE, RETRACTED = "NEW", "UNCHANGED", "DATE_CORRECTION", "TYPE_CHANGE", "RETRACTED"
CLASSES = (NEW, UNCHANGED, DATE_CORRECTION, TYPE_CHANGE, RETRACTED)
NO_PREDICTION = "NO_PREDICTION"
QUOTAS = {DATE_CORRECTION: 16, TYPE_CHANGE: 14, RETRACTED: 14, NEW: 14, UNCHANGED: 14}  # 72 first-instance items
N_REPEATS, DRAW_SEED = 8, 0
W_QUOTE, W_TYPE, W_DATE, UNMATCHED_COST = 0.6, 0.15, 0.25, 0.5  # amendment 1; a feasible pair costs at most 0.64, less than two unmatched events (1.0)
_FORBIDDEN, _POSITION_TIE = 1e6, 1e-9
STATED, INFERRED = "stated", "inferred"

_MONTHS = ("jan feb mar apr may jun jul aug sep sept oct nov dec january february march april june july august september october november december").split()
_STOP = set(("a an and are as at be been by for from had has have in into is it its of on or that the their this to was were which with "
             "st nd rd th").split())
_DROP = _STOP | set(_MONTHS)
_MON = r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\.?"
RECALL_RE = re.compile(r"\b(\d{2}[VECT])-?(\d{3})\b")
DATE_RE = re.compile(rf"\b{_MON}\s+\d{{1,2}},?\s+\d{{4}}\b|\b\d{{1,2}}/\d{{1,2}}/\d{{4}}\b|\b\d{{4}}-\d{{2}}-\d{{2}}\b|\b{_MON}\s+\d{{4}}\b", re.I)


def tokens(text: str) -> set[str]:
    """Lower-case alphanumeric tokens without stop words, month names or date-like numbers (1 to 4 digits), so a changed date does not lower the overlap."""
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in _DROP and not re.fullmatch(r"\d{1,4}", t)}


def overlap(a: str, b: str) -> float:
    """Overlap coefficient |A & B| / min(|A|, |B|). Below MIN_TOKENS on either side only identical token sets match."""
    x, y = tokens(a), tokens(b)
    if not x or not y:
        return 0.0
    if min(len(x), len(y)) < MIN_TOKENS:
        return 1.0 if x == y else 0.0
    return len(x & y) / min(len(x), len(y))


def date_distance(a: dict, b: dict) -> int:
    """Calendar days between two intervals; 0 if they overlap."""
    return max((a["lo"] - b["hi"]).days, (b["lo"] - a["hi"]).days, 0)


def _same_interval(a: dict, b: dict) -> bool:
    return a["lo"] == b["lo"] and a["hi"] == b["hi"]


def _squash(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def _align(early: list[dict], late: list[dict], theta: float, n_days: int):
    """Greedy one-to-one matching: highest overlap, then smallest date distance, then position. -> matched pairs and pairs too far apart in date."""
    cands, far = [], set()
    for i, a in enumerate(early):
        for j, b in enumerate(late):
            s = overlap(a["quote"], b["quote"])
            if s < theta:
                continue
            d = date_distance(a, b)
            if d <= n_days:
                cands.append((-s, d, i, j))
            else:
                far.add((i, j))
    used_i, used_j, out = set(), set(), []
    for _, _, i, j in sorted(cands):
        if i not in used_i and j not in used_j:
            used_i.add(i); used_j.add(j); out.append((i, j))
    return out, used_i, used_j, {i for i, _ in far}, {j for _, j in far}


def match_versions(early: list[dict], late: list[dict], early_text: str, late_text: str, theta: float = THETA, n_days: int = N_DAYS) -> list[dict]:
    """Classify every event of two successive versions. An unmatched event whose quote still stands verbatim in the other version's chronology text is
    UNCHANGED with text_carried=True (the extractor missed it there, nothing shows it changed), unless a same-quote claim exists there beyond the date window."""
    return _rows(early, late, early_text, late_text, *_align(early, late, theta, n_days))


def _rows(early, late, early_text, late_text, pairs, used_i, used_j, far_i, far_j, text_guard=True) -> list[dict]:
    out = []
    for i, j in pairs:
        a, b = early[i], late[j]
        same_date, same_type = _same_interval(a, b), a["type"] == b["type"]
        cls = DATE_CORRECTION if not same_date else TYPE_CHANGE if not same_type else UNCHANGED
        out.append({"cls": cls, "early": a, "late": b, "text_carried": False, "type_also_changed": not same_date and not same_type})
    et, lt = _squash(early_text), _squash(late_text)
    for i, a in enumerate(early):
        if i not in used_i:
            carried = text_guard and i not in far_i and bool(_squash(a["quote"])) and _squash(a["quote"]) in lt
            out.append({"cls": UNCHANGED if carried else RETRACTED, "early": a, "late": None, "text_carried": carried, "type_also_changed": False})
    for j, b in enumerate(late):
        if j not in used_j:
            carried = text_guard and j not in far_j and bool(_squash(b["quote"])) and _squash(b["quote"]) in et
            out.append({"cls": UNCHANGED if carried else NEW, "early": None, "late": b, "text_carried": carried, "type_also_changed": False})
    return out


# ---------------------------------------------------------------- global assignment (amendment 1) --------------------------------
def _recalls(quote: str) -> set[str]:
    return {a + b for a, b in RECALL_RE.findall(quote)}


def contradicts(a: dict, b: dict, theta: float = THETA, n_days: int = N_DAYS, recall_constraint: bool = True) -> bool:
    """Hard constraints: the pair may never match. Too little quote overlap, dates beyond the window, or both quotes cite recall numbers with none in common."""
    if overlap(a["quote"], b["quote"]) < theta or date_distance(a, b) > n_days:
        return True
    x, y = _recalls(a["quote"]), _recalls(b["quote"])
    return recall_constraint and bool(x) and bool(y) and not x & y


def pair_cost(a: dict, b: dict, n_days: int = N_DAYS, w_quote: float = W_QUOTE, w_type: float = W_TYPE, w_date: float = W_DATE) -> float:
    return w_quote * (1 - overlap(a["quote"], b["quote"])) + w_type * (a["type"] != b["type"]) + w_date * date_distance(a, b) / n_days


def hungarian(cost: list[list[float]]) -> list[int]:
    """Minimum-cost assignment on a square matrix (Hungarian algorithm with potentials, O(n^3)). -> for each row, its column."""
    n = len(cost)
    u, v, match, way = [0.0] * (n + 1), [0.0] * (n + 1), [0] * (n + 1), [0] * (n + 1)
    for i in range(1, n + 1):
        match[0], j0 = i, 0
        minv, used = [float("inf")] * (n + 1), [False] * (n + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = match[j0], float("inf"), 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j], way[j] = cur, j0
                    if minv[j] < delta:
                        delta, j1 = minv[j], j
            for j in range(n + 1):
                if used[j]:
                    u[match[j]] += delta; v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if match[j0] == 0:
                break
        while j0:
            j1 = way[j0]
            match[j0], j0 = match[j1], j1
    out = [0] * n
    for j in range(1, n + 1):
        out[match[j] - 1] = j - 1
    return out


def match_global(early: list[dict], late: list[dict], early_text: str, late_text: str, theta: float = THETA, n_days: int = N_DAYS, w_quote: float = W_QUOTE,
                 w_type: float = W_TYPE, w_date: float = W_DATE, recall_constraint: bool = True, text_guard: bool = True) -> list[dict]:
    """Primary matcher: the one-to-one assignment with the lowest total cost over all feasible event pairs, each event free to stay unmatched at UNMATCHED_COST.
    Classes and the text guard are those of match_versions. The flags and weights exist for the pre-declared ablations."""
    n, m = len(early), len(late)
    size = n + m
    far_i = {i for i, a in enumerate(early) for b in late if contradicts(a, b, theta, n_days, False) and overlap(a["quote"], b["quote"]) >= theta}
    far_j = {j for j, b in enumerate(late) for a in early if contradicts(a, b, theta, n_days, False) and overlap(a["quote"], b["quote"]) >= theta}
    # block layout: rows are early events then late events' slots; columns are late events then early events' slots
    cost = [[0.0] * size for _ in range(size)]
    for i, a in enumerate(early):
        for j, b in enumerate(late):
            cost[i][j] = _FORBIDDEN if contradicts(a, b, theta, n_days, recall_constraint) else pair_cost(a, b, n_days, w_quote, w_type, w_date) + _POSITION_TIE * abs(i - j)
        for k in range(n):
            cost[i][m + k] = UNMATCHED_COST if k == i else _FORBIDDEN
    for j in range(m):
        for k in range(m):
            cost[n + j][k] = UNMATCHED_COST if k == j else _FORBIDDEN
    pairs = [(i, c) for i, c in enumerate(hungarian(cost)[:n]) if c < m] if size else []
    return _rows(early, late, early_text, late_text, pairs, {i for i, _ in pairs}, {j for _, j in pairs}, far_i, far_j, text_guard)


# ---------------------------------------------------------------- evidence independence and date tags (amendment 1) ---------------
def tag_evidence(rows: list[dict], early_text: str, late_text: str) -> list[dict]:
    """evidence_copied = True when the later quote already stands verbatim in the earlier version (or a text-carried quote stands in both): same evidence,
    not independent support. Events reported in one version only have nothing to compare, so they are False."""
    et, lt = _squash(early_text), _squash(late_text)
    for r in rows:
        q = _squash(r["late"]["quote"]) if r["late"] else _squash(r["early"]["quote"])
        both = bool(r["early"] and r["late"]) or r["text_carried"]
        r["evidence_copied"] = both and bool(q) and (q in et if r["late"] else q in lt)
        if r["early"] and r["late"] and q and q == _squash(r["early"]["quote"]):
            r["evidence_copied"] = True
    return rows


def chain_support(version_rows: list[list[dict]]) -> list[dict]:
    """Follow events through a campaign's successive pairs (the later event of one pair is the earlier event of the next). Each chain reports the versions that
    claim it and the independent evidence after discounting verbatim copies. Each row gets evidence_weight: 1, or 1/m if it is one of m copied links in its chain."""
    chain_of, chains = {}, []
    for rows in version_rows:
        for r in rows:
            start = r["early"] or r["late"]
            c = chain_of.get(id(start))
            if c is None:
                c = {"rows": [], "versions": 1}
                chains.append(c)
            c["rows"].append(r)
            if r["early"] and r["late"]:
                c["versions"] += 1
                chain_of[id(r["late"])] = c
    out = []
    for c in chains:
        copied = [r for r in c["rows"] if r.get("evidence_copied")]
        linked = sum(1 for r in copied if r["early"] and r["late"])
        for r in c["rows"]:
            r["evidence_weight"] = 1 / len(copied) if r.get("evidence_copied") else 1.0
        out.append({"versions": c["versions"], "independent": c["versions"] - linked, "rows": c["rows"]})
    return out


def date_tag(date_text: str, interval, chronology_text: str) -> str:
    """stated: the date text stands in that version's chronology and was read without borrowing a year, choosing between readings or capping. Otherwise inferred."""
    if interval is None or interval.year_from_context or interval.ambiguous or interval.capped:
        return INFERRED
    q = _squash(date_text)
    return STATED if q and q in _squash(chronology_text) else INFERRED


def pair_date_tag(row: dict) -> str:
    """stated only if every event in the pair is tagged stated; a missing tag counts as inferred."""
    sides = [s for s in (row["early"], row["late"]) if s]
    return STATED if sides and all(s.get("date_tag") == STATED for s in sides) else INFERRED


# ---------------------------------------------------------------- baselines -------------------------------------------------------
def single_version_predict(pair: dict, version_events: list[dict], theta: float = THETA, n_days: int = N_DAYS) -> str:
    """Earliest-version-only and latest-version-only baselines (pass that version's events). One version shows no change, so the only claim it can make
    is UNCHANGED, and only for an event it contains; otherwise NO_PREDICTION, which counts as disagreement."""
    for side in (pair["early"], pair["late"]):
        if side and any(overlap(side["quote"], e["quote"]) >= theta and date_distance(side, e) <= n_days for e in version_events):
            return UNCHANGED
    return NO_PREDICTION


def segments(text: str, date_fn) -> list[dict]:
    """Chronology text -> lines and sentences, each with the first date found by DATE_RE and read by date_fn(str) -> (lo, hi) or None. No event extraction."""
    out = []
    for s in re.split(r"\n+|(?<=[.;])\s+", text):
        s = s.strip()
        if not tokens(s):
            continue
        m, iv = DATE_RE.search(s), None
        if m:
            iv = date_fn(m.group(0))
        out.append({"quote": s, "lo": iv[0] if iv else None, "hi": iv[1] if iv else None})
    return out


def _seg_distance(a: dict, b: dict):
    if a["lo"] is None or b["lo"] is None:
        return 0 if a["lo"] is None and b["lo"] is None else None  # one side has no date: comparable only on the words
    return date_distance(a, b)


def textdiff_classify(early_text: str, late_text: str, date_fn, theta: float = THETA, n_days: int = N_DAYS) -> list[dict]:
    """Text-diff + date rule baseline: the matcher's rule on text segments, with no event extraction and no types, so it can never say TYPE_CHANGE."""
    E, L = segments(early_text, date_fn), segments(late_text, date_fn)
    cands = []
    for i, a in enumerate(E):
        for j, b in enumerate(L):
            s = overlap(a["quote"], b["quote"])
            d = _seg_distance(a, b)
            if s >= theta and (d is None or d <= n_days):
                cands.append((-s, d or 0, i, j))
    used_i, used_j, out = set(), set(), []
    for _, _, i, j in sorted(cands):
        if i in used_i or j in used_j:
            continue
        used_i.add(i); used_j.add(j)
        a, b = E[i], L[j]
        same = (a["lo"], a["hi"]) == (b["lo"], b["hi"])
        out.append({"cls": UNCHANGED if same else DATE_CORRECTION, "early": a, "late": b})
    out += [{"cls": RETRACTED, "early": a, "late": None} for i, a in enumerate(E) if i not in used_i]
    out += [{"cls": NEW, "early": None, "late": b} for j, b in enumerate(L) if j not in used_j]
    return out


def textdiff_predict(pair: dict, records: list[dict], theta: float = THETA) -> str:
    """The baseline's class for a matcher pair: the record whose segment best contains the pair's quote; NO_PREDICTION if none reaches theta."""
    best, best_s = NO_PREDICTION, 0.0
    for r in records:
        s = max([overlap(pair[k]["quote"], r[k]["quote"]) for k in ("early", "late") if pair[k] and r[k]] or [0.0])
        if s >= theta and s > best_s:
            best, best_s = r["cls"], s
    return best


# ---------------------------------------------------------------- author label draw -----------------------------------------------
def draw_items(pair_ids_by_class: dict[str, list[str]], quotas: dict = QUOTAS, n_repeats: int = N_REPEATS, seed: int = DRAW_SEED) -> dict:
    """Stratified draw by predicted class. A class short of its quota gives the shortfall to the class with the most undrawn pairs (ties: CLASSES order).
    Returns the realised sizes, inclusion probabilities, drawn ids, repeats, and the shuffled sheet order (repeats hidden among first instances)."""
    pop = {c: sorted(pair_ids_by_class.get(c, [])) for c in CLASSES}
    n = {c: min(quotas[c], len(pop[c])) for c in CLASSES}
    short = sum(quotas.values()) - sum(n.values())
    while short > 0:
        room = {c: len(pop[c]) - n[c] for c in CLASSES}
        c = max(CLASSES, key=lambda k: (room[k], -CLASSES.index(k)))
        if room[c] == 0:
            break
        n[c] += 1; short -= 1
    rng = random.Random(seed)
    drawn = {c: rng.sample(pop[c], n[c]) for c in CLASSES}
    first = [(c, p) for c in CLASSES for p in drawn[c]]
    repeats = [first[i] for i in rng.sample(range(len(first)), min(n_repeats, len(first)))]
    sheet = [{"pair": p, "stratum": c, "repeat": False} for c, p in first] + [{"pair": p, "stratum": c, "repeat": True} for c, p in repeats]
    rng.shuffle(sheet)
    return {"n": n, "population": {c: len(pop[c]) for c in CLASSES}, "inclusion": {c: n[c] / len(pop[c]) if pop[c] else None for c in CLASSES},
            "drawn": drawn, "repeats": [p for _, p in repeats], "sheet": sheet}


def weighted_agreement(rows: list[dict], inclusion: dict) -> float:
    """Horvitz-Thompson agreement over all pairs: rows are {"stratum", "agree"}, each weighted by 1 / inclusion probability of its stratum."""
    w = [1 / inclusion[r["stratum"]] for r in rows]
    return sum(x for x, r in zip(w, rows) if r["agree"]) / sum(w)


# ---------------------------------------------------------------- ablations (amendment 1) ------------------------------------------
def predict_for_item(item: dict, variant_rows: list[dict]) -> str:
    """A variant's class for a labelled item: the class of the variant row holding the item's earlier event (the same dict object), else its later event."""
    for side in ("early", "late"):
        if item[side] is not None:
            for r in variant_rows:
                if r[side] is item[side]:
                    return r["cls"]
    return NO_PREDICTION


def _weighted_mean(rows, inclusion, agree_key, weight_key):
    w = [r.get(weight_key, 1.0) / inclusion[r["stratum"]] for r in rows]
    return sum(x for x, r in zip(w, rows) if r[agree_key]) / sum(w) if sum(w) else float("nan")


def ablation_effect(rows: list[dict], inclusion: dict, n: int = 2000, seed: int = 0) -> dict:
    """Effect of a full-vs-variant comparison on the weighted primary endpoint, on the same labelled items. rows: {"stratum", "agree_full", "agree_variant"},
    optionally "weight_full" and "weight_variant" (default 1; 0 leaves an item out of that side). Stratified bootstrap 95% interval of full minus variant.
    The full version is claimed better only if the interval's lower end is above 0; otherwise the simpler variant is reported as working as well."""
    def diff(xs):
        return _weighted_mean(xs, inclusion, "agree_full", "weight_full") - _weighted_mean(xs, inclusion, "agree_variant", "weight_variant")
    by = {}
    for r in rows:
        by.setdefault(r["stratum"], []).append(r)
    rng, boots = random.Random(seed), []
    for _ in range(n):
        d = diff([rng.choice(v) for k in sorted(by) for v in [by[k]] for _ in v])
        if d == d:
            boots.append(d)
    boots.sort()
    lo, hi = boots[int(0.025 * len(boots))], boots[min(int(0.975 * len(boots)), len(boots) - 1)]
    verdict = "FULL_BETTER" if lo > 0 else "VARIANT_BETTER" if hi < 0 else "NO_SUPPORTED_DIFFERENCE"
    return {"full": _weighted_mean(rows, inclusion, "agree_full", "weight_full"), "variant": _weighted_mean(rows, inclusion, "agree_variant", "weight_variant"),
            "effect": diff(rows), "lo": lo, "hi": hi, "verdict": verdict, "n_items": len(rows)}
