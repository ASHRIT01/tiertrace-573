import ast
from pathlib import Path

import pytest

from tt.labels import blind
from tt.labels.blind import BlindViolation, assert_blind

ROOT = Path(__file__).resolve().parents[1]


def test_runs_refused():
    for p in ("runs/x.jsonl", ROOT / "runs", ROOT / "runs/testA_passB", "data/runs/y", "./runs/../runs/z"):
        with pytest.raises(BlindViolation):
            assert_blind(p)


def test_symlink_into_runs_refused(tmp_path):
    link = tmp_path / "work"
    link.symlink_to(ROOT / "runs")
    with pytest.raises(BlindViolation):
        assert_blind(link / "a.json")


def test_allowed_paths():
    assert_blind("data/labels/work/testA/passB", "data/testA_raw", "docs/LABELING_RULES.md", "", None)


def test_cli_label_commands_call_guard():
    src = (ROOT / "tt/cli.py").read_text()
    for fn in ("pass_a_cmd", "label_select_cmd", "label_export_cmd", "label_compare_cmd", "label_final_cmd"):
        body = src.split(f"def {fn}(")[1].split("\n@app.command")[0]
        assert "assert_blind(" in body, fn


def test_pipeline_functions_call_guard():
    src = (ROOT / "tt/labels/pipeline.py").read_text()
    for fn in ("export_pass_b", "compare_and_package", "finalize"):
        assert "assert_blind(" in src.split(f"def {fn}(")[1].split("\ndef ")[0], fn


def test_labelling_code_does_not_import_model_output_code():
    banned = ("tt.agent", "tt.eval", "tt.baselines", "ollama")
    for f in (ROOT / "tt/labels").glob("*.py"):
        if f.name.startswith("._"):
            continue
        for n in ast.walk(ast.parse(f.read_text())):
            mods = [a.name for a in n.names] if isinstance(n, ast.Import) else [n.module or ""] if isinstance(n, ast.ImportFrom) else []
            assert not any(m == b or m.startswith(b + ".") for m in mods for b in banned), (f.name, mods)
