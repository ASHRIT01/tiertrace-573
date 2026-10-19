"""Mechanical comparison of two label passes (Pass A vs Pass B) per claim type, with Wilson 95% intervals,
and the list of disagreement items handed to the Pass C adjudicator.

Units and agreement:
  S1, C        one unit per filing; agree if the status is equal.
  S2           one unit per filing; agree if the status is equal and, when SUPPORTED, both name the same supplier
               (squashed names equal or one contains the other).
  U            one unit per filing; agree if the kind is equal.
  E            scored events only (not date_inferred, not fuzzy). Events are paired greedily when the types are equal and the
               date spans overlap at the coarser granularity. Each pair is one agreeing unit; each unpaired event on either side is
               one disagreeing unit. E_headline restricts both sides to the five headline types."""
import math
from datetime import date

from tt.labels.dates import Span, coarse_overlap, parse_span
from tt.norm.aliases import squash

HEADLINE = {"FILER_AWARENESS", "INVESTIGATION_START", "DECISION", "SUPPLIER_NOTICE", "NHTSA_FILING"}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def _claim(rec: dict, cid: str) -> dict:
    return next((c for c in rec["claims"] if c["id"] == cid), {"status": "MISSING", "quote": ""})


def _s2_name(c: dict) -> str:
    if c.get("name"):
        return c["name"]
    lab = c.get("label", "")
    return lab.split(": ", 1)[1].split(" (")[0] if ": " in lab else ""


def _same(a: str, b: str) -> bool:
    a, b = squash(a or ""), squash(b or "")
    return bool(a and b and (a == b or a in b or b in a))


def spans(rec: dict, years: set | None, filing: date | None) -> list[tuple[Span, dict]]:
    """Scored events of a record as (span, event)."""
    out = []
    for e in rec.get("events", []):
        if e.get("date_inferred") or not e.get("date_text"):
            continue
        sp = parse_span(e["date_text"], years=years, filing=filing)
        if sp is None or sp.inferred or sp.granularity == "fuzzy":
            continue
        out.append((sp, e))
    return out


def pair_events(ea: list, eb: list):
    """Greedy pairing (same type + overlap). Returns pairs, unpaired_a, unpaired_b, type_conflicts [(a, b)] among the unpaired
    (same/overlapping date, different type)."""
    used, pairs = set(), []
    for sa, a in ea:
        for j, (sb, b) in enumerate(eb):
            if j not in used and a["type"] == b["type"] and coarse_overlap(sa, sb):
                used.add(j); pairs.append((a, b)); break
    paired_a = {id(a) for a, _ in pairs}
    ua = [(s, a) for s, a in ea if id(a) not in paired_a]
    ub = [(s, b) for j, (s, b) in enumerate(eb) if j not in used]
    conflicts, used2 = [], set()
    for sa, a in ua:
        for j, (sb, b) in enumerate(ub):
            if j not in used2 and coarse_overlap(sa, sb):
                used2.add(j); conflicts.append((a, b)); break
    ca = {id(a) for a, _ in conflicts}
    cb = {id(b) for _, b in conflicts}
    return pairs, [a for _, a in ua if id(a) not in ca], [b for _, b in ub if id(b) not in cb], conflicts


def compare(A: list[dict], B: list[dict], context: dict) -> dict:
    """context: {file: (years, filing_date)}. Returns per-type counts and disagreement items."""
    Bm = {b["file"]: b for b in B}
    cnt = {k: [0, 0] for k in ("S1", "S2", "C", "U", "E", "E_headline")}
    items = []
    for a in A:
        f = a["file"]
        b = Bm.get(f)
        if b is None:
            continue
        for cid in ("S1", "S2"):
            ca, cb = _claim(a, cid), _claim(b, cid)
            ok = ca["status"] == cb["status"] and (cid != "S2" or ca["status"] != "SUPPORTED" or _same(_s2_name(ca), _s2_name(cb)))
            cnt[cid][0] += ok; cnt[cid][1] += 1
            if not ok:
                items.append({"file": f, "claim": cid, "A": ca, "B": cb})
        for key, field in (("C", "cause"), ("U", "upstream")):
            va, vb = a[field], b.get(field, {})
            ok = va.get("status", va.get("kind")) == vb.get("status", vb.get("kind"))
            cnt[key][0] += ok; cnt[key][1] += 1
            if not ok:
                items.append({"file": f, "claim": key, "A": va, "B": vb})
        years, fd = context[f]
        ea, eb = spans(a, years, fd), spans(b, years, fd)
        for tag, flt in (("E", lambda x: True), ("E_headline", lambda x: x[1]["type"] in HEADLINE)):
            pa, ua, ub, conf = pair_events([x for x in ea if flt(x)], [x for x in eb if flt(x)])
            cnt[tag][0] += len(pa)
            cnt[tag][1] += len(pa) + len(ua) + len(ub) + 2 * len(conf)
            if tag == "E":
                items += [{"file": f, "claim": "E", "kind": "type differs", "A": x, "B": y} for x, y in conf]
                items += [{"file": f, "claim": "E", "kind": "only in A", "A": x, "B": None} for x in ua]
                items += [{"file": f, "claim": "E", "kind": "only in B", "A": None, "B": y} for y in ub]
    stats = {k: {"agree": v[0], "units": v[1], "rate": (v[0] / v[1]) if v[1] else float("nan"), "wilson95": wilson(*v)} for k, v in cnt.items()}
    return {"stats": stats, "items": items}
