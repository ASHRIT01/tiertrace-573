import json

from tt.labels import protocol
from tt.labels.pipeline import c_agreement


def items(n=200):
    return [{"item_id": f"D{i:03d}", "file": f"f{i % 7}.pdf", "claim": "S2", "A": {"status": "SUPPORTED", "quote": "a"}, "B": {"status": "INSUFFICIENT", "quote": "b"}}
            for i in range(1, n + 1)]


def pkg(tmp_path, its, seed=0):
    texts = tmp_path / "t"; texts.mkdir(exist_ok=True)
    for f in {i["file"] for i in its}:
        (texts / (f.rsplit(".", 1)[0] + ".txt")).write_text("x")
    rules = tmp_path / "r.md"; rules.write_text("rules")
    return protocol.package_for_c(its, texts, rules, tmp_path / "out", seed=seed)


def test_x_is_seeded_and_balanced():
    a = [protocol.x_is(f"D{i:03d}") for i in range(1, 401)]
    assert a == [protocol.x_is(f"D{i:03d}") for i in range(1, 401)]
    assert 0.4 < a.count("A") / 400 < 0.6
    assert a != [protocol.x_is(f"D{i:03d}", seed=1) for i in range(1, 401)]


def test_batch_dirs_never_name_the_pass(tmp_path):
    its = items(30); its[0]["kind"] = "only in A"; its[0]["B"] = None; its[1]["kind"] = "only in B"; its[1]["A"] = None
    dirs = pkg(tmp_path, its)
    text = "".join((d / "items.json").read_text() for d in dirs)
    assert "version_A" not in text and "version_B" not in text and "only in A" not in text and "only in B" not in text and "x_is" not in text
    allit = [i for d in dirs for i in json.loads((d / "items.json").read_text())]
    one = next(i for i in allit if i["item_id"] == its[0]["item_id"])
    assert one["what_differs"] == ("only in X" if one["version_X"] is not None else "only in Y")
    assert all("x_is" in i for i in its)   # mapping kept on the master items only


def test_apply_c_translates_xy(tmp_path):
    its = items(40); pkg(tmp_path, its)
    A = [{"file": f"f{k}.pdf", "claims": [{"id": "S1", "status": "SUPPORTED", "quote": ""}, {"id": "S2", "status": "SUPPORTED", "quote": "a"}],
          "cause": {}, "upstream": {}, "events": []} for k in range(7)]
    # always pick the version that is really pass A's: X when x_is == A else Y
    dec = [{"item_id": i["item_id"], "decision": "X" if i["x_is"] == "A" else "Y"} for i in its]
    recs, counts = protocol.apply_c(A, its, dec)
    assert counts["A"] == 40 and counts["B"] == 0
    dec = [{"item_id": i["item_id"], "decision": "Y" if i["x_is"] == "A" else "X"} for i in its]
    recs, counts = protocol.apply_c(A, its, dec)
    assert counts["B"] == 40
    ag = c_agreement(its, dec, counts)
    assert ag["with_B"]["k"] == 40 and ag["with_A"]["k"] == 0 and ag["position"]["chose_X"] + ag["position"]["chose_Y"] == 40


def test_ab_answer_is_rejected_for_blind_items_but_legacy_items_still_work(tmp_path):
    its = items(2); pkg(tmp_path, its)
    A = [{"file": "f1.pdf", "claims": [{"id": "S1", "status": "SUPPORTED", "quote": ""}, {"id": "S2", "status": "SUPPORTED", "quote": "a"}],
          "cause": {}, "upstream": {}, "events": []}, {"file": "f2.pdf", "claims": [{"id": "S1", "status": "SUPPORTED", "quote": ""}, {"id": "S2", "status": "SUPPORTED", "quote": "a"}],
          "cause": {}, "upstream": {}, "events": []}]
    _, counts = protocol.apply_c(A, its, [{"item_id": i["item_id"], "decision": "A"} for i in its])
    assert counts["missing"] == 2
    legacy = [{k: v for k, v in i.items() if k != "x_is"} for i in its]
    _, counts = protocol.apply_c(A, legacy, [{"item_id": i["item_id"], "decision": "A"} for i in its])
    assert counts["A"] == 2
