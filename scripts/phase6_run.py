"""Phase 6 model runner (Amendment 1). Runs the FROZEN agent model over one split, run 1 or run 2, and writes runs/<split>_4b_v2_run<k>.jsonl.
Prints ONLY progress, timing and valid-JSON counts. It reads no gold label and computes no gold metric (the file list comes from the selection
config, which holds file names only). Resumes after any interruption and appends one line per start/restart to runs/<split>_run_log.txt.

  caffeinate -i .venv/bin/python scripts/phase6_run.py testA 1
  caffeinate -i .venv/bin/python scripts/phase6_run.py testA 2

Settings come from config/run_settings.json (model, prompt v2, think off, run1 temperature 0 seed 0, run2 temperature 0.5 seed 1, num_ctx 6144)."""
import json
import sys
import time
from pathlib import Path

import ollama

from tt.agent.run_dev import run, summarize

SPLITS = {"testA": ("config/testA_selection.json", "data/testA_raw"), "testB": ("config/testB_selection.json", "data/testB_raw"),
          "unseen": ("config/unseen_selection.json", "data/unseen_raw")}


def main(split: str, k: int):
    S = json.load(open("config/run_settings.json"))
    sel, pdf = SPLITS[split]
    files = [f["file"] for f in json.load(open(sel))["filings"] if not f["file"].startswith("._")]
    model, prompt = S["agent_model"], S["prompt"]
    r = S[f"run{k}"]
    assert S["think"] is False and prompt == "v2"
    ollama.show(model)   # raises if the server is down or the model is missing; never pulls
    out = Path(f"runs/{split}_4b_v2_run{k}.jsonl"); out.parent.mkdir(exist_ok=True)
    have = sum(1 for l in out.read_text().splitlines() if l.strip()) if out.exists() else 0
    log = Path(f"runs/{split}_run_log.txt")
    with open(log, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {'RESTART' if have else 'START'} | run {k} | records already in file: {have} of {len(files)}\n")
    print(f"model={model} prompt={prompt} think=False run{k} temperature={r['temperature']} seed={r['seed']} num_ctx={r['num_ctx']} filings={len(files)} "
          f"already_done={have} -> {out}", flush=True)
    recs = run(model, files, Path(pdf), out, r["num_ctx"], resume=True, timeout=300.0, prompt=prompt,
               extra_options={"temperature": r["temperature"], "seed": r["seed"], "presence_penalty": r["presence_penalty"]},
               progress=lambda i, n, x: print(f"  {i}/{n} {x['file']} {x['seconds']:.1f}s valid_json={x['extraction'] is not None} truncated={x.get('truncated')} "
                                              f"elapsed={x['elapsed']:.0f}s eta={x['eta']:.0f}s" + (f" ERROR {x['error'][:80]}" if x.get('error') else ""), flush=True))
    allr = [json.loads(l) for l in out.read_text().splitlines() if l.strip()]
    s = summarize(allr)
    with open(log, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | DONE | run {k} | records {len(allr)} | json_valid_rate {s['json_valid_rate']:.4f} | call errors {s['errors']}\n")
    print(f"\nDONE run{k}: records={len(allr)} of {len(files)} json_valid_rate={s['json_valid_rate']:.1%} call_errors={s['errors']} "
          f"gen_tokens/s={s['generation_tokens_per_s']:.1f} seconds/filing p50={s['seconds_p50_all']:.1f} p95={s['seconds_p95_all']:.1f}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
