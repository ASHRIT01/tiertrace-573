"""Generates kaggle/al1_extraction.ipynb. Usage: python make_nb.py OUT.ipynb M2_REF_GATE_SHA256"""
import json
import sys

out, ref_sha = sys.argv[1], sys.argv[2]

MD0 = """# TierTrace-573 AL-1 extraction (amendment 2)

Runs the **frozen** v1 agent and gate (tag `al1-amendment-2`) on the 712 AL-1 documents, after the 20-document equivalence check against the M2 reference. See `reports/AL1_AMENDMENTS.md`, amendment 2.

**Settings:** Accelerator **GPU T4** (one GPU is used even if two are present), **Internet on**. Run with **Save Version → Save & Run All (Commit)**.

**Inputs:** the private dataset made from `tiertrace_al1_kaggle_bundle.zip` (holds `al1_bundle/BUNDLE_MANIFEST.json`). On a resumed session, also the previous version's output of this notebook (holds `al1_out/OUTPUT_MANIFEST.json`).

**What it prints:** checks, counts and timing only. Never file content, claims, dates or any result, apart from the two equivalence shares (the 20 equivalence documents are not AL-1 filings).

Any failed check writes `STOP.txt`, packs whatever outputs exist, and halts the run."""

C_HELPERS = r'''# HELPERS (pure functions; tested locally by tests/test_kaggle_notebook.py)
import glob, hashlib, json, os, re, shutil, subprocess, sys, time, zipfile
from pathlib import Path

class Stop(Exception):
    pass

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()

def find_one(root, pattern, what):
    hits = sorted(glob.glob(os.path.join(root, pattern), recursive=True))
    if len(hits) > 1:
        raise Stop(f"more than one {what} found under {root}: {len(hits)}")
    return Path(hits[0]) if hits else None

def verify_bundle(broot, docs, equiv, al1_docs_sha, equiv_sha, ref_gate_sha):
    """broot = the al1_bundle folder. Every file in BUNDLE_MANIFEST must re-hash; no file may be missing or extra; the AL-1 PDFs must equal
    the committed hashes in config/al1_docs.json and the equivalence PDFs those in config/al1_equivalence.json; the M2 reference gate must
    equal the pinned hash."""
    man = json.load(open(broot / "BUNDLE_MANIFEST.json"))
    if man["al1_docs_sha256"] != al1_docs_sha or man["al1_equivalence_sha256"] != equiv_sha:
        raise Stop("bundle was built from other document lists")
    files = man["files"]
    on_disk = {str(p.relative_to(broot)) for p in broot.rglob("*") if p.is_file()} - {"BUNDLE_MANIFEST.json", "SHA256SUMS"}
    if on_disk != set(files):
        raise Stop(f"bundle files differ from its manifest: {len(on_disk - set(files))} extra, {len(set(files) - on_disk)} missing")
    bad = [n for n, h in files.items() if sha256_file(broot / n) != h]
    if bad:
        raise Stop(f"{len(bad)} bundle files fail their SHA-256")
    want = {f"al1_pdfs/{d['file']}": d["sha256"] for d in docs}
    want.update({f"equiv_pdfs/{d['file']}": d["sha256"] for d in equiv})
    bad = [n for n, h in want.items() if files.get(n) != h]
    if bad:
        raise Stop(f"{len(bad)} PDFs differ from the committed hashes")
    if files.get("m2_reference/gate.jsonl") != ref_gate_sha:
        raise Stop("M2 reference gate output is not the pinned one")
    return {"files": len(files), "al1_pdfs": sum(n.startswith("al1_pdfs/") for n in files), "equiv_pdfs": sum(n.startswith("equiv_pdfs/") for n in files)}

def output_manifest(out):
    return {str(p.relative_to(out)): sha256_file(p) for p in sorted(out.rglob("*")) if p.is_file() and p.name not in ("OUTPUT_MANIFEST.json", "SHA256SUMS")}

def verify_previous(prev_out):
    man = json.load(open(prev_out / "OUTPUT_MANIFEST.json"))
    bad = [n for n, h in man.items() if not (prev_out / n).is_file() or sha256_file(prev_out / n) != h]
    if bad:
        raise Stop(f"previous outputs: {len(bad)} files missing or changed")
    return len(man)

def package(out, zip_path):
    """Write OUTPUT_MANIFEST.json + SHA256SUMS for every file in `out`, then zip `out` (with both) to zip_path."""
    out.mkdir(parents=True, exist_ok=True)
    man = output_manifest(out)
    (out / "OUTPUT_MANIFEST.json").write_text(json.dumps(man, indent=1) + "\n")
    (out / "SHA256SUMS").write_text("".join(f"{h}  {n}\n" for n, h in man.items()))
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p.is_file():
                z.write(p, f"{out.name}/{p.relative_to(out)}")
    zsha = sha256_file(zip_path)
    Path(str(zip_path) + ".sha256").write_text(f"{zsha}  {Path(zip_path).name}\n")
    return len(man), zsha

def norm_pkg(line):
    name, ver = line.strip().split("==")
    return re.sub(r"[-_.]+", "-", name).lower() + "==" + ver

def lock_diff(lock_text, freeze_text):
    want = {norm_pkg(l) for l in lock_text.splitlines() if l.strip() and not l.startswith("#")}
    have = {norm_pkg(l) for l in freeze_text.splitlines() if "==" in l and not l.startswith("-e") and not l.lower().startswith("tiertrace")}
    return sorted(want - have), sorted(have - want)

def same_gpu(current_gpus, equiv_gpu):
    return bool(current_gpus) and current_gpus[0].split(",")[1].strip() == equiv_gpu
'''

