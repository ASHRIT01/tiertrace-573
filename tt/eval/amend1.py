"""Amendment 1 (tag amendment-1): a wrapper around the FROZEN scorer. No frozen file is edited; this module patches names at run time.

Rules (written before any Test-A model output existed; see docs/AMENDMENT_1.md):
  a) a gold event that carries a date text but yields no ISO date span is EXCLUDED from event scoring for every system (agent, B0, B1, B2);
  b) in a filing with such an excluded gold event, a predicted event of the SAME type that is not right (frozen classes wrong:extra / wrong:type)
     is IGNORED (dropped from the item list); a prediction whose own date is unparseable (wrong:date_unparsed) is handled as in the frozen scorer;
  c) counts of excluded gold events and ignored predictions are reported per split (`report`); if more than 2% of events are affected, the two
     bounding runs are added to the exploratory results: `bound_errors` (unmatched predictions counted as errors = rule b off) and `bound_drop`
     (every filing with an excluded gold event dropped).
Crash-only change: tt.labels.dates.parse_span (frozen) raises on year-less fuzzy dates and on invalid calendar dates; here it returns None in
those two cases (what it already returns for other dates it cannot parse). It never changes a value that did not crash.
Undated gold events (no date text; date_inferred by the labelling rule) are NOT "excluded" for rule b: they are handled exactly as the frozen
scorer handles them (skipped as gold, not a trigger for ignoring predictions).

Environment switches (all optional):
  TT_AMEND_MODE            amend (default) | bound_errors | bound_drop
  TT_AMEND_CONTESTED_MISS  1 = sensitivity (a): predicted claims attached to a CONTESTED gold item count as errors
  TT_AMEND_DROP_FILES      path of a JSON list of file names (or campaign ids) to drop = sensitivity (b), filings with isolation slips

Usage: python -m tt.eval.amend1 {phase3|phase4|endpoints} out.json   (same environment as the frozen modules)
       python -m tt.eval.amend1 report out.json                        (rule c counts; needs TT_PDF/TT_GOLD/TT_CACHE/TT_RUN1 [TT_B2])"""
import copy
import json
import os
import re
import runpy
import sys
from collections import Counter

import tt.labels.dates as _dates

_ORIG_PARSE = _dates.parse_span


def safe_parse_span(*a, **k):
    """Crash-only guard around the frozen parse_span: AttributeError (year-less fuzzy date) and ValueError (invalid calendar date) -> None."""
    try:
        return _ORIG_PARSE(*a, **k)
    except (AttributeError, ValueError):
        return None


def _patch_parse_span():
    _dates.parse_span = safe_parse_span
    for m in list(sys.modules.values()):
        if getattr(m, "parse_span", None) is _ORIG_PARSE:
            m.parse_span = safe_parse_span


_patch_parse_span()

from tt.eval import diagnose as D                      # noqa: E402  (must come after the patch)
from tt.eval import phase3 as P3                       # noqa: E402
from tt.eval.devscore import SUPPLIER_ROLES            # noqa: E402
from tt.kind import load_groups                        # noqa: E402
from tt.labels import protocol as _protocol            # noqa: E402

_FROZEN_PREPARE_GOLD = _protocol.prepare_gold
_FROZEN_EVENT_CLASS = D.event_class


def mode() -> str:
    m = os.environ.get("TT_AMEND_MODE", "amend")
    if m not in ("amend", "bound_errors", "bound_drop"):
        raise ValueError(f"TT_AMEND_MODE={m!r}")
    return m


def _drop_set() -> set:
    p = os.environ.get("TT_AMEND_DROP_FILES")
    if not p:
        return set()
    return {re.sub(r"^RCLRPT-|\.(pdf|PDF)$", "", x) for x in json.load(open(p))}


def _key(file: str) -> str:
    return re.sub(r"^RCLRPT-|\.(pdf|PDF)$", "", file)


