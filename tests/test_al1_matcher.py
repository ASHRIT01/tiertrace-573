"""AL-1 matcher, baselines and label draw: unit tests (protocol al1-protocol-1). Every version pair here is made up; no real filing text."""
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from al1_lib import (CLASSES, DATE_CORRECTION, NEW, NO_PREDICTION, QUOTAS, RETRACTED, THETA, TYPE_CHANGE, UNCHANGED, date_distance, draw_items,  # noqa: E402
                     match_versions, overlap, single_version_predict, textdiff_classify, textdiff_predict, tokens, weighted_agreement)

Q1 = "Acme Widgets received a field report describing a cracked bracket on a test sled"
Q2 = "The review board decided to recall the affected widget assemblies"
Q3 = "Engineers opened an analysis of the hinge coating samples"


def ev(q, t="OTHER", d=date(2024, 3, 10), hi=None):
    return {"quote": q, "type": t, "lo": d, "hi": hi or d}


def one(rows, cls):
    hit = [r for r in rows if r["cls"] == cls]
    assert len(hit) == 1
    return hit[0]


def read_date(s):
    y = {"March 10, 2024": date(2024, 3, 10), "March 15, 2024": date(2024, 3, 15), "June 1, 2024": date(2024, 6, 1)}.get(s)
    return (y, y) if y else None


# ---- tokens and overlap
def test_tokens_drop_dates_and_stop_words():
    assert tokens("On March 10, 2024 the Board met") == {"board", "met"}


def test_changed_date_inside_quote_does_not_lower_overlap():
    assert overlap("On March 10, 2024 the board reviewed bracket failures", "On April 2, 2024 the board reviewed bracket failures") == 1.0


def test_overlap_coefficient_handles_a_shorter_quote():
    assert overlap("board reviewed bracket failures yesterday morning", "board reviewed bracket") == 1.0


def test_short_quotes_match_only_when_identical():
    assert overlap("board met", "board met") == 1.0
    assert overlap("board met", "board met again today") == 0.0


def test_empty_quote_never_matches():
    assert overlap("", "") == 0.0
    assert overlap("the of", "the of") == 0.0


def test_date_distance():
    assert date_distance(ev("x"), ev("x")) == 0
    assert date_distance(ev("x", d=date(2024, 3, 1), hi=date(2024, 3, 31)), ev("x", d=date(2024, 3, 10))) == 0
    assert date_distance(ev("x", d=date(2024, 3, 10)), ev("x", d=date(2024, 3, 15))) == 5


# ---- the five classes
def test_unchanged():
    r = match_versions([ev(Q1)], [ev(Q1)], Q1, Q1)
    assert [x["cls"] for x in r] == [UNCHANGED] and not r[0]["text_carried"]


def test_new():
    r = one(match_versions([], [ev(Q2)], "", Q2), NEW)
    assert r["early"] is None and r["late"]["quote"] == Q2


def test_retracted():
    r = one(match_versions([ev(Q2)], [], Q2, ""), RETRACTED)
    assert r["late"] is None


def test_date_correction_within_window():
    r = one(match_versions([ev(Q1)], [ev(Q1, d=date(2024, 3, 30))], Q1, Q1), DATE_CORRECTION)
    assert not r["type_also_changed"]


def test_window_edge_30_days_is_in_and_31_is_out():
    assert match_versions([ev(Q1)], [ev(Q1, d=date(2024, 4, 9))], "", "")[0]["cls"] == DATE_CORRECTION
    assert {x["cls"] for x in match_versions([ev(Q1)], [ev(Q1, d=date(2024, 4, 10))], "", "")} == {RETRACTED, NEW}


def test_precision_refinement_is_a_date_correction():
    month = ev(Q1, d=date(2024, 3, 1), hi=date(2024, 3, 31))
    assert match_versions([month], [ev(Q1)], Q1, Q1)[0]["cls"] == DATE_CORRECTION


def test_type_change():
    assert match_versions([ev(Q1, "OTHER")], [ev(Q1, "DECISION")], Q1, Q1)[0]["cls"] == TYPE_CHANGE


def test_date_and_type_change_is_date_correction_with_a_flag():
    r = match_versions([ev(Q1, "OTHER")], [ev(Q1, "DECISION", d=date(2024, 3, 20))], Q1, Q1)[0]
    assert r["cls"] == DATE_CORRECTION and r["type_also_changed"]


def test_theta_edge():
    a, b = "alpha bravo charlie delta echo", "alpha bravo charlie xray yankee"
    assert overlap(a, b) == THETA
    assert match_versions([ev(a)], [ev(b)], "", "")[0]["cls"] == UNCHANGED
    assert {x["cls"] for x in match_versions([ev("alpha bravo oscar delta echo")], [ev("alpha bravo xray yankee zulu")], "", "")} == {RETRACTED, NEW}


# ---- extraction misses and one-to-one matching
def test_quote_still_in_later_text_is_carried_not_retracted():
    r = match_versions([ev(Q3)], [], Q3, "Intro. " + Q3.upper() + " More.")[0]
    assert r["cls"] == UNCHANGED and r["text_carried"]


def test_quote_already_in_earlier_text_is_carried_not_new():
    r = match_versions([], [ev(Q3)], Q3, Q3)[0]
    assert r["cls"] == UNCHANGED and r["text_carried"]


def test_far_date_blocks_the_text_guard():
    r = match_versions([ev(Q1)], [ev(Q1, d=date(2025, 3, 10))], Q1, Q1)
    assert {x["cls"] for x in r} == {RETRACTED, NEW} and not any(x["text_carried"] for x in r)


