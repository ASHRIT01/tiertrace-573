"""Date-text normalisation for event labels.

parse_span(text, years=None, filing=None) -> Span | None
  Strips 'On or about', 'approximately', 'around' (and leading on/in/by/since/during).
  granularity: day | month | quarter | year | range | fuzzy.  start/end are inclusive dates.
  Year-less dates ('May 16', '11/29') take a year only if it is unambiguous from context:
    - `years` = the set of years of the fully dated events of the same chronology; if it has exactly one year Y, use Y;
    - else, if there are no fully dated events, use the filing year, provided the result is not after the filing date;
    - otherwise the span is returned with year_inferred=False and inferred=True (date_inferred: excluded from scoring).
  'mid-2017', 'mid-August 2017', 'early/late X', 'end of X', 'beginning of X' are fuzzy (an approximate interval)."""
import calendar
import re
from dataclasses import dataclass, asdict
from datetime import date

_M = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}
_M.update({m.lower(): i for i, m in enumerate(calendar.month_abbr) if m})
_M["sept"] = 9
MON = r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sept?(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\.?"
SEP = r"\s*(?:-|–|—|～|~|through|thru|to|until|and)\s*"


@dataclass
class Span:
    start: date
    end: date
    granularity: str
    inferred: bool = False          # year could not be fixed unambiguously -> excluded from scoring
    year_from_context: bool = False  # year taken from context (unambiguous)

    def asdict(self):
        d = asdict(self)
        d["start"], d["end"] = self.start.isoformat(), self.end.isoformat()
        return d


def _mon(s: str) -> int:
    return _M[s.lower().rstrip(".")[:4] if s.lower().startswith("sept") else s.lower().rstrip(".")[:3]] if s.lower().rstrip(".")[:3] in _M else _M[s.lower().rstrip(".")]


def _y(s: str) -> int:
    y = int(s)
    return y + 2000 if y < 100 else y


def _last(y: int, m: int) -> date:
    return date(y, m, calendar.monthrange(y, m)[1])


def strip_prefix(t: str) -> str:
    t = re.sub(r"\s+", " ", t.strip().strip(",.:;")).strip()
    for _ in range(3):
        t = re.sub(r"^(on or about|approximately|approx\.?|around|about|circa|on|in|by|since|during|as of)\s+", "", t, flags=re.I)
    return t.strip(" ,")


def _point(t: str):
    """A single date expression -> (start, end, granularity, has_year) or None."""
    t = t.strip(" ,.")
    if m := re.fullmatch(rf"{MON}\s+(\d{{1,2}})/(\d{{4}})", t, re.I):          # 'APRIL 24/2021'
        d = date(int(m[3]), _mon(m[1]), int(m[2])); return d, d, "day", True
    if m := re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", t):
        d = date(int(m[1]), int(m[2]), int(m[3])); return d, d, "day", True
    if m := re.fullmatch(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", t):
        if not (1 <= int(m[1]) <= 12 and 1 <= int(m[2]) <= 31):
            return None
        d = date(_y(m[3]), int(m[1]), int(m[2])); return d, d, "day", True
    if m := re.fullmatch(r"(\d{1,2})/(\d{4})", t):
        y, mo = int(m[2]), int(m[1])
        if 1 <= mo <= 12:
            return date(y, mo, 1), _last(y, mo), "month", True
    if m := re.fullmatch(r"(\d{1,2})-(\d{1,2})-?", t):                      # '11-13-' (year missing)
        return (int(m[1]), int(m[2])), None, "day", False
    if m := re.fullmatch(MON, t, re.I):                                     # 'August' (year-less month, e.g. 'In August,')
        return ("month", _mon(m[1])), None, "month", False
    if m := re.fullmatch(r"(\d{1,2})/(\d{1,2})", t):
        return (int(m[1]), int(m[2])), None, "day", False
    if m := re.fullmatch(rf"{MON}\s+(\d{{1,2}})(?:st|nd|rd|th)?,?\s*(\d{{4}})", t, re.I):
        d = date(int(m[3]), _mon(m[1]), int(m[2])); return d, d, "day", True
    if m := re.fullmatch(rf"(\d{{1,2}})(?:st|nd|rd|th)?[\s-]+{MON},?[\s-]+(\d{{2,4}})", t, re.I):
        d = date(_y(m[3]), _mon(m[2]), int(m[1])); return d, d, "day", True
    if m := re.fullmatch(rf"{MON}\s+(\d{{1,2}})(?:st|nd|rd|th)?", t, re.I):
        return (_mon(m[1]), int(m[2])), None, "day", False
    if m := re.fullmatch(rf"{MON}\s+of\s+(\d{{4}})", t, re.I):
        y, mo = int(m[2]), _mon(m[1]); return date(y, mo, 1), _last(y, mo), "month", True
    if m := re.fullmatch(rf"{MON},?[\s-]+(\d{{4}}|\d{{2}})", t, re.I):
        y, mo = _y(m[2]), _mon(m[1]); return date(y, mo, 1), _last(y, mo), "month", True
    if m := re.fullmatch(r"(?:q([1-4])|(first|second|third|fourth) quarter(?: of)?)\s*(\d{4})", t, re.I):
        q = int(m[1]) if m[1] else ["first", "second", "third", "fourth"].index(m[2].lower()) + 1
        y = int(m[3]); return date(y, 3 * q - 2, 1), _last(y, 3 * q), "quarter", True
    if m := re.fullmatch(r"(\d{4})", t):
        y = int(m[1]); return date(y, 1, 1), date(y, 12, 31), "year", True
    return None


_FUZZ = {"early": (1, 10, 1, 4), "beginning of": (1, 10, 1, 4), "mid": (10, 20, 4, 9), "late": (20, 31, 9, 12), "end of": (20, 31, 10, 12)}


def parse_span(text: str, years: set | None = None, filing: date | None = None) -> Span | None:
    t = re.sub(r"(?<=\d)\s*([/-])\s*(?=\d)", r"\1", strip_prefix(text))
    if not t:
        return None
    # fuzzy: early/mid/late/end of/beginning of + month-year or year
    if m := re.fullmatch(r"(early|mid|late|end of|beginning of)[\s-]*(.+)", t, re.I):
        k = m[1].lower(); dlo, dhi, mlo, mhi = _FUZZ[k]
        p = _point(m[2])
        if p and p[2] == "month":
            s0 = p[0]; last = _last(s0.year, s0.month).day
            return Span(date(s0.year, s0.month, min(dlo, last)), date(s0.year, s0.month, min(dhi, last)), "fuzzy")
        if p and p[2] == "year":
            y = p[0].year; return Span(date(y, mlo, 1), _last(y, mhi), "fuzzy")
        return None
    # day range inside one month: 'March 30 and 31, 2020', 'June 14 and 15, 2020', 'April 16, 17, 2015'
    if m := re.fullmatch(rf"{MON}\s+(\d{{1,2}})\s*(?:-|–|and|to|through|,)\s*(\d{{1,2}}),?\s*(\d{{4}})", t, re.I):
        y, mo = int(m[4]), _mon(m[1]); return Span(date(y, mo, int(m[2])), date(y, mo, int(m[3])), "range")
    # 'm-d thru d-yy': '10-25 thru 28 -19'
    if m := re.fullmatch(r"(\d{1,2})-(\d{1,2})\s*(?:thru|through|to|-)\s*(\d{1,2})-(\d{2,4})", t, re.I):
        y, mo = _y(m[4]), int(m[1]); return Span(date(y, mo, int(m[2])), date(y, mo, int(m[3])), "range")
    p = _point(t)
    # range of two expressions (only if the whole text is not already a single date such as 'Nov-2015')
    parts = re.split(SEP, t, maxsplit=1, flags=re.I) if p is None else []
    if len(parts) == 2 and all(parts):
        a, b = parts[0].strip(" ,"), parts[1].strip(" ,")
        pb = _point(b)
        pa = _point(a)
        if pb and pb[3] and (pa is None or (not pa[3] and pa[0][0] == "month")) and re.fullmatch(MON, a, re.I):   # 'April through August 2016'
            pa = (date(pb[0].year, _mon(a), 1), _last(pb[0].year, _mon(a)), "month", True)
        if pa and not pa[3] and pb and pb[3]:                                    # 'April 18 - May 27, 2015'
            d0 = date(pb[0].year, pa[0][0], pa[0][1]); pa = (d0, d0, "day", True)
        if pa and pb and pa[3] and pb[3]:
            return Span(min(pa[0], pb[0]), max(pa[1], pb[1]), "range")
    if p is None:
        return None
    if p[3]:
        return Span(p[0], p[1], p[2])
    # year-less month ('In August,'): same context rule as year-less days
    if p[0][0] == "month":
        mo = p[0][1]
        if years and len(years) == 1:
            y = next(iter(years)); return Span(date(y, mo, 1), _last(y, mo), "month", year_from_context=True)
        if not years and filing is not None and date(filing.year, mo, 1) <= filing:
            return Span(date(filing.year, mo, 1), _last(filing.year, mo), "month", year_from_context=True)
        return Span(date(1900, mo, 1), _last(1900, mo), "month", inferred=True)
    # year-less day: (month, day)
    mo, dd = p[0]
    if years and len(years) == 1:
        y = next(iter(years))
        return Span(date(y, mo, dd), date(y, mo, dd), "day", year_from_context=True)
    if not years and filing is not None:
        d = date(filing.year, mo, dd)
        if d <= filing:
            return Span(d, d, "day", year_from_context=True)
    return Span(date(1900, mo, dd), date(1900, mo, dd), "day", inferred=True)


def coarse_overlap(a: Span, b: Span) -> bool:
    """Overlap after widening both spans to the coarser of their granularities (day < month < quarter < year; range kept as is)."""
    order = {"day": 0, "month": 1, "quarter": 2, "year": 3}
    g = max((a.granularity, b.granularity), key=lambda x: order.get(x, -1))
    def widen(s: Span) -> tuple[date, date]:
        if g == "month":
            return date(s.start.year, s.start.month, 1), _last(s.end.year, s.end.month)
        if g == "quarter":
            qs, qe = 3 * ((s.start.month - 1) // 3) + 1, 3 * ((s.end.month - 1) // 3) + 3
            return date(s.start.year, qs, 1), _last(s.end.year, qe)
        if g == "year":
            return date(s.start.year, 1, 1), date(s.end.year, 12, 31)
        return s.start, s.end
    (a0, a1), (b0, b1) = widen(a), widen(b)
    return a0 <= b1 and b0 <= a1