# ---- gold preparation -------------------------------------------------------------------------------------------------------
def prepare_gold(records: list[dict], pdf_dir) -> list[dict]:
    """Frozen prepare_gold (run with the guarded parse_span) + bookkeeping: `amend1_excluded_gold` = non-contested events that carry a date text
    but have no usable ISO span; `amend1_contested_events` = contested events with their span when parseable (for sensitivity (a) only)."""
    out = _FROZEN_PREPARE_GOLD(records, pdf_dir)
    ctx = _protocol.context([r["file"] for r in records], pdf_dir)
    for src, r in zip(records, out):
        assert src["file"] == r["file"]
        years, fd = ctx[r["file"]]
        excl = [{"type": e["type"], "date_text": e["date_text"]} for e in r["events"] if _is_excluded(e)]
        cont = []
        for e in src["events"]:
            if e.get("contested"):
                sp = e.get("span") if e.get("span") else None
                if sp is None and e.get("date_text") and not e.get("date_inferred"):
                    p = safe_parse_span(e["date_text"], years=years, filing=fd)
                    if p is not None and not p.inferred:
                        sp = {"start": p.start.isoformat(), "end": p.end.isoformat(), "granularity": p.granularity}
                cont.append({"type": e["type"], "span": sp})
        r["amend1_excluded_gold"] = excl
        r["amend1_contested_events"] = cont
    return out


def exclude_def() -> str:
    d = os.environ.get("TT_AMEND_EXCLUDE_DEF", "nospan")
    if d not in ("nospan", "inferred_too"):
        raise ValueError(f"TT_AMEND_EXCLUDE_DEF={d!r}")
    return d


def _is_excluded(e: dict) -> bool:
    """Which gold events count as 'date cannot be parsed to an ISO date' (rule a), for rules a and b.
    nospan       : the event carries a date text and no ISO span exists for it (parse_span gave nothing usable).
    inferred_too : additionally the events the labelling flagged date_inferred although a (inferred) span exists (e.g. dev '11-13-').
    Undated events (no date text) are never 'excluded' here; the frozen scorer skips them as before."""
    if not (e.get("date_text") or "").strip():
        return False
    if exclude_def() == "inferred_too":
        return bool(e.get("date_inferred")) or not e.get("span")
    return not e.get("span")


# ---- event classes (rule b) -----------------------------------------------------------------------------------------------
def event_class(e, l, doc, years):
    c = _FROZEN_EVENT_CLASS(e, l, doc, years)
    if mode() == "amend" and c in ("wrong:extra", "wrong:type") and any(g["type"] == e.type for g in l.get("amend1_excluded_gold", [])):
        return "ignored"
    return c


def _contested_claims(l) -> set:
    return {c["claim"] for c in l.get("contested", [])}


def _overlaps_contested(e, l, doc, years) -> bool:
    from datetime import date
    from tt.labels.dates import Span, coarse_overlap
    sp = D.pred_span(e, doc.filing_date, years)
    if sp is None:
        return False
    for g in l.get("amend1_contested_events", []):
        s = g.get("span")
        if g["type"] == e.type and s and s["granularity"] != "fuzzy" and coarse_overlap(Span(date.fromisoformat(s["start"]), date.fromisoformat(s["end"]), s["granularity"]), sp):
            return True
    return False


def items_for(gold, docs, preds, score_fn=None, _stats=None):
    """phase3.items_for with the amendment: dropped filings (bound_drop, sensitivity b), ignored predictions (rule b), contested-as-miss (sensitivity a).
    With no excluded gold events and no switches it returns exactly what the frozen function returns."""
    groups = load_groups()
    drop = _drop_set()
    cmiss = os.environ.get("TT_AMEND_CONTESTED_MISS") == "1"
    res = {"S2": [], "E": [], "C": []}; unl = 0
    for l in gold:
        f = l["file"]
        if _key(f) in drop or (mode() == "bound_drop" and l.get("amend1_excluded_gold")):
            if _stats is not None:
                _stats["filings_dropped"] += 1
            continue
        ex = preds[f]; doc = docs[f]; years = D.years_of(ex); cl = doc.filer.lower().strip()
        cc = _contested_claims(l) if cmiss else set()
        for c in ex.companies:
            if c.role in SUPPLIER_ROLES and c.status == "SUPPORTED":
                k = D.company_class(c, l, doc, groups)
                if "S2" in cc:
                    k = "wrong"
                if k == "unlabelled":
                    unl += 1; continue
                res["S2"].append((k == "right", score_fn("S2", ex, c, f) if score_fn else 0, cl))
        for e in ex.events:
            k = D.event_class(e, l, doc, years)
            if k == "ignored":
                if _stats is not None:
                    _stats["ignored_predictions"] += 1
                continue
            ok = k == "right"
            if ok and cmiss and _overlaps_contested(e, l, doc, years):
                ok = False
            res["E"].append((ok, score_fn("E", ex, e, f) if score_fn else 0, cl))
        okc = ex.cause_reported == (l["cause"]["status"] == "SUPPORTED")
        if "C" in cc:
            okc = False
        res["C"].append((okc, score_fn("C", ex, None, f) if score_fn else 0, cl))
    return res, unl