def test_matching_is_one_to_one_and_prefers_the_closest_date():
    early = [ev(Q2, d=date(2024, 3, 1)), ev(Q2, d=date(2024, 3, 20))]
    late = [ev(Q2, d=date(2024, 3, 20))]
    r = match_versions(early, late, "", "")
    same = [x for x in r if x["late"]]
    assert len(same) == 1 and same[0]["cls"] == UNCHANGED and same[0]["early"]["lo"] == date(2024, 3, 20)
    assert one(r, RETRACTED)["early"]["lo"] == date(2024, 3, 1)


def test_deterministic_regardless_of_repeated_calls():
    args = [ev(Q1), ev(Q2)], [ev(Q2), ev(Q3)], Q1 + Q2, Q2 + Q3
    assert match_versions(*args) == match_versions(*args)


def test_every_event_appears_exactly_once():
    early, late = [ev(Q1), ev(Q2)], [ev(Q2), ev(Q3)]
    r = match_versions(early, late, "", "")
    assert sum(x["early"] is not None for x in r) == 2 and sum(x["late"] is not None for x in r) == 2


# ---- baselines
def test_earliest_and_latest_only_can_say_only_unchanged():
    new_pair = {"early": None, "late": ev(Q2)}
    assert single_version_predict(new_pair, [ev(Q1)]) == NO_PREDICTION  # earliest version: does not contain it
    assert single_version_predict(new_pair, [ev(Q2)]) == UNCHANGED  # latest version: contains it, cannot see that it is new


def test_textdiff_finds_new_retracted_unchanged():
    e = f"March 10, 2024: {Q1}.\nMarch 15, 2024: {Q3}."
    l = f"March 10, 2024: {Q1}.\nJune 1, 2024: {Q2}."
    got = {r["cls"] for r in textdiff_classify(e, l, read_date)}
    assert got == {UNCHANGED, RETRACTED, NEW}


def test_textdiff_date_correction_and_window():
    a = f"March 10, 2024: {Q1}."
    assert textdiff_classify(a, f"March 15, 2024: {Q1}.", read_date)[0]["cls"] == DATE_CORRECTION
    assert {r["cls"] for r in textdiff_classify(a, f"June 1, 2024: {Q1}.", read_date)} == {RETRACTED, NEW}


def test_textdiff_never_says_type_change():
    assert TYPE_CHANGE not in {r["cls"] for r in textdiff_classify(f"March 10, 2024: {Q1}.", f"March 10, 2024: {Q1}.", read_date)}


def test_textdiff_predict_maps_a_pair_to_its_segment():
    recs = textdiff_classify(f"March 10, 2024: {Q1}.", f"March 10, 2024: {Q1}.\nJune 1, 2024: {Q2}.", read_date)
    assert textdiff_predict({"early": ev(Q1), "late": ev(Q1)}, recs) == UNCHANGED
    assert textdiff_predict({"early": None, "late": ev(Q2)}, recs) == NEW
    assert textdiff_predict({"early": ev(Q3), "late": None}, recs) == NO_PREDICTION


# ---- label draw
def pop(sizes):
    return {c: [f"{c}-{i:03d}" for i in range(n)] for c, n in sizes.items()}


def test_quotas_sum_to_72():
    assert sum(QUOTAS.values()) == 72 and set(QUOTAS) == set(CLASSES)


def test_draw_is_reproducible_and_records_inclusion_probabilities():
    p = pop({NEW: 100, UNCHANGED: 700, DATE_CORRECTION: 40, TYPE_CHANGE: 28, RETRACTED: 50})
    a, b = draw_items(p), draw_items(p)
    assert a == b
    assert a["n"] == QUOTAS and a["inclusion"][DATE_CORRECTION] == 16 / 40 and a["inclusion"][UNCHANGED] == 14 / 700


def test_short_class_takes_all_and_gives_shortfall_to_the_largest_remainder():
    d = draw_items(pop({NEW: 100, UNCHANGED: 700, DATE_CORRECTION: 40, TYPE_CHANGE: 3, RETRACTED: 50}))
    assert d["n"][TYPE_CHANGE] == 3 and d["inclusion"][TYPE_CHANGE] == 1.0
    assert d["n"][UNCHANGED] == 14 + 11 and sum(d["n"].values()) == 72


def test_empty_class_has_no_inclusion_probability():
    d = draw_items(pop({NEW: 100, UNCHANGED: 700, DATE_CORRECTION: 40, TYPE_CHANGE: 0, RETRACTED: 50}))
    assert d["inclusion"][TYPE_CHANGE] is None and sum(d["n"].values()) == 72


def test_repeats_are_eight_first_instances_hidden_by_the_shuffle():
    d = draw_items(pop({NEW: 100, UNCHANGED: 700, DATE_CORRECTION: 40, TYPE_CHANGE: 28, RETRACTED: 50}))
    assert len(d["sheet"]) == 80 and len(d["repeats"]) == 8 == len(set(d["repeats"]))
    firsts = {s["pair"] for s in d["sheet"] if not s["repeat"]}
    assert set(d["repeats"]) <= firsts and len(firsts) == 72
    assert any(s["repeat"] for s in d["sheet"][:72])  # repeats are not all at the end


def test_weighted_agreement_undoes_the_oversampling():
    rows = [{"stratum": "a", "agree": True}, {"stratum": "b", "agree": False}]
    assert weighted_agreement(rows, {"a": 1.0, "b": 0.5}) == pytest.approx(1 / 3)
