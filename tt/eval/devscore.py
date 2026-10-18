"""Score model predictions against the dev label DRAFTS (AI-drafted, not human-verified: not gold).
Predictions: JSONL, one per filing: {"file": ..., "extraction": <Extraction dict> | null, "seconds": float}.
Metrics: JSON validity; verifier pass rate; S2 recovery (supplier named in the narrative WITH a located quote) among filings whose
draft S2 is SUPPORTED; unsupported-claim rate (a supplier asserted with status SUPPORTED where the draft S2 is not SUPPORTED); event date
precision/recall/F1; cause-reported accuracy.

EVENT MATCHING (Phase 0 rules d, e): every event has a normalised date span (tt.labels.dates.parse_span). A predicted event matches a gold
event if the types are equal and the two date spans overlap after widening both to the coarser granularity (day < month < quarter < year;
ranges kept as is). Each gold event is matched at most once (greedy, gold in order). Gold events with date_inferred=True are not scored.
HEADLINE event metric: the five types FILER_AWARENESS, INVESTIGATION_START, DECISION, SUPPLIER_NOTICE, NHTSA_FILING. OTHER is reported
separately. Fuzzy dates ('mid-2017') are scored separately (recall only). Quote spans and date wording are NOT compared."""
import json
from datetime import date
from pathlib import Path

from pydantic import ValidationError

from tt.agent.schemas import Extraction
from tt.labeldraft import load
from tt.norm.aliases import AliasTable, squash
from tt.parse.sections import Doc, norm
from tt.verify.dates import parse_date
from tt.labels.dates import parse_span, coarse_overlap
from tt.verify.verifier import verify

HEADLINE = {"FILER_AWARENESS", "INVESTIGATION_START", "DECISION", "SUPPLIER_NOTICE", "NHTSA_FILING"}
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
             cause_n=0, cause_ok=0, H_tp=0, H_pred=0, H_gold=0, O_tp=0, O_pred=0, O_gold=0, F_tp=0, F_gold=0)
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
            for k, v in _gold_counts(L).items():
                m[k] += v
            m["cause_n"] += 1
            continue
        m["verifier_pass"] += not verify(ex, doc, aliases)
        asserted = [c for c in ex.companies if c.role in SUPPLIER_ROLES and c.status == "SUPPORTED"]
        if st == "SUPPORTED":
            m["s2_gold_supported"] += 1
            m["s2_recovered"] += any(_same(c.name, name) and norm(c.evidence.quote) in norm(doc.sections.get(c.evidence.section, "")) for c in asserted)
        else:
            m["s2_not_supported_gold"] += 1
            m["s2_unsupported_claims"] += bool(asserted)
        for k, v in match_events(L, [(e.date_text, e.type) for e in ex.events], doc.filing_date).items():
            m[k] += v
        truth_reported = L["cause"]["status"] == "SUPPORTED"
        m["cause_n"] += 1; m["cause_ok"] += ex.cause_reported == truth_reported
    r = lambda a, b: a / b if b else float("nan")
    def prf(tp, pr, go):
        p_, r_ = r(tp, pr), r(tp, go)
        return p_, r_, (2 * p_ * r_ / (p_ + r_) if p_ == p_ and r_ == r_ and (p_ + r_) else float("nan"))
    hp, hr, hf = prf(m["H_tp"], m["H_pred"], m["H_gold"]); op, orr, of = prf(m["O_tp"], m["O_pred"], m["O_gold"])
    return {**m, "json_valid_rate": r(m["valid"], m["n"]), "verifier_pass_rate": r(m["verifier_pass"], m["n"]),
            "s2_recovery": r(m["s2_recovered"], m["s2_gold_supported"]), "unsupported_claim_rate": r(m["s2_unsupported_claims"], m["s2_not_supported_gold"]),
            "event_precision": hp, "event_recall": hr, "event_f1": hf,                       # headline: 5 types
            "event_other_precision": op, "event_other_recall": orr, "event_other_f1": of,
            "event_fuzzy_recall": r(m["F_tp"], m["F_gold"]),
            "cause_accuracy": r(m["cause_ok"], m["cause_n"])}


def _gold_spans(L: dict):
    """[(Span, type)] for gold events that are scored (not date_inferred); fuzzy kept (scored separately)."""
    from tt.labels.dates import Span
    from datetime import date as _d
    out = []
    for e in L.get("events", []):
        sp = e.get("span")
        if e.get("date_inferred") or not sp:
            continue
        out.append((Span(_d.fromisoformat(sp["start"]), _d.fromisoformat(sp["end"]), sp["granularity"]), e["type"]))
    return out


def _gold_counts(L: dict) -> dict:
    g = _gold_spans(L)
    return {"H_gold": sum(1 for s, t in g if t in HEADLINE and s.granularity != "fuzzy"),
            "O_gold": sum(1 for s, t in g if t == "OTHER" and s.granularity != "fuzzy"),
            "F_gold": sum(1 for s, t in g if s.granularity == "fuzzy")}


def match_events(L: dict, pred: list[tuple[str, str]], filing) -> dict:
    """pred = [(date_text, type)]. Returns TP/pred/gold counts for headline (H), OTHER (O) and fuzzy (F)."""
    gold = _gold_spans(L)
    full_years = set()
    parsed = []
    for dt, t in pred:
        sp = parse_span(dt or "")
        if sp and not sp.inferred and not sp.year_from_context and sp.granularity != "range":
            full_years.add(sp.start.year)
    for dt, t in pred:
        sp = parse_span(dt or "", years=full_years or None, filing=filing)
        if sp and not sp.inferred:
            parsed.append((sp, t))
    used = set()
    res = _gold_counts(L)
    res.update({"H_tp": 0, "O_tp": 0, "F_tp": 0,
                "H_pred": sum(1 for s, t in parsed if t in HEADLINE and s.granularity != "fuzzy"),
                "O_pred": sum(1 for s, t in parsed if t == "OTHER" and s.granularity != "fuzzy")})
    for gs, gt in gold:
        for j, (ps, pt) in enumerate(parsed):
            if j in used or pt != gt or not coarse_overlap(gs, ps):
                continue
            used.add(j)
            key = "F_tp" if gs.granularity == "fuzzy" else ("H_tp" if gt in HEADLINE else "O_tp")
            res[key] += 1
            if key == "F_tp" and ps.granularity != "fuzzy":   # a prediction spent on a fuzzy gold is not a headline/OTHER false positive
                res["H_pred" if pt in HEADLINE else "O_pred"] -= 1
            break
    return res
