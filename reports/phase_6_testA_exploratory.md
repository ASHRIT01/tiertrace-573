# Phase 6 Test-A: EXPLORATORY analyses (not preregistered endpoints; silver labels, AI-made, not human-verified)

From the existing Test-A outputs, scoring only, no model run. Primary amendment-1 settings; run-1 claims; run 2 only as the agreement filter (4 run-2 timeouts missing). Same paired filer-cluster bootstrap as H1 (2000 resamples, seed 0). The 'both' row reproduces the committed H1 exactly (checked by the script).

## (a) Decomposition of the H1 gain (events; unfiltered error 0.402, 1005 claims)

| accepted set | accepted | coverage | accepted error | delta = unfiltered - accepted [95% CI] |
|---|---|---|---|---|
| verifiers only (no verifier reason fired) | 662 | 0.659 | 0.296 | 0.106 [0.058, 0.160] |
| run-2 agreement only (ignoring verifiers) | 718 | 0.714 | 0.299 | 0.103 [0.057, 0.155] |
| both (= the accepted set of H1) | 536 | 0.533 | 0.267 | 0.135 [0.086, 0.192] |

The deltas are not additive: the two filters overlap, and the table says how much each does alone on this data, not a causal split.

## (b) Risk-coverage curve and AURC, events

Ordering (the frozen one, nothing new): frozen tt.eval.phase4 score: 0 if any verifier fired, else 1 + 2*[run 2 agrees] + [B1 agrees]; higher score accepted first; ties included fractionally (expected value under random tie-breaking); no model confidence.

Score counts (0..4): {0: 343, 1: 83, 2: 43, 3: 303, 4: 233}; N = 1005; error with no ranking = 0.402.

* AURC 0.269 [0.215, 0.332]
* risk@90% 0.379 [0.324, 0.441]; risk@70% 0.315 [0.258, 0.377]; risk@50% 0.262 [0.213, 0.319]

| coverage | 0.05 | 0.10 | 0.20 | 0.30 | 0.40 | 0.50 | 0.60 | 0.70 | 0.80 | 0.90 | 1.00 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| error among accepted | 0.180 | 0.180 | 0.180 | 0.215 | 0.245 | 0.262 | 0.278 | 0.315 | 0.351 | 0.379 | 0.402 |

Plot: `reports/phase_6_testA_riskcoverage_events.svg` (dashed line = no ranking). Because the score has only five values, ties are large and the curve is a few linear stretches.

## (c) Accepted vs unfiltered error, cause and supplier claims

| claim type | candidates | accepted (coverage) | unfiltered error [CI] | accepted error [CI] | delta [CI] |
|---|---|---|---|---|---|
| cause (NR-or-not detection) | 199 | 155 (0.779) | 0.161 [0.103, 0.223] (32 errors) | 0.026 [0.006, 0.058] (4 errors) | 0.135 [0.080, 0.198] |
| supplier claims | 70 | 20 (0.286) | 0.686 [0.526, 0.809] (48 errors) | 0.400 [0.062, 0.655] (8 errors) | 0.286 [0.054, 0.601] |

Supplier claims are few (the interval is wide); 39 company claims were excluded as unlabelled (named in the text, no silver claim). Cause = detecting NR-or-not only, never cause correctness.
