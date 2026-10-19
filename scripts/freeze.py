"""FREEZE (NOT RUN by the assistant). Run only after the owner has read reports/PREREGISTRATION_PROPOSED_FINAL.md, edited the thresholds
(config/thresholds.json: status OWNER_APPROVED and primary_endpoint chosen), filled config/labelling_model.json and created
reports/APPROVED_BY_OWNER.txt. It refuses to run on a dirty git tree. Before it writes anything it gathers, checks and PRINTS:
  1. leak check: no Test-A / Test-B / unseen-filer ID has a PDF, parsed text, label, run output or score under data/, runs/, reports/
     (tt/leakcheck.py; the flat file, its parsed index and the split lists are excluded and their matches printed separately);
  2. git commit; SHA-256 of the agent prompt (and output schema), the thresholds file, the verifier code (verifier.py, extra.py);
  3. for each Ollama model: digest (ollama list / API), SHA-256 of `ollama show` and of the weight blobs, Ollama version;
  4. seeds and options (checked against the code), and for labelling: the Claude model per role and SHA-256 of the labelling prompts and rules.
Then it moves the proposed Phase 6 subsets into data/splits/, writes data/splits/SHA256SUMS and data/FREEZE_MANIFEST.json, appends a FROZEN
section to PREREGISTRATION.md and tags the commit `freeze-v1`. Nothing in data/splits/dev_ids.txt or testA_ids.txt changes."""
import hashlib
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

FILES = ["data/labels/dev_silver_v1.json", "data/labels/passA_v1.json", "data/labels/passB_v1.json", "data/labels/passC_decisions_v1.json",
         "docs/LABELING_RULES.md", "docs/LABELS.md", "docs/PROMPT_LOG.md", "docs/PASS_B_PROMPT.txt", "docs/PASS_C_PROMPT.txt", "docs/PHASE6_RUNBOOK.md",
         "config/injection_heldout_v1.json", "config/model.yaml", "config/event_overrides.json", "config/claim_overrides.json",
         "config/affiliates.csv", "config/aliases.csv", "config/thresholds.json", "config/run_settings.json", "config/labelling_model.json",
         "tt/verify/verifier.py", "tt/verify/extra.py", "tt/agent/agent.py", "tt/agent/run_dev.py", "tt/agent/schemas.py",
         "tt/agent/inject.py", "tt/baselines/rules.py", "tt/eval/riskcov.py", "tt/eval/phase3.py", "tt/eval/phase4.py", "tt/eval/diagnose.py",
         "tt/eval/devscore.py", "tt/labels/dates.py", "tt/labels/events.py", "tt/labels/agree.py", "tt/labels/protocol.py", "tt/labels/schema.py",
         "tt/labels/pipeline.py", "tt/labels/draft.py", "tt/labels/texts.py", "tt/labels/blind.py", "tt/labeldraft.py", "tt/cli.py",
         "tt/eval/endpoints.py", "tt/kind.py", "tt/norm/aliases.py", "tt/parse/block.py", "tt/parse/sections.py", "tt/parse/pdf.py", "tt/verify/dates.py",
         "tt/leakcheck.py", "scripts/freeze.py", "reports/PREREGISTRATION_PROPOSED_FINAL.md"]
