"""TS-1 timeliness screen: unit tests (protocol ts-protocol-1, sections B, D, E, F, H). Pure Python, no data files except the holiday CSV."""
import csv
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ts_lib import (anchor, cites_other_recall, flag, holiday_rows, kappa_pabak, quantile, resolve, wd_between, wilson)  # noqa: E402

HOL = {date.fromisoformat(r["observed"]) for r in holiday_rows()}


# ---- B. holidays
def test_known_observed_dates():
    for d in ["2021-12-31", "2021-06-18", "2020-07-03", "2022-12-26", "2023-11-10"]:
        assert date.fromisoformat(d) in HOL, d


def test_juneteenth_only_from_2021():
    assert date(2020, 6, 19) not in HOL and date(2021, 6, 18) in HOL and date(2024, 6, 19) in HOL


def test_actual_weekend_dates_are_not_listed():
    assert date(2022, 1, 1) not in HOL and date(2020, 7, 4) not in HOL and date(2022, 12, 25) not in HOL


def test_csv_matches_code():
    p = Path(__file__).resolve().parents[1] / "data/holidays_us_federal.csv"
    with open(p) as f:
        assert {date.fromisoformat(r["observed"]) for r in csv.DictReader(f)} == HOL


# ---- F. working days and flag
def test_same_day_is_zero():
    assert wd_between(date(2023, 3, 8), date(2023, 3, 8), HOL) == 0


def test_monday_to_next_monday_is_five():
    assert wd_between(date(2023, 3, 6), date(2023, 3, 13), HOL) == 5


def test_friday_to_next_monday_is_one():
    assert wd_between(date(2023, 3, 10), date(2023, 3, 13), HOL) == 1


def test_saturday_decision():
    assert wd_between(date(2023, 3, 11), date(2023, 3, 13), HOL) == 1
    assert wd_between(date(2023, 3, 11), date(2023, 3, 17), HOL) == 5


def test_span_over_observed_holiday():
    assert wd_between(date(2020, 7, 2), date(2020, 7, 6), HOL) == 1          # Fri 2020-07-03 observed Independence Day
    assert wd_between(date(2020, 7, 2), date(2020, 7, 6), set()) == 2        # holidays not excluded


def test_calendar_days_variant():
    assert wd_between(date(2023, 3, 10), date(2023, 3, 13), set(), weekends=False) == 3


def test_flag_rule():
    assert flag(6, 9) == "FLAGGED" and flag(0, 5) == "NOT_FLAGGED" and flag(5, 6) == "INDETERMINATE" and flag(5, 5) == "NOT_FLAGGED"


def test_month_interval_gives_indeterminate():
    filing = date(2023, 3, 15)
    iv = resolve("March 2023", filing, {2023})
    assert (iv.lo, iv.hi, iv.capped) == (date(2023, 3, 1), filing, True)
    gmin, gmax = wd_between(iv.hi, filing, HOL), wd_between(iv.lo, filing, HOL)
    assert (gmin, gmax) == (0, 10) and flag(gmin, gmax) == "INDETERMINATE"


# ---- D. intervals
def test_day_and_iso():
    f = date(2024, 1, 1)
    assert resolve("On or about March 5, 2023", f, set()).lo == date(2023, 3, 5)
    assert resolve("2023-02-02", f, set()).precision == "day"
    assert resolve("20. Jan 2023", f, set()).lo == date(2023, 1, 20)


def test_week_month_quarter_year_parts():
    f = date(2024, 1, 1)
    w = resolve("CW51/2022", f, set()); assert (w.lo, w.hi, w.precision) == (date(2022, 12, 19), date(2022, 12, 23), "iso_week")
    q = resolve("Q1 2023", f, set()); assert (q.lo, q.hi) == (date(2023, 1, 1), date(2023, 3, 31))
    m = resolve("mid-March 2023", f, set()); assert (m.lo, m.hi) == (date(2023, 3, 11), date(2023, 3, 20))
    e = resolve("end of February 2023", f, set()); assert (e.lo, e.hi) == (date(2023, 2, 21), date(2023, 2, 28))
    y = resolve("early 2023", f, set()); assert (y.lo, y.hi) == (date(2023, 1, 1), date(2023, 4, 30))


