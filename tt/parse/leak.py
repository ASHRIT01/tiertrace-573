"""Detect page-break / page-header text that leaked into a parsed section (cause, chronology, ...).
Independent of the cleaning patterns: it looks at the final section text for page furniture."""
import re

PATTERNS = {
    "page_marker": re.compile(r"\bPage\s*\d+(?:\s*of\s*\d+)?\b"),
    "report_title": re.compile(r"Part 573 Safety Recall Report", re.I),
    "submitted_pursuant": re.compile(r"information contained in this report was submitted pursuant", re.I),
    "dot_header": re.compile(r"U\.S\. Department\s+of Transportation", re.I),
    "header_fields": re.compile(r"Manufacturer Recall No\.?\s*:|NHTSA Recall No\.?\s*:|Submission Date\s*:", re.I),
    "omb": re.compile(r"OMB Control No", re.I),
}
SECTIONS = ("cause", "chronology", "defect", "risk")


def leaks(sections: dict[str, str]) -> dict[str, list[str]]:
    """{section: [pattern names found]} for sections with any leakage."""
    out = {}
    for s in SECTIONS:
        hit = [k for k, p in PATTERNS.items() if p.search(sections.get(s, ""))]
        if hit:
            out[s] = hit
    return out