SPLITS = ["data/splits/dev_ids.txt", "data/splits/testA_ids.txt"]
PROPOSED = ["testA_labelled_ids.txt", "testB_ids.txt", "unseen_filer_ids.txt"]
VERIFIER = ["tt/verify/verifier.py", "tt/verify/extra.py"]
LABEL_PROMPTS = ["docs/PASS_B_PROMPT.txt", "docs/PASS_C_PROMPT.txt", "docs/LABELING_RULES.md"]
LABEL_ROLES = ["pass_a_drafter", "pass_b_labeller", "pass_c_adjudicator"]   # test roles: must be exact Claude model IDs; dev roles are recorded verbatim
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
if not OLLAMA_HOST.startswith("http"):
    OLLAMA_HOST = "http://" + OLLAMA_HOST


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha_s(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def eval_closure(entry="tt/eval/endpoints.py", extra=("tt/eval/devscore.py",)) -> list[str]:
    """The scorer code: `entry`, `extra`, and every tt/eval module they import (transitively), found by parsing the imports."""
    import ast
    seen, todo = [], [entry, *extra]
    while todo:
        f = todo.pop(0)
        if f in seen:
            continue
        seen.append(f)
        for n in ast.walk(ast.parse((ROOT / f).read_text())):
            mods = [n.module] if isinstance(n, ast.ImportFrom) and n.module else [a.name for a in n.names] if isinstance(n, ast.Import) else []
            for m in mods:
                if m == "tt.eval" and isinstance(n, ast.ImportFrom):
                    todo += [f"tt/eval/{a.name}.py" for a in n.names if (ROOT / f"tt/eval/{a.name}.py").exists()]
                elif m.startswith("tt.eval.") and (ROOT / (m.replace(".", "/") + ".py")).exists():
                    todo.append(m.replace(".", "/") + ".py")
    return sorted(seen)


def sh(*a) -> str:
    return subprocess.run(a, cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def ollama_info(model: str) -> dict:
    """Digest from the Ollama API (the same value `ollama list` shows as ID, in full), hash of the `ollama show` text, and a re-hash of
    every weight blob named in the modelfile (a blob's file name is the SHA-256 of its content, so this verifies the files on disk)."""
    tags = json.load(urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=10))["models"]
    m = next((t for t in tags if t["name"] == model), None)
    if m is None:
        raise RuntimeError(f"model {model!r} is not installed")
    show = subprocess.run(["ollama", "show", model], capture_output=True, text=True, check=True).stdout
    mf = subprocess.run(["ollama", "show", "--modelfile", model], capture_output=True, text=True, check=True).stdout
    blobs = {}
    for path in re.findall(r"^FROM (/\S+sha256-[0-9a-f]{64})$", mf, re.M):
        want = path.rsplit("sha256-", 1)[1]
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 24), b""):
                h.update(chunk)
        blobs[want] = h.hexdigest() == want
    return {"model": model, "digest": m["digest"], "size_bytes": m["size"], "modified_at": m["modified_at"], "details": m["details"],
            "ollama_show_sha256": sha_s(show), "weight_blobs_verified": blobs, "modelfile_sha256": sha_s(mf)}


def declared_vs_code(rs: dict) -> tuple[dict, list[str]]:
    """Seeds and options as they will be used, read from the code, and a list of mismatches with config/run_settings.json."""
    from tt.agent import run_dev
    from tt.eval.riskcov import cluster_bootstrap
    from tt import cli
    bad = []
    code = {"run1_options": {**run_dev.OPTIONS}, "num_ctx_default": inspect.signature(cli.dev_bench).parameters["ctx"].default,
            "dev_bench_default_temperature": inspect.signature(cli.dev_bench).parameters["temperature"].default,
            "dev_bench_default_seed": inspect.signature(cli.dev_bench).parameters["seed"].default,
            "bootstrap_resamples": inspect.signature(cluster_bootstrap).parameters["n"].default,
            "bootstrap_seed": inspect.signature(cluster_bootstrap).parameters["seed"].default,
            "draw_splits_seed": inspect.signature(cli.draw_splits).parameters["seed"].default,
            "phase6_subsets_seed": inspect.signature(cli.phase6_subsets_cmd).parameters["seed"].default}
    r1 = rs["run1"]
    for k, v in (("temperature", r1["temperature"]), ("seed", r1["seed"]), ("presence_penalty", r1["presence_penalty"])):
        if code["run1_options"].get(k) != v:
            bad.append(f"run1 {k}: config {v} vs code {code['run1_options'].get(k)}")
    if code["num_ctx_default"] != r1["num_ctx"]:
        bad.append(f"num_ctx: config {r1['num_ctx']} vs code {code['num_ctx_default']}")
    if (code["bootstrap_resamples"], code["bootstrap_seed"]) != (rs["bootstrap"]["resamples"], rs["bootstrap"]["seed"]):
        bad.append("bootstrap resamples/seed differ between config and code")
    if code["phase6_subsets_seed"] != rs["split_seed"]:
        bad.append("split seed differs between config and code")
    rb = (ROOT / "docs/PHASE6_RUNBOOK.md").read_text()
    r2 = rs["run2"]
    if f"--temperature {r2['temperature']} --seed {r2['seed']}" not in rb:
        bad.append("run 2 temperature/seed in config/run_settings.json do not appear in the runbook command")
    inj = (ROOT / "tt/agent/inject.py").read_text()
    if f'"temperature": {r2["temperature"]}, "seed": {r2["seed"]}' not in inj:
        bad.append("run 2 temperature/seed in config/run_settings.json do not appear in tt/agent/inject.py")
    return code, bad


SCORER = eval_closure()


