# Phase 6 secondary splits: Test-B and unseen-filer (EXPLORATORY, not the primary endpoint)

All numbers are **exploratory**: the preregistration lists Test-B and unseen-filer results as exploratory (compared with Test-A, with intervals) and makes no pass/fail claim for them. They are scored against **silver labels (AI-made, cross-checked, not human-verified)**, which are not independent of the pipeline (Pass C sided with Pass B, both Opus, in 72.2% of Test-B and 77.6% of unseen items); **no label-error figure is claimed**. Frozen model qwen3.5:4b-q4_K_M, prompt v2, think off, num_ctx 6144; run 1 temperature 0 seed 0 supplies every scored claim, run 2 (temperature 0.5, seed 1) only the agreement filter. Frozen scorer through the amendment-1 wrapper (`python -m tt.eval.amend1`, primary settings), scored once per split. Nothing in the prompt, verifiers, thresholds or scorer changed. Test-A (primary) is in `reports/phase_6_testA_primary.md`.

## 1. Results
Paired filer-cluster bootstrap, 2000 resamples, seed 0. delta = B2 event error (all claims) minus agent event error (accepted claims). The code also prints a mechanical pass flag for H1/H5 against the Test-A thresholds; it is not repeated here as a verdict.

| | Test-A (reference, primary) | **Test-B** | **unseen-filer** |
|---|---|---|---|
| filings scored | 199 | 100 | 98 |
| non-contested gold events / with a date text | 1,445 / 991 | 790 / 527 | 569 / 436 |
| gold events excluded (amendment 1) | 27 (11 filings) | 4 (2 filings) | 3 (3 filings) |
| event claims, B2 (all) | 1,005 | 510 | 444 |
| accepted event claims / coverage | 536 / 0.533 | 263 / 0.516 | 231 / 0.520 |
| event error, B2 (all claims) | 0.402 | 0.386 [0.306, 0.456] | 0.417 [0.345, 0.503] |
| event error, agent accepted | 0.267 | 0.354 [0.244, 0.461] | 0.329 [0.258, 0.412] |
| event error, B1 (full coverage) | 0.511 (624 claims) | 0.532 (327 claims) [0.410, 0.639] | 0.504 (230 claims) [0.435, 0.565] |
| **H1 delta (B2 - agent), 95% CI** | 0.1352 [0.0855, 0.1924] | **0.0327 [-0.0244, 0.0984]** | **0.0877 [0.0219, 0.1587]** |
| **H5 (B1 - B2), 95% CI** | 0.1092 [0.0308, 0.1765] | **0.1458 [0.0639, 0.2048]** | **0.0877 [-0.0103, 0.1612]** |
| agent accepted vs B1 (exploratory, with coverage) | 0.267 at 53.3% vs 0.511 | 0.354 at 51.6% vs 0.532; diff 0.178 [0.120, 0.227] | 0.329 at 52.0% vs 0.504; diff 0.175 [0.077, 0.253] |
| **H2 (cause NR-or-not), B2 - agent, 95% CI** | 0.1350 [0.0803, 0.1977] | **0.2739 [0.1103, 0.4712]** | **0.1003 [0.0384, 0.1712]** |
| cause error: B2 / accepted (coverage) | 0.161 / 0.026 (0.779) | 0.290 / 0.016 (62 of 100, 0.62) | 0.112 / 0.012 (84 of 98, 0.857) |
| cause error, B1 / B0 | 0.060 / 0.327 | 0.100 / 0.400 | 0.061 / 0.276 |
| supplier claims (candidates; B2 error [CI]) | 70; 0.686 [0.526, 0.809] | 35; 0.629 [0.375, 0.792] | 38; 0.579 [0.375, 0.766] |
| supplier claims accepted (coverage); error [CI] | 20 (0.286); 0.400 [0.062, 0.655] | 13 (0.371); 0.231 [0.000, 0.529] | 20 (0.526); 0.300 [0.000, 0.565] |
| company claims excluded as unlabelled | 39 | 15 | 29 |
| run-2 missing (timeouts / crashes / invalid) | 4 timeouts (1 crash retried) | **0** | **0** |
| ignored predictions (rule b): B2 and agent / B1 | 1 of 1,006 / 3 of 627 | 14 of 524 (2.7%) / 1 of 328 | 1 of 445 (0.2%) / 1 of 231 |
| injection (H4) | 2/30 (Test-A hosts) | not applicable | not applicable |

Reading, without a verdict: on Test-B the H1 interval includes 0 and the point delta is about a quarter of Test-A's; on unseen-filer the H1 interval excludes 0 but the H5 interval includes 0; the cause (H2) differences are positive and their intervals exclude 0 on both. Supplier-claim figures rest on 13 and 20 accepted claims and have very wide intervals. The injection set (H4) was written for, and run on, 30 Test-A host filings; it does not apply to these splits and was not run on them.

