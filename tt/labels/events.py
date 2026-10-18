"""Sentence-level event labels from a Part 573 chronology (DRAFT rules, PREREGISTRATION.md).

Rules implemented here:
 E1 one event per dated sentence; a sentence with two distinct dates yields one event per date (the first date takes the sentence's type,
    later dates are OTHER unless overridden).
 E2 date inheritance only inside a DATED ENTRY or a BULLET: an entry starts at a sentence that begins with a date (no preposition before it)
    or at a bullet item, and runs until the next entry/bullet or a blank line. An undated sentence inside an entry inherits the entry's date.
    An undated sentence in prose is stored with date_inferred=True (no date; excluded from scoring).
 E3 dates are normalised with tt.labels.dates.parse_span (prefix stripping, granularity, year-less dates resolved only if unambiguous).
 Not events: status / no-incident statements, remedy logistics, pointer chronologies, and sentences excluded by an override (with a reason).
 Dates that only bound a data range (production/build windows, 'ranging from') are mentions, not event dates.
Overrides (config/event_overrides.json): {file: {sentence-prefix (or '=' + whole sentence): {include, why, type, dates, ignore_dates, quote}}}."""
import json
import re
from datetime import date
from pathlib import Path

from tt.labeldraft import sentence_end
from tt.labels.dates import parse_span

MONC = (r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|"
        r"Dec(?:ember)?|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEPT?|OCT|NOV|DEC)\.?")
_D = rf"(?:{MONC}\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s*\d{{4}}|\d{{1,2}}/\d{{1,2}}/\d{{2,4}}|\d{{4}}-\d{{2}}-\d{{2}}|\d{{1,2}}\s+{MONC},?\s+\d{{4}})"
_MO = rf"(?:{MONC},?[\s-]+\d{{4}}|{MONC}-\d{{2}}(?!\d))"
DATE_FIND = re.compile(
    rf"(?<![\w/])(?:"
    rf"{MONC}\s+\d{{1,2}}\s*(?:-|–|and|to|through)\s*\d{{1,2}},?\s*\d{{4}}"                       # March 30 and 31, 2020
    rf"|(?:{_D}|{_MO}|{MONC})\s*(?:-|–|—|through|thru|to|until)\s*(?:{_D}|{_MO})"                   # ranges
    rf"|(?:early|mid|late|end of|beginning of)[\s-]*(?:{_MO}|\d{{4}})"                               # fuzzy
    rf"|{_D}|{_MO}|Q[1-4]\s*\d{{4}}"
    rf"|{MONC}\s+\d{{1,2}}(?:st|nd|rd|th)?(?!\d)(?!\s*,?\s*\d{{4}})"                                 # year-less day
    rf"|(?<![\d.])\d{{1,2}}/\d{{1,2}}(?![\d/])"
    rf"|(?<=\b[Ii]n\s)\d{{4}}(?![\d-])"                                                              # 'in 2015'
    rf")(?![\w/])")
STATUS = re.compile(r"\bnot aware\b|\bno known\b|\bno identified\b|\bno (?:reports|crashes|reported)\b|^\s*as of\b|\bas of (?:today|this date)\b|\bto date\b|\bknows of no\b|\bno change\b|\bis aware of\b", re.I)
REMEDY = re.compile(r"mailed|stericycle|letters? |dealer notification|owner notification|customer\(end user\)|docusign", re.I)
MENTION_CUE = re.compile(r"(?:production|produced|built|manufactured|model year|ranging from|between|start of production through|data from|through)\s*$", re.I)
POINTER = re.compile(r"see (?:the )?(?:attach|file|separate|uploaded)|attached (?:document|chronology|573|part 573)|separate document|uploaded to|is too long|see attachment|please find", re.I)


def typ(s: str) -> str:
    t = s.lower()
    if re.search(r"inform\w* nhtsa that|submit\w* .*(573|report).*nhtsa|nhtsa portal|573 report submitted|submitted to the national highway|files? (?:a )?(?:573|part 573)", t):
        return "NHTSA_FILING"
    if re.search(r"\bdecid\w+|\bdeclare\w*|determin\w+,? (?:through [^,]+, )?(?:that )?(?:a |an )?(?:safety|defect|noncompliance|non-compliance|potential non|to conduct)|"
                 r"approved a field action|a recall was needed|determined to (?:do|conduct|issue) a (?:new )?recall|constitutes a defect|decision was made|presence of a defect was determined|recall should be initiated", t):
        return "DECISION"
    if re.search(r"(?:supplier|vendor)\b.{0,60}\b(?:inform\w*|notif\w*|report\w*|provid\w*|advis\w*|confirm\w*)|notice from|letter from|report was sent from|"
                 r"supplier informed|information from (?:the |a |its )?supplier|informed of a .{0,30}recall|recall notice from|received (?:a |an )?(?:recall )?(?:notice|notification|letter) from (?!its)", t):
        return "SUPPLIER_NOTICE"
    if re.search(r"\b(?:open\w*|initiat\w*|began|begin|begun|commenc\w+|launch\w*|start\w*)\b.{0,70}(?:investigat|analys|root cause|testing)|"
                 r"investigations? (?:was|were|is) (?:initiated|begun|opened|launched|commenced)|product investigation", t):
        return "INVESTIGATION_START"
    if re.search(r"\breceiv\w+ (?:a |an |the |\d+ )?(?:\w+ ){0,2}?(?:report|notification|complaint|claim|field report|warranty)|first claim|notified of|was notified|is notified|"
                 r"discovered|detected|noted a discrepancy|was informed|became aware|was made aware|brought to|experienced a|reviewed a concern|"
                 r"concern .{0,40}(?:review group|ccrg)", t):
        return "FILER_AWARENESS"
    return "OTHER"


