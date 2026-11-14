"""AL-1 amendment 2: tests of the Kaggle/Mac extraction helpers. Everything here is made up: fake blobs, fake records, fake PDFs (empty
files), a fake model call. No AL-1 filing is read and no lineage result is computed."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import al1_kaggle_lib as L  # noqa: E402
from al1_kaggle_lib import (Budget, accepted_keys, campaign_groups, equivalence, model_check, norm_date, read_jsonl_repair,  # noqa: E402
                            sha256_file, verify_files)


def h(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---- hashes ---------------------------------------------------------------------------------------------------------------
def test_verify_files(tmp_path):
    (tmp_path / "a.pdf").write_bytes(b"%PDF-a")
    (tmp_path / "b.pdf").write_bytes(b"%PDF-b")
    exp = {"a.pdf": h(b"%PDF-a"), "b.pdf": h(b"%PDF-x"), "c.pdf": h(b"%PDF-c")}
    r = verify_files(exp, tmp_path)
    assert r == {"ok": 1, "missing": ["c.pdf"], "bad": ["b.pdf"]}
    assert sha256_file(tmp_path / "a.pdf") == h(b"%PDF-a")


def test_pinned_constants_match_repo():
    assert sha256_file(ROOT / "config/run_settings.json") == L.RUN_SETTINGS_SHA256
    assert sha256_file(ROOT / "reports/al1/AL1_ORDER.json") == L.AL1_ORDER_SHA256
    fm = json.load(open(ROOT / "data/FREEZE_MANIFEST.json"))["models"]["qwen3.5:4b-q4_K_M"]
    assert fm["digest"] == L.FROZEN_DIGEST
    assert set(fm["weight_blobs_verified"]) == set(L.FROZEN_WEIGHT_BLOBS)


# ---- model check ----------------------------------------------------------------------------------------------------------
def fake_store(tmp_path, corrupt=None, drop=None, wrong_size=None):
    blobs = tmp_path / "blobs"
    blobs.mkdir()
    parts = {"config": b'{"model_format":"gguf"}', "weights": b"W" * 1000, "projector": b"P" * 300, "params": b'{"temperature":1}'}
    dig = {k: h(v) for k, v in parts.items()}
    man = {"schemaVersion": 2, "config": {"digest": f"sha256:{dig['config']}", "size": len(parts["config"])},
           "layers": [{"digest": f"sha256:{dig[k]}", "size": len(parts[k]) + (1 if k == wrong_size else 0)} for k in ("weights", "projector", "params")]}
    mb = json.dumps(man).encode()
    for k, v in parts.items():
        if k == drop:
            continue
        (blobs / f"sha256-{dig[k]}").write_bytes(v[:-1] + b"!" if k == corrupt else v)   # same size, different bytes
    (blobs / f"sha256-{h(mb)}").write_bytes(mb)
    return blobs, h(mb), (dig["weights"], dig["projector"])


def test_model_check_accepts_the_frozen_store(tmp_path):
    blobs, d, w = fake_store(tmp_path)
    out = model_check(d, blobs, frozen_digest=d, weight_blobs=w)
    assert len(out) == 5 and d in out


def test_model_check_rejects_other_digest(tmp_path):
    blobs, d, w = fake_store(tmp_path)
    with pytest.raises(ValueError, match="API digest"):
        model_check("0" * 64, blobs, frozen_digest=d, weight_blobs=w)


@pytest.mark.parametrize("kw,msg", [({"corrupt": "weights"}, "re-hash"), ({"drop": "projector"}, "missing"), ({"wrong_size": "params"}, "size")])
def test_model_check_rejects_bad_blobs(tmp_path, kw, msg):
    blobs, d, w = fake_store(tmp_path, **kw)
    with pytest.raises(ValueError, match=msg):
        model_check(d, blobs, frozen_digest=d, weight_blobs=w)


def test_model_check_rejects_missing_weight_blob_and_tampered_manifest(tmp_path):
    blobs, d, w = fake_store(tmp_path)
    with pytest.raises(ValueError, match="weight blobs"):
        model_check(d, blobs, frozen_digest=d, weight_blobs=(w[0], "f" * 64))
    (blobs / f"sha256-{d}").write_bytes(b"{}")
    with pytest.raises(ValueError, match="manifest blob"):
        model_check(d, blobs, frozen_digest=d, weight_blobs=w)


def test_model_check_does_not_use_the_manifest_file_hash(tmp_path):
    """The acceptance rule is the API digest + blob hashes; a local manifest file with another SHA-256 is irrelevant."""
    blobs, d, w = fake_store(tmp_path)
    (tmp_path / "local_manifest").write_bytes(b"anything")
    assert model_check(d, blobs, frozen_digest=d, weight_blobs=w)


# ---- resume ---------------------------------------------------------------------------------------------------------------
def test_read_jsonl_repair_drops_cut_last_line(tmp_path):
    p = tmp_path / "run1.jsonl"
    p.write_text('{"file": "a"}\n{"file": "b"}\n{"file": "c", "extr')
    assert [r["file"] for r in read_jsonl_repair(p)] == ["a", "b"]
    assert p.read_text() == '{"file": "a"}\n{"file": "b"}\n'
    assert read_jsonl_repair(tmp_path / "none.jsonl") == []


def test_read_jsonl_repair_refuses_bad_middle_line(tmp_path):
    p = tmp_path / "run1.jsonl"
    p.write_text('{"file": "a"}\nGARBAGE\n{"file": "b"}\n')
    with pytest.raises(ValueError, match="not the last line"):
        read_jsonl_repair(p)


def test_budget():
    t = [1000.0]
    b = Budget(deadline=1000.0 + 300, first_guess=100, margin=60, clock=lambda: t[0])
    assert b.can_start()                      # 1000 + 100 + 60 <= 1300
    b.record(50); t[0] += 50
    assert b.estimate() == 50 and b.can_start()
    t[0] = 1200.0
    assert not b.can_start()                  # 1200 + 50 + 60 > 1300
    assert Budget(None).can_start()


def test_campaign_groups():
    docs = [{"campaign": "X", "file": "x1"}, {"campaign": "X", "file": "x2"}, {"campaign": "Y", "file": "y1"}]
    assert campaign_groups(docs) == [("X", ["x1", "x2"]), ("Y", ["y1"])]
    with pytest.raises(ValueError):
        campaign_groups(docs + [{"campaign": "X", "file": "x3"}])


# ---- equivalence metric ---------------------------------------------------------------------------------------------------
def g(*events, valid=True):
    return {"run1_valid": valid, "events": [{"type": t, "date_text": d, "accepted": a} for t, d, a in events]}


def test_norm_date():
    assert norm_date("May 5, 2020") == norm_date("may 5 2020") == "may52020"


def test_equivalence_identical():
    ref = {"f1": g(("DECISION", "May 5, 2020", True), ("OTHER", "June 2020", False)), "f2": g(("NHTSA_FILING", "7/1/2020", True))}
    R = equivalence(ref, ref, ["f1", "f2"])
    assert (R["reference_accepted"], R["new_accepted"], R["matched"]) == (2, 2, 2)
    assert R["share_reference_also_new"] == R["share_new_also_reference"] == 1.0 and R["continue"]


def test_equivalence_partial_and_asymmetric():
    ref = {f"f{i}": g(("DECISION", f"May {i}, 2020", True)) for i in range(10)}
    new = {f"f{i}": g(("DECISION", f"May {i}, 2020", True)) for i in range(9)}            # f9 lost its claim
    new["f9"] = g(("OTHER", "May 9, 2020", True), ("DECISION", "June 9, 2020", True))      # wrong type, wrong date
    R = equivalence(ref, new, [f"f{i}" for i in range(10)])
    assert (R["reference_accepted"], R["new_accepted"], R["matched"]) == (10, 11, 9)
    assert R["share_reference_also_new"] == 0.9 and R["share_new_also_reference"] == pytest.approx(9 / 11)
    assert not R["continue"]                  # 0.818 < 0.85


def test_equivalence_multiset_and_document_scope():
    ref = {"a": g(("OTHER", "2020", True), ("OTHER", "2020", True)), "b": g()}
    new = {"a": g(("OTHER", "2020", True)), "b": g(("OTHER", "2020", True))}             # same key in another document does not count
    R = equivalence(ref, new, ["a", "b"])
    assert (R["reference_accepted"], R["new_accepted"], R["matched"]) == (2, 2, 1)


def test_equivalence_missing_invalid_and_empty():
    ref = {"a": g(("DECISION", "2020", True))}
    R = equivalence(ref, {"a": g(("DECISION", "2020", True), valid=False)}, ["a"])
    assert R["matched"] == 0 and not R["continue"]
    R = equivalence(ref, {}, ["a"])
    assert R["new_missing"] == ["a"] and not R["continue"]
    R = equivalence({"a": g()}, {"a": g()}, ["a"])
    assert R["share_reference_also_new"] is None and not R["continue"]   # zero denominator does not pass
    assert accepted_keys(None) == {}


def test_equivalence_threshold_boundary():
    ref = {f"f{i}": g(("DECISION", str(i), True)) for i in range(20)}
    new = {f"f{i}": g(("DECISION", str(i), True)) for i in range(17)}
    R = equivalence(ref, new, list(ref))
    assert R["share_reference_also_new"] == 0.85 and R["share_new_also_reference"] == 1.0 and R["continue"]


def test_equiv_check_script(tmp_path):
    import al1_equiv_check as C
    files = [d["file"] for d in json.load(open(ROOT / "config/al1_equivalence.json"))["documents"]]
    assert len(files) == 20
    ref = [{"file": f, **g(("DECISION", "May 1, 2020", True))} for f in files]
    for name, recs in (("ref", ref), ("same", ref), ("half", ref[:10])):
        (tmp_path / f"{name}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in recs))
    assert C.main(tmp_path / "ref.jsonl", tmp_path / "same.jsonl", tmp_path / "o1.json") == 0
    assert C.main(tmp_path / "ref.jsonl", tmp_path / "half.jsonl", tmp_path / "o2.json") == 1
    assert json.load(open(tmp_path / "o2.json"))["share_reference_also_new"] == 0.5


# ---- document lists -------------------------------------------------------------------------------------------------------
def test_lists_rules():
    import al1_lists as LS
    order = {"20V001": {"order_status": "ORDERED", "versions_in_order": ["b.pdf", "a.pdf"],
                        "versions": [{"fileName": "a.pdf", "usable": True, "sha256": "A"}, {"fileName": "b.pdf", "usable": True, "sha256": "B"}]},
             "24V528": {"order_status": "ORDERED", "versions_in_order": [], "versions": []},
             "20V002": {"order_status": "ORDER_AMBIGUOUS", "versions_in_order": ["c.pdf"], "versions": [{"fileName": "c.pdf", "usable": True, "sha256": "C"}]}}
    assert LS.primary_docs(order) == [{"campaign": "20V001", "file": "b.pdf", "sha256": "B"}, {"campaign": "20V001", "file": "a.pdf", "sha256": "A"}]
    sn1 = {"cache/static.nhtsa.gov_odi_rcl_2020_RCLRPT-20V010-1111.PDF": {"sha256": "x"},
           "cache/static.nhtsa.gov_odi_rcl_2020_RCLRPT-20V011-2222.pdf": {"sha256": "y"},
           "cache/static.nhtsa.gov_odi_rcl_2020_RCLRPT-20V012-3333.PDF": {"sha256": "z"},
           "api_cache/20V010.json": {"sha256": "j"}}
    fr = LS.equivalence_frame(sn1, excluded={"20V011"}, is_pdf=lambda p: "3333" not in p)
    assert set(fr) == {"20V010"} and fr["20V010"][1] == "RCLRPT-20V010-1111.PDF"


def test_committed_lists():
    docs = json.load(open(ROOT / "config/al1_docs.json"))
    assert len(docs) == 712 and len({d["campaign"] for d in docs}) == 248 and len({d["file"].lower() for d in docs}) == 712
    campaign_groups(docs)                     # contiguous
    eq = json.load(open(ROOT / "config/al1_equivalence.json"))
    ids = {d["campaign"] for d in eq["documents"]}
    excl = set(json.load(open(ROOT / "reports/al1/AL1_ORDER.json"))["campaigns"])
    for s in ("dev_ids", "testA_ids", "testA_labelled_ids", "testB_ids", "unseen_filer_ids"):
        excl |= {l.strip() for l in open(ROOT / f"data/splits/{s}.txt") if l.strip()}
    assert len(ids) == 20 and not ids & excl and not ids & {d["campaign"] for d in docs}


# ---- runner resume (fake model, fake gate) --------------------------------------------------------------------------------
@pytest.fixture
def runner(monkeypatch, tmp_path):
    import al1_extract as X
    calls = []

    def fake_run(model, files, pdf_dir, out, ctx, resume=True, timeout=300.0, prompt="v2", extra_options=None, **_):
        assert resume and len(files) == 1 and prompt == "v2" and ctx == 6144
        recs = read_jsonl_repair(out)
        rec = {"file": files[0], "extraction": {"events": []}, "seconds": 1.0, "options": extra_options}
        with open(out, "a") as f:
            f.write(json.dumps(rec) + "\n")
        calls.append((extra_options["seed"], files[0]))
        return recs + [rec]

    monkeypatch.setattr(X, "run", fake_run)
    monkeypatch.setattr(X, "server_checks", lambda m, b: {"ollama_version": "0.40.6", "digest": L.FROZEN_DIGEST, "blobs_verified": None})
    monkeypatch.setattr(X, "gate_record", lambda c, f, d, p1, p2: {"campaign": c, "file": f, "run1_valid": bool(p1), "run2_valid": bool(p2), "events": []})
    monkeypatch.setattr(X, "build_user", lambda p: f"user message for {p.name}")
    pdf = tmp_path / "pdfs"
    pdf.mkdir()
    docs = [{"campaign": c, "file": f"{c}-{i}.pdf"} for c, n in (("X", 2), ("Y", 3), ("Z", 2)) for i in range(n)]
    for d in docs:
        (pdf / d["file"]).write_bytes(b"%PDF")
    (tmp_path / "docs.json").write_text(json.dumps(docs))
    args = ["--docs", str(tmp_path / "docs.json"), "--pdf-dir", str(pdf), "--out-dir", str(tmp_path / "out")]
    return X, calls, docs, args, tmp_path / "out"


def test_runner_campaign_order_deadline_and_resume(runner, monkeypatch):
    X, calls, docs, args, out = runner

    class Stop3(Budget):
        def can_start(self):
            return self.n < 3

    monkeypatch.setattr(X, "Budget", Stop3)
    assert X.main(args) == 3                                       # stopped after 3 calls
    assert calls == [(0, "X-0.pdf"), (0, "X-1.pdf"), (1, "X-0.pdf")]
    assert json.load(open(out / "progress.json"))["state"] == "STOPPED_BY_DEADLINE"
    with open(out / "run1.jsonl", "a") as f:                       # a record cut off by a kill
        f.write('{"file": "Y-0.pdf", "extrac')
    monkeypatch.setattr(X, "Budget", Budget)
    calls.clear()
    assert X.main(args) == 0
    assert calls[0] == (1, "X-1.pdf") and calls[1:4] == [(0, "Y-0.pdf"), (0, "Y-1.pdf"), (0, "Y-2.pdf")]
    for k in (1, 2):
        assert sorted(r["file"] for r in read_jsonl_repair(out / f"run{k}.jsonl")) == sorted(d["file"] for d in docs)
    gate = read_jsonl_repair(out / "gate.jsonl")
    assert [r["file"] for r in gate] == [d["file"] for d in docs] and all(r["run1_valid"] and r["run2_valid"] for r in gate)
    assert len(read_jsonl_repair(out / "prompts.jsonl")) == len(docs)
    log = (out / "run_log.txt").read_text()
    assert "START" in log and "RESTART" in log and "DEADLINE STOP" in log and "DONE" in log
    calls.clear()
    assert X.main(args) == 0 and calls == []                       # nothing left to do


def test_runner_batch_mode_and_progress_has_no_content(runner, capsys):
    X, calls, docs, args, out = runner
    assert X.main(args + ["--mode", "batch"]) == 0
    assert [s for s, _ in calls] == [0] * len(docs) + [1] * len(docs)
    prog = (out / "progress.json").read_text()
    printed = capsys.readouterr().out
    for d in docs:
        assert d["file"] not in prog and d["file"] not in printed


def test_runner_refuses_missing_pdfs(runner):
    X, calls, docs, args, out = runner
    (Path(args[3]) / docs[0]["file"]).unlink()
    assert X.main(args) == 2 and calls == []