## 2. Amendment-1 counts and bounding runs
* Excluded gold events (date text, no ISO span): Test-B 4 (26V279 `20 to 24-Apr-2026`; 26V307 `January through February` x2 and `April through August`), 0.51% of events (0.76% of dated events). Unseen 3 (24E067 `February 29`, 24V203 `March12, 2024`, 26E004 `12/16/20205`), 0.53% (0.69%).
* Test-B ignored predictions (rule b) were 14 of 524 agent/B2 events (2.7%), all in the two filings above, which exceeds the 2% line, so the two pre-declared bounding runs were added (`reports/phase_6_testB_sens/`): rule b off (unmatched predictions counted as errors): H1 delta 0.0466 [-0.0223, 0.1362], coverage 0.504 (264/524), H5 0.1309 [0.0270, 0.2018], H2 0.2739 [0.1103, 0.4712]; affected filings dropped (496 claims): H1 delta 0.0191 [-0.0392, 0.0750], coverage 0.524, H5 0.1577 [0.0794, 0.2150], H2 0.2793 [0.1147, 0.4731]. The H1 interval includes 0 in all three Test-B variants. Unseen is under the line (no bounding runs required).

## 3. Diagnosis of Test-B's small H1 delta (descriptive, nothing changed)
* The accepted claims are not much cleaner than the unfiltered ones on Test-B (0.354 vs 0.386), against 0.267 vs 0.402 on Test-A. The verifiers rejected 39% and run 2 disagreed on 20% of the 510 event claims.
* Errors are concentrated in a few templated filers. Ford is 85 of 510 claims (16.7%) with 0.541 error, and its 34 accepted claims have 0.676 error; Jayco is 20 claims at 0.700, its 19 accepted at 0.684. Other large filers look like Test-A (FCA 42 claims, accepted error 0.185; Altec 27, 0.125). These are filings with repeated committee-meeting or long boilerplate chronologies, where the quoted text is verbatim (so the verifiers pass) but silver event typing often differs.
* A one-off, post hoc diagnostic (not a result and not part of any endpoint): without the Ford cluster the Test-B H1 delta is 0.0496 [-0.0117, 0.1130] at coverage 0.539, still below Test-A's. Whether the shortfall is the agent or silver-labelling conventions for committee events (typing OTHER vs DECISION, per the logged rule problems) is not settled by this data.
* Nothing looked broken: Test-B has 100/100 and unseen 98/98 JSON-valid records in both runs, no run-2 gaps, and the same code path as Test-A.

## 4. What ran, restart history, errors
| split | run | start | done | records | JSON-valid | call errors |
|---|---|---|---|---|---|---|
| Test-B | 1 | 2026-10-25 15:19:16 | 2026-10-25 17:52:00 | 100 | 100% | 0 |
| Test-B | 2 | 2026-10-25 17:52:03 (empty file); RESTART 2026-10-27 11:48:06; START 11:48:29 | 2026-10-27 12:46:55 | 100 | 100% | 0 |
| unseen | 1 | 2026-10-27 12:47:02 | 2026-10-27 13:39:30 | 98 | 100% | 0 |
| unseen | 2 | 2026-10-27 13:39:32 | 2026-10-27 14:30:00 | 98 | 100% | 0 |
* **Cause of the only interruption:** `pmset` shows the Mac entered Low Power Sleep at 2026-10-25 17:56:21 while on battery at 1% charge (the Ollama log stops mid-generation at the same time; the machine rebooted at 19:22:49). The runner and Ollama processes were lost with it; Test-B run 1 was already complete and run 2 had written no record. Resumed 2026-10-27 on AC power after checking Ollama 0.40.6 and the `qwen3.5:4b-q4_K_M` digest `d8b0f5e9760c...` (unchanged). The chain then ran under `scripts/phase6_supervise.sh` (one model process at a time, restart-on-exit logic); it never had to intervene (no SUPERVISOR or OLLAMA-restart lines).
* Errors: none. No timeouts, no crashes, no invalid-JSON outputs, nothing retried, no run-2 gaps. All four files checked: unique filing IDs, equal to the selection lists, last line complete.
* The pre-resume backups are `runs/testB_4b_v2_run{1,2}.pre_resume_20261027_114805.jsonl` (run 2's is the empty file).

## 5. Files and hashes
| file | records | SHA-256 |
|---|---|---|
| runs/testB_4b_v2_run1.jsonl (= its pre_resume backup) | 100 | 237744acf4b55975bdeb800002cf09f6727122cdc661515393c6dcb96a99f2a4 |
| runs/testB_4b_v2_run2.jsonl | 100 | 6a3b15c893cdc9765f064581cdb795900c3b558d50ac2824a69f6302396592f0 |
| runs/unseen_4b_v2_run1.jsonl | 98 | 2de2357b39efd14fdb9b68b3ebfff8440c63d8c0936254b9e86527c7656faf7e |
| runs/unseen_4b_v2_run2.jsonl | 98 | 22d63e4f636427fd91e439bf400603be257645050d9cd378318716aacc6c50e8 |
| runs/testB_4b_v2_run2.pre_resume_20261027_114805.jsonl (empty) | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
Scoring outputs: `reports/phase_6_{testB,unseen}_{endpoints,phase3,phase4,amend1_counts}.json`, `reports/phase_6_testB_sens/*.json`.
