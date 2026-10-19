"""Baselines on the same masked input the LLM sees. B0: most common value per claim type (no text). B1: rules/regex only.
Both return dicts shaped like agent Extraction so tt.eval.devscore.score treats them exactly like model output."""
import re
from collections import Counter

MONTH = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
DATE = re.compile(rf"\b{MONTH}\.?\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}\b|\b\d{{1,2}}/\d{{1,2}}/\d{{2,4}}\b|\b\d{{1,2}}-\d{{1,2}}-\d{{2,4}}\b", re.I)
TYPES = [  # first match wins; keyword lists written before looking at dev results
    ("NHTSA_FILING", re.compile(r"\bNHTSA\b|Part 573|\bsubmitted\b.*\b(?:report|notice)|\bfiled\b", re.I)),
    ("SUPPLIER_NOTICE", re.compile(r"\b(?:supplier|vendor|manufacturer)\b.*\b(?:notif|inform|advis|contact|alert)|\b(?:notif|inform|advis|contact|alert)\w*\b.*\b(?:supplier|vendor)\b", re.I)),
    ("DECISION", re.compile(r"\b(?:determin|decid|conclud|safety[- ]related|decision)\w*", re.I)),
    ("INVESTIGATION_START", re.compile(r"\b(?:investigat|analy[sz]|test|inspect|evaluat|review|audit|examin)\w*", re.I)),
    ("FILER_AWARENESS", re.compile(r"\b(?:aware|learned|received|report(?:ed)?|complaint|warranty|field|claim|notif)\w*", re.I)),
]
ORG = re.compile(r"\b(?:[A-Z][\w&.'\-]*\s+){0,4}[A-Z][\w&.'\-]*\s+(?:Inc\.?|LLC|L\.L\.C\.|Corp\.?|Corporation|Co\.|Company|Ltd\.?|GmbH|AG|S\.A\.|Industries|Manufacturing|Systems|Technologies)(?=\W|$)")
NR = {"", "nr", "n/r", "n/a", "na", "not reported", "not available"}


def _sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text)) if s.strip()]


def b0(majority_cause_reported: bool) -> dict:
    return {"companies": [], "supply_path": [], "locus": "UNDETERMINED", "locus_status": "NOT_REPORTED", "locus_evidence": None,
            "events": [], "cause_reported": majority_cause_reported, "abstain_reason": None}


def b1(cause: str, chron: str, filer: str) -> dict:
    """cause/chron are the (masked) section texts."""
    comps, seen = [], set()
    for sec, text in (("cause", cause), ("chronology", chron)):
        for s in _sentences(text):
            for m in ORG.finditer(s):
                nm = m.group(0).strip()
                if nm.lower() in seen or nm.lower() in filer.lower() or filer.lower() in nm.lower() or len(comps) >= 8:
                    continue
                seen.add(nm.lower())
                comps.append({"name": nm, "role": "SUPPLIER", "status": "SUPPORTED", "evidence": {"section": sec, "quote": s[:300]}})
    events = []
    for s in _sentences(chron):
        m = DATE.search(s)
        if not m or len(events) >= 24:
            continue
        t = next((name for name, rx in TYPES if rx.search(s)), "OTHER")
        events.append({"date_text": m.group(0), "type": t, "status": "SUPPORTED", "evidence": {"section": "chronology", "quote": s[:300]}})
    c = cause.strip().lower().rstrip(".")
    return {"companies": comps, "supply_path": [], "locus": "UNDETERMINED", "locus_status": "NOT_REPORTED", "locus_evidence": None,
            "events": events, "cause_reported": c not in NR, "abstain_reason": None}
