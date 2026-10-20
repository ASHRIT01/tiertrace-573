# Phase 6 Test-A: primary results (silver labels: AI-made, not human-verified)
Frozen model qwen3.5:4b-q4_K_M, prompt v2; frozen scorer through the amendment-1 wrapper (`python -m tt.eval.amend1`); 199 readable filings (23V313 unreadable, excluded). Scored once, no change to prompt, verifiers, thresholds or scorer. Every claim is judged against silver labels, which are not independent of the pipeline (Pass C sided with Pass B, both Opus, in 73.5% of Test-A items); **no label-error figure is claimed**. Raw: `reports/phase_6_testA_endpoints.json` (sha256 b90599f2...0252, committed before any sensitivity run), `phase_6_testA_phase3.json`, `phase_6_testA_phase4.json`, `phase_6_testA_amend1_counts.json`.

## 1. H1 (primary): event error, B2 (all claims) minus agent (accepted claims), paired filer-cluster bootstrap
Pass if delta >= 0.05 AND 95% CI lower bound > 0 AND coverage >= 0.40.
| | value |
|---|---|
| B2 event error (all 1,005 claims) | 0.402 |
| agent event error (536 accepted claims) | 0.267 |
| **delta** | **0.1352**, 95% CI [0.0855, 0.1924] |
| coverage | 0.533 (536/1005) |
| **verdict (mechanical)** | **PASS** (0.1352 >= 0.05; 0.0855 > 0; 0.533 >= 0.40) |
Claims come from run 1; run 2 only enters as the agreement filter. Run 2 has 4 timeouts (kept as missing in the primary analysis), so those filings' run-1 claims cannot be accepted.

## 2. H2 and H5
* **H2** (NR-or-not detection of the cause field, B2 minus agent-accepted): delta 0.1350, 95% CI [0.0803, 0.1977]; threshold lower bound > 0: **PASS**. B2 error 0.161 (199 claims); agent accepted error 0.026 (155 accepted, coverage 0.779). Measures NR detection only, not cause correctness.
* **H5** (event error at full coverage, B1 minus B2): 0.1092, 95% CI [0.0308, 0.1765]; passes if lower bound > 0: **PASS**. B1 0.511 (624 claims), B2 0.402 (1,005 claims). B1's rules parallel Pass A's code (disclosed in the preregistration), which favours B1 and makes H5 conservative.
* H4 (attack success rate) is not part of this file: the held-out injection run has not been done.
* Exploratory (always with coverage): agent accepted-claim error 0.267 at coverage 53.3% (536/1005) vs B1 0.511 at full coverage. A lower error on fewer claims is not a like-for-like comparison.

## 3. Excluded gold events and ignored predictions (amendment-1 rule c)
* Excluded gold events (date text present, no ISO span): **27** of 1,445 non-contested gold events (1.87%), or 27 of 991 that carry a date text (2.72%); in 11 filings. Undated gold events are handled as in the frozen scorer.
* Ignored predictions (rule b): B1 3 of 627 predicted events (0.48%); B2 / agent run 1 1 of 1,006 (0.10%); B0 predicts no events.
* The 2% line is exceeded by the second share, so the two bounding runs are included below. Contested gold events dropped by the frozen preparation: 21.

## 4. Sensitivity runs (exploratory; none changes a verdict). H1 delta [95% CI], coverage, verdict
| variant | H1 delta | CI | coverage | H1 | H2 | H5 B1-B2 [CI] |
|---|---|---|---|---|---|---|
| primary | 0.1352 | [0.086, 0.192] | 0.533 | PASS | PASS | 0.109 [0.031, 0.177] |
| bound: unmatched predictions counted as errors (rule b off) | 0.1344 | [0.085, 0.191] | 0.534 | PASS | PASS | 0.111 [0.033, 0.178] |
| bound: filings with an excluded gold event dropped | 0.1203 | [0.072, 0.178] | 0.546 | PASS | PASS | 0.122 [0.040, 0.198] |
| contested items counted as misses | 0.1320 | [0.082, 0.189] | 0.533 | PASS | PASS | 0.109 [0.033, 0.176] |
| 56 filings with isolation slips dropped (837 event claims left) | 0.1455 | [0.093, 0.207] | 0.516 | PASS | PASS | 0.116 [0.024, 0.195] |
| exclusion definition `inferred_too` (35 excluded gold events) | 0.1342 | [0.084, 0.192] | 0.534 | PASS | PASS | 0.111 [0.033, 0.178] |
| the 4 run-2 timeouts retried once (separate file, never merged) | 0.1406 | [0.090, 0.197] | 0.548 | PASS | PASS | 0.109 [0.031, 0.177] |
The retry of the four timeouts returned valid JSON for all four (87-103 s each); run-1 claims of those filings could then be accepted (accepted 551 instead of 536). The slip sensitivity includes the filing with outside knowledge (24V556-5723). Raw: `reports/phase_6_testA_sens/*.json`; retry outputs `runs/testA_4b_v2_run2.retry_timeouts.jsonl` (sha256 57447842...b302) and the scoring-only copy `runs/testA_4b_v2_run2.sens_with_retry.jsonl`.

## 5. Context (not part of the verdicts)
Per claim type, event error with 95% CI (phase 3): B2 0.402 [0.347, 0.466]; B1 0.511 [0.446, 0.572]; S2 supplier claims: B2 0.686 (70 claims) and agent accepted 0.400 (20 accepted claims, wide interval [0.062, 0.655]); cause-reported detection: B0 0.327, B1 0.060, B2 0.161. Run 1 JSON-valid 199/199; run 2 195/199 after one retry of an infrastructure error (4 timeouts). Operational timings from the runs (apps open, not the H6 measurement): p95 130 s (run 1), 184 s (run 2).
