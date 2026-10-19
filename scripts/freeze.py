"""FREEZE (NOT RUN by the assistant). Run only after the owner has read reports/PREREGISTRATION_PROPOSED_FINAL.md, edited the thresholds
and created reports/APPROVED_BY_OWNER.txt. It: refuses to run on a dirty git tree; moves the proposed Phase 6 subsets into data/splits/;
writes data/splits/SHA256SUMS and data/FREEZE_MANIFEST.json (sha256 of labels, rules, prompts, configs, code commit); appends a FROZEN
section to PREREGISTRATION.md; tags the commit `prereg-v1`. Nothing in data/splits/dev_ids.txt or testA_ids.txt changes."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ["data/labels/dev_silver_v1.json", "data/labels/passA_v1.json", "data/labels/passB_v1.json", "data/labels/passC_decisions_v1.json",
         "docs/LABELING_RULES.md", "docs/LABELS.md", "docs/PROMPT_LOG.md", "docs/PASS_B_PROMPT.txt", "docs/PASS_C_PROMPT.txt",
         "config/injection_heldout_v1.json", "config/model.yaml", "config/event_overrides.json", "config/claim_overrides.json",
         "config/affiliates.csv", "config/aliases.csv", "tt/verify/verifier.py", "tt/verify/extra.py", "tt/agent/agent.py", "tt/agent/run_dev.py",
         "tt/agent/inject.py", "tt/baselines/rules.py", "tt/eval/riskcov.py", "tt/eval/phase3.py", "tt/eval/phase4.py", "tt/eval/diagnose.py",
         "tt/eval/devscore.py", "tt/labels/dates.py", "tt/labels/events.py", "tt/labels/agree.py", "tt/labels/protocol.py", "tt/labels/schema.py",
         "reports/PREREGISTRATION_PROPOSED_FINAL.md"]
SPLITS = ["data/splits/dev_ids.txt", "data/splits/testA_ids.txt"]
PROPOSED = ["testA_labelled_ids.txt", "testB_ids.txt", "unseen_filer_ids.txt"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sh(*a) -> str:
    return subprocess.run(a, cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def main():
    if not (ROOT / "reports/APPROVED_BY_OWNER.txt").exists():
        sys.exit("Refusing: reports/APPROVED_BY_OWNER.txt does not exist (the owner creates it after approving the preregistration).")
    if sh("git", "status", "--porcelain"):
        sys.exit("Refusing: git tree is not clean. Commit first.")
    for n in PROPOSED:
        shutil.copy(ROOT / "data/splits/proposed" / n, ROOT / "data/splits" / n)
    split_files = SPLITS + [f"data/splits/{n}" for n in PROPOSED]
    (ROOT / "data/splits/SHA256SUMS").write_text("".join(f"{sha(ROOT / f)}  {Path(f).name}\n" for f in split_files))
    man = {"git_commit": sh("git", "rev-parse", "HEAD"), "files": {f: sha(ROOT / f) for f in FILES + split_files},
           "models": ["qwen3.5:4b-q4_K_M", "qwen3.5:2b-q8_0"], "ollama": sh("ollama", "--version") if shutil.which("ollama") else "unknown"}
    (ROOT / "data/FREEZE_MANIFEST.json").write_text(json.dumps(man, indent=1))
    with open(ROOT / "PREREGISTRATION.md", "a") as f:
        f.write("\n## FROZEN (see reports/PREREGISTRATION_PROPOSED_FINAL.md for the full text)\n"
                f"Code commit before freeze: {man['git_commit']}\n\n| file | sha256 |\n|---|---|\n" + "".join(f"| {k} | {v} |\n" for k, v in man["files"].items()))
    sh("git", "add", "PREREGISTRATION.md", "data/splits", "data/FREEZE_MANIFEST.json")
    sh("git", "commit", "-m", "Freeze preregistration, labels and splits (owner approved)")
    sh("git", "tag", "prereg-v1")
    print("Frozen. Tag prereg-v1.")


if __name__ == "__main__":
    main()
