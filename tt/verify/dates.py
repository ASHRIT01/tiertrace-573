"""Rule-based date parsing. Returns None rather than guessing."""
import re
from datetime import date

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"], 1)}
MONTHS.update({k[:3]: v for k, v in list(MONTHS.items())})
MONTHS["sept"] = 9

_MON = r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sept?(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
_FUZZY = {"early": 5, "mid": 15, "late": 25}


def _mk(y: int, m: int, d: int) -> date | None:
    try:
        return date(y, m, d)
    except ValueError:
        return None


def parse_date(text: str, anchor: date) -> date | None:
    """Parse a date expression. Fuzzy phrases ('late April') map to day 5/15/25.
    A month with no year resolves to the latest such month not after `anchor`."""
    t = re.sub(r"[,.]", " ", text.lower()).replace("-", " ")
    t = re.sub(r"\s+", " ", t).strip()
    if m := re.fullmatch(r"(\d{4}) (\d{1,2}) (\d{1,2})", t):
        return _mk(int(m[1]), int(m[2]), int(m[3]))
    if m := re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4}|\d{2})", text.strip()):
        y = int(m[3]) + (2000 if len(m[3]) == 2 else 0)
        return _mk(y, int(m[1]), int(m[2]))
    if m := re.fullmatch(rf"{_MON} (\d{{1,2}})(?:st|nd|rd|th)? (\d{{4}})", t):
        return _mk(int(m[3]), MONTHS[m[1]], int(m[2]))
    if m := re.fullmatch(rf"(\d{{1,2}}) {_MON} (\d{{4}})", t):
        return _mk(int(m[3]), MONTHS[m[2]], int(m[1]))
    if m := re.fullmatch(rf"(?:(early|mid|late) )?{_MON}(?: (\d{{4}}))?", t):
        day = _FUZZY.get(m[1], 1) if m[1] else 1
        mon = MONTHS[m[2]]
        if m[3]:
            return _mk(int(m[3]), mon, day)
        d = _mk(anchor.year, mon, day)
        return d if d and d <= anchor else _mk(anchor.year - 1, mon, day)
    if m := re.fullmatch(rf"{_MON} (\d{{1,2}})(?:st|nd|rd|th)?", t):
        d = _mk(anchor.year, MONTHS[m[1]], int(m[2]))
        return d if d and d <= anchor else _mk(anchor.year - 1, MONTHS[m[1]], int(m[2]))
    return None
