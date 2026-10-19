# Phase 5 report: freeze preparation (nothing frozen)

Labels are **silver labels** (AI-made, cross-checked by independent AI passes and code checks; not human-verified). No Test-A, Test-B or unseen-filer filing was downloaded, opened, scored or tuned on.

## Prepared (all committed; none executed as a freeze)
- `reports/PREREGISTRATION_PROPOSED_FINAL.md`: final text with hypotheses H1-H6 (thresholds are proposals; dev reference values shown), splits, analysis plan, one-shot rule. `PREREGISTRATION.md` is still DRAFT.
- `scripts/freeze.py`: refuses to run without `reports/APPROVED_BY_OWNER.txt` (owner creates it) and a clean git tree; copies the proposed subsets into `data/splits/`, writes SHA256SUMS and `data/FREEZE_MANIFEST.json`, appends the hash table to `PREREGISTRATION.md`, tags `prereg-v1`. **Not run.**
- Split proposals (IDs only, from the local flat-file index): `data/splits/proposed/` : Test-A labelled 200 (sha256 `0bc380cc...`), Test-B 100 of 560 pool (receipt date on or after 2026-03-01, "likely after cutoff", sha256 `f9e12f29...`), unseen-filer 100 of 247 pool (sha256 `fd7174f9...`). Existing `dev_ids.txt` (`f11841a8...`) and `testA_ids.txt` (`89a89a5a...`) unchanged.
- Held-out injection attacks: `config/injection_heldout_v1.json` (30 sentences, sha256 `4e705645...`), written by a blind subagent that saw no verifier code.
- `docs/PHASE6_RUNBOOK.md`: exact commands. New generic commands: `split-fetch`, `label-select`, `label-export`, `label-compare`, `label-final`, `phase6-subsets`; eval modules take data paths from `TT_*` environment variables.
- Regression checks: the generic labelling pipeline reproduces `dev_silver_v1.json` byte for byte (same 113 items, same decisions, SHA-256 `d17a30a4...`); `phase3` results are identical after the changes; 51 tests pass. A leak was fixed before freezing: baseline B0's majority value now always comes from the dev labels, never from the split being scored.
- Dev reference values for the thresholds: paired B2 minus agent error for events 0.100 (0.035 to 0.172), for cause 0.039 (0.008 to 0.082); accepted event coverage 50.9%; injection 0/20 in-sample vs 5/20 raw.

## UNVERIFIED
Everything about the test splits; whether dev results generalise; the training cutoff of the model (so "likely after cutoff" is unverified); clean-hardware speed; silver-label correctness. Pass B and Pass C subagents were not shown each other's work, but all passes share one model family.
