# Phase 2 report: dev-bench of both models on 100 silver-labelled dev filings

Scores are **vs silver labels** (AI-made, cross-checked by independent AI passes and code checks; not human-verified). Dev only.
**All speed and memory numbers were measured with Claude Code and other apps open, with 6-14 GB of swap in use, so they are not the clean hardware result.**
Full diagnosis: `reports/phase_2_diagnosis.md`; prompt log: `docs/PROMPT_LOG.md`.

## What changed
Real Ollama path fixed and exercised (raw output, `done_reason`, truncation flag, 300 s timeout, `--resume`, ETA, `--prompt`); silver scoring view (`tt.labels.protocol.prepare_gold`); diagnosis code `tt/eval/diagnose.py`; baselines `tt/baselines/rules.py`; prompt v2; verification layer `tt/verify/extra.py` (`verifier.py` not edited).

## Numbers (dev-bench, 100 filings, thinking off, temperature 0)
| | JSON-valid | gen tok/s | prompt tok/s | p50 / p95 s (all 100) | p95 excluding first call | truncated outputs |
|---|---|---|---|---|---|---|
| 4B q4_K_M v1 | 100% | 12.4 | 199.9 | 40.4 / 130.9 | 130.9 | 0 (no flag in this run's code; `done_reason` was "stop" for all 100 and prompt+output tokens peaked at 2383 of 6144) |
| 2B q8_0 v1 | 100% | 14.1 | 379.1 | 53.2 / 119.9 | 126.1 | 0 (flag false for all 100; max tokens 3467 of 6144) |
| 4B q4_K_M v2 | 100% | 16.6 | 168.2 | 40.4 / 100.2 | 114.0 | 0 (flag false for all 100; max tokens 3177 of 6144) |

Peak memory from `ollama ps`: 4B 3.2 GB and 2B 2.5 GB, 100% GPU, context 6144. `memory_pressure` free: 12-17%. Swap used 4-14 GB (macOS resizes it); before-run snapshots are in `runs/mem_before_*.txt`.
Gates (JSON-valid >= 95% and p95 <= 120 s): both models pass JSON; 4B v1 fails p95; 2B passes or fails p95 depending on whether the first call is counted; 4B v2 passes. No model fails both, so none is dropped and no other model is pulled.
Scores vs silver: see the table in `reports/phase_2_diagnosis.md` section 2 (4B v1 headline event F1 0.211, 2B 0.235, 4B v2 0.647 (dev-optimistic); cause accuracy 98% / 94% / 95%).

## Clean-measurement command (optional, do not wait for it)
Close other apps, then run: `cd "/Volumes/ASHI P1/Project A/tiertrace" && . .venv/bin/activate && python -u -m tt.cli dev-bench --model qwen3.5:4b-q4_K_M --labels data/labels/dev_silver_v1.json --out runs/clean_4b.jsonl --prompt v2 2>&1 | tee reports/hw_report.md`

## UNVERIFIED
Swap at the time of each call; clean-hardware speed; the 2B under prompt v2 (not run); correctness of the silver labels.