def test_ambiguous_numeric_both_before_filing_is_union():
    iv = resolve("03/04/2023", date(2023, 6, 30), set())
    assert (iv.lo, iv.hi, iv.ambiguous) == (date(2023, 3, 4), date(2023, 4, 3), True)


def test_ambiguous_numeric_one_reading_after_filing_is_dropped():
    iv = resolve("09/12/2025", date(2025, 9, 20), set())          # 12 Sep kept, 9 Dec is after the filing date
    assert (iv.lo, iv.hi, iv.ambiguous) == (date(2025, 9, 12), date(2025, 9, 12), False)


def test_unambiguous_numeric():
    assert resolve("13/04/2023", date(2023, 6, 30), set()).lo == date(2023, 4, 13)
    assert resolve("04/13/2023", date(2023, 6, 30), set()).lo == date(2023, 4, 13)


def test_yearless_rule():
    f = date(2023, 6, 30)
    assert resolve("May 16", f, {2023}).lo == date(2023, 5, 16)
    assert resolve("May 16", f, set()).lo == date(2023, 5, 16)          # no dated events: filing year, not after filing
    assert resolve("July 16", f, set()) is None                         # would be after the filing date
    assert resolve("May 16", f, {2022, 2023}) is None                   # several context years: unresolved


def test_range_and_cap():
    f = date(2023, 1, 15)
    r = resolve("September 2022, through January 2023", f, set())
    assert (r.lo, r.hi, r.capped, r.precision) == (date(2022, 9, 1), f, True, "range")
    assert resolve("December - January 2023", date(2023, 6, 1), set()).lo == date(2022, 12, 1)


def test_unparsed_is_none():
    assert resolve("During the course of the investigation", date(2023, 1, 1), set()) is None


# ---- E. anchor
def test_anchor_latest_decision_and_other_recall_rule():
    f = date(2023, 3, 20)
    ev = [{"date_text": "March 1, 2023", "type": "DECISION", "quote": "decided to recall"},
          {"date_text": "March 10, 2023", "type": "DECISION", "quote": "in recall 22V-123 the committee decided"},
          {"date_text": "March 8, 2023", "type": "DECISION", "quote": "decided to recall (23V100)"},
          {"date_text": "March 30, 2023", "type": "DECISION", "quote": "after the filing"},
          {"date_text": "March 15, 2023", "type": "OTHER", "quote": "other"}]
    iv, n = anchor(ev, f, "23V100", set())
    assert iv.lo == date(2023, 3, 8) and n == 2
    assert anchor(ev, f, "23V100", set(), mode="earliest_decision")[0].lo == date(2023, 3, 1)
    assert anchor(ev, f, "23V100", set(), mode="latest_any")[0].lo == date(2023, 3, 15)
    assert anchor(ev, f, "23V100", set(), mode="latest_lexicon")[0].lo == date(2023, 3, 8)


def test_no_decision_date():
    assert anchor([{"date_text": "", "type": "DECISION", "quote": "x"}], date(2023, 1, 1), "23V100", set()) == (None, 0)


def test_cites_other_recall():
    assert cites_other_recall("see 22V-123", "23V100") and not cites_other_recall("our 23V-100", "23V100") and not cites_other_recall("", "23V100")


# ---- H. statistics
def test_wilson_and_quantile():
    lo, hi = wilson(5, 10); assert abs(lo - 0.2366) < 1e-3 and abs(hi - 0.7634) < 1e-3
    assert quantile([1, 2, 3, 4], 0.5) == 2.5 and quantile([7], 0.9) == 7


def test_kappa_pabak():
    pairs = [("FLAGGED", "FLAGGED")] * 4 + [("NOT_FLAGGED", "NOT_FLAGGED")] * 4 + [("FLAGGED", "NOT_FLAGGED")] * 2
    k, p = kappa_pabak(pairs)
    assert abs(k - 0.32 / 0.52) < 1e-9 and abs(p - 0.7) < 1e-9        # p_o 0.8, p_e 0.6*0.4 + 0.4*0.6 = 0.48; PABAK (3*0.8 - 1)/2
