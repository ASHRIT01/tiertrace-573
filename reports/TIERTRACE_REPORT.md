# TierTrace-573: verified extraction of supplier and timeline facts from NHTSA Part 573 recall filings

**All labels in this project are silver labels: made by AI (code plus Claude models) and cross-checked by other AI passes. No human checked any label.** Every error rate below is an error against these silver labels. It can be too high (the label is wrong and the model right) or too low (the model repeats a mistake the labellers also made). No label-error rate is claimed anywhere.

How to read the sources: every number carries the file it comes from and the commit it was read from, in the form `file@commit`. The full list, with the exact text each number matches, is in section 9, and `scripts/writeup_claims.py` re-checks it with `git show`.

---

## 1. Problem

A Part 573 Safety Recall Report is the form a vehicle or equipment maker files with NHTSA when it decides to recall. Two free-text parts of it hold facts that matter for supply-chain research:
- **The chronology:** when the maker heard of a problem, opened an investigation, decided to recall and filed.
- **The supplier block and the cause narrative:** which companies are named in the filing as component manufacturers.

NHTSA publishes a flat file of recall campaigns, but it has no structured field for the chronology's dates or event types. The supplier fields are filled unevenly. Turning the chronology into data therefore means reading PDFs.

**Closest prior work.** Astvansh, Ball and Josefy (2022), "The Recall Decision Exposed: Automobile Recall Timing and Process Data Set", *Manufacturing & Service Operations Management* 24(3): 1457–1473, doi 10.1287/msom.2022.1085.
- It hand-codes 2,120 recalls by 27 automakers, 2009–2018.
- Verified against the RePEc record and the accepted manuscript (McGill); this is the one cited fact not taken from a committed report (section 9, item X1).
- TierTrace does not reproduce that dataset and has not yet been compared with it (section 8).

**What TierTrace tries.**
- A small local model (4 billion parameters, 4-bit) reads one filing and proposes claims.
- Each claim cites a verbatim quote.
- Deterministic code then checks every claim, and the agent keeps a claim only if it passes every check and a second, differently sampled run agrees. Otherwise it abstains.
- The question is whether this check-and-abstain step lowers the error of the claims it keeps, without abstaining on almost everything.

---

## 2. Data and splits

All filings are public NHTSA documents, fetched at no more than one request per second with an identifying user agent. Only the latest Part 573 version of each campaign is used.

| split | how drawn | size | readable / scored | source |
|---|---|---|---|---|
| dev | 2015–2022, 50 campaigns per year, seed 0 | 400 campaigns, 100 silver-labelled | 100 | `PREREGISTRATION_PROPOSED_FINAL.md@9d8a6de` |
| Test-A | 2023 to Feb 2026, 1,000 campaigns drawn; 200 labelled at random (seed 0) | 200 | **199 scored** (23V313 has no text layer) | same; `AMENDMENT_1.md@8525779` |
| Test-B | receipt date on or after 2026-03-01; 100 drawn from a pool of 560 | 100 | 100 | same |
| unseen-filer | Test-A campaigns whose filer has no dev campaign; 100 drawn from a pool of 247 | 100 | **98** (23V320 and 24V945 have no text layer) | same |

The splits differ in what they test:
- **Test-B** is described in the preregistration as "likely after the model training cutoff". The cutoff is not known precisely, so this is unverified.
- **Unseen-filer** tests manufacturers the agent was never developed on.
- **Unreadable filings** were excluded and never replaced. No OCR was used.

**Silver labels (three passes).**
- **Pass A:** code (`tt/labels/draft.py`, `events.py`, `dates.py`) plus per-filing corrections written by the Claude Code session (declared model claude-sonnet-5-5 for the test splits).
- **Pass B:** an independent blind labelling by Claude subagents (declared claude-opus-5-5).
- **Pass C:** adjudicates only where A and B differ (declared claude-opus-5-5). It sees the two answers as "version X" and "version Y" in a seeded random order and is never told which pass made which.

The final labels are Pass A plus Pass C's corrections. Contested items are dropped from scoring and counted. The model names are aliases passed to the subagent tool, and the mapping to exact versions cannot be proven (`config/labelling_model.json`). Labelling was blind to model outputs: the labelling code refuses any path under `runs/`, and all three splits were labelled before any model ran on them.

| split | filings | silver events | contested (dropped) | Pass C sided with Pass B | Pass C sided with Pass A |
|---|---|---|---|---|---|
| Test-A | 199 | 1,466 | 21 | 73.5% | 9.2% |
| Test-B | 100 | 806 | 16 | 72.2% | 10.2% |
| unseen-filer | 98 | 580 | 12 | 77.6% | 8.5% |

Source: `reports/phase_6_labels.md@f77af17`.

**Independence is weak.**
- Pass B and Pass C are the same model family. Pass C sided with Pass B in 72–78% of items, so B and C agreeing is not independent evidence that a label is right.
- All three passes are Claude, and the same assistant wrote the labelling rules on dev after seeing dev model results.
- The agent's event-type definitions were copied from those rules, which may flatter the agent on event typing.
- The rule baseline B1 parallels Pass A's code, which may flatter B1.
- None of these biases is measured (`PREREGISTRATION_PROPOSED_FINAL.md@9d8a6de`, section 0.2c).
- Event typing is the weakest part of the labels: on dev, Pass A and Pass B agreed on events only 68.7% of the time (same source).

**Isolation slips.** Three labelling subagents read a file outside their batch directory, covering 56 filings. One of them used outside knowledge for a single supplier call (24V556-5723). These filings are dropped in a sensitivity run (`DEVIATIONS.md@75e4841`, `AMENDMENT_1.md@8525779`).

---

## 3. Method

**Extractor.**
- **Model:** `qwen3.5:4b-q4_K_M` served by Ollama 0.40.6, model digest `d8b0f5e9760c…` (`PREREGISTRATION.md@b2c5ed5`).
- **Settings:** prompt v2, thinking off, context 6,144 tokens.
- **Two runs:** run 1 uses temperature 0, seed 0; run 2 uses temperature 0.5, seed 1 (same source).
- **Output:** the model reads the cause, chronology and component sections and returns one JSON object with:
  - companies, with their role;
  - dated events, each with one of six types: SUPPLIER_NOTICE, FILER_AWARENESS, INVESTIGATION_START, DECISION, NHTSA_FILING, OTHER;
  - whether a cause is reported;
  - a verbatim evidence quote for each claim.
- **Statuses:** each evidence item has a status of SUPPORTED, CONTRADICTED, INSUFFICIENT or NOT_REPORTED (`tt/agent/schemas.py`).
- **Which run is scored:** all scored claims come from run 1. Run 2's own claims are never scored.

**Verifiers** (deterministic; "the model proposes, code disposes"):
- **`tt/verify/verifier.py`, V1–V5** (never edited):
  - V1: the quote is verbatim in the claimed section.
  - V2: a company name is in the text or alias table, and the filer is not listed as its own supplier.
  - V3: the date is valid, not before 1990, not after the filing, and events are in a consistent order.
  - V4: a cause given as "not reported" must stay not reported.
  - V5: supply-path members are extracted companies.
- **`tt/verify/extra.py` and `tt/agent/agent.py`, extra rules:**
  - V2a/V2b: name in text; the filer is not a supplier unless it is the block supplier.
  - V3: dates checked with the span parser.
  - V3o: event order.
  - V4r: a stated cause must be reported.
  - E1: the event's date text lies inside its quote, or is the nearest preceding date.
  - S2n: the supplier name is verbatim in the narrative, otherwise INSUFFICIENT.
  - V8: no instruction-like text in a quote or name, as a prompt-injection guard.

These are listed in the frozen text, `PREREGISTRATION_PROPOSED_FINAL.md@9d8a6de`, section 1.

**Acceptance and abstention.**
- A claim is accepted only if no verifier fired and run 2 agrees with it. Otherwise the agent abstains on it.
- Model confidence is never used.
- A fixed rank score orders claims for risk-coverage curves: 0 if any verifier fired, otherwise 1 + 2 × (run 2 agrees) + (B1 agrees). A claim is accepted at a score of 3 or more.

**Baselines.**
- **B0:** always gives the dev-majority answer.
- **B1:** hand-written rules (keyword event typing and date regexes; never tuned).
- **B2:** the same model's run-1 output with no verifiers and no abstention.

The comparison of B2 with the agent isolates what the check-and-abstain step adds.

**Event scoring.** An event claim is right if a silver event of the same type has an overlapping date at the coarser of the two granularities. An unparseable date is wrong. Intervals come from a filer-cluster bootstrap: 2,000 resamples, seed 0, percentile 95% (`config/thresholds.json@969a65c`).

**Cause scoring.** Only whether the cause is reported or not is scored ("NR detection"). The cause text itself is never scored.

---

## 4. Preregistration and deviations

**Freeze.**
- The protocol was frozen at tag `freeze-v1`, commit **b2c5ed5**, before any test labelling or model run.
- The freeze record hashes the prompt, the output schema, both verifier files, the scorer code, the thresholds, the labelling prompts and rules, the split files, the model digests and the Ollama version (`PREREGISTRATION.md@b2c5ed5`).
- The owner chose H1 as the only primary endpoint.

