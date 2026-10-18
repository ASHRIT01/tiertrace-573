"""Deterministic verifier (V1-V6). The model proposes; this code disposes.
All quotes are located in the canonical normalised text of their section."""
from datetime import date
from typing import Iterator

from tt.agent.schemas import Evidence, Extraction
from tt.norm.aliases import AliasTable
from tt.parse.sections import Doc, norm
from tt.verify.dates import parse_date

EARLIEST = date(1990, 1, 1)
EVENT_ORDER = ["SUPPLIER_NOTICE", "FILER_AWARENESS", "DECISION", "NHTSA_FILING"]


def locate(quote: str, text: str) -> tuple[int, int] | None:
    """Offsets into norm(text), or None. Exact match after whitespace normalisation."""
    q = norm(quote)
    if not q:
        return None
    i = norm(text).find(q)
    return None if i < 0 else (i, i + len(q))


def iter_evidence(ex: Extraction) -> Iterator[Evidence]:
    for c in ex.companies:
        yield c.evidence
    for e in ex.events:
        yield e.evidence
    if ex.locus_evidence:
        yield ex.locus_evidence


def verify(ex: Extraction, doc: Doc, aliases: AliasTable) -> list[str]:
    errs: list[str] = []
    # V1 quotes verbatim, in the claimed section
    for ev in iter_evidence(ex):
        if locate(ev.quote, doc.sections.get(ev.section, "")) is None:
            errs.append(f"V1 quote not in {ev.section}: {ev.quote[:40]!r}")
    # status rules: SUPPORTED needs a located quote (covered by V1); CONTRADICTED needs two
    if ex.locus_status == "SUPPORTED" and ex.locus_evidence is None:
        errs.append("V1 locus SUPPORTED without evidence")
    # V2 companies
    filer = norm(doc.filer)
    for c in ex.companies:
        if not (locate(c.name, doc.full_text) or aliases.resolve(c.name)):
            errs.append(f"V2 company not in text or alias table: {c.name}")
        if c.role != "FILER" and norm(c.name) == filer:
            errs.append("V2 filer listed as a supplier")
    # V3 dates
    dated: list[tuple[date, str]] = []
    for e in ex.events:
        d = parse_date(e.date_text, anchor=doc.filing_date)
        if d is None:
            errs.append(f"V3 unparseable date: {e.date_text}")
        elif d < EARLIEST:
            errs.append(f"V3 date before 1990: {e.date_text}")
        elif d > doc.filing_date:
            errs.append(f"V3 event after the filing date: {e.date_text}")
        else:
            dated.append((d, e.type))
    ranks = [(d, EVENT_ORDER.index(t)) for d, t in dated if t in EVENT_ORDER]
    for (d1, r1) in ranks:
        for (d2, r2) in ranks:
            if r1 < r2 and d1 > d2:
                errs.append("V3 event order inconsistent")
                break
        else:
            continue
        break
    # V4 NR must stay NR
    if doc.cause_is_nr and ex.cause_reported:
        errs.append("V4 cause reported although the source says NR")
    # V5 supply path: path members must be extracted companies or the filer
    known = {norm(c.name) for c in ex.companies} | {filer}
    for p in ex.supply_path:
        if norm(p) not in known:
            errs.append(f"V5 path member not among extracted companies: {p}")
    return errs