C_CONFIG = f'''T0 = time.time()
BUDGET_S = 11 * 3600                 # session budget (amendment 2)
PACK_RESERVE_S = 20 * 60             # kept free for writing and zipping outputs
DEADLINE = T0 + BUDGET_S - PACK_RESERVE_S
REPO, TAG, TAG_COMMIT = "https://github.com/ASHRIT01/tiertrace-573", "al1-amendment-2", "e5cc4fe9c486816595481ebf3357792f7fc6af84"
OLLAMA_VERSION = "0.40.6"
OLLAMA_URL = f"https://github.com/ollama/ollama/releases/download/v{{OLLAMA_VERSION}}/ollama-linux-amd64.tar.zst"
OLLAMA_SHA256 = "c164ab8b1b28e2a247c29719b8e404c423c5b83ae64c3ab4e59d50c7ff7fc5e0"
MODEL = "qwen3.5:4b-q4_K_M"
FROZEN_DIGEST = "d8b0f5e9760cd1682034f292d7ef72ec46f432149be0df7574bf2d6e92e38c04"
PY_VERSION, UV_VERSION = "3.12.6", "0.13.0"
M2_REF_GATE_SHA256 = "{ref_sha}"
PINNED = {{   # files of the tag that this notebook relies on, beyond the 57 frozen files in data/FREEZE_MANIFEST.json
 "data/FREEZE_MANIFEST.json": "0ff5f678039cd1208db2aabf891c0e236c06d2ae6091e00099caa6402257c254",
 "config/run_settings.json": "7a13cd4a37e391d672c1ad8c071d03cde0bdf62c30e8c50a4c4a00328f0edbb9",
 "reports/al1/AL1_ORDER.json": "29e181b5b064bf1cde6844b46377faf530b9462430ea79f98d839c1fce434f17",
 "config/al1_docs.json": "53b62d1625c1c2463789451745949c049bc56da86d779ff79d5682c707e92674",
 "config/al1_equivalence.json": "3515bc101df07dbb4b709772eb96d587c2f1ffead53bc41a739686e5254c31f0",
 "kaggle/requirements-lock.txt": "ff68ab2d47d68d7990f4183a1edffd64ee64c0cdae90a4e278c143bc7006f158",
 "scripts/al1_kaggle_lib.py": "1b0215603de49498056b7d065a8309353e6d9fb1cf63c38399d7f8d5007bb445",
 "scripts/al1_extract.py": "741d647d376d0e91de24d57c1bfec6274ff6089846eddcd95a74247cfb0d5da7",
 "scripts/al1_equiv_check.py": "9877998dff0444b7032f859c1cdf280e7020309b4693309fa3131f35cd40399e",
 "scripts/al1_env.py": "f1046d95c341e4ac17ee7ddd6afff2dde6bdfec7cc75fcda1116e065ea5a9876",
 "tt/eval/amend1.py": "ffb6dbb279614ed13069e3ee6af9b43a8759d03eb1f4278d535adaddc73ca4e8",
}}
WORKING = Path("/kaggle/working"); OUT = WORKING / "al1_out"; ZIP = WORKING / "al1_outputs.zip"
TMP = Path("/tmp/al1"); REPO_DIR = TMP / "repo"; VENV = TMP / "venv"; VPY = VENV / "bin/python"
OLLAMA_DIR = TMP / "ollama"; MODELS = TMP / "ollama_models"; BLOBS = MODELS / "blobs"
TMP.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
SERVER_ENV = {{**os.environ, "OLLAMA_MODELS": str(MODELS), "OLLAMA_HOST": "127.0.0.1:11434", "CUDA_VISIBLE_DEVICES": "0"}}

def stop(msg):
    """Record the reason, pack whatever outputs exist, halt the run."""
    (WORKING / "STOP.txt").write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " " + msg + "\\n")
    try:
        n, z = package(OUT, ZIP); print(f"outputs packed: {{n}} files, zip sha256 {{z}}")
    except Exception as e:
        print("packing failed:", type(e).__name__)
    raise Stop(msg)

def sh(cmd, env=None, check=True):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
    if check and r.returncode != 0:
        stop(f"command failed ({{r.returncode}}): {{cmd.split()[0]}}")
    return r.stdout.strip()

print("budget ends", time.strftime("%H:%M:%S", time.gmtime(DEADLINE)), "UTC")'''

