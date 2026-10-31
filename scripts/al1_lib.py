"""AL-1 amendment lineage: deterministic matcher, baselines and label draw (protocol al1-protocol-1). Pure Python; no model call, no file access.
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

_MONTHS = ("jan feb mar apr may jun jul aug sep sept oct nov dec january february march april june july august september october november december").split()
_STOP = set(("a an and are as at be been by for from had has have in into is it its of on or that the their this to was were which with "
             "st nd rd th").split())
_DROP = _STOP | set(_MONTHS)
_MON = r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\.?"
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
    pairs, used_i, used_j, far_i, far_j = _align(early, late, theta, n_days)
    out = []
    for i, j in pairs:
        a, b = early[i], late[j]
        same_date, same_type = _same_interval(a, b), a["type"] == b["type"]
        cls = DATE_CORRECTION if not same_date else TYPE_CHANGE if not same_type else UNCHANGED
        out.append({"cls": cls, "early": a, "late": b, "text_carried": False, "type_also_changed": not same_date and not same_type})
    et, lt = _squash(early_text), _squash(late_text)
    for i, a in enumerate(early):
        if i not in used_i:
            carried = i not in far_i and bool(_squash(a["quote"])) and _squash(a["quote"]) in lt
            out.append({"cls": UNCHANGED if carried else RETRACTED, "early": a, "late": None, "text_carried": carried, "type_also_changed": False})
    for j, b in enumerate(late):
        if j not in used_j:
            carried = j not in far_j and bool(_squash(b["quote"])) and _squash(b["quote"]) in et
            out.append({"cls": UNCHANGED if carried else NEW, "early": None, "late": b, "text_carried": carried, "type_also_changed": False})
    return out


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
