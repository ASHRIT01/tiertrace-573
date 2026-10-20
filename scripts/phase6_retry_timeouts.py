"""Sensitivity only (owner decision 2026-10-20): re-run the four run-2 timeouts ONCE with run 2's frozen settings into a SEPARATE file; the primary run-2 file is never touched.
Then builds runs/testA_4b_v2_run2.sens_with_retry.jsonl (primary records with those four replaced) for the exploratory scoring only. Prints no result content."""
import json
import time
from pathlib import Path

from tt.agent.run_dev import run

NAMES = ["RCLRPT-25V507-9357.pdf", "RCLRPT-25V544-9834.pdf", "RCLRPT-25V562-5431.pdf", "RCLRPT-25V565-4354.pdf"]
S = json.load(open("config/run_settings.json")); r = S["run2"]
prim = Path("runs/testA_4b_v2_run2.jsonl"); out = Path("runs/testA_4b_v2_run2.retry_timeouts.jsonl")
assert not out.exists()
P = [json.loads(l) for l in prim.read_text().splitlines() if l.strip()]
assert all(next(x for x in P if x["file"] == n).get("timeout") for n in NAMES)
with open("runs/testA_run_log.txt", "a") as f:
    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | SENSITIVITY RETRY of the 4 run-2 timeouts (separate file, once) | {', '.join(NAMES)}\n")
recs = run(S["agent_model"], NAMES, Path("data/testA_raw"), out, r["num_ctx"], resume=False, timeout=300.0, prompt=S["prompt"],
           extra_options={"temperature": r["temperature"], "seed": r["seed"], "presence_penalty": r["presence_penalty"]},
           progress=lambda i, n, x: print(f"  {i}/{n} {x['file']} {x['seconds']:.1f}s valid_json={x['extraction'] is not None}" + (f" ERROR {x['error'][:60]}" if x.get('error') else ""), flush=True))
byf = {x["file"]: x for x in recs}
merged = [byf.get(x["file"], x) for x in P]
Path("runs/testA_4b_v2_run2.sens_with_retry.jsonl").write_text("".join(json.dumps(x) + "\n" for x in merged))
print("valid after retry:", sum(x["extraction"] is not None for x in recs), "of", len(recs))
