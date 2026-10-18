from datetime import date
from tt.labels.dates import parse_span, coarse_overlap, strip_prefix

F = date(2022, 6, 3)


def g(t, **k):
    s = parse_span(t, **k); return (s.start, s.end, s.granularity, s.inferred) if s else None


def test_points():
    assert g("July 25, 2015") == (date(2015, 7, 25), date(2015, 7, 25), "day", False)
    assert g("On or about May 5, 2022") == (date(2022, 5, 5),) * 2 + ("day", False)
    assert g("12/2/2014")[0] == date(2014, 12, 2) and g("03/26/2016")[0] == date(2016, 3, 26)
    assert g("2017-12-03")[0] == date(2017, 12, 3) and g("9 OCT 2019")[0] == date(2019, 10, 9) and g("Jan 2, 2018")[0] == date(2018, 1, 2)
    assert g("November 2016")[2] == "month" and g("Nov-2015")[:2] == (date(2015, 11, 1), date(2015, 11, 30))
    assert g("Jan-16")[:3] == (date(2016, 1, 1), date(2016, 1, 31), "month")
    assert g("Sept 2017")[0] == date(2017, 9, 1) and g("Q3 2019")[:2] == (date(2019, 7, 1), date(2019, 9, 30))
    assert g("approximately March 2019")[2] == "month" and strip_prefix("around June 3, 2020") == "June 3, 2020"


def test_ranges_and_fuzzy():
    assert g("April through August 2016")[:3] == (date(2016, 4, 1), date(2016, 8, 31), "range")
    assert g("May – June, 2020")[:3] == (date(2020, 5, 1), date(2020, 6, 30), "range")
    assert g("Nov to Dec 2017")[:2] == (date(2017, 11, 1), date(2017, 12, 31))
    assert g("May 2019-July 2019")[:2] == (date(2019, 5, 1), date(2019, 7, 31))
    assert g("September - October 2018")[2] == "range" and g("April to May 2019")[2] == "range"
    assert g("04/02/2018 - 04/23/18")[:2] == (date(2018, 4, 2), date(2018, 4, 23))
    assert g("March 30 and 31, 2020")[:3] == (date(2020, 3, 30), date(2020, 3, 31), "range")
    assert g("August – September 2019")[:2] == (date(2019, 8, 1), date(2019, 9, 30))
    assert g("mid-2017")[2] == "fuzzy" and g("mid-August 2017")[:3] == (date(2017, 8, 10), date(2017, 8, 20), "fuzzy")
    assert g("end of Jan-16")[2] == "fuzzy"


def test_yearless():
    assert g("May 16", years={2022}) == (date(2022, 5, 16),) * 2 + ("day", False)
    assert g("11/29", years=set(), filing=date(2021, 12, 20))[0] == date(2021, 11, 29)
    assert g("12/25", years=set(), filing=date(2021, 12, 20))[3] is True        # would be after filing -> ambiguous
    assert g("May 16", years={2021, 2022})[3] is True                           # two candidate years -> inferred


def test_overlap():
    d = parse_span("May 5, 2022"); m = parse_span("May 2022"); r = parse_span("April to May 2022"); o = parse_span("June 2022")
    assert coarse_overlap(d, m) and coarse_overlap(d, r) and not coarse_overlap(d, o)
