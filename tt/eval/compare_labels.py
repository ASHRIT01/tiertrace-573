"""AI-vs-AI comparison of two label sets (e.g. blind labels vs drafts). NOT human verification.
Per claim type S1, S2, E, C, U each unit is classed:
  same       every compared field is equal (quotes compared after whitespace/case normalisation, ignoring trailing punctuation;
             label wording is ignored)
  detail     the status/kind (event: type) agrees but a quote span, a names list, an event date_text or quote presence differs ('fix')
  substance  the status/kind differs, or an event type differs, or an event exists in only one set ('no')
S1/S2 compare status + quote; C compares status + quote; U compares kind + set of names + quote.
Events are paired by normalised date text ('On or about May 5, 2022' == 'May 5, 2022'), then by type and quote."""
import re
from collections import defaultdict

from tt.parse.sections import norm


def q(s: str) -> str:
    return norm(s or "").rstrip(" .,;:")


def _date_key(s: str) -> str:
    return re.sub(r"^(on or about|on|in)\s+", "", norm(s))


def _overlap(a: str, b: str) -> bool:
    a, b = q(a), q(b)
    return bool(a and b and (a in b or b in a))


def classify_simple(da: dict, db: dict, fields: tuple[str, ...]) -> tuple[str, list[str]]:
    """da/db: dicts with the key field first (status or kind)."""
    key = fields[0]
    if da[key] != db[key]:
        return "substance", [f"{key}: {da[key]} vs {db[key]}"]
    diffs = []
    for f in fields[1:]:
        if f == "quote":
            if q(da.get("quote", "")) != q(db.get("quote", "")):
                diffs.append("quote span/presence")
        elif f == "names":
            if {norm(x) for x in da.get("names", [])} != {norm(x) for x in db.get("names", [])}:
                diffs.append(f"names: {da.get('names')} vs {db.get('names')}")
    return ("detail" if diffs else "same"), diffs


def compare_event_lists(ea: list[dict], eb: list[dict]) -> list[tuple[str, dict | None, dict | None, list[str]]]:
    """-> [(verdict, event_a, event_b, reasons)] covering every event in either list."""
    ga, gb = defaultdict(list), defaultdict(list)
    for e in ea:
        ga[_date_key(e["date_text"])].append(e)
    for e in eb:
        gb[_date_key(e["date_text"])].append(e)
    out = []
    for k in list(dict.fromkeys([_date_key(e["date_text"]) for e in ea] + [_date_key(e["date_text"]) for e in eb])):
        A, B = ga[k][:], gb[k][:]
        pairs = []
        for same_type in (True, False):          # pair identical type first, then leftovers by quote overlap
            for a in A[:]:
                cand = [b for b in B if (b["type"] == a["type"]) == same_type] if same_type else [b for b in B if _overlap(a["quote"], b["quote"])]
                cand.sort(key=lambda b: (q(a["quote"]) != q(b["quote"]), not _overlap(a["quote"], b["quote"])))
                if cand:
                    pairs.append((a, cand[0])); A.remove(a); B.remove(cand[0])
        for a, b in pairs:
            if a["type"] != b["type"]:
                out.append(("substance", a, b, [f"type: {a['type']} vs {b['type']}"]))
                continue
            d = []
            if q(a["quote"]) != q(b["quote"]):
                d.append("quote span")
            if a["date_text"] != b["date_text"]:
                d.append(f"date_text: {a['date_text']!r} vs {b['date_text']!r}")
            out.append(("detail" if d else "same", a, b, d))
        for a in A:
            out.append(("substance", a, None, ["event only in set A"]))
        for b in B:
            out.append(("substance", None, b, ["event only in set B"]))
    return out


def compare(a_labels: list[dict], b_labels: list[dict]) -> dict:
    """a = reference drafts, b = blind labels. Returns rows per claim type for filings present in both."""
    A = {x["file"]: x for x in a_labels}
    rows, only_b = [], []
    for lb in b_labels:
        la = A.get(lb["file"])
        if la is None:
            only_b.append(lb["file"]); continue
        for cid in ("S1", "S2"):
            ca = next((c for c in la["claims"] if c["id"] == cid), None)
            cb = next((c for c in lb["claims"] if c["id"] == cid), None)
            v, why = classify_simple(ca, cb, ("status", "quote"))
            rows.append((cid, lb["file"], v, why, ca, cb))
        for a, b, v, why in [(x[1], x[2], x[0], x[3]) for x in compare_event_lists(la["events"], lb["events"])]:
            rows.append(("E", lb["file"], v, why, a, b))
        v, why = classify_simple(la["cause"], lb["cause"], ("status", "quote"))
        rows.append(("C", lb["file"], v, why, la["cause"], lb["cause"]))
        v, why = classify_simple(la["upstream"], lb["upstream"], ("kind", "names", "quote"))
        rows.append(("U", lb["file"], v, why, la["upstream"], lb["upstream"]))
    return {"rows": rows, "only_in_b": only_b}


def render_markdown(res: dict, a_labels: list[dict], a_name: str, b_name: str) -> str:
    import collections
    dn = {d["file"]: i + 1 for i, d in enumerate(a_labels)}
    c = collections.defaultdict(collections.Counter)
    for t, f, v, w, a, b in res["rows"]:
        c[t][v] += 1
    files = sorted({r[1] for r in res["rows"]}, key=lambda f: dn[f])
    out = ["# AI-vs-AI agreement, not human verification", "",
           f"Set A = {a_name} (reference); set B = {b_name}. Both were produced by AI. Agreement here shows consistency between two AI passes, not correctness.",
           f"Filings compared: {len(files)} ({', '.join('#%d %s' % (dn[f], f[7:19]) for f in files)}).",
           f"Filings in B with no counterpart in A (not compared): {', '.join(x[7:19] for x in res['only_in_b']) or 'none'}.", "",
           "Classes: **same** (all compared fields equal) / **detail** (agree on status, kind or event type; quote span, names list or date_text differs: 'fix') /",
           "**substance** (status, kind or event type differs, or an event exists on one side only: 'no'). Rules: tt/eval/compare_labels.py.", "",
           "| claim | units | same | differs in detail (fix) | differs in substance (no) |", "|---|---|---|---|---|"]
    for t in ("S1", "S2", "E", "C", "U"):
        n = sum(c[t].values())
        out.append(f"| {t} | {n} | {c[t]['same']} | {c[t]['detail']} | {c[t]['substance']} |")
    tot = collections.Counter()
    for t in c:
        tot.update(c[t])
    out += [f"| all | {sum(tot.values())} | {tot['same']} | {tot['detail']} | {tot['substance']} |", "", "## Every difference (A = draft, B = blind)", ""]
    for t, f, v, w, a, b in res["rows"]:
        if v == "same":
            continue
        out.append(f"### {t} on #{dn[f]} {f}: **{v}** — {'; '.join(w)}")
        for tag, x in (("A", a), ("B", b)):
            if x is None:
                out.append(f"- {tag}: (none)")
            elif t == "E":
                out.append(f"- {tag}: {x['date_text']!r} {x['type']} — \"{x['quote']}\"")
            elif t == "U":
                out.append(f"- {tag}: {x['kind']} {x.get('names') or ''} — \"{x.get('quote', '')}\"")
            else:
                out.append(f"- {tag}: {x['status']} — \"{x.get('quote', '')}\"")
        out.append("")
    return "\n".join(out)
