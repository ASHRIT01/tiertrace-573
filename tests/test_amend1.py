"""Amendment 1: synthetic tests for the scorer wrapper (rules a and b) and the crash-only date guard. No PDFs, no models."""
import json
from datetime import date
from types import SimpleNamespace

import pytest

import tt.eval.amend1 as A
from tt.agent.schemas import Extraction
from tt.labels import protocol


def _ex(events, cause_reported=True):
    ev = [{"date_text": d, "type": t, "status": "SUPPORTED", "evidence": {"section": "chronology", "quote": "q"}} for d, t in events]
    return Extraction.model_validate({"companies": [], "supply_path": [], "locus": "UNDETERMINED", "locus_status": "NOT_REPORTED", "events": ev,
                                      "cause_reported": cause_reported})


def _rec(file, events, contested=None, cause="SUPPORTED"):
    return {"file": file, "events": events, "contested": contested or [], "claims": [{"id": "S1", "status": "NOT_REPORTED"}, {"id": "S2", "status": "NOT_REPORTED"}],
            "cause": {"status": cause}, "upstream": {"kind": "NONE_MENTIONED"}}


GOLD_EVENTS = [
    {"date_text": "March 3, 2023", "type": "DECISION", "quote": "q1"},                       # valid date -> scored
    {"date_text": "mid-April", "type": "OTHER", "quote": "q2"},                             # year-less fuzzy date: frozen parse_span raises AttributeError
    {"date_text": "September 31, 2023", "type": "INVESTIGATION_START", "quote": "q3"},      # invalid calendar date: frozen parse_span raises ValueError
    {"date_text": "", "type": "OTHER", "quote": "q4", "date_inferred": True},               # undated prose: frozen handling, NOT an excluded event
    {"date_text": "May 5, 2023", "type": "FILER_AWARENESS", "quote": "q5", "contested": True},
]


@pytest.fixture
def gold(monkeypatch):
    monkeypatch.setattr(protocol, "context", lambda files, pdf_dir: {f: (set(), date(2024, 1, 1)) for f in files})
    A.install()
    recs = [_rec("RCLRPT-T1.pdf", json.loads(json.dumps(GOLD_EVENTS)), contested=[{"item_id": "D001", "claim": "E"}]),
            _rec("RCLRPT-T2.pdf", [{"date_text": "March 3, 2023", "type": "DECISION", "quote": "q1"}])]
    return A.prepare_gold(recs, "unused")


def test_frozen_parse_span_really_crashes_and_the_guard_does_not():
    with pytest.raises(AttributeError):
        A._ORIG_PARSE("mid-April")
    with pytest.raises(ValueError):
        A._ORIG_PARSE("September 31, 2023")
    assert A.safe_parse_span("mid-April") is None
    assert A.safe_parse_span("September 31, 2023") is None
    sp = A.safe_parse_span("March 3, 2023")                 # a value that did not crash is untouched
    assert sp is not None and sp.start == date(2023, 3, 3)


def test_rule_a_gold_events_without_iso_date_are_excluded_and_nothing_crashes(gold):
    l = gold[0]
    assert [(g["type"], g["date_text"]) for g in l["amend1_excluded_gold"]] == [("OTHER", "mid-April"), ("INVESTIGATION_START", "September 31, 2023")]
    spans = {e["date_text"]: e.get("span") for e in l["events"]}
    assert spans["March 3, 2023"]["start"] == "2023-03-03" and spans["mid-April"] is None and spans["September 31, 2023"] is None
    assert len(l["events"]) == 4                              # contested event dropped by the frozen preparation
    assert l["amend1_contested_events"][0]["type"] == "FILER_AWARENESS"
    assert gold[1]["amend1_excluded_gold"] == []


def _docs(gold):
    return {l["file"]: SimpleNamespace(filer="Acme", filing_date=date(2024, 1, 1), full_text="") for l in gold}


def _items(gold, preds, **env):
    return A.items_for(gold, _docs(gold), preds)[0]