C_GPU = '''# (a0) GPU: one T4-class GPU is used. Two independent servers would change which request precedes which on each server, which cannot be
# shown to leave every document's output unchanged (amendment 2), so a second GPU is never used.
gpus = sh("nvidia-smi --query-gpu=index,name,driver_version,memory.total --format=csv,noheader", check=False).splitlines()
print("GPUs:", gpus)
if not gpus or "T4" not in gpus[0]:
    stop("no T4 GPU as GPU 0 (set Accelerator to GPU T4)")
print("using GPU 0 only:", gpus[0])'''

C_OLLAMA = '''# (a) Ollama: the official Linux build of the same version, checked by SHA-256; stop if unavailable
tgz = TMP / "ollama-linux-amd64.tar.zst"
if not (OLLAMA_DIR / "bin/ollama").exists():
    r = subprocess.run(["curl", "-fsSL", "-o", str(tgz), OLLAMA_URL])
    if r.returncode != 0 or not tgz.exists():
        stop(f"Ollama {OLLAMA_VERSION} Linux build unavailable")
    if sha256_file(tgz) != OLLAMA_SHA256:
        stop("Ollama download does not match the pinned SHA-256")
    if not shutil.which("zstd"):
        sh("apt-get -qq update && apt-get -qq install -y zstd")
    OLLAMA_DIR.mkdir(parents=True, exist_ok=True)
    sh(f"tar --use-compress-program=unzstd -xf {tgz} -C {OLLAMA_DIR}")
    tgz.unlink()
OLLAMA = str(OLLAMA_DIR / "bin/ollama")
serve_log = open(TMP / "ollama_serve.log", "a")
server = subprocess.Popen([OLLAMA, "serve"], env=SERVER_ENV, stdout=serve_log, stderr=subprocess.STDOUT)
import urllib.request
for _ in range(60):
    try:
        v = json.load(urllib.request.urlopen("http://127.0.0.1:11434/api/version", timeout=2))["version"]; break
    except Exception:
        time.sleep(1)
else:
    stop("Ollama server did not start")
print("Ollama server version", v)
if v != OLLAMA_VERSION:
    stop(f"Ollama server version {v} != {OLLAMA_VERSION}")'''

C_REPO = '''# (c) repository at the tag, Python environment from the lock, frozen-file hashes
if not REPO_DIR.exists():
    sh(f"git clone --quiet --depth 1 --branch {TAG} {REPO} {REPO_DIR}")
head = sh(f"git -C {REPO_DIR} rev-parse HEAD")
if head != TAG_COMMIT:
    stop(f"tag {TAG} resolves to {head[:12]}, not {TAG_COMMIT[:12]}")
bad = [f for f, h in PINNED.items() if sha256_file(REPO_DIR / f) != h]
if bad:
    stop(f"{len(bad)} pinned files differ: {bad}")
if not VPY.exists():
    sh(f"{sys.executable} -m pip install -q uv=={UV_VERSION}")
    sh(f"{sys.executable} -m uv python install -q {PY_VERSION}")
    sh(f"{sys.executable} -m uv venv -q --python {PY_VERSION} {VENV}")
    sh(f"{sys.executable} -m uv pip install -q --python {VPY} -r {REPO_DIR}/kaggle/requirements-lock.txt")
    sh(f"{sys.executable} -m uv pip install -q --python {VPY} --no-deps -e {REPO_DIR}")
pyv = sh(f"{VPY} -c 'import platform; print(platform.python_version())'")
missing, extra = lock_diff((REPO_DIR / "kaggle/requirements-lock.txt").read_text(), sh(f"{sys.executable} -m uv pip freeze --python {VPY}"))
print("python", pyv, "| packages missing from lock:", missing, "| extra:", extra)
if pyv != PY_VERSION or missing or extra:
    stop("Python environment differs from the lock")
check = r"""
import hashlib, inspect, json
from pathlib import Path
m = json.load(open("data/FREEZE_MANIFEST.json"))
bad = [f for f, h in m["files"].items() if hashlib.sha256(Path(f).read_bytes()).hexdigest() != h]
from tt.agent import run_dev
from tt.agent.schemas import Extraction
s = lambda x: hashlib.sha256(x.encode()).hexdigest()
H = m["hashes"]
ok = [s(run_dev.PROMPTS["v2"]) == H["agent_prompt_v2_system"], s(json.dumps(Extraction.model_json_schema(), sort_keys=True)) == H["agent_output_schema"],
      s(inspect.getsource(run_dev.build_user_from)) == H["agent_user_message_template"]]
print(json.dumps({"frozen_files": len(m["files"]), "bad": bad, "prompt_schema_template_ok": ok}))
"""
r = json.loads(subprocess.run([str(VPY), "-c", check], cwd=REPO_DIR, capture_output=True, text=True, check=True).stdout)
print("frozen files:", r["frozen_files"], "| mismatches:", len(r["bad"]), "| prompt, schema, template:", r["prompt_schema_template_ok"])
if r["bad"] or not all(r["prompt_schema_template_ok"]):
    stop("frozen files or prompt hashes differ")'''

