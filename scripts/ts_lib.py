"""TS-1 timeliness screen: library (pure Python, deterministic). Descriptive screening signal only, not a legal finding.
All event dates come from silver reference labels (AI-generated, not human-verified) or from the frozen agent's accepted run-1 claims.
Nothing here edits or replaces frozen code; frozen helpers are imported read-only.

Contents: holiday table (5 U.S.C. 6103 rules), working-day counting, date-text -> interval parser, decision anchor, flag, statistics."""
import calendar
import hashlib
import math
import re
from dataclasses import dataclass
from datetime import date, timedelta

# ---------------------------------------------------------------- holidays (5 U.S.C. 6103(a), observed rule 6103(b)) -------------
HOLIDAY_YEARS = range(1980, 2028)


def _nth_weekday(y: int, m: int, weekday: int, n: int) -> date:
    d = date(y, m, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def _last_weekday(y: int, m: int, weekday: int) -> date:
    d = date(y, m, calendar.monthrange(y, m)[1])
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def holiday_rows(years=HOLIDAY_YEARS) -> list[dict]:
    """Legal public holidays of 5 U.S.C. 6103(a) and their observed dates (Saturday -> Friday before, Sunday -> Monday after).
    Start years: Monday holidays (Washington's Birthday, Memorial Day, Columbus Day) 1971; Veterans Day on Nov 11 from 1978;
    Martin Luther King Jr. Day from 1986; Juneteenth from 2021. One-off executive-order closures and Inauguration Day (6103(c),
    DC area only) are not included."""
    out = []
    for y in years:
        hs = [("New Year's Day", date(y, 1, 1)), ("Washington's Birthday", _nth_weekday(y, 2, 0, 3)),
              ("Memorial Day", _last_weekday(y, 5, 0)), ("Independence Day", date(y, 7, 4)), ("Labor Day", _nth_weekday(y, 9, 0, 1)),
              ("Columbus Day", _nth_weekday(y, 10, 0, 2)), ("Veterans Day", date(y, 11, 11)),
              ("Thanksgiving Day", _nth_weekday(y, 11, 3, 4)), ("Christmas Day", date(y, 12, 25))]
        if y >= 1986:
            hs.append(("Birthday of Martin Luther King, Jr.", _nth_weekday(y, 1, 0, 3)))
        if y >= 2021:
            hs.append(("Juneteenth National Independence Day", date(y, 6, 19)))
        for name, d in hs:
            obs = d - timedelta(days=1) if d.weekday() == 5 else d + timedelta(days=1) if d.weekday() == 6 else d
            out.append({"observed": obs.isoformat(), "holiday": name, "actual": d.isoformat(), "shifted": obs != d})
    return sorted(out, key=lambda r: r["observed"])


def load_holidays(path="data/holidays_us_federal.csv") -> set[date]:
    import csv
    with open(path) as f:
        return {date.fromisoformat(r["observed"]) for r in csv.DictReader(f)}


# ---------------------------------------------------------------- working days ----------------------------------------------------
def wd_between(a: date, b: date, holidays: set[date], weekends: bool = True) -> int:
    """Working days d with a < d <= b (Mon-Fri, not an observed federal holiday). 0 if b <= a.
    weekends=False and holidays=set() gives calendar days."""
    if b <= a:
        return 0
    n, d = 0, a + timedelta(days=1)
    while d <= b:
        if (not weekends or d.weekday() < 5) and d not in holidays:
            n += 1
        d += timedelta(days=1)
    return n


def flag(gap_min: int, gap_max: int, limit: int = 5) -> str:
    if gap_min > limit:
        return "FLAGGED"
    if gap_max <= limit:
        return "NOT_FLAGGED"
    return "INDETERMINATE"


# ---------------------------------------------------------------- date text -> interval ---------------------------------------------
MON = r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\.?"
_MNUM = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
_PREFIX = re.compile(r"^(?:on or about|on or around|in or about|in or around|at or about|approximately|approx\.?|around|about|circa|"
                     r"between|from|since|during|as of|on|in|by|the)\s+", re.I)
_PART = {"early": "early", "beginning of": "early", "start of": "early", "mid": "mid", "middle of": "mid", "late": "late", "end of": "late"}
_ORD = {"first": 1, "second": 2, "third": 3, "fourth": 4, "1st": 1, "2nd": 2, "3rd": 3, "4th": 4}


def _mnum(s: str) -> int:
    return _MNUM[s.lower().rstrip(".")[:3]]


def _year(s: str) -> int:
    y = int(s)
    return y + 2000 if y < 100 else y


def _last(y, m):
    return date(y, m, calendar.monthrange(y, m)[1])


def normalise(t: str) -> str:
    t = t.replace(" ", " ")
    t = re.sub(r"[‐-―−~～]", "-", t)
    t = re.sub(r"(?<=\d)(st|nd|rd|th)\b", "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip(" ,.;:")
    for _ in range(4):
        t2 = _PREFIX.sub("", t).strip(" ,.;:")
        if t2 == t:
            break
        t = t2
    return t


# A reading is (kind, fn) where fn(year_or_None) -> (lo, hi) ; fixed readings ignore the argument. `yl` marks year-less readings.
@dataclass(frozen=True)
class Reading:
    kind: str          # day | iso_week | month | month_part | quarter | year_part | year | range
    y: int | None      # None = year-less
    spec: tuple        # kind-specific fields

    def interval(self, y: int | None = None) -> tuple[date, date]:
        Y = self.y if self.y is not None else y
        k, s = self.kind, self.spec
        if k == "day":
            d = date(Y, s[0], s[1]); return d, d
        if k == "month":
            return date(Y, s[0], 1), _last(Y, s[0])
        if k == "year":
            return date(Y, 1, 1), date(Y, 12, 31)
        if k == "quarter":
            return date(Y, 3 * s[0] - 2, 1), _last(Y, 3 * s[0])
        if k == "iso_week":
            if s[0] == "week":
                return date.fromisocalendar(Y, s[1], 1), date.fromisocalendar(Y, s[1], 5)
            iy, iw, _ = date(Y, s[1], s[2]).isocalendar()          # 'week of <date>'
            return date.fromisocalendar(iy, iw, 1), date.fromisocalendar(iy, iw, 5)
        if k == "month_part":
            m, part = s; last = calendar.monthrange(Y, m)[1]
            lo, hi = {"early": (1, 10), "mid": (11, 20), "late": (21, last)}[part]
            return date(Y, m, lo), date(Y, m, hi)
        if k == "year_part":
            m0, m1 = {"early": (1, 4), "mid": (5, 8), "late": (9, 12)}[s[0]]
            return date(Y, m0, 1), _last(Y, m1)
        if k == "range":
            a, b = s
            b_lo, b_hi = b.interval(Y)
            if a.y is None:                                        # start borrows the end's year (or the year before)
                a_lo, a_hi = a.interval(b_hi.year)
                if a_lo > b_hi:
                    a_lo, a_hi = a.interval(b_hi.year - 1)
            else:
                a_lo, a_hi = a.interval(Y)
            if a_lo > b_hi:
                raise ValueError("range start after end")
            return a_lo, b_hi
        raise ValueError(k)


def _points(t: str) -> list[Reading]:
    """All readings of a single (non-range) date expression; [] if not a date."""
    t = t.strip(" ,.;:")
    if m := re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", t):
        return [Reading("day", int(m[1]), (int(m[2]), int(m[3])))]
    if m := re.fullmatch(r"(\d{1,2})([/.-])(\d{1,2})\2(\d{2}|\d{4})", t):            # numeric day: m/d/y and d/m/y readings
        a, b, y = int(m[1]), int(m[3]), _year(m[4])
        rs = []
        if 1 <= a <= 12 and 1 <= b <= 31:
            rs.append(Reading("day", y, (a, b)))
        if 1 <= b <= 12 and 1 <= a <= 31 and a != b:
            rs.append(Reading("day", y, (b, a)))
        return rs
    if m := re.fullmatch(r"(\d{1,2})/(\d{4})", t):
        return [Reading("month", int(m[2]), (int(m[1]),))] if 1 <= int(m[1]) <= 12 else []
    if m := re.fullmatch(r"(\d{1,2})[/-](\d{1,2})-?", t):                              # year-less numeric day
        a, b = int(m[1]), int(m[2]); rs = []
        if 1 <= a <= 12 and 1 <= b <= 31:
            rs.append(Reading("day", None, (a, b)))
        if 1 <= b <= 12 and 1 <= a <= 31 and a != b:
            rs.append(Reading("day", None, (b, a)))
        return rs
    if m := re.fullmatch(rf"{MON}\s*(\d{{1,2}}),?\s*(\d{{4}})", t, re.I):
        return [Reading("day", int(m[3]), (_mnum(m[1]), int(m[2])))]
    if m := re.fullmatch(rf"{MON}\s+(\d{{1,2}})/(\d{{4}})", t, re.I):
        return [Reading("day", int(m[3]), (_mnum(m[1]), int(m[2])))]
    if m := re.fullmatch(rf"(\d{{1,2}})\.?[\s-]*{MON}[\s,-]*(\d{{4}}|\d{{2}})", t, re.I):
        return [Reading("day", _year(m[3]), (_mnum(m[2]), int(m[1])))]
    if m := re.fullmatch(rf"{MON}(?:\s+of)?[\s,-]*(\d{{4}})", t, re.I):
        return [Reading("month", int(m[2]), (_mnum(m[1]),))]
    if m := re.fullmatch(r"(19\d{2}|20\d{2})", t):
        return [Reading("year", int(m[1]), ())]
    if m := re.fullmatch(r"(?:q([1-4])|([1-4])q|(first|second|third|fourth|1st|2nd|3rd|4th) quarter(?: of)?)[\s,/-]*(\d{4}|\d{2})", t, re.I):
        q = int(m[1] or m[2] or _ORD[m[3].lower()])
        return [Reading("quarter", _year(m[4]), (q,))]
    if m := re.fullmatch(r"(?:cw|kw|wk|week)\.?\s*(\d{1,2})(?:\s*(?:/|,|-|of)?\s*(\d{4}|\d{2}))?", t, re.I):
        return [Reading("iso_week", _year(m[2]) if m[2] else None, ("week", int(m[1])))]
    if m := re.fullmatch(r"week of\s+(.+)", t, re.I):
        return [Reading("iso_week", r.y, ("of", r.spec[0], r.spec[1])) for r in _points(m[1]) if r.kind == "day"]
    if m := re.fullmatch(r"(early|beginning of|start of|middle of|mid|late|end of)[\s-]*(.+)", t, re.I):
        part = _PART[m[1].lower()]
        rs = []
        for r in _points(m[2]):
            if r.kind == "month":
                rs.append(Reading("month_part", r.y, (r.spec[0], part)))
            elif r.kind == "year":
                rs.append(Reading("year_part", r.y, (part,)))
        return rs
    if m := re.fullmatch(rf"{MON}\s*(\d{{1,2}})", t, re.I):                         # year-less textual day
        return [Reading("day", None, (_mnum(m[1]), int(m[2])))]
    if m := re.fullmatch(rf"(\d{{1,2}})\.?\s+{MON}", t, re.I):
        return [Reading("day", None, (_mnum(m[2]), int(m[1])))]
    if m := re.fullmatch(MON, t, re.I):
        return [Reading("month", None, (_mnum(m[1]),))]
    return []


_WORD_SEP = re.compile(r"\s+(?:through|thru|until|till|to|and|&)\s+|\s+-\s+", re.I)


def readings(text: str) -> list[Reading]:
    """All readings of a date text (single date or range); [] if it is not a date this parser knows."""
    t = normalise(text or "")
    if not t:
        return []
    rs = _points(t)
    if rs:
        return rs
    # day range inside one month: 'March 30 and 31, 2020', 'June 14-15, 2020', 'MON D - D' (year-less), '20 to 24 Apr 2026'
    if m := re.fullmatch(rf"{MON}\s*(\d{{1,2}})\s*(?:-|and|to|through|thru|&|,)\s*(\d{{1,2}})(?:,?\s*(\d{{4}}))?", t, re.I):
        y = int(m[4]) if m[4] else None; mo = _mnum(m[1])
        return [Reading("range", y, (Reading("day", y, (mo, int(m[2]))), Reading("day", y, (mo, int(m[3])))))]
    if m := re.fullmatch(rf"(\d{{1,2}})\s*(?:-|and|to|through|thru)\s*(\d{{1,2}})[\s-]+{MON}[\s,-]*(\d{{4}})", t, re.I):
        y = int(m[4]); mo = _mnum(m[3])
        return [Reading("range", y, (Reading("day", y, (mo, int(m[1]))), Reading("day", y, (mo, int(m[2])))))]
    # general range: two expressions; word separators and spaced dashes first, then each unspaced dash
    cands = [(t[:m.start()], t[m.end():]) for m in _WORD_SEP.finditer(t)]
    cands += [(t[:i], t[i + 1:]) for i, ch in enumerate(t) if ch == "-"]
    for a, b in cands:
        ra, rb = _points(a.strip(" ,")), _points(b.strip(" ,"))
        if not ra or not rb:
            continue
        out = []
        for x in ra:
            for z in rb:
                if x.y is not None and z.y is None:
                    continue                                         # 'March 2020 - May' is not supported
                out.append(Reading("range", z.y, (x, z)))
        if out:
            return out
    return []


@dataclass
class Interval:
    lo: date
    hi: date
    precision: str
    ambiguous: bool = False
    year_from_context: bool = False
    capped: bool = False


def resolve(text: str, filing: date, ctx_years: set) -> Interval | None:
    """Date text -> [lo, hi] (protocol D). Year-less dates take the year by the frozen labelling rule (tt.labels.dates.parse_span):
    the single year of the chronology's fully dated events, else (no such year) the filing year if the result is not after the
    filing date, else unresolved (None). Ambiguous numeric dates keep each reading <= filing date (all readings if none qualifies);
    two or more distinct readings -> union interval, ambiguous=True. hi is capped at the filing date when lo <= filing < hi."""
    ivs = []
    for r in readings(text):
        yfc = False
        try:
            if r.y is None:
                if len(ctx_years) == 1:
                    lo, hi = r.interval(next(iter(ctx_years))); yfc = True
                elif not ctx_years and filing is not None:
                    lo, hi = r.interval(filing.year); yfc = True
                    if lo > filing:
                        continue
                else:
                    continue
            else:
                lo, hi = r.interval()
        except ValueError:
            continue
        ivs.append((lo, hi, r.kind, yfc))
    if not ivs:
        return None
    ivs = sorted(set(ivs))
    keep = [v for v in ivs if v[0] <= filing] or ivs
    lo, hi = min(v[0] for v in keep), max(v[1] for v in keep)
    iv = Interval(lo, hi, keep[0][2] if len({v[2] for v in keep}) == 1 else "range", len(keep) > 1, any(v[3] for v in keep))
    if iv.lo <= filing < iv.hi:
        iv.hi, iv.capped = filing, True
    return iv


def date_format(text: str) -> str:
    """Format class of a raw date text, independent of any filing (inventory item 7)."""
    rs = readings(text)
    if not rs:
        return "unparsed"
    if len(rs) > 1:
        return "numeric_ambiguous"
    r = rs[0]
    if r.kind == "range":
        return "range"
    if r.y is None:
        return "yearless"
    return {"day": "full_date", "iso_week": "week", "month": "month", "month_part": "early_mid_late", "year_part": "early_mid_late",
            "quarter": "quarter", "year": "year"}[r.kind]


# ---------------------------------------------------------------- anchors ---------------------------------------------------------------
RECALL_NO = re.compile(r"\d{2}[VECT]-?\d{3}")


def cites_other_recall(quote: str, campaign: str) -> bool:
    return any(m.group(0).replace("-", "") != campaign for m in RECALL_NO.finditer(quote or ""))


LEXICON = ["decided to conduct", "decided to recall", "determined that a defect", "determination", "recall determination committee",
           "product safety committee", "field review committee", "safety committee"]


def lexicon_hit(quote: str) -> bool:
    q = (quote or "").lower()
    return any(w in q for w in LEXICON)


def anchor(events: list[dict], filing: date, campaign: str, ctx_years: set, mode: str = "latest_decision"):
    """events: dicts with date_text, type, quote. -> (Interval, n_candidates) or (None, n_candidates).
    modes: latest_decision (primary), earliest_decision, latest_any, latest_lexicon."""
    cands = []
    for e in events:
        if mode in ("latest_decision", "earliest_decision") and e["type"] != "DECISION":
            continue
        if mode == "latest_lexicon" and not lexicon_hit(e.get("quote")):
            continue
        iv = resolve(e.get("date_text") or "", filing, ctx_years)
        if iv is None or iv.lo > filing:
            continue
        if cites_other_recall(e.get("quote"), campaign):
            continue
        cands.append(iv)
    if not cands:
        return None, 0
    if mode == "earliest_decision":
        return min(cands, key=lambda v: (v.lo, v.hi)), len(cands)
    return max(cands, key=lambda v: (v.hi, v.lo)), len(cands)


# ---------------------------------------------------------------- statistics ------------------------------------------------------------
def wilson(k: int, n: int, z: float = 1.959963984540054):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def quantile(xs, p):
    """Linear interpolation between order statistics (position (n-1)p)."""
    xs = sorted(xs)
    if not xs:
        return float("nan")
    i = (len(xs) - 1) * p; lo = math.floor(i); hi = math.ceil(i)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def kappa_pabak(pairs, cats=("FLAGGED", "NOT_FLAGGED", "INDETERMINATE")):
    n = len(pairs)
    if n == 0:
        return float("nan"), float("nan")
    po = sum(a == b for a, b in pairs) / n
    pe = sum((sum(a == c for a, _ in pairs) / n) * (sum(b == c for _, b in pairs) / n) for c in cats)
    k = len(cats)
    kap = (po - pe) / (1 - pe) if pe < 1 else float("nan")
    return kap, (k * po - 1) / (k - 1)


def anon_labels(counts: dict) -> dict:
    """Manufacturer -> M1..Mk, ordered by count (descending), ties by a hash of the name (no alphabetical leak)."""
    order = sorted(counts, key=lambda f: (-counts[f], hashlib.sha256(f.encode()).hexdigest()))
    return {f: f"M{i}" for i, f in enumerate(order, 1)}
