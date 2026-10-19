import json
from pathlib import Path

from tt import leakcheck as L


def make(tmp: Path):
    (tmp / "data/splits").mkdir(parents=True)
    (tmp / "data/splits/testA_ids.txt").write_text("23V001\n23V002\n23E003\n")
    (tmp / "data/splits/dev_ids.txt").write_text("22V009\n")
    for d in ("data/flat", "data/cache", "runs", "reports", "config"):
        (tmp / d).mkdir(parents=True)
    (tmp / "data/flat/RCL.txt").write_text("23V001000\t23V002\n")
    return tmp


def test_clean(tmp_path):
    t = make(tmp_path)
    (t / "runs/dev.jsonl").write_text('{"file": "RCLRPT-22V009-1111.PDF"}\n')
    r = L.run(t)
    assert not r["leaks"] and r["excluded"].keys() >= {"data/flat/RCL.txt", "data/splits/testA_ids.txt"}


def test_name_and_content_leaks(tmp_path):
    t = make(tmp_path)
    (t / "data/cache/static_RCLRPT-23V001-1234.PDF").write_bytes(b"x")          # a test filing, by name
    (t / "runs/b.jsonl").write_text('{"campaign": "23E003"}\n')                  # run output naming a test ID
    (t / "reports/s.md").write_text("score on 23V-002\n")                         # hyphenated form
    r = L.run(t)
    assert set(r["leaks"]) == {"data/cache/static_RCLRPT-23V001-1234.PDF", "runs/b.jsonl", "reports/s.md"}


def test_dir_named_for_test_id(tmp_path):
    t = make(tmp_path)
    (t / "runs/23V001").mkdir()
    (t / "runs/23V001/out.json").write_text("{}")
    assert "runs/23V001/out.json" in L.run(t)["leaks"]


def test_cross_reference_not_a_leak(tmp_path):
    t = make(tmp_path)
    (t / "data/cache/x_RCLRPT-22V009-1.json").write_text("see recall 23V002 for details")
    r = L.run(t)
    assert not r["leaks"] and "data/cache/x_RCLRPT-22V009-1.json" in r["cross_refs"]


def test_waiver_only_for_unscored_ids(tmp_path):
    t = make(tmp_path)
    (t / "data/splits/testA_labelled_ids.txt").write_text("23V002\n")
    (t / "data/cache/RCLRPT-23V001-1.PDF").write_bytes(b"x")
    (t / "config/leak_waivers.json").write_text(json.dumps({"23V001": "parser golden file, not scored"}))
    r = L.run(t)
    assert not r["leaks"] and not r["bad_waivers"]
    (t / "config/leak_waivers.json").write_text(json.dumps({"23V001": "x", "23V002": "y"}))
    assert L.run(t)["bad_waivers"] == ["23V002"]


def test_id_regex_boundaries():
    assert L._ids_in(b"id 23V001000 and 23V-002, X123V001 no, 23V0011 no") == {"23V001", "23V002"}
