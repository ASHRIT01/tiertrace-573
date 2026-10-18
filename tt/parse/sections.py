"""Split Part 573 text into sections. Two layouts seen in real filings (2023-2026):
 old: 'Label : value' on one line; new: 'Label:' then value on the next line.
Tuned on the six reference filings (data/raw, tests/test_golden.py)."""
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date

from tt.verify.dates import parse_date


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", " ", s).strip().lower()


# Boundary headings (line-anchored). Several names may share a section key; a section
# runs until the next heading of a *different* key.
HEADINGS = [
    ("defect", r"description of the defect(?: or noncompliance)?"),
    ("fmvss", r"fmvss\s*1"),
    ("risk", r"description of the safety risk[^:\n]*"),
    ("cause", r"description of the cause"),
    ("warning", r"identification of any warning"),
    ("block", r"supplier identification"),
    ("block", r"component manufacturer"),
    ("components", r"involved components"),
    ("chronology", r"chronology"),
    ("related", r"related nhtsa recall number"),
    ("remedy", r"description of (?:the )?remedy"),
]

# Page furniture that PDF text extraction drops into the middle of running text.
# 1) The stacked layout's page-header block, removed as one unit (it spans many lines).
_HEADER_BLOCK = re.compile(
    r"U\.S\. Department\s+of Transportation\s+National Highway\s+Traffic Safety\s+Administration"
    r".{0,400}?Manufacturer Recall No\.?\s*:[^\n]*\n?"
    r"(?:[ \t]*The information contained in this report[^\n]*\n?)?(?:[ \t]*OMB Control No[^\n]*\n?)?", re.S | re.I)
# 2) Single-line furniture.
_NOISE = [
    r"^\s*OMB Control No\.?\s*:?\s*\S*\s*$",
    r"^\s*Part 573 Safety Recall Report\s*$",
    r"^\s*\d{2}[VEvEe]-?\d{3}\s*$",
    r"^\s*The information contained in this report was submitted pursuant to.*$",
    r"^[ \t]*Page[ \t]*\d+([ \t]*of[ \t]*\d+)?[ \t]*$",       # 'Page 2' / 'Page 2 of 4'
    r"^[ \t]*Page[ \t]*\n[ \t]*\d+([ \t]*of[ \t]*\d+)?[ \t]*$",  # 'Page' and the number on separate lines
    r"^\s*\* NR - Not Reported\s*$",
]


def clean(text: str) -> str:
    text = _HEADER_BLOCK.sub("\n", text)
    for pat in _NOISE:
        text = re.sub(pat, "", text, flags=re.M | re.I)
    return re.sub(r"\n{3,}", "\n\n", text)


@dataclass
class Doc:
    campaign: str
    filer: str
    filing_date: date
    full_text: str
    sections: dict[str, str] = field(default_factory=dict)

    @property
    def cause_is_nr(self) -> bool:
        c = self.sections.get("cause", "").strip().lower().rstrip(".")
        return c in {"nr", "n/r", "not reported", "not available", "n/a", ""}


def split_sections(text: str) -> dict[str, str]:
    text = clean(text)
    hits = []
    for key, pat in HEADINGS:
        for m in re.finditer(rf"(?im)^[ \t]*(?:{pat})[ \t]*:?[ \t]*", text):
            hits.append((m.start(), m.end(), key))
    hits.sort()
    out: dict[str, str] = {}
    for i, (_, end, key) in enumerate(hits):
        if key in out:
            continue
        nxt = len(text)
        for s, _, k in hits[i + 1:]:
            if k != key:
                nxt = s
                break
        out[key] = re.sub(r"\s+", " ", text[end:nxt]).strip()
    return out


def parse_header(text: str) -> dict:
    """Filer name, submission date and campaign number from the first page."""
    t = text  # raw: the first-page header block is exactly what we read here
    name = re.search(r"Manufacturer Name\s*:\s*(.+?)(?=\n\s*(?:Address|Submission Date|NHTSA Recall)|\n[A-Z][\w ]+\s*:|\Z)", t, re.S)
    sub = re.search(r"Submission Date\s*:\s*([A-Za-z]{3,9}\s+\d{1,2},\s*\d{4})", t)
    camp = re.search(r"NHTSA Recall No\.?\s*:\s*(\d{2}[VE]-?\d{3})", t)
    filer = re.sub(r"\s+", " ", name.group(1)).strip() if name else ""
    sd = parse_date(sub.group(1), date(2100, 1, 1)) if sub else None
    return {"filer": filer, "filing_date": sd, "campaign": camp.group(1).replace("-", "") if camp else ""}
