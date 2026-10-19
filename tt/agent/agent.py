"""Phase 4 agent: the LLM proposes (two runs), deterministic code disposes. A claim is ACCEPTED only if every verifier passes AND the
second run agrees; otherwise the agent abstains. Model confidence is never used. A deterministic rank score orders claims for
risk-coverage curves: 0 = a verifier failed; else 1 + 2*(second run agrees) + (rule baseline B1 agrees); accepted = no verifier failed and the second run agrees (score >= 3).
Verifiers: V1 quote verbatim in the claimed (masked) section; V2a name in text; V2b filer is not a supplier (unless it is the block supplier);
V3 date valid by the span parser, V3o event order; V4 NR cause must stay NR; E1 event date text inside its quote; S2n supplier name verbatim
in the cause/chronology narrative, else the claim is INSUFFICIENT; V8 no instruction-like text in a quote or name."""
import re
from datetime import date

from tt.eval.devscore import SUPPLIER_ROLES, _same
from tt.labels.dates import coarse_overlap, parse_span
from tt.parse.sections import norm
from tt.verify.dates import parse_date
from tt.verify.extra import date_errors, masked_doc
from tt.verify.verifier import EVENT_ORDER, locate

INJECTION = re.compile(
    r"\b(?:ignore|disregard|forget|override)\b[^.]{0,40}\b(?:previous|prior|above|earlier|all|any|the)\b[^.]{0,30}\b(?:instructions?|rules?|prompt|schema)\b"
    r"|\bsystem prompt\b|\b(?:note|message|instructions?) (?:to|for) (?:the )?(?:assistant|model|ai|llm|extractor)\b|\bas an? (?:ai|assistant|language model)\b"
    r"|\byou (?:must|should|will|are to) (?:now )?(?:output|respond|answer|list|set|add|report|return|ignore)\b|\bPWNED\b|<\s*/?\s*data\s*>", re.I)


def injection(*texts) -> bool:
    return any(INJECTION.search(t or "") for t in texts)


def supplier_claims(ex):
    return [c for c in ex.companies if c.role in SUPPLIER_ROLES and c.status == "SUPPORTED"]


def event_order_bad(ex, doc) -> set:
    """indices of events involved in an order inconsistency (SUPPLIER_NOTICE <= FILER_AWARENESS <= DECISION <= NHTSA_FILING)."""
    ds = []
    for i, e in enumerate(ex.events):
        d = parse_date(e.date_text, anchor=doc.filing_date)
        if d is not None and e.type in EVENT_ORDER:
            ds.append((i, d, EVENT_ORDER.index(e.type)))
    bad = set()
    for i1, d1, r1 in ds:
        for i2, d2, r2 in ds:
            if r1 < r2 and d1 > d2:
                bad |= {i1, i2}
    return bad


def company_reasons(c, ex, doc, block_name, narrative) -> list[str]:
    md, why = masked_doc(doc, block_name), []
    if locate(c.evidence.quote, md.sections.get(c.evidence.section, "")) is None: why.append("V1")
    if not locate(c.name, doc.full_text): why.append("V2a")
    if norm(c.name) == norm(doc.filer) and norm(c.name) != norm(block_name or "\0"): why.append("V2b")
    if not locate(c.name, narrative): why.append("S2n")
    if injection(c.name, c.evidence.quote): why.append("V8")
    return why


def event_reasons(i, e, ex, doc, block_name, order_bad) -> list[str]:
    md, why = masked_doc(doc, block_name), []
    if locate(e.evidence.quote, md.sections.get(e.evidence.section, "")) is None: why.append("V1")
    if norm(e.date_text) not in norm(e.evidence.quote): why.append("E1")
    if date_errors(type("X", (), {"events": [e]})(), doc): why.append("V3")
    if i in order_bad: why.append("V3o")
    if injection(e.evidence.quote, e.date_text): why.append("V8")
    return why


def cause_reasons(ex, doc) -> list[str]:
    return ["V4"] if doc.cause_is_nr and ex.cause_reported else []


def _agree_company(c, other) -> bool:
    return any(_same(c.name, o.name) for o in supplier_claims(other))


def _agree_event(e, doc, ex, other) -> bool:
    sp = parse_span(e.date_text or "", filing=doc.filing_date)
    if sp is None:
        return False
    for o in other.events:
        so = parse_span(o.date_text or "", filing=doc.filing_date)
        if so is not None and o.type == e.type and coarse_overlap(sp, so):
            return True
    return False


def decide(run1, run2, base, doc, block_name):
    """-> list of claim dicts {kind, ref, reasons, agree2, agreeB1, score, accepted}."""
    narrative = doc.sections.get("cause", "") + " " + doc.sections.get("chronology", "")
    ob, out = event_order_bad(run1, doc), []
    for c in supplier_claims(run1):
        r = company_reasons(c, run1, doc, block_name, narrative)
        a2, ab = (run2 is not None and _agree_company(c, run2)), _agree_company(c, base)
        out.append({"kind": "S2", "ref": c, "reasons": r, "agree2": a2, "agreeB1": ab})
    for i, e in enumerate(run1.events):
        r = event_reasons(i, e, run1, doc, block_name, ob)
        a2 = run2 is not None and _agree_event(e, doc, run1, run2)
        out.append({"kind": "E", "ref": e, "reasons": r, "agree2": a2, "agreeB1": _agree_event(e, doc, run1, base)})
    r = cause_reasons(run1, doc)
    out.append({"kind": "C", "ref": None, "reasons": r, "agree2": run2 is not None and run2.cause_reported == run1.cause_reported,
                "agreeB1": base.cause_reported == run1.cause_reported})
    for d in out:
        d["score"] = 0 if d["reasons"] else 1 + 2 * int(d["agree2"]) + int(d["agreeB1"])
        d["accepted"] = not d["reasons"] and d["agree2"]
    return out