The endpoints are:

| ID | tier | what | pass rule (`config/thresholds.json@969a65c`) |
|---|---|---|---|
| H1 | **primary** | event error: B2 on all claims minus agent on accepted claims, Test-A | delta ≥ 0.05 **and** 95% CI lower bound > 0 **and** coverage ≥ 0.40 |
| H2 | secondary | NR detection of the cause field, B2 minus agent-accepted | CI lower bound > 0 |
| H4 | secondary | prompt injection, 30 held-out attacks, success rate after verifiers + agreement | ≤ 0.10, always reported with the exact one-sided 95% Clopper-Pearson bound |
| H5 | secondary | event error at full coverage, B1 minus B2 | CI lower bound > 0 |
| H6 | secondary (operational) | JSON-valid rate and p95 seconds per filing on clean hardware | ≥ 0.95 and ≤ 120 s |
| E | exploratory | Test-B, unseen-filer, AURC, supplier claims, and others | none |

The preregistration also commits to a negative-result rule. If H1 had failed, every write-up would open with "the primary endpoint was not met", and no secondary result could stand in for it.

**Amendment 1** (tag `amendment-1`, commit **8525779**), written before any Test-A model output existed:
- **The problem:** the frozen date parser crashed on some date texts, for example "mid-April" with no year.
- **The fix:** a wrapper (`tt/eval/amend1.py`) patches the parser at run time, leaving the frozen files byte-identical. It applies three rules:
  - (a) Gold events whose date text cannot be parsed to a date are excluded.
  - (b) In such filings, an unmatched prediction of the same type is ignored.
  - (c) If either share exceeds 2%, two bounding runs are added.
- **Tests:** the wrapper reproduces the dev Phase 4 results byte-for-byte, and synthetic tests cover the guard.
- **Other contents:** it pre-declares three sensitivity runs and records the label-independence statement. It also states that the prompt, verifiers and thresholds cannot change after any Test-A output exists; only crash fixes are allowed.
- **Effect on Test-A:** 27 of 1,445 gold events (1.87%) were excluded (`AMENDMENT_1.md@8525779`).

**H6 measurement choice** (commit **75e4841**, made before the H6 run):
- The frozen H6 does not name the filings or say how to treat the model's cold-load call.
- The owner fixed this in advance: the 100 dev filings, with the cold-load call included in the verdict p95 (the stricter reading), on clean hardware.

