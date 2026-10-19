from datetime import date

from tt.agent.schemas import Extraction
from tt.baselines.rules import b1
from tt.eval.diagnose import qfound, qnorm
from tt.verify.extra import date_errors
from tt.parse.sections import Doc


def test_qfound_principled():
    text = "The supplier’s part was\nmanufac-\nturing late – see 5/3/2020."
    assert qfound("supplier's part was manufacturing late - see 5/3/2020.", text)
    assert not qfound("SUPPLIER'S PART", text)          # case-sensitive
    assert qnorm("a“b”", False) == 'a"b"'


def test_extra_dates_accept_ranges_and_yearless():
    doc = Doc("C", "F", date(2020, 6, 1), "", {})
    ex = Extraction.model_validate({"companies": [], "supply_path": [], "locus": "UNDETERMINED", "locus_status": "NOT_REPORTED", "events": [
        {"date_text": "April to May 2019", "type": "OTHER", "status": "SUPPORTED", "evidence": {"section": "chronology", "quote": "x"}},
        {"date_text": "banana", "type": "OTHER", "status": "SUPPORTED", "evidence": {"section": "chronology", "quote": "x"}}], "cause_reported": True})
    errs = date_errors(ex, doc)
    assert len(errs) == 1 and "banana" in errs[0]


def test_b1_validates_as_extraction():
    ex = b1("The weld failed.", "On 5/3/2020, Acme Corp. notified Zed Inc. of the problem. NHTSA was told on June 1, 2020.", "Zed Inc.")
    Extraction.model_validate(ex)
    assert [e["date_text"] for e in ex["events"]] == ["5/3/2020", "June 1, 2020"] and ex["cause_reported"] is True
