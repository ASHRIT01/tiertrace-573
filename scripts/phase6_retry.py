"""Deviation tool (docs/AMENDMENT_1.md, owner decision of 2026-10-20): re-run ONLY records in which NO model call completed (infrastructure error:
connection refused, model runner stopped, ...), with the frozen settings of that run. Timeouts and invalid-JSON outputs are never retried (refused here).
The original failed record is kept in runs/<split>_4b_v2_run<k>.pre_retry.jsonl; the retried record replaces it at the same line. Prints no result content.
  .venv/bin/python scripts/phase6_retry.py testA 2 RCLRPT-25V574-1873.pdf"""
import json
import shutil
import sys
import time
from pathlib import Path

from tt.agent.run_dev import run
from scripts.phase6_run import SPLITS

INFRA = ("refused", "connect", "unexpectedly stopped", "unreachable", "reset by peer", "eof", " 502", " 503")


def main(split, k, names):
    S = json.load(open("config/run_settings.json")); r = S[f"run{k}"]
    out = Path(f"runs/{split}_4b_v2_run{k}.jsonl"); pdf = Path(SPLITS[split][1])
    lines = [json.loads(l) for l in out.read_text().splitlines() if l.strip()]
    pre = out.with_name(out.stem + ".pre_retry.jsonl")
    if not pre.exists():
        shutil.copy(out, pre)    # whole original file, byte for byte
    for name in names:
        i = next(j for j, x in enumerate(lines) if x["file"] == name)
        old = lines[i]; err = (old.get("error") or "").lower()
        assert old.get("extraction") is None and err and not old.get("timeout") and "timed out" not in err and old.get("eval_count") is None and not old.get("raw"), \
            f"{name}: not a retry-eligible record (a model call completed, or it is a timeout / invalid-JSON output)"
        assert any(s in err for s in INFRA), f"{name}: error is not an infrastructure error: {err[:80]}"
        for attempt in range(1, 4):
            tmp = Path(f"runs/_retry_{k}.jsonl"); tmp.unlink(missing_ok=True)
            new = run(S["agent_model"], [name], pdf, tmp, r["num_ctx"], resume=False, timeout=300.0, prompt=S["prompt"],
                      extra_options={"temperature": r["temperature"], "seed": r["seed"], "presence_penalty": r["presence_penalty"]})[0]
            tmp.unlink(missing_ok=True)
            e2 = (new.get("error") or "").lower()
            print(f"{name} attempt {attempt}: seconds={new['seconds']:.1f} valid_json={new['extraction'] is not None} error={e2[:70]!r}", flush=True)
            if not (e2 and any(s in e2 for s in INFRA) and not new.get("timeout")):   # a model call completed (or timed out): keep this result, stop
                break
            time.sleep(10)
        lines[i] = new
        with open("runs/testA_run_log.txt", "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | RETRY (infrastructure error, no model call completed) | run {k} | {name} | attempts {attempt} | valid_json {new['extraction'] is not None}\n")
    out.write_text("".join(json.dumps(x) + "\n" for x in lines))


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3:])
