"""AL-1 amendment 2: tests of kaggle/al1_extraction.ipynb that need no Kaggle, GPU, model or AL-1 filing. The helpers cell is executed on
made-up bundles and outputs; the pinned constants are checked against the tagged repository."""
import ast
import hashlib
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "kaggle/al1_extraction.ipynb"
pytestmark = pytest.mark.skipif(not NB.exists(), reason="notebook not written yet")


def cells():
    return ["".join(c["source"]) for c in json.load(open(NB))["cells"] if c["cell_type"] == "code"]


@pytest.fixture(scope="module")
def H():
    src = next(c for c in cells() if c.startswith("# HELPERS"))
    ns = {}
    exec(compile(src, "helpers", "exec"), ns)
    return ns


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def pinned_assignments():
    cfg = next(c for c in cells() if "PINNED = {" in c)
    out = {}
    for node in ast.parse(cfg).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            try:
                out[node.targets[0].id] = ast.literal_eval(node.value)
            except ValueError:
                pass
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Tuple):
            try:
                for t, v in zip(node.targets[0].elts, ast.literal_eval(node.value)):
                    out[t.id] = v
            except ValueError:
                pass
    return out


# ---- pinned constants -----------------------------------------------------------------------------------------------------
def test_pins_match_the_tag():
    P = pinned_assignments()
    tag = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "al1-amendment-2^{commit}"], capture_output=True, text=True).stdout.strip()
    assert P["TAG"] == "al1-amendment-2" and P["TAG_COMMIT"] == tag
    for f, h in P["PINNED"].items():
        blob = subprocess.run(["git", "-C", str(ROOT), "show", f"{tag}:{f}"], capture_output=True).stdout
        assert sha(blob) == h, f
    fm = json.load(open(ROOT / "data/FREEZE_MANIFEST.json"))
    assert P["FROZEN_DIGEST"] == fm["models"]["qwen3.5:4b-q4_K_M"]["digest"]
    assert P["OLLAMA_VERSION"] == "0.40.6" and fm["ollama_version"].endswith(P["OLLAMA_VERSION"])
    assert P["MODEL"] == json.load(open(ROOT / "config/run_settings.json"))["agent_model"]
    assert "BUDGET_S = 11 * 3600" in next(c for c in cells() if "PINNED = {" in c)


def test_reference_pin_matches_committed_record():
    P = pinned_assignments()
    rec = ROOT / "reports/al1/AL1_EQUIV_M2.json"
    if not rec.exists():
        pytest.skip("M2 reference record not committed yet")
    assert P["M2_REF_GATE_SHA256"] == json.load(open(rec))["files"]["gate.jsonl"]


def test_cells_compile_and_one_gpu_only():
    src = cells()
    for c in src:
        compile(c, "cell", "exec")
    allsrc = "\n".join(src)
    assert '"CUDA_VISIBLE_DEVICES": "0"' in allsrc and "--mode\", mode" in allsrc


# ---- bundle verification --------------------------------------------------------------------------------------------------
def make_bundle(tmp_path, ref=b'{"file": "e.pdf"}\n'):
    b = tmp_path / "al1_bundle"
    files = {"al1_pdfs/a1.pdf": b"%PDF a1", "al1_pdfs/a2.pdf": b"%PDF a2", "equiv_pdfs/e.pdf": b"%PDF e", "m2_reference/gate.jsonl": ref}
    for n, v in files.items():
        (b / n).parent.mkdir(parents=True, exist_ok=True)
        (b / n).write_bytes(v)
    man = {"al1_docs_sha256": "D", "al1_equivalence_sha256": "E", "files": {n: sha(v) for n, v in files.items()}}
    (b / "BUNDLE_MANIFEST.json").write_text(json.dumps(man))
    (b / "SHA256SUMS").write_text("")
    docs = [{"file": "a1.pdf", "sha256": sha(b"%PDF a1")}, {"file": "a2.pdf", "sha256": sha(b"%PDF a2")}]
    equiv = [{"file": "e.pdf", "sha256": sha(b"%PDF e")}]
    return b, docs, equiv, sha(ref)


def test_verify_bundle_ok(H, tmp_path):
    b, docs, equiv, r = make_bundle(tmp_path)
    assert H["verify_bundle"](b, docs, equiv, "D", "E", r) == {"files": 4, "al1_pdfs": 2, "equiv_pdfs": 1}


