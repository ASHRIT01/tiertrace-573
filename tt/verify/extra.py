"""Verification layer on top of tt/verify/verifier.py (which is NOT edited). Two changes, both motivated by the Phase 2 diagnosis:
 1. quotes are checked against the SAME masked text the model saw (the model copies the mask token into quotes);
 2. V2 'filer listed as a supplier' is not raised for a company that is the manufacturer-reported block supplier (the block, not
    the model, says the filer or an affiliate made the part)."""
from dataclasses import replace

from tt.parse.block import mask_text
from tt.parse.sections import Doc, norm
from tt.labels.dates import parse_span
from tt.verify.verifier import EARLIEST, verify


def masked_doc(doc: Doc, block_name: str | None) -> Doc:
    if not block_name:
        return doc
    return replace(doc, sections={k: mask_text(v, block_name) for k, v in doc.sections.items()})


def date_errors(ex, doc: Doc) -> list[str]:
    """V3 with the span parser: ranges, month-only and year-less dates are valid dates; unparseable only if parse_span gives nothing."""
    years = {sp.start.year for sp in (parse_span(e.date_text or "") for e in ex.events) if sp and not sp.inferred and not sp.year_from_context and sp.granularity != "range"}
    errs = []
    for e in ex.events:
        sp = parse_span(e.date_text or "", years=years or None, filing=doc.filing_date)
        if sp is None or sp.inferred:
            errs.append(f"V3 unparseable date: {e.date_text}")
        elif sp.start < EARLIEST:
            errs.append(f"V3 date before 1990: {e.date_text}")
        elif sp.start > doc.filing_date:
            errs.append(f"V3 event after the filing date: {e.date_text}")
    return errs


def verify_masked(ex, doc: Doc, aliases, block_name: str | None) -> list[str]:
    base = verify(ex, masked_doc(doc, block_name), aliases)
    errs = [e for e in base if e != "V2 filer listed as a supplier" and not e.startswith(("V3 unparseable", "V3 date before", "V3 event after"))]
    filer, blk = norm(doc.filer), norm(block_name or "")
    errs += ["V2 filer listed as a supplier" for c in ex.companies if c.role != "FILER" and norm(c.name) == filer and norm(c.name) != blk]
    return errs + date_errors(ex, doc)