def gather() -> tuple[dict, list[str], list[str]]:
    """-> (manifest, report lines, problems). Reads only; writes nothing."""
    from tt import leakcheck
    from tt.agent import run_dev
    from tt.agent.schemas import Extraction
    L, problems, man = [], [], {}
    # 1. leak check
    lk = leakcheck.run()
    L.append(leakcheck.report(lk))
    if lk["leaks"]:
        problems.append(f"leak check: {len(lk['leaks'])} file(s) belong to a Test-A/Test-B/unseen-filer campaign. Remove them, or (only for an ID in no scored subset) list the ID in config/leak_waivers.json with a reason.")
    if lk["bad_waivers"]:
        problems.append(f"leak waivers refused for IDs in a scored subset: {lk['bad_waivers']}")
    man["leak_check"] = {"leak_files": sorted(lk["leaks"]), "waivers": lk["waivers"], "scanned": lk["scanned"],
                         "cross_references": {k: sorted(v[0]) for k, v in lk["cross_refs"].items()},
                         "excluded_matches": {k: {"n_ids": len(v), "sorted_ids_sha256": sha_s("\n".join(sorted(v)))} for k, v in lk["excluded"].items()}}
    # 2. commit and hashes
    man["git_commit"] = sh("git", "rev-parse", "HEAD")
    prompt = run_dev.PROMPTS["v2"]
    man["scorer_files"] = SCORER
    man["hashes"] = {"agent_prompt_v2_system": sha_s(prompt),
                     "agent_output_schema": sha_s(json.dumps(Extraction.model_json_schema(), sort_keys=True)),
                     "agent_user_message_template": sha_s(inspect.getsource(run_dev.build_user_from)),
                     "thresholds_file": sha(ROOT / "config/thresholds.json"),
                     **{f"verifier:{Path(f).name}": sha(ROOT / f) for f in VERIFIER},
                     "preregistration_proposed_final": sha(ROOT / "reports/PREREGISTRATION_PROPOSED_FINAL.md"),
                     **{f"scorer:{Path(f).name}": sha(ROOT / f) for f in SCORER}}
    L += ["", "FREEZE RECORD", f"  git commit (HEAD at freeze time, before the freeze commit): {man['git_commit']}",
          f"  scorer code = tt/eval/endpoints.py, devscore.py and the tt/eval modules they import: {', '.join(Path(f).name for f in SCORER)}"]
    L += [f"  sha256 {k:34} {v}" for k, v in man["hashes"].items()]
    th = json.loads((ROOT / "config/thresholds.json").read_text())
    if th.get("status") != "OWNER_APPROVED":
        problems.append("config/thresholds.json: status is not OWNER_APPROVED (the owner reviews and sets every threshold)")
    if th.get("primary_endpoint") not in th.get("endpoints", {}):
        problems.append("config/thresholds.json: primary_endpoint is not set to one of the endpoint ids (the owner chooses it; proposed_primary is only a suggestion)")
    elif th["endpoints"][th["primary_endpoint"]]["claim"].startswith("cause_reported"):
        problems.append("primary_endpoint is the cause_reported (NR-or-not) claim, which measures NR detection only and cannot be the primary endpoint")
    man["primary_endpoint"] = th.get("primary_endpoint")
    L.append(f"  thresholds status {th.get('status')}; primary endpoint {th.get('primary_endpoint')} (chosen by the owner)")
    # 3. models
    rs = json.loads((ROOT / "config/run_settings.json").read_text())
    man["ollama_version"] = subprocess.run(["ollama", "--version"], capture_output=True, text=True).stdout.strip() or "unknown"
    man["models"] = {}
    L += ["", f"  Ollama: {man['ollama_version']}"]
    for role, name in (("agent", rs["agent_model"]), ("dev_only", rs["dev_only_model"])):
        try:
            info = ollama_info(name)
        except Exception as e:
            problems.append(f"Ollama model {name} ({role}): {e} (start `ollama serve`; nothing is pulled by this script)")
            L.append(f"  model {name} ({role}): UNAVAILABLE ({e})")
            continue
        man["models"][name] = {"role": role, **info}
        if not all(info["weight_blobs_verified"].values()):
            problems.append(f"Ollama model {name}: a weight blob's SHA-256 does not match its file name")
        L.append(f"  model {name} ({role}): digest {info['digest']}; ollama-show sha256 {info['ollama_show_sha256'][:16]}; "
                 f"weight blobs re-hashed OK: {all(info['weight_blobs_verified'].values())}; {info['details'].get('quantization_level')} {info['details'].get('parameter_size')}")
    # 4. seeds and options
    code, bad = declared_vs_code(rs)
    problems += [f"run settings: {b}" for b in bad]
    man["seeds_and_options"] = {"declared": rs, "from_code": code}
    L += ["", "  seeds and options (config/run_settings.json, checked against the code):",
          f"    prompt {rs['prompt']}, think {rs['think']}; run 1 {rs['run1']}; run 2 {rs['run2']}",
          f"    bootstrap {rs['bootstrap']}; split seed {rs['split_seed']}; subset sizes {rs['subset_sizes']}; injection fixture seed {rs['injection_fixture_seed']}",
          f"    code: {code}" + ("" if not bad else f"\n    MISMATCH: {bad}")]
    # 5. labelling
    lm = json.loads((ROOT / "config/labelling_model.json").read_text())
    for r in LABEL_ROLES:
        v = str(lm.get("test", {}).get(r, ""))
        if not (re.search(r"claude-[A-Za-z0-9.\-]+", v) and "tt/labels/draft.py" in v if r == "pass_a_drafter" else re.fullmatch(r"claude-[A-Za-z0-9.\-]+", v)):
            problems.append(f"config/labelling_model.json: test.{r} must be an exact Claude model ID (Pass A: the code description naming the model) (got {lm.get('test', {}).get(r)!r})")
    pc = (ROOT / "docs/PASS_C_PROMPT.txt").read_text()
    if "version_X" not in pc or "version_A" in pc or '"A"' in pc:
        problems.append("docs/PASS_C_PROMPT.txt must use the blind X/Y wording (version_X, version_Y) and never name pass A or B")
    man["labelling"] = {"claude_models_test": {r: lm["test"].get(r) for r in LABEL_ROLES}, "claude_models_dev_not_recorded": lm.get("dev"), "alias_note": lm.get("note"), "sha256": {Path(f).name: sha(ROOT / f) for f in LABEL_PROMPTS},
                        "blind_to_runs": "tt/labels/blind.py refuses any path in runs/ (sha256 " + sha(ROOT / "tt/labels/blind.py") + ")"}
    L += ["", "  labelling:", "    Pass A prompt: NONE EXISTS. Pass A is code-assisted (tt/labels/draft.py, events.py, dates.py) plus per-filing overrides (config/event_overrides.json, "
          "config/claim_overrides.json), all hashed in the manifest; there is no stored Pass A prompt text to hash."] + [f"    Claude model, test {r}: {lm['test'].get(r)!r}" for r in LABEL_ROLES]
    L += [f"    dev {k}: {v}" for k, v in lm.get("dev", {}).items()] + ["    (aliases as passed to the Agent tool; alias-to-version mapping cannot be proven from inside a subagent)"]
    L += [f"    sha256 {Path(f).name:24} {man['labelling']['sha256'][Path(f).name]}" for f in LABEL_PROMPTS]
    L.append(f"    blind guard tt/labels/blind.py sha256 {sha(ROOT / 'tt/labels/blind.py')}")
    return man, L, problems


