"""Split Part 573 text into sections.

NOTE: heading regexes follow the section list in the PRD and are UNTESTED against
real PDFs (Week 1 gate). Adjust HEADINGS once real text is available.
"""
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", " ", s).strip().lower()


HEADINGS = {
    "defect": r"(?:description of the defect|defect description)",
    "risk": r"(?:safety risk|description of the safety risk)",
    "cause": r"(?:description of the cause|cause of the defect)",
    "block": r"(?:component manufacturer|supplier identification)",
    "components": r"(?:involved components|identification of (?:any )?involved components)",
    "chronology": r"(?:chronology|description of (?:the )?chronology)",
    "related": r"(?:related recall|identification of any warranty)",
    "remedy": r"(?:description of the remedy|remedy program|recall remedy)",
}


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
    """Return {name: body}. A heading is a line that starts with the pattern."""
    hits = []
    for name, pat in HEADINGS.items():
        for m in re.finditer(rf"(?im)^\s*(?:\d+[.)]?\s*)?{pat}\b[^\n]*:?\s*$|^\s*(?:\d+[.)]?\s*)?{pat}\b[^\n]*:\s*", text):
            hits.append((m.start(), m.end(), name))
    hits.sort()
    out: dict[str, str] = {}
    for i, (_, end, name) in enumerate(hits):
        nxt = hits[i + 1][0] if i + 1 < len(hits) else len(text)
        out.setdefault(name, text[end:nxt].strip())
    return out
