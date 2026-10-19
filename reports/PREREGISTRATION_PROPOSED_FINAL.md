# TierTrace-573 preregistration: PROPOSED FINAL TEXT (not frozen; the owner reviews, edits thresholds and approves)

Status: **DRAFT until the owner creates `reports/APPROVED_BY_OWNER.txt` and runs `python scripts/freeze.py`.** `PREREGISTRATION.md` stays DRAFT until then.
Wording rule: results say a supplier is "named in the filing as component manufacturer", never that it "caused" or is "responsible for" a recall.

## 0. What the labels are
**All labels are silver labels: AI-made, cross-checked by independent AI passes and code checks. No label is human-verified.** All three label passes (A, B, C)
and the models under test come from one model family, so agreement between them is not independent evidence of correctness. Every score is "vs silver labels".
Dev silver labels: `data/labels/dev_silver_v1.json`, SHA-256 `d17a30a4c710e1aadb46fb773f2b4759cea49eea3ba5457279ae3441be46f35e` (100 filings; 16 contested items excluded from scoring).
Dev A-vs-B agreement: S1 100%, S2 93.0%, cause 99.0%, upstream 97.0%, events 68.7% (headline-type events 73.1%); event-type agreement given a matching date 84.8% (Wilson 81.1-87.9%).

## 1. What was tuned on dev (everything below is already fixed; nothing is tuned on a test split)
Prompt v2 (`tt/agent/run_dev.py`, log `docs/PROMPT_LOG.md`), verifier layer `tt/verify/extra.py`, agent rules `tt/agent/agent.py` (V1, V2a, V2b, V3, V3o, V4, V4r, E1 with inherited dates,
S2n, V8), second-run settings (temperature 0.5, seed 1), run 1 settings (temperature 0, seed 0, presence_penalty 0, context 6144, thinking off), acceptance rule (no verifier failed AND run 2 agrees), B1 rules (`tt/baselines/rules.py`, never tuned),
`tt/verify/verifier.py` (never edited). Models: qwen3.5:4b-q4_K_M (agent, B2) and qwen3.5:2b-q8_0 (dev only; not part of the Phase 6 agent). The optional 2B-to-4B cascade was not built.
**v2 and the agent were designed after seeing dev results, and the v2 event-type definitions are copied from the rules that define the silver labels, so dev scores are optimistic.**

## 2. Splits (IDs only; hashes written by `scripts/freeze.py`)
| split | definition | size | file |
|---|---|---|---|
| Dev | 2015-2022, 50 campaigns per year, seed 0 (already drawn) | 400 campaigns (100 silver-labelled) | `data/splits/dev_ids.txt` sha256 `f11841a8...` |
| Test-A | 2023 to Feb 2026, allocated by year, seed 0 (already drawn) | 1,000 campaigns | `data/splits/testA_ids.txt` sha256 `89a89a5a...` |
| Test-A labelled | 200 random Test-A campaigns (seed 0): the scored set for H1-H4 | 200 | `data/splits/proposed/testA_labelled_ids.txt` sha256 `0bc380cc...` |
| Test-B | campaigns with flat-file receipt date on or after 2026-03-01 (V/E, not audit-sample), 100 drawn at random (seed 0). **Called "likely after the model training cutoff"; the cutoff is not known precisely: UNVERIFIED.** The flat-file date is the campaign receipt date, not the Part 573 submission date | 100 of a pool of 560 | `data/splits/proposed/testB_ids.txt` sha256 `f9e12f29...` |
| Unseen-filer | Test-A campaigns whose filer has no campaign in dev, outside the Test-A labelled set, 100 drawn at random (seed 0) | 100 of a pool of 247 | `data/splits/proposed/unseen_filer_ids.txt` sha256 `fd7174f9...` |
| Injection | 30 held-out attack sentences written by a blind subagent that saw no verifier code (`config/injection_heldout_v1.json`, sha256 `4e705645...`), one per Test-A labelled filing | 30 | |
The Test-A, Test-B and unseen-filer filings have not been downloaded or read. Sizes (200/100/100) are proposals for the owner to change before freezing.
Only the latest Part 573 version of each campaign is evaluated. Unreadable (no text layer) or empty filings are excluded and counted in every table; no replacement filings are drawn after results are seen.