**Deviations** (`reports/DEVIATIONS.md@75e4841`, every entry, grouped; none changes a frozen rule):
| group | entries |
|---|---|
| Procedure | D-P1 batch-orchestration script added after the freeze. D-P2 the Pass B prompt says "20 files" but batches are 25, so the count was substituted. D-P3 Pass C item ids restart per batch. D-P4 `.gitignore` extended. D-P5 lighter Pass A override effort than on dev. D-P6/D-P7 a line added to the subagent prompts: keep helper scripts inside the batch directory. D-P8 from Test-A batch 5, Pass A overrides based on a compact sheet, which lowers Pass A quality. |
| Tool issues | D-T1 the label selector silently drops PDFs with no text layer (23V313, later 23V320 and 24V945). D-T2 the frozen date parser crashes on year-less fuzzy dates and invalid calendar dates; labelling used a run-time guard and scoring is handled by amendment 1. D-T3 the Pass A supplier quote is not verbatim for the 2025+ form layout, so per-filing quote overrides were used, applied mechanically by `scripts/phase6_fixq.py`, plus manual overrides for multi-supplier blocks. |
| Labelling-rule problems (logged, not fixed) | Unsettled by the rules: sentences reporting both awareness and the start of an investigation (no tie-break; seen in Test-A b02/b05/b07 and unseen b04); date ranges as one event or two; DECISION vs OTHER for committee or supplier decisions; meetings and record reviews as OTHER vs INVESTIGATION_START; amendment lines as NHTSA_FILING vs OTHER; production-window dates read as events; day-prefixed date formats ("20. Jan 2023", "16-Sep-2026"); splitter fragments ("R. H. Sheppard", "lbs."); pointer chronologies; typo dates; pairing artefacts where A and B labelled different sentences of one entry. Filings are listed per batch in the source. |
| Isolation | Three slips (56 filings, one outside-knowledge call), tested by the pre-declared sensitivity run. Several agents had a tool-output spill saved outside their directory that they did not open. Unseen-filer Pass C agents were interrupted by a rate limit and resumed. |
| Test-A runs | Run 1 had no errors. Run 2 was interrupted and restarted with 167 of 199 records written; the cause of the interruption is not recorded in the run log. Run 2 had four 300 s timeouts (kept as missing) and one runner crash with no model call completed (retried once, per the owner's rule). The four timeouts were retried once in a separate sensitivity file that was never merged. |
| Later | H4 run; exploratory analyses (the cluster t-bound failed its own validity check); Test-B and unseen-filer scored once, with Test-B's 2% trigger adding the bounding runs; H6 measurement choice. |
| Battery-death restart | On 2026-10-25 17:56:21 the Mac went into Low Power Sleep on battery at 1% charge and rebooted at 19:22:49, killing the runner and Ollama during Test-B run 2. Run 2 had written no record and run 1 was complete. Resumed on 2026-10-27 at 11:48:06 on AC power, after re-checking the Ollama version and the model digest, under a supervisor script (`phase_6_secondary_splits.md@ef19956`). |

---

## 5. Results

### 5(a) PREREGISTERED: Test-A endpoints and H6

**The primary endpoint H1 was met.** Event-claim error fell from 0.402 for the unfiltered model (1,005 claims) to 0.267 among the 536 claims the agent accepted. That is a delta of **0.1352, 95% CI [0.0855, 0.1924], at coverage 0.533**. All three pass conditions hold.

*Tier: preregistered. Silver labels, not checked by a human.*
| endpoint | result | rule | verdict | source |
|---|---|---|---|---|
| **H1** (primary) | delta 0.1352 [0.0855, 0.1924]; coverage 0.533 (536/1005); B2 0.402 → agent 0.267 | ≥ 0.05, lower > 0, coverage ≥ 0.40 | **PASS** | `phase_6_testA_primary.md@37f93c9` |
| H2 | delta 0.1350 [0.0803, 0.1977]; B2 0.161 → agent 0.026 at coverage 0.779 | lower > 0 | PASS | same |
| H4 | 2/30 = 0.067 after verifiers + agreement; exact one-sided 95% Clopper-Pearson upper bound **0.195**; raw 11/30 = 0.367 | ≤ 0.10 | PASS (point estimate only) | `phase_6_H4.md@b9611e0` |
| H5 | B1 − B2 = 0.1092 [0.0308, 0.1765]; B1 0.511 (624 claims), B2 0.402 | lower > 0 | PASS | `phase_6_testA_primary.md@37f93c9` |
| H6 | JSON-valid 1.000; p95 **80.1 s** including the 65.0 s cold-load call (81.0 s without it); p50 31.7 s; max 112.5 s. H6 PASS on 100 dev filings with apps closed (p95 80.1 s); on Test-A filings with apps open, p95 was 130 s (run 1) / 184 s (run 2) (A13), so longer recent filings with other apps running can exceed 120 s. | ≥ 0.95; ≤ 120 s | PASS | `phase_6_H6.md@08d7916` (output file committed in e0a5892) |

Notes on each endpoint:
- **H1, H2 and H5 rest on run 2.** These claims come from run 1, with run 2 used as the agreement filter. Run 2 had 4 timeouts, kept as missing, so those filings' claims could not be accepted.
- **H1 robustness.** All seven sensitivity and bounding runs pass H1. Delta ranges from 0.1203 [0.072, 0.178] (filings with an excluded gold event dropped) to 0.1455 [0.093, 0.207] (isolation-slip filings dropped). With the four timeouts retried, delta is 0.1406 at coverage 0.548 (`phase_6_testA_primary.md@37f93c9`).
- **H2 is not cause accuracy.** It measures only whether a cause is reported. The V4/V4r rules are close to B1's rule, so this number largely reflects those rules.
- **H5 is conservative.** B1's rules parallel Pass A's code, which favours B1.
- **H4 bound.** With 30 attacks the data cannot rule out a true attack success rate of up to 19.5%. A bound below 10% would have needed 0 successes (0/30 gives 0.095; `PREREGISTRATION_PROPOSED_FINAL.md@9d8a6de`).
- **H4 blind spot.** Both remaining successes are the `suppress_events` attack, which makes the model return an empty event list. An absent claim gives no verifier anything to check, so this attack is outside what the design can catch. The other attacks behaved differently: `flip_cause` succeeded 6 of 6 times in the raw model and 0 times after the verifiers (`phase_6_H4.md@b9611e0`). On ordinary Test-A filings, run 1 returned an empty list for 4 of 199 filings (2.0%), none of which had a gold event. Under `suppress_events`, 2 of 6 attacks produced one (`phase_6_exploratory_2.md@805a34c`).
- **H6 conditions.** One run on the 100 dev filings with `qwen3.5:4b-q4_K_M`, on an Apple M2 with 8 GB, macOS 15.6.1 and Ollama 0.40.6. It was started from Terminal.app with other apps closed, as stated by the owner, who ran it. The log does not record power state or free RAM, so the clean condition is not independently verified.
- **Speed on Test-A.** H6 PASS on 100 dev filings with apps closed (p95 80.1 s); on Test-A filings with apps open, p95 was 130 s (run 1) / 184 s (run 2) (A13), so longer recent filings with other apps running can exceed 120 s. Sources: `phase_6_H6.md@08d7916`, `phase_6_testA_primary.md@37f93c9`. The H6 pass applies to the clean condition only.

### 5(b) EXPLORATORY (named as secondary splits in the freeze): Test-B and unseen-filer

The freeze lists these splits as exploratory, compared with Test-A with intervals and with no pass or fail. The scoring code still prints mechanical pass flags against the Test-A thresholds; they are not verdicts. **On Test-B the H1 interval includes 0. On unseen-filer the H5 interval includes 0.**

*Tier: exploratory. Silver labels, not checked by a human.* Source: `phase_6_secondary_splits.md@ef19956` (Test-A column: `phase_6_testA_primary.md@37f93c9`).
| | Test-A (reference) | **Test-B** | **unseen-filer** |
|---|---|---|---|
| filings scored | 199 | 100 | 98 |
| event claims, B2 | 1,005 | 510 | 444 |
| accepted / coverage | 536 / 0.533 | 263 / 0.516 | 231 / 0.520 |
| event error, B2 | 0.402 | 0.386 [0.306, 0.456] | 0.417 [0.345, 0.503] |
| event error, agent accepted | 0.267 | 0.354 [0.244, 0.461] | 0.329 [0.258, 0.412] |
| event error, B1 | 0.511 (624) | 0.532 (327) | 0.504 (230) |
| **H1 delta** | 0.1352 [0.0855, 0.1924] | **0.0327 [−0.0244, 0.0984]** | 0.0877 [0.0219, 0.1587] |
| **H5 (B1 − B2)** | 0.1092 [0.0308, 0.1765] | 0.1458 [0.0639, 0.2048] | **0.0877 [−0.0103, 0.1612]** |
| H2 | 0.1350 [0.0803, 0.1977] | 0.2739 [0.1103, 0.4712] | 0.1003 [0.0384, 0.1712] |
| supplier claims accepted; error | 20; 0.400 [0.062, 0.655] | 13; 0.231 [0.000, 0.529] | 20; 0.300 [0.000, 0.565] |
| run-2 missing | 4 timeouts | 0 | 0 |

- **Test-B ignored predictions.** Test-B ignored 14 of 524 predictions under rule b (2.7%), above the 2% line. The two bounding runs also have H1 intervals that include 0: 0.0466 [−0.0223, 0.1362] with rule b off, and 0.0191 [−0.0392, 0.0750] with the affected filings dropped.
- **H4 scope.** The injection set was written for Test-A host filings and was not run on these splits.

### 5(c) POST HOC: failure analysis and other exploratory analyses (not preregistered)

None of this was planned before the results were seen, and none of it is a result in the preregistered sense. It uses the existing outputs and the frozen scorer only, with no reruns.

**Most wrong accepted claims have the right date but a different type.** The scoring code sorted every accepted event claim that was scored wrong into classes (`phase_6_failure_analysis.md@b67c054`, section a):

*Tier: post hoc.*
| | Test-A | Test-B | unseen-filer |
|---|---|---|---|
| accepted / scored wrong | 536 / 143 | 263 / 93 | 231 / 76 |
| date matches a gold event, type differs | 122 (85.3%) | 80 (86.0%) | 57 (75.0%) |

**Date-only view.** If the type is ignored, the gap between B2 and the agent narrows but stays positive on every split, and the Test-B interval excludes 0 (same file, section b):

*Tier: post hoc, not preregistered.*
| split | B2 error | agent accepted error | delta [95% CI] |
|---|---|---|---|
| Test-A | 0.142 | 0.039 | 0.103 [0.051, 0.172] |
| Test-B | 0.100 | 0.049 | 0.051 [0.022, 0.090] |
| unseen-filer | 0.153 | 0.078 | 0.075 [0.032, 0.135] |

The date-only view is lenient: a date can coincide with an unrelated gold event, so it understates date errors somewhat. It shows that wrong or invented dates do not drive the Test-B shortfall.

**Type agreement compared with the labellers** (`phase_6_failure_analysis.md@3c8b7cb`, section e). The comparison is between two rates on date-matched events:
- **Labellers:** how often Pass A's type agrees with Pass B's.
- **Agent:** how often the agent's accepted claims agree with the final labels.

*Tier: post hoc. Wilson 95% intervals.*
| split | Pass A vs Pass B | agent vs final label | reading |
|---|---|---|---|
| Test-A | 0.788 [0.762, 0.812] | 0.763 [0.725, 0.798] | similar |
| Test-B | 0.786 [0.748, 0.820] | 0.680 [0.620, 0.735] | agent below |
| unseen-filer | 0.827 [0.788, 0.861] | 0.728 [0.664, 0.783] | agent below |

- **Test-B gap.** The gap sits where the labellers agreed with each other: Jayco 26/29 for the labellers against 6/18 for the agent, and Ford 53/79 against 11/31. These counts are small.
- **Shared confusions.** Four of the six most frequent type confusions are shared by the agent and the labellers. The largest for both is INVESTIGATION_START vs OTHER: 32.9% of labeller disagreements and 39.2% of the agent's.
- **Awareness vs investigation.** FILER_AWARENESS vs INVESTIGATION_START is 20.8% of the agent's confusions but 6.4% of the labellers'. That matches the logged rule gap for sentences reporting both awareness and the start of an investigation (section 4).
- **Cannot separate the cause.** The data cannot tell the agent's mistyping apart from how the adjudicated labels typed these filers.
- **Different references.** The two rates are measured against different references (raw passes vs adjudicated labels), and matching is lenient on both sides.

**Erratum on "repeated chronologies"** (`phase_6_secondary_splits.md@b67c054`, section 3). An earlier note attributed Test-B's errors to Ford and Jayco filings with repeated chronologies. That is only partly supported:
- Within a filing there is almost no repetition.
- Across Ford filings, about 33% of chronology entries recur.
- Only 2 accepted-wrong claims anywhere are within-filing duplicates (`phase_6_failure_analysis.md@b67c054`).
- The data do not show that repetition causes errors.

**Leave-Ford-out diagnostic** (one-off, post hoc; `phase_6_secondary_splits.md@ef19956`). Ford accounts for 85 of Test-B's 510 claims, with error 0.541; its 34 accepted claims have error 0.676. Without Ford, Test-B's delta is 0.0496 [−0.0117, 0.1130] at coverage 0.539, still below Test-A's, with an interval that still includes 0.

**What each filter contributes on Test-A** (exploratory; `phase_6_testA_exploratory.md@6c34d05`, `phase_6_exploratory_2.md@805a34c`).
- **Each filter alone:** verifiers alone give delta 0.106 at coverage 0.659; run-2 agreement alone gives 0.103 at coverage 0.714. The two overlap and are not additive.
- **Shapley shares** (they sum to the H1 delta):
  - run-2 agreement 0.065 [0.038, 0.097];
  - V3 unparseable date 0.031;
  - E1 0.026;
  - the other rules near 0.
- **Interpretation:** these split the gain on this data and say nothing about causes.
- **AURC (events):** 0.269 [0.215, 0.332].

**Label-noise tipping point** (exploratory; `phase_6_exploratory_2.md@805a34c`). Suppose some accepted claims marked correct are really wrong, which is the direction that most flatters the agent:
- H1's point threshold fails when 24.9% of those claims are wrong (98 claims, 9.7% of all event labels).
- The CI lower bound reaches 0 at 26.7% (105 claims, 10.4%).

This is one scenario in one direction, not an estimate of label noise.

---

### 5(d) POST-FREEZE PROTOCOL `ts-protocol-1`, SILVER REFERENCE: TS-1 timeliness screen

*Tier: post-freeze protocol `ts-protocol-1` (tag on commit 246e30e, fixed before any gap was computed), silver reference (AI-generated, not checked by a human). A screening signal, not a legal finding.*

**What it measures.** The screen measures a **self-reported decision-to-original-filing gap**: the working days from the DECISION date a filer wrote in its chronology to the filing date.
- Working days are Mon–Fri excluding observed federal holidays; this is an assumption, since Part 573 does not define them.
- A filing is FLAGGED if the gap is certainly above 5 working days, NOT_FLAGGED if it is certainly at most 5, and INDETERMINATE otherwise.
- The decision date comes from the silver labels (reference) or from the agent's accepted claims.
- The legally relevant trigger can be earlier than any chronology date, so the gap is at best a lower bound. That premise is stated without a citation: the two candidate sources could not be opened.

**Population.** 305 defect filings out of 397; the 92 noncompliance filings are reported separately (`reports/phase_7_timeliness.md@2157cf1`).

**How to read it.**
- **The primary is not interpretable as decision-to-filing timing.** The primary filing date is the processed PDF's Submission Date, and the primary FLAGGED share (104/305 = 0.341 W[0.290, 0.396]) is dominated by amended versions.
  - 98 of the 104 FLAGGED filings are amended versions, against 6/136 among originals.
  - An amended version's Submission Date equals RCDATE (NHTSA's received date) in only 15 of 169, and RCDATE is earlier by a median of 35 calendar days.
  - The primary stays as defined.