PRED_EVENTS = [("March 3, 2023", "DECISION"),            # right
               ("June 1, 2023", "OTHER"),                # unmatched, same type as an excluded gold event -> ignored (rule b)
               ("June 2, 2023", "INVESTIGATION_START"),  # unmatched, same type as the other excluded gold event -> ignored
               ("June 3, 2023", "NHTSA_FILING"),         # unmatched, type NOT among excluded types -> stays wrong
               ("somewhere in spring", "OTHER")]         # own date unparseable -> wrong:date_unparsed, as in the frozen scorer


def test_rule_b_ignores_unmatched_same_type_predictions_only(gold):
    preds = {"RCLRPT-T1.pdf": _ex(PRED_EVENTS), "RCLRPT-T2.pdf": _ex(PRED_EVENTS)}
    E = [x[0] for x in _items(gold, preds)["E"]]
    # T1: right, (ignored), (ignored), wrong NHTSA_FILING, wrong unparsed  -> 3 items ; T2 has no excluded gold: right + 4 wrong -> 5 items
    assert E == [True, False, False] + [True, False, False, False, False]


def test_bounding_modes_and_switches(gold, monkeypatch):
    preds = {"RCLRPT-T1.pdf": _ex(PRED_EVENTS), "RCLRPT-T2.pdf": _ex(PRED_EVENTS)}
    monkeypatch.setenv("TT_AMEND_MODE", "bound_errors")        # rule b off: unmatched predictions counted as errors
    assert len(_items(gold, preds)["E"]) == 10
    monkeypatch.setenv("TT_AMEND_MODE", "bound_drop")          # the affected filing is dropped
    assert len(_items(gold, preds)["E"]) == 5
    monkeypatch.setenv("TT_AMEND_MODE", "amend")
    monkeypatch.setenv("TT_AMEND_DROP_FILES", str(p_path := __import__("pathlib").Path(__file__).with_name("_drop_tmp.json")))
    p_path.write_text(json.dumps(["T2"]));
    try:
        assert len(_items(gold, preds)["E"]) == 3             # sensitivity (b): filing T2 dropped
    finally:
        p_path.unlink()


def test_contested_as_miss_sensitivity(gold, monkeypatch):
    c = [x[0] for x in _items(gold, {"RCLRPT-T1.pdf": _ex([("May 5, 2023", "FILER_AWARENESS")]), "RCLRPT-T2.pdf": _ex([])})["E"]]
    assert c == [False]                                       # frozen: contested gold dropped -> already an error
    # a prediction that is right on a scored gold event stays right unless it also overlaps a contested gold event of the same type
    gold[0]["events"].append({"date_text": "May 5, 2023", "type": "FILER_AWARENESS", "quote": "q", "span": {"start": "2023-05-05", "end": "2023-05-05", "granularity": "day"}})
    preds = {"RCLRPT-T1.pdf": _ex([("May 5, 2023", "FILER_AWARENESS")]), "RCLRPT-T2.pdf": _ex([])}
    assert [x[0] for x in _items(gold, preds)["E"]] == [True]
    monkeypatch.setenv("TT_AMEND_CONTESTED_MISS", "1")
    assert [x[0] for x in _items(gold, preds)["E"]] == [False]


def test_exclusion_definitions(monkeypatch):
    spanless = {"date_text": "x", "type": "OTHER"}
    inferred_with_span = {"date_text": "11-13-", "type": "OTHER", "date_inferred": True, "span": {"start": "2019-11-13", "end": "2019-11-13", "granularity": "day"}}
    undated = {"date_text": "", "type": "OTHER", "date_inferred": True}
    monkeypatch.setenv("TT_AMEND_EXCLUDE_DEF", "nospan")
    assert A._is_excluded(spanless) and not A._is_excluded(inferred_with_span) and not A._is_excluded(undated)
    monkeypatch.setenv("TT_AMEND_EXCLUDE_DEF", "inferred_too")
    assert A._is_excluded(spanless) and A._is_excluded(inferred_with_span) and not A._is_excluded(undated)


def test_leakcheck_skips_appledouble_files():
    import inspect
    import tt.leakcheck as L
    assert 'startswith("._")' in inspect.getsource(L)
