"""Exploratory sensitivity runs for Test-A (pre-declared in docs/AMENDMENT_1.md plus the timeout retry). Each variant = the frozen endpoints via the amend1 wrapper
with one switch changed; outputs reports/phase_6_testA_sens/<name>.json. Not part of the primary analysis."""
import os
import subprocess
import sys
from pathlib import Path

BASE = {"TT_PDF": "data/testA_raw", "TT_GOLD": "data/labels/testA_silver.json", "TT_CACHE": "runs/testA_cache.pkl",
        "TT_B2": "B2_4b_v2=runs/testA_4b_v2_run1.jsonl", "TT_RUN1": "runs/testA_4b_v2_run1.jsonl", "TT_RUN2": "runs/testA_4b_v2_run2.jsonl"}
VARIANTS = {
    "bound_errors": {"TT_AMEND_MODE": "bound_errors"},
    "bound_drop": {"TT_AMEND_MODE": "bound_drop"},
    "contested_as_miss": {"TT_AMEND_CONTESTED_MISS": "1"},
    "drop_isolation_slip_filings": {"TT_AMEND_DROP_FILES": "config/isolation_slips_drop_list.json"},
    "exclude_def_inferred_too": {"TT_AMEND_EXCLUDE_DEF": "inferred_too", "TT_CACHE": "runs/testA_cache_inferred_too.pkl"},
    "run2_timeouts_retried": {"TT_RUN2": "runs/testA_4b_v2_run2.sens_with_retry.jsonl"},
}
Path("reports/phase_6_testA_sens").mkdir(exist_ok=True)
for name, env in VARIANTS.items():
    out = f"reports/phase_6_testA_sens/{name}.json"
    r = subprocess.run([sys.executable, "-m", "tt.eval.amend1", "endpoints", out], env={**os.environ, **BASE, **env}, capture_output=True, text=True)
    print(name, "exit", r.returncode, (r.stderr.strip().splitlines() or [""])[-1][:150] if r.returncode else "", flush=True)