## 3. Hypotheses (thresholds are PROPOSALS for the owner to set; dev values are shown for reference only)
Old H1-H6 are superseded as follows: old H1 (masked-block parent-supplier recovery) becomes the report-only supplier-claim analysis (dev has 24 recoverable cases; 20% of filings name the supplier in the narrative); old H2 becomes H1 and H4; old H3 becomes the event reporting in H1/H2; old H4 (tier/locus) is cut; old H5 (4-bit vs full precision) is not tested (no full-precision model fits the 8 GB machine); old H6 is cut.
| ID | Hypothesis | Proposed threshold | Dev reference |
|---|---|---|---|
| H1 (headline) | On Test-A labelled, the error among accepted **event** claims (verifiers + two-run agreement) is lower than the error among all event claims from the single pass (B2) | paired difference B2 minus agent >= 0.05, 95% filer-cluster bootstrap interval above 0 | 0.100 (0.035 to 0.172) |
| H2 | Same comparison for the **cause-reported** claim | paired difference interval above 0 | 0.039 (0.008 to 0.082) |
| H3 | Abstention is not trivial: accepted event claims cover at least a minimum share of all event claims | coverage >= 40% | 50.9% |
| H4 | Prompt injection: on the 30 held-out attacks, attack success rate after verifiers + agreement | <= 10%; raw (no-verifier) rate is reported | dev (in-sample, 20 fixtures): 0/20 vs 5/20 raw |
| H5 | The agent's event error among accepted claims is no worse than baseline B1's error at full coverage | point estimate <= B1's | agent 0.281, B1 0.476 |
| H6 | Speed gates measured by the owner on clean hardware (Claude Code and other apps closed) | JSON-valid >= 95% and p95 <= 120 s per filing | measured with apps open: 100%, p95 100-114 s |
Descriptive, no threshold: supplier-claim error among accepted claims (dev has only 27 candidate claims), date-only and date+type event F1, AURC, risk at 50/70/90% coverage, results on Test-B and unseen-filer (compared with Test-A with intervals), B0 and B1 baselines, B2 and agent per claim type. B1 beating the LLM is reported plainly.
Primary test: H1 only; the rest are secondary and reported without correction for multiple comparisons.

## 4. Analysis plan
Claim types: supplier claims (S2-type companies), event claims (all six types; headline five-type F1 also reported), cause-reported claim. Correctness rules are those in `reports/phase_3.md`.
Excluded and counted: contested labels, unlabelled companies (named in the text, no silver claim), unreadable filings. Curves: risk-coverage with deterministic score (0 if a verifier failed, else 1 + 2 x run-2 agreement + B1 agreement); ties are included fractionally. No model confidence is ever used.
Intervals: filer-cluster bootstrap, 2,000 resamples, seed 0, percentile 95%. Event matching: equal type and date-span overlap at the coarser granularity; fuzzy dates scored separately.

## 5. One-shot rule and reporting
Model outputs for each split are produced once (run 1, run 2). No rerun, prompt, rule, threshold or label change after the first Test-A score is seen; any deviation is written in `reports/deviations.md` with the reason and the unmodified results are still reported. Negative and null results are reported. Nothing is described as human-verified.

## 6. Frozen artifacts
`scripts/freeze.py` records the git commit and the SHA-256 of: dev labels (A, B, C decisions, final), labelling rules, prompt log and the Pass B/C prompts, held-out attacks, model and override configs, the verifier, agent, baseline, evaluation and labelling code, the split files and this document.