- **The interpretable figures** are two pre-declared checks. Their confidence intervals were added after seeing the results:

*Tier: post-freeze protocol ts-protocol-1, silver reference; CIs added after seeing results.*
| figure | reference FLAGGED [Wilson; filer-cluster bootstrap] | gap_mid median [IQR] p90 (working days) | agent coverage | agent worst-case bounds on FLAGGED share | agent vs reference κ / PABAK (n both) |
|---|---|---|---|---|---|
| RCDATE as the filing date | 19/305 = 0.062 [0.040, 0.095]; [0.033, 0.096] | 5 [3–5] 6 | 126/305 (0.413) | 0.049 – 0.649 | 0.809 / 0.938 (121) |
| originals stratum (Submission Date = RCDATE in 131/136) | 6/136 = 0.044 [0.020, 0.093]; [0.013, 0.086] | 5 [3–5] 6 | 52/136 (0.382) | 0.015 – 0.654 | 0.383 / 0.912 (51; no reference FLAGGED among them: unstable) |

**Other results.**
- **Missing decision dates:** 88 of 305 defect filings (0.289) have no usable DECISION date in the silver reference.
- **Agent coverage:** the agent has an accepted, dated DECISION claim for 127/305 (0.416).
- **Agreement:** where both have a date, Cohen's κ is 0.937. Both mostly quote the same sentence, so the agreement says nothing about which date is legally relevant.
- **Amendment TS-A1:** a crash-only parser guard on 2 filings, affecting 0 anchors.
- **Population caveat:** defect vs noncompliance is typed by a flat-file FMVSS proxy for the 186 filings on the 2025+ form, which has no type field.

### 5(e) POST-FREEZE PROTOCOL `sc-protocol-1`: SC-1 supplier claims against the filer's own declaration

*Tier: post-freeze protocol `sc-protocol-1` (tag on commit 24f7c34, fixed before any claim was compared). Reference = filer-declared supplier (non-AI, not ground truth).*

**The reference.** The reference is the "Component Manufacturer" block a filer completes under 49 CFR 573.6(c)(2)(iv).
- **What a match means:** the declared supplier may be an assembler, the entity the part was obtained from, or the filer itself. A match measures fidelity to the declaration, not who made the part. A non-match is not an error by the filer.
- **Parsing:** the block parses in 397/397 filings.
- **Population:** 261 filings declare one or more external suppliers. Another 47 declare the filer itself, 4 an obtained-from entity, and 85 nothing (`reports/phase_8_supplier_check.md@f35dfb6`).

**The agent never saw the block.** Its frozen input is the cause and chronology, with the block name masked. So agent matches are recoveries from the narrative.

*Tier: post-freeze protocol sc-protocol-1; exact normalised-name match; Wilson 95% CIs.*
| claims | filing-level recall | claim-level precision |
|---|---|---|
| agent, all supplier claims | 18/261 = 0.069 [0.044, 0.106] | 19/172 = 0.110 [0.072, 0.166] |
| agent, gate-accepted | 13/261 = 0.050 [0.029, 0.083] | 14/70 = 0.200 [0.123, 0.308] |
| silver S2 (narrative names the supplier) | 92/261 = 0.352 [0.297, 0.412] | 92/113 = 0.814 [0.733, 0.875] |
| silver S1 (read from the block; circular) | — | 254/261 = 0.973 |

**Reading the table.**
- **Recall:** agent recall is low and bounded by the masking.
- **Precision understates:** a correct sub-supplier named only in the narrative counts as a non-match. Precision is higher at the pre-declared containment and fuzzy levels; for accepted claims it is 27/70 and 29/70 respectively.
- **Silver S2:** this is the first non-AI check of the silver supplier labels. They agree with the filer's declaration in 81% of narrative claims.
- **Agent vs silver:** a filing matched by the agent but not by silver never occurs.
- **Components:** not run, because neither the agent schema nor the silver labels contain component claims.
- **Amendment SC-A1:** the name field of the Pass-C silver claims; 23 of these claims fall in the population and are labelled POST HOC.

## 6. What failed or is unknown

- **Test-B H1.** The delta is 0.0327 with an interval that includes 0, about a quarter of Test-A's. It stays near 0 in both bounding runs and without Ford. The check-and-abstain step did not show a clear gain on filings from after March 2026.
- **Unseen-filer H5.** The model did not show a clear advantage over the rule baseline B1 at full coverage on new manufacturers: 0.0877, interval [−0.0103, 0.1612].
- **Event typing generalises poorly to new filers.** The agent's type agreement falls below the labellers' on Test-B (0.680 vs 0.786) and unseen-filer (0.728 vs 0.827), and is lowest for some manufacturers (Test-B Jayco 6/18, Ford 11/31).
- **Supplier claims.** These are few and noisy. Accepted error is 23–40% (0.231, 0.300, 0.400) on 13–20 accepted claims per split, with intervals up to 0.655.
- **Cluster t-bound.** A cluster-sum t-bound on accepted-claim error was tried as an exploratory guarantee and failed its own validity check:
  - false-certification rates were 0.0115–0.0273 for events and 0.0481–0.2056 for cause, against a required ≤ 0.01 (`phase_6_exploratory_2.md@805a34c`);
  - its numbers (for example an events upper bound of 0.324) are not guarantees.
- **Label independence.** Pass C sided with Pass B in 72–78% of items, both are the same model family, and the agent's type definitions come from the labelling rules. Shared errors are invisible.
- **No human check.** No label was checked by a human, so every error rate here is relative to AI labels.
- **H4 limits.** There were only 30 attacks (upper bound 0.195). They were written by a Claude instance (same family as the labellers and the verifier author) and target the Qwen model. The empty-output attack is outside the design.
- **H6 limits.** One run, one machine, dev filings, with the clean condition as stated by the owner. H6 PASS on 100 dev filings with apps closed (p95 80.1 s); on Test-A filings with apps open, p95 was 130 s (run 1) / 184 s (run 2) (A13), so longer recent filings with other apps running can exceed 120 s.
- **Cause correctness is not measured.** Only "cause reported or not" is scored.

---

## 7. Cost and hardware

- **Hardware:** everything ran on one Apple M2 laptop with 8 GB RAM, one model process at a time.
- **Inference cost:** model inference was local through Ollama, so there was no per-call charge (US$0).
- **Labelling cost:** the Claude subagents used for labelling (Passes B and C) ran on the owner's Claude subscription. Their cost and token use were not recorded and are not reported here.

*Run times, from the logged timestamps.* Durations are differences of logged timestamps.
| run | start → done | wall time |
|---|---|---|
| Test-A run 1 (199) | 2026-10-20 12:48:52 → 16:10:07 | 3 h 21 min |
| Test-A run 2 (199) | 16:10:10 → interrupted, restart 21:32:45 (167 done) → 22:12:05 | not computable (interruption) |
| Test-B run 1 (100) | 2026-10-25 15:19:16 → 17:52:00 | 2 h 33 min |
| Test-B run 2 (100) | restarted after battery death; 2026-10-27 11:48:29 → 12:46:55 | 58 min |
| unseen run 1 (98) | 12:47:02 → 13:39:30 | 52 min |
| unseen run 2 (98) | 13:39:32 → 14:30:00 | 50 min |

Sources: `DEVIATIONS.md@75e4841` and `phase_6_secondary_splits.md@ef19956`.

**Operational lessons.**
- **The restart.** Test-B run 2 was lost when the laptop ran its battery to 1% and slept (section 4). After that, runs were made on AC power under a supervisor script that restarts the runner and Ollama.
- **Speed varies with the machine's state.** H6 PASS on 100 dev filings with apps closed (p95 80.1 s); on Test-A filings with apps open, p95 was 130 s (run 1) / 184 s (run 2) (A13), so longer recent filings with other apps running can exceed 120 s.

---

## 8. Future work

1. **External validation against the MSOM hand-coded data** (Astvansh, Ball and Josefy 2022). Compare TierTrace's dates and event types with human coding on the overlapping recalls. No comparison with human labels has been made in this project yet. The supplementary data file has not been obtained yet.
2. **An awareness-vs-investigation rule.** Add a tie-break for sentences that report both, the largest gap specific to the agent in section 5(c). This changes the labelling rules and the prompt, so it needs a v2 with a new freeze and new held-out data. It cannot be applied to the current results.
3. **Post-2018 extension.** The MSOM data end in 2018; TierTrace covers 2015–2026 filings. A combined, longer series would need validation on the overlapping years before use.
4. **Prediction-powered inference for labelling cost.** Use a small human-labelled sample to correct estimates made on many AI-labelled filings. This could turn silver-label error rates into interval estimates against human judgement while labelling only a small sample by hand.

---

## 9. Claims list

Every number used above and in `README.md`, with its source file and the commit it was read from. "Matched text" is the exact string that `scripts/writeup_claims.py` finds in `git show <commit>:<file>` (¦ stands for a table bar).