C_MODEL = '''# (b) model: pulled, accepted only if the API digest and every blob hash equal the frozen record (not the manifest file's own SHA-256)
r = subprocess.run([OLLAMA, "pull", MODEL], env=SERVER_ENV, capture_output=True, text=True)
if r.returncode != 0:
    stop("model pull failed")
mc = r"""
import json, sys, urllib.request
sys.path.insert(0, "scripts")
from al1_kaggle_lib import model_check
tags = json.load(urllib.request.urlopen("http://127.0.0.1:11434/api/tags"))["models"]
d = next(t["digest"] for t in tags if t["name"] == sys.argv[1])
try:
    print(json.dumps({"digest": d, "blobs": len(model_check(d, sys.argv[2]))}))
except ValueError as e:
    print(json.dumps({"digest": d, "error": str(e)}))
"""
r = json.loads(subprocess.run([str(VPY), "-c", mc, MODEL, str(BLOBS)], cwd=REPO_DIR, capture_output=True, text=True, check=True).stdout)
print("model digest", r["digest"], "| blobs verified:", r.get("blobs"), "| error:", r.get("error"))
if r["digest"] != FROZEN_DIGEST or "error" in r:
    stop(f"model is not the frozen one: digest {r['digest']}")'''

C_INPUTS = '''# (d) inputs: every PDF verified against the bundle manifest and the committed hashes; (g) previous outputs restored and verified
bm = find_one("/kaggle/input", "**/al1_bundle/BUNDLE_MANIFEST.json", "bundle")
if bm is None:
    z = find_one("/kaggle/input", "**/tiertrace_al1_kaggle_bundle.zip", "bundle zip")
    if z is None:
        stop("bundle dataset not attached")
    with zipfile.ZipFile(z) as zz:
        zz.extractall(TMP)
    bm = TMP / "al1_bundle/BUNDLE_MANIFEST.json"
BUNDLE = bm.parent
docs = json.load(open(REPO_DIR / "config/al1_docs.json"))
equiv = json.load(open(REPO_DIR / "config/al1_equivalence.json"))["documents"]
try:
    vb = verify_bundle(BUNDLE, docs, equiv, PINNED["config/al1_docs.json"], PINNED["config/al1_equivalence.json"], M2_REF_GATE_SHA256)
except Stop as e:
    stop(str(e))
print("bundle verified:", vb)

prev = find_one("/kaggle/input", "**/al1_out/OUTPUT_MANIFEST.json", "previous output")
if prev is not None and not (OUT / "OUTPUT_MANIFEST.json").exists() and not any(OUT.iterdir()):
    try:
        n = verify_previous(prev.parent)
    except Stop as e:
        stop(str(e))
    shutil.rmtree(OUT); shutil.copytree(prev.parent, OUT)
    print("resumed from previous outputs:", n, "files verified")
else:
    print("previous outputs:", "none attached" if prev is None else "not used (working folder already has outputs)")
sessions = sorted((OUT / "env").glob("session_*.json")) if (OUT / "env").exists() else []
SESSION = len(sessions) + 1
(OUT / "env").mkdir(parents=True, exist_ok=True)
env_file = OUT / "env" / f"session_{SESSION}.json"
subprocess.run([str(VPY), "scripts/al1_env.py", str(env_file), "--where", "Kaggle"], cwd=REPO_DIR, env=SERVER_ENV, check=True)
ENV = json.load(open(env_file))
ENV.update({"session": SESSION, "gpus_all": gpus, "ollama_url": OLLAMA_URL, "ollama_sha256": OLLAMA_SHA256, "tag": TAG})
env_file.write_text(json.dumps(ENV, indent=1) + "\\n")
print("session", SESSION, "| GPU", gpus[0], "| commit", ENV["repo_commit"][:12])'''