def main():
    if not (ROOT / "reports/APPROVED_BY_OWNER.txt").exists():
        sys.exit("Refusing: reports/APPROVED_BY_OWNER.txt does not exist (the owner creates it after approving the preregistration).")
    if sh("git", "status", "--porcelain"):
        sys.exit("Refusing: git tree is not clean. Commit first.")
    if sh("git", "tag", "--list", "freeze-v1"):
        sys.exit("Refusing: tag freeze-v1 already exists.")
    gathered, lines, problems = gather()
    print("\n".join(lines))
    if problems:
        print("\nREFUSING TO FREEZE; nothing was written:")
        sys.exit("\n".join(f"  - {p}" for p in problems))
    for n in PROPOSED:
        shutil.copy(ROOT / "data/splits/proposed" / n, ROOT / "data/splits" / n)
    split_files = SPLITS + [f"data/splits/{n}" for n in PROPOSED]
    (ROOT / "data/splits/SHA256SUMS").write_text("".join(f"{sha(ROOT / f)}  {Path(f).name}\n" for f in split_files))
    man = {**gathered, "files": {f: sha(ROOT / f) for f in sorted(set(FILES + SCORER)) + split_files}}
    (ROOT / "data/FREEZE_MANIFEST.json").write_text(json.dumps(man, indent=1))
    with open(ROOT / "PREREGISTRATION.md", "a") as f:
        f.write("\n## FROZEN (see reports/PREREGISTRATION_PROPOSED_FINAL.md for the full text)\n"
                f"Code commit before freeze: {man['git_commit']}\n\nPrimary endpoint (chosen by the owner): {man['primary_endpoint']}\n\n```\n" + "\n".join(lines) + "\n```\n\n"
                "| file | sha256 |\n|---|---|\n" + "".join(f"| {k} | {v} |\n" for k, v in man["files"].items()))
    sh("git", "add", "PREREGISTRATION.md", "data/splits", "data/FREEZE_MANIFEST.json")
    sh("git", "commit", "-m", "Freeze preregistration, labels and splits (owner approved)")
    sh("git", "tag", "freeze-v1")
    print(f"Frozen. Tag freeze-v1 on {sh('git', 'rev-parse', 'HEAD')}.")


if __name__ == "__main__":
    main()