def install():
    """Patch the frozen modules (by name, at run time). Idempotent."""
    _protocol.prepare_gold = prepare_gold
    D.prepare_gold = prepare_gold
    D.event_class = event_class
    P3.items_for = items_for
    for name in ("tt.eval.phase4", "tt.eval.endpoints"):
        m = sys.modules.get(name)
        if m is not None and hasattr(m, "items_for"):
            m.items_for = items_for


# ---- rule c: counts ---------------------------------------------------------------------------------------------------------
def report():
    gold, docs, raw, blocks = D.load_world()
    preds = P3.predictions(gold, docs, blocks)
    from tt.agent.schemas import Extraction
    run1 = D.load_preds(os.environ.get("TT_RUN1", "runs/dev_bench_4b_silver_v2.jsonl"))
    preds["agent_run1"] = {f: Extraction.model_validate(p["extraction"]) for f, p in run1.items() if p.get("extraction")}
    n_gold = sum(len(l["events"]) for l in gold)
    n_dated = sum(1 for l in gold for e in l["events"] if (e.get("date_text") or "").strip())
    excl = [(l["file"], g) for l in gold for g in l.get("amend1_excluded_gold", [])]
    R = {"filings": len(gold), "gold_events_noncontested": n_gold, "gold_events_with_date_text": n_dated,
         "gold_contested_events_dropped_by_frozen_prepare": sum(len(l.get("amend1_contested_events", [])) for l in gold),
         "excluded_gold_events": len(excl), "excluded_gold_share_of_events": len(excl) / n_gold if n_gold else None,
         "excluded_gold_share_of_dated_events": len(excl) / n_dated if n_dated else None,
         "filings_with_excluded_gold": len({f for f, _ in excl}), "excluded_gold_list": [{"file": f, **g} for f, g in excl], "systems": {}}
    trig = (R["excluded_gold_share_of_events"] or 0) > 0.02 or (R["excluded_gold_share_of_dated_events"] or 0) > 0.02
    for name, ex in preds.items():
        st = Counter()
        items_for(gold, docs, ex, _stats=st)
        total = sum(len(x.events) for f, x in ex.items())
        R["systems"][name] = {"predicted_events": total, "ignored_predictions": st["ignored_predictions"],
                              "ignored_share": st["ignored_predictions"] / total if total else None}
        trig = trig or (total and st["ignored_predictions"] / total > 0.02)
    R["bounding_runs_required"] = bool(trig)
    R["bounding_runs"] = ["TT_AMEND_MODE=bound_errors (unmatched predictions counted as errors)", "TT_AMEND_MODE=bound_drop (all affected filings dropped)"]
    return R


def main(argv):
    install()
    if argv[0] == "report":
        R = report(); json.dump(R, open(argv[1], "w"), indent=1)
        print(json.dumps({k: v for k, v in R.items() if k != "excluded_gold_list"}, indent=1))
        return
    if argv[0] == "phase3":   # runpy would re-execute phase3 with its own (unpatched) items_for; call the patched module instead
        R = P3.run(); json.dump(R, open(argv[1], "w"), indent=1)
        for name, r in R.items():
            for t in ("S2", "E", "C"):
                s = r[t]; f = lambda x: f"{x[0]:.3f} [{x[1]:.3f},{x[2]:.3f}]"
                print(name, t, "n=", s["n"], "error", f(s["error"]) if s["n"] else "n/a", "AURC", f(s["AURC"]) if s["n"] else "n/a")
        return
    mod = {"phase4": "tt.eval.phase4", "endpoints": "tt.eval.endpoints"}[argv[0]]
    sys.argv = [mod, *argv[1:]]
    runpy.run_module(mod, run_name="__main__")


if __name__ == "__main__":
    main(sys.argv[1:])