C_EQUIV = '''# (e) equivalence check (once; later sessions reuse its result and must run on the same GPU model)
EQ = OUT / "equivalence"; res = EQ / "result.json"
def runner(docs_file, pdf_dir, out_dir, mode):
    p = subprocess.Popen([str(VPY), "-u", "scripts/al1_extract.py", "--docs", docs_file, "--pdf-dir", str(pdf_dir), "--out-dir", str(out_dir),
                          "--mode", mode, "--deadline", str(DEADLINE), "--blobs-dir", str(BLOBS)],
                         cwd=REPO_DIR, env=SERVER_ENV, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in p.stdout:
        print(line, end="")          # the runner prints counts and timing only
    return p.wait()

if res.exists():
    R = json.load(open(res))
    print("equivalence already computed in session", R["session"], "| continue:", R["continue"])
    if not R["continue"]:
        stop("equivalence check failed earlier; the decision returns to the author")
    if not same_gpu(gpus, R["gpu"]):
        stop(f"GPU differs from the equivalence session ({R['gpu']})")
else:
    rc = runner("config/al1_equivalence.json", BUNDLE / "equiv_pdfs", EQ / "kaggle", "batch")
    if rc == 3:
        stop("deadline reached during the equivalence run; resume in a new session")
    if rc != 0:
        stop(f"equivalence runner exited {rc}")
    rc = subprocess.run([str(VPY), "scripts/al1_equiv_check.py", str(BUNDLE / "m2_reference/gate.jsonl"), str(EQ / "kaggle/gate.jsonl"), str(res)],
                        cwd=REPO_DIR, capture_output=True, text=True)
    print(rc.stdout.strip())
    R = json.load(open(res)); R.update({"session": SESSION, "gpu": gpus[0].split(",")[1].strip()})
    res.write_text(json.dumps(R, indent=1) + "\\n")
    if not R["continue"]:
        stop("equivalence check failed (a share is below 0.85); the decision returns to the author")'''

C_RUN = '''# (f) the frozen agent and gate on the 712 AL-1 documents, campaign by campaign; counts only; stops cleanly at the budget
rc = runner("config/al1_docs.json", BUNDLE / "al1_pdfs", OUT / "al1", "campaign")
STATE = {0: "DONE", 3: "STOPPED_AT_BUDGET"}.get(rc)
if STATE is None:
    stop(f"AL-1 runner exited {rc}")
print("AL-1 state:", STATE)'''

C_PACK = '''# (h) outputs: zip of everything + SHA-256 manifest + environment record (GPU, driver, Ollama version, model digest, repo commit)
server.terminate()
shutil.copy(TMP / "ollama_serve.log", OUT / "env" / f"ollama_serve_session_{SESSION}.log")
p = json.load(open(OUT / "al1/progress.json"))
summary = {k: p[k] for k in ("state", "documents", "run1_records", "run2_records", "gated", "run1_valid_json", "run2_valid_json", "timeouts", "call_errors", "truncated")}
(OUT / "env" / f"summary_session_{SESSION}.json").write_text(json.dumps({**summary, "session": SESSION, "seconds": round(time.time() - T0)}, indent=1) + "\\n")
n, z = package(OUT, ZIP)
print("counts:", summary)
print(f"outputs: {n} files | {ZIP.name} sha256 {z}")
print("NEXT:", "all 712 documents done" if STATE == "DONE" else "save this version, then start a new version with this output attached as input")'''

cells = [("markdown", MD0), ("code", C_HELPERS), ("code", C_CONFIG), ("code", C_GPU), ("code", C_OLLAMA), ("code", C_REPO), ("code", C_MODEL),
         ("code", C_INPUTS), ("code", C_EQUIV), ("code", C_RUN), ("code", C_PACK)]
nb = {"cells": [{"cell_type": t, "metadata": {}, "source": s.splitlines(keepends=True), **({"execution_count": None, "outputs": []} if t == "code" else {})}
                for t, s in cells],
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                   "language_info": {"name": "python"}, "kaggle": {"accelerator": "nvidiaTeslaT4", "isInternetEnabled": True, "isGpuEnabled": True}},
      "nbformat": 4, "nbformat_minor": 5}
json.dump(nb, open(out, "w"), indent=1)
print("wrote", out, len(cells), "cells")
