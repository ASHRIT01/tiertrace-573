"""Score model predictions against the dev label DRAFTS (AI-drafted, not human-verified: not gold).
Predictions: JSONL, one per filing: {"file": ..., "extraction": <Extraction dict> | null, "seconds": float}.
Metrics: JSON validity; verifier pass rate; S2 recovery (supplier named in the narrative WITH a located quote) among filings whose
draft S2 is SUPPORTED; unsupported-claim rate (a supplier asserted with status SUPPORTED where the draft S2 is not SUPPORTED); event date
precision/recall/F1; cause-reported accuracy.

EVENT MATCHING: an event is the pair (ISO date, type). Gold and predicted events are compared as multisets of those pairs: a predicted event is a
true positive if a gold event has the same ISO date (after parse_date with the filing date as anchor) AND the same type; each gold event can be matched
once. The quote span and the wording of the date text are NOT compared. Events whose date does not parse (for example 'April through August 2016')
are left out of both sides. Month-only dates parse to the first of the month, so a month-only gold date and a day-level predicted date do not match."""
import json
from collections import Counter
from datetime import date
from pathlib import Path

from pydantic import ValidationError

from tt.agent.schemas import Extraction
from tt.labeldraft import load
from tt.norm.aliases import AliasTable, squash
from tt.parse.sections import Doc, norm
from tt.verify.dates import parse_date
from tt.verify.verifier import verify

SUPPLIER_ROLES = {"SUPPLIER", "SUB_SUPPLIER", "DISTRIBUTOR"}


def _same(a: str, b: str) -> bool:
    a, b = squash(a), squash(b)
    return bool(a and b and (a == b or a in b or b in a))


def gold_supplier(L: dict) -> tuple[str | None, str]:
    for c in L["claims"]:
        if c["id"] == "S2":
            name = c["label"].split(": ", 1)[1].split(" (")[0] if c["status"] == "SUPPORTED" else None
            return name, c["status"]
    return None, "NOT_REPORTED"


def _doc(L: dict, pdf_dir: Path) -> Doc:
    d = load(pdf_dir / L["file"])
    h = d["header"]
    return Doc(h["campaign"], h["filer"], h["filing_date"] or date(2100, 1, 1), d["clean"], d["sections"])


def score(labels: list[dict], preds: list[dict], pdf_dir: Path, aliases: AliasTable | None = None) -> dict:
    aliases = aliases or AliasTable()
    by = {p["file"]: p for p in preds}
    m = dict(n=len(labels), valid=0, verifier_pass=0, s2_gold_supported=0, s2_recovered=0, s2_not_supported_gold=0, s2_unsupported_claims=0,
             ev_tp=0, ev_pred=0, ev_gold=0, cause_n=0, cause_ok=0)
    for L in labels:
        p = by.get(L["file"])
        doc = _doc(L, pdf_dir)
        name, st = gold_supplier(L)
        ex = None
        if p and p.get("extraction") is not None:
            try:
                ex = Extraction.model_validate(p["extraction"])
            except ValidationError:
                ex = None
        m["valid"] += ex is not None
        if ex is None:  # invalid output counts against recovery, not as an unsupported claim
            m["s2_gold_supported"] += st == "SUPPORTED"
            m["s2_not_supported_gold"] += st != "SUPPORTED"
            m["ev_gold"] += sum(_gold_events(L, doc).values()); m["cause_n"] += 1
            continue
        m["verifier_pass"] += not verify(ex, doc, aliases)
        asserted = [c for c in ex.companies if c.role in SUPPLIER_ROLES and c.status == "SUPPORTED"]
        if st == "SUPPORTED":
            m["s2_gold_supported"] += 1
            m["s2_recovered"] += any(_same(c.name, name) and norm(c.evidence.quote) in norm(doc.sections.get(c.evidence.section, "")) for c in asserted)
        else:
            m["s2_not_supported_gold"] += 1
            m["s2_unsupported_claims"] += bool(asserted)
        g = _gold_events(L, doc)
        pr = Counter((d, e.type) for e in ex.events if (d := parse_date(e.date_text, doc.filing_date)))
        m["ev_gold"] += sum(g.values()); m["ev_pred"] += sum(pr.values()); m["ev_tp"] += sum((g & pr).values())
        truth_reported = L["cause"]["status"] == "SUPPORTED"
        m["cause_n"] += 1; m["cause_ok"] += ex.cause_reported == truth_reported
    r = lambda a, b: a / b if b else float("nan")
    p_, r_ = r(m["ev_tp"], m["ev_pred"]), r(m["ev_tp"], m["ev_gold"])
    return {**m, "json_valid_rate": r(m["valid"], m["n"]), "verifier_pass_rate": r(m["verifier_pass"], m["n"]),
            "s2_recovery": r(m["s2_recovered"], m["s2_gold_supported"]), "unsupported_claim_rate": r(m["s2_unsupported_claims"], m["s2_not_supported_gold"]),
            "event_precision": p_, "event_recall": r_, "event_f1": r(2 * p_ * r_, p_ + r_) if p_ == p_ and r_ == r_ else float("nan"),
            "cause_accuracy": r(m["cause_ok"], m["cause_n"])}


def _gold_events(L: dict, doc: Doc) -> Counter:
    """Multiset of (ISO date, type) over the gold events whose date text parses."""
    return Counter((d, e["type"]) for e in L.get("events", []) if (d := parse_date(e["date_text"], doc.filing_date)))
