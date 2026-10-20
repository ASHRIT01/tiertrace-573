# Amendment 1 to the frozen protocol (tag `amendment-1`)

Written and committed **before any Test-A model output exists**. The freeze (`freeze-v1`, preregistration, thresholds, prompts, verifiers, scorer code) is not
edited: the scorer is wrapped (`tt/eval/amend1.py`), nothing frozen is changed. All labels are silver (AI-made, not human-verified).

## 1. Scoring wrapper (owner decision 1)
Use `python -m tt.eval.amend1 {phase3|phase4|endpoints|report} out.json` instead of `python -m tt.eval.<same>` for every Phase 6 scoring step (same environment
variables). The wrapper patches names at run time; the frozen files are byte-identical.

* **Crash-only guard.** The frozen `tt.labels.dates.parse_span` raises on year-less fuzzy dates (AttributeError, D-T2) and on invalid calendar dates
  (ValueError). The wrapper makes exactly those two cases return `None` (what `parse_span` already returns for other dates it cannot parse). A value that did
  not crash is never changed.
* **Rule a.** A gold event that carries a date text but has no ISO date span is excluded from event scoring for **all** systems (agent, B0, B1, B2).
* **Rule b.** In a filing with an excluded gold event, a predicted event of the **same type** that is not right (frozen classes `wrong:extra`, `wrong:type`) is
  ignored (dropped from the item list). A prediction whose own date is unparseable (`wrong:date_unparsed`) is handled exactly as in the frozen scorer.
* **Rule c.** `report` prints, per split, the number of excluded gold events and the number of ignored predictions per system. If more than 2% of events are
  affected (excluded gold events as a share of all non-contested gold events, or of the gold events that carry a date text; or ignored predictions as a share of a
  system's predicted events), two bounding runs are added to the exploratory results: `TT_AMEND_MODE=bound_errors` (unmatched predictions counted as errors, i.e.
  rule b off) and `TT_AMEND_MODE=bound_drop` (every filing with an excluded gold event dropped).

### Definition of "excluded gold event" (an interpretation, disclosed)
The first dev re-score used the broad reading "has a date text and is flagged `date_inferred` or has no span". That excludes one dev gold event
(19V811-5724, date text `11-13-`, which has an inferred span) and rule b then drops one dev prediction (434 -> 433 event candidates), so test (i) failed
(diff not empty). The reading below was then fixed, **after seeing that dev result and before any Test-A model output**:

* **Primary (`TT_AMEND_EXCLUDE_DEF=nospan`, default):** the event carries a date text and **no ISO span exists for it** (the date could not be parsed at all).
  Dev: 0 such events; Test-A 27 of 1,445 non-contested gold events (1.87%, 11 filings); Test-B 4 of 790 (0.51%, 2 filings); unseen 3 of 569 (0.53%, 3 filings).
* **Pre-declared sensitivity (`inferred_too`):** additionally the events whose date is flagged `date_inferred` although an inferred span exists. Dev 1 (0.17%);
  Test-A 35 (2.42%, 17 filings); Test-B 38 (4.81%, 6 filings); unseen 13 (2.28%, 7 filings). Its dev result differs from the reference by one prediction by design.
* Undated gold events (no date text at all, `date_inferred` by the labelling rule) are neither "excluded" nor a trigger for rule b: the frozen scorer already skips
  them as gold and the dev reference depends on that.

## 2. Tests (owner decision 2), passed before the model runs
(i) `TT_CACHE=<fresh> python -m tt.eval.amend1 phase4 out.json` on the dev data vs `reports/phase_4_results.json`: `diff` empty, files byte-identical (the frozen
`python -m tt.eval.phase4` also reproduces it byte-identically, checked first). (ii) `tests/test_amend1.py`: synthetic gold with a year-less fuzzy date and an invalid
calendar date (the frozen function is shown to raise, the guard does not), rule a exclusion, rule b ignoring (same type only; unparsed predictions stay wrong;
other filings untouched), the two bounding modes, the two sensitivity switches and the exclusion definitions. Nothing crashes.

## 3. Pre-declared sensitivity runs (owner decision 3), exploratory only
(a) **Contested counted as misses:** `TT_AMEND_CONTESTED_MISS=1`: a predicted S2 or C claim in a filing whose S2 or C item is CONTESTED counts as an error (instead
of being skipped); a predicted event that overlaps a contested gold event of the same type counts as an error even if it is also right on a scored gold event.
(b) **Excluding filings with isolation slips:** `TT_AMEND_DROP_FILES=config/isolation_slips.json`-derived list (the `sensitivity_b_drop_these` field, 56 filings).
Slips (agents whose `files_seen.txt` lists a path outside their batch directory, found by scanning all of them, plus reported ones):
* S1 Test-A b01 Pass B: ran its own helper script from the scratchpad outside the batch directory (25 filings in scope).
* S2 Test-A b04 Pass C batch_2: read back its own tool-output spill (only the batch's texts) **and used outside knowledge for one S2 call: D028, filing 24V556-5723**
  (6 filings in scope). This is the one outside-knowledge case.
* S3 Test-B b02 Pass B: read the tool-captured stdout of `cat texts/*.txt` outside the batch directory (25 filings in scope).
Agents that only reported a tool-output spill without opening it are not slips. Full filing lists: `config/isolation_slips.json`.
(c) **`inferred_too`** exclusion definition (section 1). The bounding runs of rule c are added when the rule-c threshold is exceeded.

## 4. Unreadable filings (owner decision 4)
Excluded, never replaced, no OCR: 23V313 (Test-A), 23V320 and 24V945 (unseen-filer); reasons in `config/amendment1_manifest.json`. `._*` AppleDouble files are not
filings: the runner reads the selection list only, and `tt/leakcheck.py` already skips names starting `._` (tested).

## 5. Label independence (owner decision 5)
Pass C sided with Pass B in 72-78% of its items (Test-A 73.5%, Test-B 72.2%, unseen 77.6%), and Pass B and Pass C are both Opus; Pass C sided with Pass A in
8-10%. The silver labels are therefore not independent evidence about the filings, and **no label-error figure is claimed** anywhere.

## 6. Freeze of the agent from now on (owner decision 6)
No change to the prompt, the verifiers or the thresholds after any Test-A output exists. Crash-only fixes are allowed; each is logged in `reports/DEVIATIONS.md`
with its reason.

## 7. Test-A run procedure
`scripts/phase6_run.py` (frozen model `qwen3.5:4b-q4_K_M`, prompt v2, think off, num_ctx 6144, via `tt.agent.run_dev.run`): run 1 temperature 0 seed 0, then run 2
temperature 0.5 seed 1, 199 filings each, under `caffeinate`, resuming after any interruption (each start/restart is appended to `runs/testA_run_log.txt` and logged
as a deviation). The runner reads no gold label and prints only progress, timing and valid-JSON counts. B0 and B1 are rule-based and B2 is the run-1 output scored
without verifiers, so no further model run is needed. Outputs are force-added to git (`runs/` is ignored) and hashed. No scoring and no looking at results until the
owner says so. Test-B and the unseen-filer set run in a separate sitting.