def _collapse_map(raw: str) -> tuple[str, list[int]]:
    """Collapsed text (whitespace runs -> one space, stripped) and, for each collapsed index, the raw index."""
    out, idx, prev_space = [], [], True
    for i, ch in enumerate(raw):
        if ch.isspace():
            if not prev_space:
                out.append(" "); idx.append(i)
            prev_space = True
        else:
            out.append(ch); idx.append(i); prev_space = False
    while out and out[-1] == " ":
        out.pop(); idx.pop()
    return "".join(out), idx


def sentences(raw: str) -> list[dict]:
    c, idx = _collapse_map(raw)
    res, pos, prev_end_raw = [], 0, 0
    while pos < len(c):
        e = max(sentence_end(c, pos + 1), pos + 1)
        seg = c[pos:e]
        lead = len(seg) - len(seg.lstrip())
        s0 = pos + lead
        s = seg.strip()
        bullet = bool(re.match(r"^[•·*]\s|^[-–]\s", s)) or s in ("•", "-", "–")
        s = re.sub(r"^[•·*\-–\s]+", "", s)
        if s and re.search(r"[A-Za-z0-9]", s):
            r0 = idx[s0] if s0 < len(idx) else len(raw)
            between = raw[prev_end_raw:r0]
            res.append({"text": s, "c_start": s0, "bullet": bullet or bool(re.search(r"[•·]\s*$", between)),
                        "para_break": bool(re.search(r"\n[ \t]*\n", between)), "line_start": bool(re.search(r"\n[ \t•·*\-–]*$", between)) or not res})
            prev_end_raw = idx[e - 1] + 1 if e - 1 < len(idx) else len(raw)
        pos = e
    return res


def find_dates(s: str) -> list[tuple[str, int]]:
    out = []
    for m in DATE_FIND.finditer(s):
        if MENTION_CUE.search(s[:m.start()][-45:]):
            continue
        out.append((m.group(0).strip(" ,"), m.start()))
    return out


def _cut(q: str, must: str | None) -> str:
    if len(q) <= 300:
        return q
    k = max(q.rfind(", ", 0, 300), q.rfind("; ", 0, 300), q.rfind(" and ", 0, 300), q.rfind(" but ", 0, 300))
    cut = q[:k if k > 150 else 300].rstrip(" ,;")
    if must and must not in cut:
        i = q.find(must)
        cut = q[max(0, i - 60):i + 240].strip()
    return cut


def _override(ov: dict, s: str) -> dict:
    for k, v in ov.items():
        if (k.startswith("=") and s == k[1:]) or (not k.startswith("=") and s.startswith(k)):
            return v
    return {}


def build(raw_chron: str, filing: date | None, overrides: dict | None = None) -> tuple[list[dict], list[tuple[str, str]]]:
    """-> (events, excluded[(sentence, reason)])"""
    overrides = overrides or {}
    sents = sentences(raw_chron)
    flat = " ".join(x["text"] for x in sents)
    if not sents or (POINTER.search(flat) and len(flat) < 260):
        return [], [(x["text"], "pointer chronology") for x in sents]
    # years of fully dated expressions (context for year-less dates)
    years = set()
    for x in sents:
        for d, _ in find_dates(x["text"]):
            sp = parse_span(d)
            if sp and not sp.inferred and not sp.year_from_context:
                years.update({sp.start.year, sp.end.year} if sp.granularity != "range" else {sp.end.year})
    events, excluded = [], []
    cur = None           # (date_text, entry sentence, in_entry)
    for x in sents:
        s = x["text"]
        o = _override(overrides, s)
        if x["para_break"] or x["bullet"]:
            if cur:
                cur = (cur[0], cur[1], False)
        dates = [] if o.get("ignore_dates") else find_dates(s)
        if o.get("dates"):
            dates = [(d["date_text"], s.find(d["date_text"])) for d in o["dates"]]
        entry_head = bool(dates) and (x["bullet"] or dates[0][1] == 0)
        if dates:
            cur = (dates[0][0], s, entry_head or (x["bullet"]))
        elif x["bullet"]:
            cur = None
        if o.get("include") is False:
            excluded.append((s, o.get("why", "override"))); continue
        if not o.get("include") and (STATUS.search(s) or REMEDY.search(s)):
            excluded.append((s, "status/no-incident statement" if STATUS.search(s) else "remedy logistics")); continue
        t0 = o.get("type") or typ(s)
        quote_base = o.get("quote") or s
        if dates:
            seen = []
            for k, (dt, _) in enumerate(dates):
                sp = parse_span(dt, years=years, filing=filing)
                key = (sp.start, sp.end) if sp else dt
                if key in seen:
                    continue
                seen.append(key)
                tt = (o["dates"][k].get("type") if o.get("dates") else None) or (t0 if k == 0 else "OTHER")
                events.append({"date_text": dt, "type": tt, "quote": _cut(quote_base, dt), "inherited_date": False,
                               "date_inferred": bool(sp is None or sp.inferred), "span": sp.asdict() if sp else None})
        elif cur and cur[2]:
            sp = parse_span(cur[0], years=years, filing=filing)
            events.append({"date_text": cur[0], "type": t0, "quote": _cut(quote_base, None), "inherited_date": True,
                           "entry_quote": _cut(cur[1], cur[0]), "date_inferred": bool(sp is None or sp.inferred), "span": sp.asdict() if sp else None})
        else:
            events.append({"date_text": "", "type": t0, "quote": _cut(quote_base, None), "inherited_date": False, "date_inferred": True,
                           "date_inferred_from": cur[0] if cur else None, "span": None})
    return events, excluded


def load_overrides(path: str | Path = "config/event_overrides.json") -> dict:
    p = Path(path)
    return json.loads(p.read_text()) if p.exists() else {}
