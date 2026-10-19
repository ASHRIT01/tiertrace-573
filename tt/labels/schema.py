"""Schema and code checks for silver label records (Phase 1, step 3).

Checks (each failure is reported, never silently fixed):
  Q1 every quote appears verbatim (whitespace-normalised) in its named section (block, cause, chronology);
  Q2 an own-date event's date text is inside its quote; an inherited-date event's date text is inside its entry_quote, which is
     located in the chronology at or before the event's quote;
  Q3 the record is schema-valid (statuses/types from the fixed lists, quotes <= 300 characters);
  Q4 no claim without a quote, except NOT_REPORTED (S1, S2, C), INSUFFICIENT S2 where the block has no name line, NONE_MENTIONED
     and NOT_REPORTED (U). Events always need a quote."""
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field, ValidationError

from tt.labeldraft import load
from tt.parse.sections import norm

Status = Literal["SUPPORTED", "INSUFFICIENT", "NOT_REPORTED", "CONTRADICTED"]
Kind = Literal["NAMED", "UNNAMED", "NONE_MENTIONED", "NOT_REPORTED"]
EType = Literal["SUPPLIER_NOTICE", "FILER_AWARENESS", "INVESTIGATION_START", "DECISION", "NHTSA_FILING", "OTHER"]
Section = Literal["block", "cause", "chronology", "any"]


class Claim(BaseModel):
    id: Literal["S1", "S2"]
    status: Status
    quote: str = Field(default="", max_length=300)
    section: Section = "any"


class Cause(BaseModel):
    status: Status
    quote: str = Field(default="", max_length=300)
    section: Section = "cause"


class Upstream(BaseModel):
    kind: Kind
    names: list[str] = []
    quote: str = Field(default="", max_length=300)
    section: Section = "any"


class Ev(BaseModel):
    date_text: str
    type: EType
    quote: str = Field(min_length=1, max_length=300)
    inherited_date: bool = False
    entry_quote: Optional[str] = None
    date_inferred: bool = False


class Record(BaseModel):
    file: str
    claims: list[Claim] = Field(min_length=2, max_length=2)
    cause: Cause
    upstream: Upstream
    events: list[Ev]


def _found(quote: str, section: str, d: dict) -> bool:
    body = d["clean"] if section == "any" else d["sections"].get(section, "")
    return norm(quote) in norm(body)


def check(records: list[dict], pdf_dir: Path) -> list[tuple[str, str, str]]:
    """-> [(file, check id, detail)] for every failure."""
    fails = []
    for r in records:
        f = r.get("file", "?")
        try:
            Record.model_validate(r)
        except ValidationError as e:
            fails.append((f, "Q3", str(e).splitlines()[0][:160]))
        d = load(pdf_dir / f)
        chron = norm(d["sections"].get("chronology", ""))
        claims = [(c["id"], c.get("status"), c.get("quote", ""), c.get("section", "any")) for c in r.get("claims", [])]
        claims += [("C", r["cause"].get("status"), r["cause"].get("quote", ""), r["cause"].get("section", "cause")),
                   ("U", r["upstream"].get("kind"), r["upstream"].get("quote", ""), r["upstream"].get("section", "any"))]
        for cid, st, q, sec in claims:
            if q and not _found(q, sec, d):
                fails.append((f, "Q1", f"{cid} quote not in {sec}: {q[:60]!r}"))
            allowed_empty = st in ("NOT_REPORTED", "NONE_MENTIONED") or (cid == "S2" and st == "INSUFFICIENT" and not d["block"].name)
            if not q and not allowed_empty:
                fails.append((f, "Q4", f"{cid} {st} without a quote"))
        for i, e in enumerate(r.get("events", []), 1):
            q = e.get("quote", "")
            if not q or norm(q) not in chron:
                fails.append((f, "Q1", f"E{i} quote not in chronology: {q[:60]!r}"))
            if e.get("date_inferred") and not e.get("date_text"):
                continue
            if e.get("inherited_date"):
                eq = e.get("entry_quote") or ""
                pe, pq = chron.find(norm(eq)), chron.find(norm(q))
                if not (eq and norm(e["date_text"]) in norm(eq) and 0 <= pe <= pq):
                    fails.append((f, "Q2", f"E{i} inherited date not in an earlier entry sentence: {e['date_text']!r}"))
            elif norm(e.get("date_text", "")) not in norm(q):
                fails.append((f, "Q2", f"E{i} date text not inside quote: {e.get('date_text')!r}"))
    return fails
