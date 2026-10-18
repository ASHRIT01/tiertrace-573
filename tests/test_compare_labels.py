from tt.eval.compare_labels import classify_simple, compare_event_lists


def test_simple_classes():
    a = {"status": "SUPPORTED", "quote": "The bolt failed."}
    assert classify_simple(a, {"status": "SUPPORTED", "quote": "the bolt failed"}, ("status", "quote"))[0] == "same"
    assert classify_simple(a, {"status": "SUPPORTED", "quote": "The bolt failed. It was loose."}, ("status", "quote"))[0] == "detail"
    assert classify_simple(a, {"status": "NOT_REPORTED", "quote": ""}, ("status", "quote"))[0] == "substance"
    u1 = {"kind": "NAMED", "names": ["A", "B"], "quote": "x"}
    assert classify_simple(u1, {"kind": "NAMED", "names": ["A"], "quote": "x"}, ("kind", "names", "quote"))[0] == "detail"
    assert classify_simple(u1, {"kind": "UNNAMED", "names": [], "quote": "x"}, ("kind", "names", "quote"))[0] == "substance"


def test_events():
    e = lambda d, t, qt: {"date_text": d, "type": t, "quote": qt}
    A = [e("May 5, 2022", "FILER_AWARENESS", "On May 5, 2022 x."), e("June 3, 2022", "OTHER", "June 3 y.")]
    B = [e("On or about May 5, 2022", "FILER_AWARENESS", "On May 5, 2022 x."), e("May 5, 2022", "INVESTIGATION_START", "On May 5, 2022 x. It began.")]
    r = compare_event_lists(A, B)
    v = sorted(x[0] for x in r)
    assert v == ["detail", "substance", "substance"]  # date_text differs; extra event in B; June 3 only in A
