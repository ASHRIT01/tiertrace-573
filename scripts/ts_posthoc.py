"""TS-1 follow-up: CIs ADDED AFTER SEEING RESULTS for two already-computed, pre-declared variants (no new variant, no protocol change).
  (1) RCDATE as filing date (variant 6) over all defect filings;  (2) the original (only-version) stratum (variant 7a) under the primary rule.
For each: the outputs the primary got in H(a), H(b), H(c). Same code paths as scripts/ts_screen.py.
  python scripts/ts_posthoc.py -> reports/ts/phase_7_posthoc.json (aggregates only)"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ts_screen as T  # noqa: E402
from ts_lib import wilson  # noqa: E402


def main():
    t = subprocess.run([sys.executable, "-m", "pytest", "tests/test_ts_screen.py", "-q"], capture_output=True, text=True)
    if t.returncode != 0:
        sys.exit("unit tests failed: no result written")
    F = T.load_filings()
    for name in ("primary", "rcdate_as_filing_date"):
        T.run_variant(F, name)
    D = [f for f in F if f["type"] == "DEFECT"]
    groups = {"testA": lambda f: f["split"] == "testA", "testB": lambda f: f["split"] == "testB", "unseen": lambda f: f["split"] == "unseen", "pooled": lambda f: True}
    R = {"note": T.NOTE + "; CIs ADDED AFTER SEEING RESULTS (post hoc additions for two pre-declared variants)", "tests": t.stdout.strip().splitlines()[-1],
         "rcdate_as_filing_date": {}, "original_version_only": {}}
    for g, sel in groups.items():
        G = [f for f in D if sel(f)]
        O = [f for f in G if f["original"]]
        R["rcdate_as_filing_date"][g] = {"a": T.table_a(G, "ref", "rcdate_as_filing_date"), "b": T.table_b(G, "rcdate_as_filing_date"),
                                         "c": T.table_c(G, "rcdate_as_filing_date")}
        R["original_version_only"][g] = {"a": T.table_a(O, "ref", "primary"), "b": T.table_b(O, "primary"), "c": T.table_c(O, "primary")}
    chk = {"19/305": [round(x, 3) for x in wilson(19, 305)], "6/136": [round(x, 3) for x in wilson(6, 136)]}
    R["wilson_checks"] = chk
    assert R["rcdate_as_filing_date"]["pooled"]["a"]["status"]["FLAGGED"]["k"] == 19 and R["rcdate_as_filing_date"]["pooled"]["a"]["N"] == 305
    assert R["original_version_only"]["pooled"]["a"]["status"]["FLAGGED"]["k"] == 6 and R["original_version_only"]["pooled"]["a"]["N"] == 136
    json.dump(R, open("reports/ts/phase_7_posthoc.json", "w"), indent=1, default=str)
    print(R["tests"], chk)


if __name__ == "__main__":
    main()