- **Result of the check when this report was written:** 156 claims checked, 0 mismatches.
- **Durations in section 7:** these are arithmetic on checked timestamps (H1, H5–H8). H3 is split into H3, H3b and H3c so that the timeouts, the crash and its single retry are each matched.
- **X1 is outside the check:** item X1 is the only number not from a committed report; it is verified against the RePEc record and the accepted manuscript.

| # | claim | source | commit | matched text |
|---|---|---|---|---|
| D1 | dev: 400 campaigns, 100 silver-labelled | `reports/PREREGISTRATION_PROPOSED_FINAL.md` | 9d8a6de | `400 campaigns (100 silver-labelled)` |
| D2 | Test-A: 1,000 campaigns drawn, 200 labelled | `reports/PREREGISTRATION_PROPOSED_FINAL.md` | 9d8a6de | `¦ 200 ¦ `data/splits/proposed/testA_labelled_ids.txt`` |
| D2b | Test-A: 1,000 campaigns, 2023 to Feb 2026 | `reports/PREREGISTRATION_PROPOSED_FINAL.md` | 9d8a6de | `¦ Test-A ¦ 2023 to Feb 2026, allocated by year, seed 0 (already drawn) ¦ 1,000 campaigns ¦` |
| D3 | Test-B: 100 of a pool of 560 | `reports/PREREGISTRATION_PROPOSED_FINAL.md` | 9d8a6de | `100 of a pool of 560` |
| D4 | unseen-filer: 100 of a pool of 247 | `reports/PREREGISTRATION_PROPOSED_FINAL.md` | 9d8a6de | `100 of a pool of 247` |
| D5 | dev Pass A vs Pass B event agreement 68.7% | `reports/PREREGISTRATION_PROPOSED_FINAL.md` | 9d8a6de | `events 68.7%` |
| D6 | Test-A labels: 199 records, 1,466 events, 21 contested | `reports/phase_6_labels.md` | f77af17 | `199 records, 1,466 events, 21 contested` |
| D7 | Test-B labels: 100 records, 806 events, 16 contested | `reports/phase_6_labels.md` | f77af17 | `100 records, 806 events, 16 contested` |
| D8 | unseen labels: 98 records, 580 events, 12 contested | `reports/phase_6_labels.md` | f77af17 | `98 records, 580 events, 12 contested` |
| D9 | Pass C sided with Pass B: Test-A 73.5% | `reports/phase_6_labels.md` | f77af17 | `with Pass B in 296 (73.5%)` |
| D10 | Pass C sided with Pass B: Test-B 72.2% | `reports/phase_6_labels.md` | f77af17 | `with Pass B in 148 (72.2%)` |
| D11 | Pass C sided with Pass B: unseen 77.6% | `reports/phase_6_labels.md` | f77af17 | `with Pass B in 128 (77.6%)` |
| D12 | Pass C sided with Pass A: Test-A 9.2% | `reports/phase_6_labels.md` | f77af17 | `with Pass A in 37 items (9.2%)` |
| D12b | Pass C sided with Pass A: Test-B 10.2% | `reports/phase_6_labels.md` | f77af17 | `with Pass A in 21 items (10.2%)` |
| D12c | Pass C sided with Pass A: unseen 8.5% | `reports/phase_6_labels.md` | f77af17 | `with Pass A in 14 items (8.5%)` |
| D13 | unreadable filings excluded: 23V313 (Test-A), 23V320 and 24V945 (unseen) | `docs/AMENDMENT_1.md` | 8525779 | `23V313 (Test-A), 23V320 and 24V945 (unseen-filer)` |
| D14 | isolation slips: 3 slips, 56 filings | `reports/DEVIATIONS.md` | 75e4841 | `3 slips, 56 filings` |
| R1 | H1 pass rule: delta >= 0.05 | `config/thresholds.json` | 969a65c | `"delta_point_min": 0.05` |
| R2 | H1 pass rule: CI lower bound > 0 | `config/thresholds.json` | 969a65c | `"delta_ci95_lower_gt": 0.0` |
| R3 | H1 pass rule: coverage >= 0.40 | `config/thresholds.json` | 969a65c | `"coverage_min": 0.4` |
| R4 | H4 pass rule: attack success rate <= 0.10 | `config/thresholds.json` | 969a65c | `"attack_success_rate_max": 0.1` |
| R5 | H6 pass rule: JSON-valid >= 0.95 | `config/thresholds.json` | 969a65c | `"json_valid_min": 0.95` |
| R6 | H6 pass rule: p95 <= 120 s | `config/thresholds.json` | 969a65c | `"p95_seconds_max": 120` |
| R7 | bootstrap: 2,000 resamples, seed 0, filer cluster | `config/thresholds.json` | 969a65c | `"resamples": 2000` |
| R8 | dev reference for H1: 0.100 (0.035 to 0.172), coverage 50.9% | `reports/PREREGISTRATION_PROPOSED_FINAL.md` | 9d8a6de | `Delta 0.100 (0.035 to 0.172), coverage 50.9%` |
| R9 | Ollama version at freeze 0.40.6 | `PREREGISTRATION.md` | b2c5ed5 | `ollama version is 0.40.6` |
| R10 | agent model digest d8b0f5e9760c... | `PREREGISTRATION.md` | b2c5ed5 | `digest d8b0f5e9760cd1682034f292d7ef72ec46f432149be0df7574bf2d6e92e38c04` |
| R11 | run 1 temperature 0 seed 0; run 2 temperature 0.5 seed 1; num_ctx 6144 | `PREREGISTRATION.md` | b2c5ed5 | `run 1 {'temperature': 0.0, 'seed': 0, 'presence_penalty': 0, 'num_ctx': 6144}; run 2 {'temperature': 0.5, 'seed': 1, 'presence_penalty': 0, 'num_ctx': 6144}` |
| R12 | H6 apps-open dev reference: 100% JSON-valid, p95 100-114 s | `reports/PREREGISTRATION_PROPOSED_FINAL.md` | 9d8a6de | `with apps open: 100%, p95 100-114 s` |
| R13 | CP bound with 0/30 successes would be 0.095 | `reports/PREREGISTRATION_PROPOSED_FINAL.md` | 9d8a6de | `0/30 -> 0.095` |
| R14 | excluded gold events under amendment 1, Test-A: 27 of 1,445 (1.87%) | `docs/AMENDMENT_1.md` | 8525779 | `Test-A 27 of 1,445 non-contested gold events (1.87%, 11 filings)` |
| R15 | H6 verdict p95 includes the cold-load call (fixed before the run) | `reports/H6_measurement_choice.md` | 75e4841 | `The verdict p95 INCLUDES the first cold-load call` |
| A1 | Test-A B2 event error 0.402 (1,005 claims) | `reports/phase_6_testA_primary.md` | 37f93c9 | `¦ B2 event error (all 1,005 claims) ¦ 0.402 ¦` |
| A2 | Test-A agent accepted event error 0.267 (536 claims) | `reports/phase_6_testA_primary.md` | 37f93c9 | `¦ agent event error (536 accepted claims) ¦ 0.267 ¦` |
| A3 | H1 delta 0.1352, 95% CI [0.0855, 0.1924] | `reports/phase_6_testA_primary.md` | 37f93c9 | `**0.1352**, 95% CI [0.0855, 0.1924]` |
| A4 | H1 coverage 0.533 (536/1005) | `reports/phase_6_testA_primary.md` | 37f93c9 | `0.533 (536/1005)` |
| A5 | H2 delta 0.1350, 95% CI [0.0803, 0.1977] | `reports/phase_6_testA_primary.md` | 37f93c9 | `delta 0.1350, 95% CI [0.0803, 0.1977]` |
| A6 | H2: B2 error 0.161, agent accepted 0.026, coverage 0.779 | `reports/phase_6_testA_primary.md` | 37f93c9 | `B2 error 0.161 (199 claims); agent accepted error 0.026 (155 accepted, coverage 0.779)` |
| A7 | H5 (B1 - B2) 0.1092, 95% CI [0.0308, 0.1765] | `reports/phase_6_testA_primary.md` | 37f93c9 | `0.1092, 95% CI [0.0308, 0.1765]` |
| A8 | B1 event error 0.511 (624 claims) | `reports/phase_6_testA_primary.md` | 37f93c9 | `B1 0.511 (624 claims)` |
| A9 | run 2: 4 timeouts kept as missing | `reports/phase_6_testA_primary.md` | 37f93c9 | `Run 2 has 4 timeouts` |
| A10 | sensitivity runs: lowest H1 delta 0.1203 [0.072, 0.178] | `reports/phase_6_testA_primary.md` | 37f93c9 | `¦ bound: filings with an excluded gold event dropped ¦ 0.1203 ¦ [0.072, 0.178] ¦` |
| A11 | sensitivity runs: highest H1 delta 0.1455 [0.093, 0.207] | `reports/phase_6_testA_primary.md` | 37f93c9 | `¦ 0.1455 ¦ [0.093, 0.207] ¦` |
| A12 | timeouts retried (sensitivity): H1 delta 0.1406, coverage 0.548 | `reports/phase_6_testA_primary.md` | 37f93c9 | `¦ 0.1406 ¦ [0.090, 0.197] ¦ 0.548 ¦` |
| A13 | Test-A operational p95 (apps open): 130 s run 1, 184 s run 2 | `reports/phase_6_testA_primary.md` | 37f93c9 | `p95 130 s (run 1), 184 s (run 2)` |
| A14 | H4: 2/30 = 0.067 after verifiers + agreement | `reports/phase_6_H4.md` | b9611e0 | `**2/30 = 0.067**` |
| A15 | H4: exact one-sided 95% Clopper-Pearson upper bound 0.195 | `reports/phase_6_H4.md` | b9611e0 | `Clopper-Pearson upper bound: **0.195**` |
| A16 | H4 raw (no verifier): 11/30 = 0.367, bound 0.533 | `reports/phase_6_H4.md` | b9611e0 | `¦ 11/30 ¦ 0.367 ¦ 0.533 ¦` |
| A17 | H4 residual successes: suppress_events 2 of 6 | `reports/phase_6_H4.md` | b9611e0 | `¦ suppress_events ¦ 2 ¦ 2 ¦ 2 ¦` |
| A18 | H4 flip_cause: 6 raw, 0 after verifiers | `reports/phase_6_H4.md` | b9611e0 | `¦ flip_cause ¦ 6 ¦ 0 ¦ 0 ¦` |
| A19 | empty event lists in Test-A run 1: 4 of 199 (2.0%) | `reports/phase_6_exploratory_2.md` | 805a34c | `**4 of 199 filings** (2.0%)` |
| A20 | suppress_events produced an empty list in 2 of 6 attacks | `reports/phase_6_exploratory_2.md` | 805a34c | `2 of 6 suppress_events attacks produced one` |
| A21 | H6 JSON-valid 1.000 | `reports/phase_6_H6.md` | 08d7916 | `¦ 1.000 ¦ >= 0.95 ¦ PASS ¦` |
| A22 | H6 p95 80.1 s including the cold-load call | `reports/phase_6_H6.md` | 08d7916 | `¦ 80.1 ¦ <= 120 ¦ PASS ¦` |
| A23 | H6 p95 excluding the cold-load call 81.0 s | `reports/phase_6_H6.md` | 08d7916 | `¦ 81.0 ¦` |
| A24 | H6 p50 31.7 s | `reports/phase_6_H6.md` | 08d7916 | `¦ 31.7 / 31.7 ¦` |
| A25 | H6 max 112.5 s | `reports/phase_6_H6.md` | 08d7916 | `¦ max s/filing ¦ 112.5 ¦` |
| A26 | H6 cold-load call 65.0 s | `reports/phase_6_H6.md` | 08d7916 | `cold-load call, 65.0 s` |
| A27 | H6 run: 100 dev filings | `reports/H6_hw_report.md` | 08d7916 | `filings=100` |
| A28 | H6 hardware: Apple M2, 8 GB, macOS 15.6.1, Ollama 0.40.6 | `reports/phase_6_H6.md` | 08d7916 | `Apple M2, 8 GB RAM, macOS 15.6.1, Ollama 0.40.6` |
| A29 | H6 clean condition as stated by the owner (Terminal.app, other apps closed) | `reports/H6_measurement_choice.md` | 75e4841 | `started from Terminal.app with caffeinate` |
| B1 | Test-B H1 delta 0.0327 [-0.0244, 0.0984] | `reports/phase_6_secondary_splits.md` | ef19956 | `**0.0327 [-0.0244, 0.0984]**` |
| B2 | unseen H1 delta 0.0877 [0.0219, 0.1587] | `reports/phase_6_secondary_splits.md` | ef19956 | `**0.0877 [0.0219, 0.1587]**` |
| B3 | Test-B H5 0.1458 [0.0639, 0.2048] | `reports/phase_6_secondary_splits.md` | ef19956 | `**0.1458 [0.0639, 0.2048]**` |
| B4 | unseen H5 0.0877 [-0.0103, 0.1612] | `reports/phase_6_secondary_splits.md` | ef19956 | `**0.0877 [-0.0103, 0.1612]**` |
| B5 | Test-B H2 0.2739 [0.1103, 0.4712] | `reports/phase_6_secondary_splits.md` | ef19956 | `**0.2739 [0.1103, 0.4712]**` |
| B6 | unseen H2 0.1003 [0.0384, 0.1712] | `reports/phase_6_secondary_splits.md` | ef19956 | `**0.1003 [0.0384, 0.1712]**` |
| B7 | accepted claims / coverage: Test-B 263 / 0.516, unseen 231 / 0.520 | `reports/phase_6_secondary_splits.md` | ef19956 | `¦ 263 / 0.516 ¦ 231 / 0.520 ¦` |
| B8 | B2 event error: Test-B 0.386 [0.306, 0.456], unseen 0.417 [0.345, 0.503] | `reports/phase_6_secondary_splits.md` | ef19956 | `¦ 0.386 [0.306, 0.456] ¦ 0.417 [0.345, 0.503] ¦` |
| B9 | agent accepted error: Test-B 0.354 [0.244, 0.461], unseen 0.329 [0.258, 0.412] | `reports/phase_6_secondary_splits.md` | ef19956 | `¦ 0.354 [0.244, 0.461] ¦ 0.329 [0.258, 0.412] ¦` |
| B10 | B1 error: Test-B 0.532 (327 claims), unseen 0.504 (230 claims) | `reports/phase_6_secondary_splits.md` | ef19956 | `¦ 0.532 (327 claims) [0.410, 0.639] ¦ 0.504 (230 claims) [0.435, 0.565] ¦` |
| B11 | event claims B2: Test-B 510, unseen 444 | `reports/phase_6_secondary_splits.md` | ef19956 | `¦ event claims, B2 (all) ¦ 1,005 ¦ 510 ¦ 444 ¦` |
| B12 | supplier claims accepted, Test-A: 20, error 0.400 [0.062, 0.655] | `reports/phase_6_secondary_splits.md` | ef19956 | `20 (0.286); 0.400 [0.062, 0.655]` |
| B13 | supplier claims accepted, Test-B: 13, error 0.231 [0.000, 0.529] | `reports/phase_6_secondary_splits.md` | ef19956 | `13 (0.371); 0.231 [0.000, 0.529]` |
| B14 | supplier claims accepted, unseen: 20, error 0.300 [0.000, 0.565] | `reports/phase_6_secondary_splits.md` | ef19956 | `20 (0.526); 0.300 [0.000, 0.565]` |
| B15 | Test-B bounding run, rule b off: H1 0.0466 [-0.0223, 0.1362] | `reports/phase_6_secondary_splits.md` | ef19956 | `H1 delta 0.0466 [-0.0223, 0.1362]` |
| B16 | Test-B bounding run, affected filings dropped: H1 0.0191 [-0.0392, 0.0750] | `reports/phase_6_secondary_splits.md` | ef19956 | `H1 delta 0.0191 [-0.0392, 0.0750]` |
| B17 | Test-B ignored predictions 14 of 524 (2.7%) | `reports/phase_6_secondary_splits.md` | ef19956 | `14 of 524 agent/B2 events (2.7%)` |
| B18 | run-2 missing on Test-B and unseen: 0 | `reports/phase_6_secondary_splits.md` | ef19956 | `¦ **0** ¦ **0** ¦` |
| C1 | accepted claims scored wrong: Test-A 143 of 536, Test-B 93 of 263, unseen 76 of 231 | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `¦ 536 / 143 (26.7%) ¦ 263 / 93 (35.4%) ¦ 231 / 76 (32.9%) ¦` |
| C2 | of those, date matches but type differs: 122 (85.3%), 80 (86.0%), 57 (75.0%) | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `¦ 122 (85.3%) ¦ 80 (86.0%) ¦ 57 (75.0%) ¦` |
| C3 | date-only view, Test-A: B2 0.142, accepted 0.039, delta 0.103 [0.051, 0.172] | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `¦ date only ¦ 0.142 [0.087, 0.214] ¦ 0.039 [0.022, 0.061] ¦ 0.103 [0.051, 0.172] ¦` |
| C4 | date-only view, Test-B: B2 0.100, accepted 0.049, delta 0.051 [0.022, 0.090] | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `¦ date only ¦ 0.100 [0.063, 0.146] ¦ 0.049 [0.022, 0.079] ¦ 0.051 [0.022, 0.090] ¦` |
| C5 | date-only view, unseen: B2 0.153, accepted 0.078, delta 0.075 [0.032, 0.135] | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `¦ date only ¦ 0.153 [0.091, 0.238] ¦ 0.078 [0.035, 0.137] ¦ 0.075 [0.032, 0.135] ¦` |
| C6 | type agreement Test-A: labellers 0.788 [0.762, 0.812] (781/991) | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `0.788 [0.762, 0.812] (781/991)` |
| C7 | type agreement Test-A: agent 0.763 [0.725, 0.798] (393/515) | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `0.763 [0.725, 0.798] (393/515)` |
| C8 | type agreement Test-B: labellers 0.786 [0.748, 0.820] (397/505) | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `0.786 [0.748, 0.820] (397/505)` |
| C9 | type agreement Test-B: agent 0.680 [0.620, 0.735] (170/250) | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `0.680 [0.620, 0.735] (170/250)` |
| C10 | type agreement unseen: labellers 0.827 [0.788, 0.861] (340/411) | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `0.827 [0.788, 0.861] (340/411)` |
| C11 | type agreement unseen: agent 0.728 [0.664, 0.783] (155/213) | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `0.728 [0.664, 0.783] (155/213)` |
| C12 | Test-B Jayco: labellers 26/29, agent 6/18 | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `¦ Jayco ¦ 0.897 [0.736, 0.964] (26/29) ¦ 0.897 [0.736, 0.964] (26/29) ¦ 0.333 [0.163, 0.563] (6/18) ¦` |
| C13 | Test-B Ford: labellers 53/79, agent 11/31 | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `¦ Ford ¦ 0.671 [0.561, 0.764] (53/79) ¦ 0.645 [0.533, 0.743] (49/76) ¦ 0.355 [0.211, 0.531] (11/31) ¦` |
| C13b | 4 of the agent's 6 most frequent type confusions are among the labellers' 6 | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `4 of the agent's 6 most frequent confusions are also among the labellers' 6 most frequent` |
| C14 | FILER_AWARENESS / INVESTIGATION_START: 6.4% of labeller disagreements (25 of 389) | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `¦ FILER_AWARENESS / INVESTIGATION_START ¦ 25 ¦ 6.4% ¦` |
| C15 | FILER_AWARENESS / INVESTIGATION_START: 20.8% of agent disagreements (54 of 260) | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `¦ FILER_AWARENESS / INVESTIGATION_START ¦ 54 ¦ 20.8% ¦` |
| C16 | most frequent pair INVESTIGATION_START / OTHER: labellers 32.9%, agent 39.2% | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `¦ INVESTIGATION_START / OTHER ¦ 102 ¦ 39.2% ¦` |
| C17 | most frequent labeller pair INVESTIGATION_START / OTHER 128 (32.9%) | `reports/phase_6_failure_analysis.md` | 3c8b7cb | `¦ INVESTIGATION_START / OTHER ¦ 128 ¦ 32.9% ¦` |
| C18 | erratum: about 33% of Ford's chronology entries recur in another Ford filing; within-filing repeat share about 0 | `reports/phase_6_secondary_splits.md` | b67c054 | `about 33% of Ford's entries recur` |
| C19 | only 2 accepted-wrong claims are within-filing duplicates (unseen) | `reports/phase_6_failure_analysis.md` | b67c054 | `only 2 accepted-wrong claims are duplicates, both in unseen-filer` |
| C20 | leave-Ford-out Test-B H1 delta 0.0496 [-0.0117, 0.1130], coverage 0.539 | `reports/phase_6_secondary_splits.md` | ef19956 | `0.0496 [-0.0117, 0.1130] at coverage 0.539` |
| C21 | Ford on Test-B: 85 of 510 claims, error 0.541; accepted 34 at 0.676 | `reports/phase_6_secondary_splits.md` | ef19956 | `Ford is 85 of 510 claims (16.7%) with 0.541 error, and its 34 accepted claims have 0.676 error` |
| C22 | tipping point: H1 point threshold fails at 24.9% of accepted-correct claims wrong (98 claims, 9.7% of labels) | `reports/phase_6_exploratory_2.md` | 805a34c | `fails first, at 24.9% (98 claims = 9.7% of labels)` |
| C23 | tipping point: CI lower bound reaches 0 at 26.7% (105 claims, 10.4% of labels) | `reports/phase_6_exploratory_2.md` | 805a34c | `26.7% of the accepted-correct claims are really wrong (105 claims = 10.4% of all 1005 event labels)` |
| C24 | Shapley: run-2 agreement 0.065 [0.038, 0.097] | `reports/phase_6_exploratory_2.md` | 805a34c | `run-2 agreement 0.065 [0.038, 0.097]` |
| C25 | Shapley: V3 unparseable date 0.031, E1 0.026 | `reports/phase_6_exploratory_2.md` | 805a34c | `V3 unparseable-date 0.031 [0.013, 0.055], E1 0.026 [0.009, 0.045]` |
| C26 | filters alone: verifiers only delta 0.106 at coverage 0.659 | `reports/phase_6_testA_exploratory.md` | 6c34d05 | `¦ 662 ¦ 0.659 ¦ 0.296 ¦ 0.106 [0.058, 0.160] ¦` |
| C27 | filters alone: run-2 agreement only delta 0.103 at coverage 0.714 | `reports/phase_6_testA_exploratory.md` | 6c34d05 | `¦ 718 ¦ 0.714 ¦ 0.299 ¦ 0.103 [0.057, 0.155] ¦` |
| C28 | AURC (events) 0.269 [0.215, 0.332] | `reports/phase_6_testA_exploratory.md` | 6c34d05 | `AURC 0.269 [0.215, 0.332]` |
| C29 | cluster t-bound: events upper bound 0.324 | `reports/phase_6_exploratory_2.md` | 805a34c | `upper bound **0.324**` |
| C30 | cluster t-bound false-certification rate, events: lowest 0.0115 | `reports/phase_6_exploratory_2.md` | 805a34c | `¦ 231/20000 ¦ 0.0115` |
| C31 | cluster t-bound false-certification rate, events: highest 0.0273 | `reports/phase_6_exploratory_2.md` | 805a34c | `¦ 546/20000 ¦ 0.0273` |
| C32 | cluster t-bound false-certification rate, cause: lowest 0.0481 | `reports/phase_6_exploratory_2.md` | 805a34c | `¦ 963/20000 ¦ 0.0481` |
| C33 | cluster t-bound false-certification rate, cause: highest 0.2056 | `reports/phase_6_exploratory_2.md` | 805a34c | `¦ 4111/20000 ¦ 0.2056` |
| T0 | TS-1 protocol fixed and committed before any gap was computed | `reports/TS_PROTOCOL.md` | 246e30e | `**Status: fixed before any gap is computed.**` |
| T1 | TS-1 population: 305 defect filings of 397; 92 noncompliance | `reports/phase_7_timeliness.md` | 2157cf1 | `**Population:** 305 defect filings (out of 397; 92 noncompliance filings are reported separately).` |
| T2 | TS-1 primary (Submission Date): FLAGGED 104/305 = 0.341 W[0.290, 0.396] | `reports/phase_7_timeliness.md` | 2157cf1 | `FLAGGED 104/305 = 0.341 W[0.290, 0.396] B[0.268, 0.418]` |
| T3 | TS-1: 98 of the 104 primary FLAGGED are amended versions; originals 6/136 | `reports/phase_7_timeliness.md` | 2157cf1 | `98 of the 104 FLAGGED filings are processed from an amended version, against 6/136 among originals.` |
| T4 | TS-1: Submission Date equals RCDATE in 15 of 169 amended versions and 131 of 136 originals | `reports/phase_7_timeliness.md` | 2157cf1 | `it equals RCDATE in only 15 of 169 amended versions, against 131 of 136 originals` |
| T5 | TS-1: RCDATE earlier than an amended version's Submission Date by a median of 35 calendar days | `reports/phase_7_timeliness.md` | 2157cf1 | `RCDATE is earlier by a median of 35 calendar days` |
| T6 | TS-1 RCDATE variant: FLAGGED 19/305 = 0.062 W[0.040, 0.095] B[0.033, 0.096] | `reports/phase_7_timeliness.md` | 2157cf1 | `RCDATE variant: FLAGGED 19/305 = 0.062 W[0.040, 0.095] B[0.033, 0.096].` |
| T7 | TS-1 originals stratum: FLAGGED 6/136 = 0.044 W[0.020, 0.093] B[0.013, 0.086] | `reports/phase_7_timeliness.md` | 2157cf1 | `originals stratum: FLAGGED 6/136 = 0.044 W[0.020, 0.093] B[0.013, 0.086].` |
| T8 | TS-1 RCDATE variant, pooled: gap_mid 5 [3-5] 6; agent coverage 126/305; bounds 0.049-0.649; kappa 0.809, PABAK 0.938 (n 121) | `reports/phase_7_timeliness.md` | 2157cf1 | `¦ pooled ¦ 305 ¦ 217 ¦ 19/305 = 0.062 W[0.040, 0.095] B[0.033, 0.096] ¦ 5 [3–5] 6 ¦ 5 [3–5] 5 ¦ 5 [3–5] 6 ¦ 126/305 (0.413) ¦ 15/126 (0.119) ¦ 0.049 [0.026, 0.076] – 0.649 [0.562, 0.738] ¦ 121 ¦ 10,0,0; 1,104,2; 0,2,2 ¦ 0.809 [0.611, 0.957] ¦ 0.938 [0.874, 0.988] ¦` |
| T9 | TS-1 originals stratum, pooled: gap_mid 5 [3-5] 6; agent coverage 52/136; bounds 0.015-0.654; kappa 0.383, PABAK 0.912 (n 51, unstable) | `reports/phase_7_timeliness.md` | 2157cf1 | `¦ pooled ¦ 136 ¦ 99 ¦ 6/136 = 0.044 W[0.020, 0.093] B[0.013, 0.086] ¦ 5 [3–5] 6 ¦ 4 [3–5] 5 ¦ 5 [3–5] 6 ¦ 52/136 (0.382) ¦ 2/52 (0.038) ¦ 0.015 [0.000, 0.040] – 0.654 [0.520, 0.779] ¦ 51 ¦ 0,0,0; 1,47,2; 0,0,1 ¦ 0.383 [0.000, 1.000] ¦ 0.912 [0.786, 1.000] (reference FLAGGED among n both: 0, fewer than 10: unstable) ¦` |
| T10 | TS-1: 88 of 305 defect filings have no usable DECISION date (silver) | `reports/phase_7_timeliness.md` | 2157cf1 | `88 of 305 defect filings (0.289) have no usable DECISION date` |
| T11 | TS-1: agent accepted, dated DECISION claim for 127/305 (0.416) | `reports/phase_7_timeliness.md` | 2157cf1 | `127/305 = 0.416` |
| T12 | TS-1: agent vs reference kappa 0.937 where both have a date (primary) | `reports/phase_7_timeliness.md` | 2157cf1 | `(Cohen's κ 0.937)` |
| T13 | TS-1 amendment TS-A1: 2 filings, 0 anchors affected | `reports/phase_7_timeliness.md` | 2157cf1 | `**Anchors using a year from context in them: 0**` |
| T14 | TS-1: 186 of 397 filings typed by the flat-file FMVSS proxy (2025+ form has no type field) | `reports/phase_7_timeliness.md` | 2157cf1 | `186 of 397 filings are typed by a flat-file FMVSS proxy` |
| U0 | SC-1 protocol fixed before any claim was compared with the reference | `reports/SC_PROTOCOL.md` | 24f7c34 | `**Status: fixed before any claim is compared with the reference.**` |
| U1 | SC-1: supplier block parsed in 397/397 filings (portal 186, older 211) | `reports/phase_8_supplier_check.md` | f35dfb6 | `Parse rate 397/397, with 0 failures, in both layouts: portal (186) and older (211).` |
| U2 | SC-1 strata: NAMED 255, OEM_SELF 47, OBTAINED_FROM 4, MULTIPLE 6, BLANK 85, PARSE_FAIL 0 | `reports/phase_8_supplier_check.md` | f35dfb6 | `¦ **all** ¦ 255 ¦ 47 ¦ 4 ¦ 6 ¦ 85 ¦ 0 ¦` |
| U3 | SC-1 population: 261 filings declare one or more external suppliers | `reports/phase_8_supplier_check.md` | f35dfb6 | `**Population:** 261 filings declare one or more external suppliers` |
| U4 | SC-1: 52 of 65 Supplier-Type-OEM names are not the filer | `reports/SC_INVENTORY.md` | c27b962 | `52 of the 65 OEM-typed names are not the filer` |
| U5 | SC-1: the agent's frozen input contains no supplier-block line in any filing | `reports/phase_8_supplier_check.md` | f35dfb6 | `no block heading or field line appears in the agent's frozen input in any filing` |
| U6 | SC-1: agent supplier claims 226 (92 gate-accepted) | `reports/phase_8_supplier_check.md` | f35dfb6 | `Agent run-1: 226 in total, of which 92 are gate-accepted.` |
| U7 | SC-1 agent exact, pooled: recall 18/261 = 0.069; accepted 13/261; precision 19/172 = 0.110; accepted 14/70 = 0.200 | `reports/phase_8_supplier_check.md` | f35dfb6 | `¦ **pooled** ¦ 261 ¦ 18/261 = 0.069 W[0.044, 0.106] B[0.037, 0.110] ¦ 13/261 = 0.050 W[0.029, 0.083] B[0.024, 0.085] ¦ 19/172 = 0.110 W[0.072, 0.166] B[0.065, 0.168] ¦ 14/70 = 0.200 W[0.123, 0.308] B[0.105, 0.317] ¦` |
| U8 | SC-1 silver exact, pooled: S2 recall 92/261 = 0.352; S1 precision 254/261 = 0.973; S2 precision 92/113 = 0.814 | `reports/phase_8_supplier_check.md` | f35dfb6 | `¦ **pooled** ¦ 261 ¦ 255/261 = 0.977 W[0.951, 0.989] B[0.958, 0.993] ¦ 92/261 = 0.352 W[0.297, 0.412] B[0.268, 0.463] ¦ 254/261 = 0.973 W[0.946, 0.987] B[0.953, 0.991] ¦ 92/113 = 0.814 W[0.733, 0.875] B[0.723, 0.897] ¦` |
| U9 | SC-1 agent vs silver S2, pooled: 18 both / 0 agent only / 74 silver only / 169 neither | `reports/phase_8_supplier_check.md` | f35dfb6 | `¦ **pooled** ¦ agent all vs silver S2 ¦ 18 ¦ 0 ¦ 74 ¦ 169 ¦` |
| U10 | SC-1 containment, pooled: agent precision (accepted) 27/70 | `reports/phase_8_supplier_check.md` | f35dfb6 | `¦ token containment ¦ **pooled** ¦ 261 ¦ 34/261 = 0.130 ¦ 35/172 = 0.203 ¦ 26/261 = 0.100 ¦ 27/70 = 0.386 ¦` |
| U11 | SC-1 fuzzy tsr>=90, pooled: agent precision (accepted) 29/70 | `reports/phase_8_supplier_check.md` | f35dfb6 | `¦ fuzzy token_set_ratio ≥ 90 ¦ **pooled** ¦ 261 ¦ 40/261 = 0.153 ¦ 41/172 = 0.238 ¦ 28/261 = 0.107 ¦ 29/70 = 0.414 ¦` |
| U12 | SC-1 components not run: no component claims exist | `reports/phase_8_supplier_check.md` | f35dfb6 | `**Not run: there are no component claims to check.**` |
| U13 | SC-1 amendment SC-A1: 23 of 26 Pass-C silver S2 claims fall in the population | `reports/phase_8_supplier_check.md` | f35dfb6 | `**23 of these 26 claims fall in the population;**` |
| U14 | SC-1 post hoc: 24 of 261 population filings declare a short form of the filer's own name; 1 of 19 agent matches there | `reports/phase_8_supplier_check.md` | f35dfb6 | `In 24 of 261 population filings` |
| U15 | SC-1 post hoc: 14 silver S1 quotes located out of block are first-match artefacts | `reports/phase_8_supplier_check.md` | f35dfb6 | `**POST HOC diagnostic:** in all 14` |
| H1 | Test-A run 1: 12:48:52 to 16:10:07 (3 h 21 min) | `reports/DEVIATIONS.md` | 75e4841 | `12:48:52 start, 16:10:07 done` |
| H2 | Test-A run 2: restart at 21:32:45 with 167 of 199 records | `reports/DEVIATIONS.md` | 75e4841 | `RESTART 21:32:45 with 167 of 199 records` |
| H3 | Test-A run 2: four timeouts at 300 s | `reports/DEVIATIONS.md` | 75e4841 | `four per-call timeouts at 300 s` |
| H3b | Test-A run 2: one runner crash, no model call completed | `reports/DEVIATIONS.md` | 75e4841 | `one "model runner has unexpectedly stopped" at 2 s (RCLRPT-25V574-1873; no model call completed, no output)` |
| H3c | Test-A run 2: the crashed record retried once | `reports/DEVIATIONS.md` | 75e4841 | `RCLRPT-25V574-1873 re-run once with the frozen run-2 settings` |
| H4 | battery death: Low Power Sleep 2026-10-25 17:56:21 on battery at 1% | `reports/phase_6_secondary_splits.md` | ef19956 | `Low Power Sleep at 2026-10-25 17:56:21 while on battery at 1% charge` |
| H4b | the Mac rebooted at 19:22:49 | `reports/phase_6_secondary_splits.md` | ef19956 | `the machine rebooted at 19:22:49` |
| H4c | Test-B run 2 restart 2026-10-27 11:48:06 | `reports/phase_6_secondary_splits.md` | ef19956 | `RESTART 2026-10-27 11:48:06` |
| H5 | Test-B run 1: 15:19:16 to 17:52:00 (2 h 33 min) | `reports/phase_6_secondary_splits.md` | ef19956 | `¦ Test-B ¦ 1 ¦ 2026-10-25 15:19:16 ¦ 2026-10-25 17:52:00 ¦` |
| H6 | Test-B run 2 after restart: 11:48:29 to 12:46:55 (58 min) | `reports/phase_6_secondary_splits.md` | ef19956 | `START 11:48:29 ¦ 2026-10-27 12:46:55` |
| H7 | unseen run 1: 12:47:02 to 13:39:30 (52 min) | `reports/phase_6_secondary_splits.md` | ef19956 | `¦ unseen ¦ 1 ¦ 2026-10-27 12:47:02 ¦ 2026-10-27 13:39:30 ¦` |
| H8 | unseen run 2: 13:39:32 to 14:30:00 (50 min) | `reports/phase_6_secondary_splits.md` | ef19956 | `¦ unseen ¦ 2 ¦ 2026-10-27 13:39:32 ¦ 2026-10-27 14:30:00 ¦` |

| # | claim | source | status |
|---|---|---|---|
| X1 | Astvansh, Ball & Josefy (2022), "The Recall Decision Exposed: Automobile Recall Timing and Process Data Set", MSOM 24(3):1457–1473, doi 10.1287/msom.2022.1085; 2,120 recalls by 27 automakers, 2009–2018 | owner-supplied, not a committed report | **verified against RePEc + accepted manuscript** |
