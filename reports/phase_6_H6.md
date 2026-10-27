# H6 (speed, secondary): PASS

**Verdict: PASS.** JSON-valid rate 1.000 (>= 0.95) and p95 per-filing latency 80.1 s including the cold-load call (<= 120 s). Operational endpoint; it says nothing about accuracy. Scores printed by the bench are vs silver labels (AI-made, not human-verified) and are not part of H6.

| measure | value | threshold | result |
|---|---|---|---|
| json_valid_rate (100 filings, 0 call errors, 0 truncated) | 1.000 | >= 0.95 | PASS |
| p95 s/filing, all 100 (includes first cold-load call, 65.0 s): **verdict** | 80.1 | <= 120 | PASS |
| p95 s/filing, excluding first call (reported only) | 81.0 | | |
| p50 s/filing (all / excluding first) | 31.7 / 31.7 | | |
| max s/filing | 112.5 | | |
| generation / prompt tokens per second | 19.2 / 414.0 | | |

## What was run
Exactly the choice fixed before the run in `reports/H6_measurement_choice.md` (commit 75e4841): the `reports/phase_2.md` clean-measurement command, `dev-bench` on the 100 dev filings (`data/labels/dev_silver_v1.json`), qwen3.5:4b-q4_K_M, prompt v2, think off, temperature 0, seed 0, num_ctx 6144. The frozen H6 does not name filings or sample size; the 100 dev filings are the choice recorded in advance. The verdict p95 includes the first call (the stricter reading). Nothing frozen changed.

## Conditions
Apple M2, 8 GB RAM, macOS 15.6.1, Ollama 0.40.6; run started from Terminal.app with `caffeinate` on 2026-10-27/28 (output file written 00:23). Per the pre-declared clean condition: Claude Code, VS Code and other apps closed, Chrome Remote Desktop session disconnected (its host service stays installed, idle), AC power. These conditions are as stated by the owner, who ran it; the bench log does not record power state or free RAM, so they are not independently verified from the files. Free RAM at start was not captured.

## Caveats
Single run on one machine; dev filings, not Test-A. Latencies are per filing for one extraction call set (run 1 settings); the full pipeline with run 2 would double model time.

## Files
| file | SHA-256 |
|---|---|
| runs/H6_clean_4b.jsonl (100 records, 100 unique filings) | a568ea8d4e1dca5e508fa44185b6ec79ec3cfa36009946af7a71126cac46e6d6 |
| reports/H6_hw_report.md | d805d90a1aa02009f839f17a73eeeccacf5df70037e99a71fe1eb7848de67615 |

Figures above were recomputed from the jsonl (n=100, max 112.46 s, 100 valid extractions, 0 errors) and match the bench printout.