@pytest.mark.parametrize("damage,msg", [
    (lambda b: (b / "al1_pdfs/a1.pdf").write_bytes(b"%PDF XX"), "fail their SHA-256"),
    (lambda b: (b / "al1_pdfs/a2.pdf").unlink(), "differ from its manifest"),
    (lambda b: (b / "al1_pdfs/extra.pdf").write_bytes(b"x"), "differ from its manifest"),
])
def test_verify_bundle_rejects_damage(H, tmp_path, damage, msg):
    b, docs, equiv, r = make_bundle(tmp_path)
    damage(b)
    with pytest.raises(H["Stop"], match=msg):
        H["verify_bundle"](b, docs, equiv, "D", "E", r)


def test_verify_bundle_rejects_other_lists_hashes_or_reference(H, tmp_path):
    b, docs, equiv, r = make_bundle(tmp_path)
    with pytest.raises(H["Stop"], match="other document lists"):
        H["verify_bundle"](b, docs, equiv, "X", "E", r)
    with pytest.raises(H["Stop"], match="committed hashes"):
        H["verify_bundle"](b, [{"file": "a1.pdf", "sha256": "0" * 64}], equiv, "D", "E", r)
    with pytest.raises(H["Stop"], match="M2 reference"):
        H["verify_bundle"](b, docs, equiv, "D", "E", "0" * 64)


# ---- outputs, resume ------------------------------------------------------------------------------------------------------
def test_package_and_verify_previous_round_trip(H, tmp_path):
    out = tmp_path / "al1_out"
    (out / "al1").mkdir(parents=True)
    (out / "al1/run1.jsonl").write_text('{"file": "x"}\n')
    (out / "env").mkdir()
    (out / "env/session_1.json").write_text("{}")
    n, z = H["package"](out, tmp_path / "al1_outputs.zip")
    assert n == 2 and z == sha((tmp_path / "al1_outputs.zip").read_bytes())
    assert (tmp_path / "al1_outputs.zip.sha256").read_text().startswith(z)
    import zipfile
    names = set(zipfile.ZipFile(tmp_path / "al1_outputs.zip").namelist())
    assert {"al1_out/al1/run1.jsonl", "al1_out/OUTPUT_MANIFEST.json", "al1_out/SHA256SUMS"} <= names
    assert H["verify_previous"](out) == 2
    (out / "al1/run1.jsonl").write_text('{"file": "y"}\n')
    with pytest.raises(H["Stop"], match="missing or changed"):
        H["verify_previous"](out)


def test_package_twice_is_stable(H, tmp_path):
    out = tmp_path / "al1_out"
    out.mkdir()
    (out / "a.txt").write_text("a")
    H["package"](out, tmp_path / "z.zip")
    m1 = (out / "OUTPUT_MANIFEST.json").read_text()
    H["package"](out, tmp_path / "z.zip")
    assert (out / "OUTPUT_MANIFEST.json").read_text() == m1      # the manifest never lists itself


def test_find_one(H, tmp_path):
    assert H["find_one"](str(tmp_path), "**/al1_out/OUTPUT_MANIFEST.json", "x") is None
    for d in ("v1", "v2"):
        (tmp_path / d / "al1_out").mkdir(parents=True)
        (tmp_path / d / "al1_out/OUTPUT_MANIFEST.json").write_text("{}")
    with pytest.raises(H["Stop"], match="more than one"):
        H["find_one"](str(tmp_path), "**/al1_out/OUTPUT_MANIFEST.json", "previous output")
    (tmp_path / "v2/al1_out/OUTPUT_MANIFEST.json").unlink()
    assert H["find_one"](str(tmp_path), "**/al1_out/OUTPUT_MANIFEST.json", "x").parent.parent.name == "v1"


def test_lock_diff_and_gpu(H):
    lock = (ROOT / "kaggle/requirements-lock.txt").read_text()
    freeze = lock.replace("pydantic_core==", "pydantic-core==").replace("PyYAML==", "pyyaml==") + "tiertrace @ file:///tmp/al1/repo\n"
    assert H["lock_diff"](lock, freeze) == ([], [])
    m, e = H["lock_diff"](lock, freeze.replace("numpy==2.5.4", "numpy==2.5.3"))
    assert m == ["numpy==2.5.4"] and e == ["numpy==2.5.3"]
    assert H["same_gpu"](["0, Tesla T4, 550.54.15, 15360 MiB"], "Tesla T4")
    assert not H["same_gpu"](["0, Tesla P100-PCIE-16GB, 550.54.15, 16384 MiB"], "Tesla T4") and not H["same_gpu"]([], "Tesla T4")
