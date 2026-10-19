# STOP: owner approval needed before the freeze (Phase 5 -> Phase 6)

Nothing has been frozen, and no test data has been touched. Work is paused here as required by the brief.

## What I need from you
1. **Read** `reports/PREREGISTRATION_PROPOSED_FINAL.md` and **edit the thresholds and set sizes** (Test-A labelled 200, Test-B 100, unseen-filer 100 are my proposals; the labelling cost is roughly 4-5x the dev effort for 400 filings).
2. **Approve** by creating `reports/APPROVED_BY_OWNER.txt`, then run `python scripts/freeze.py` (or tell me to). Then I follow `docs/PHASE6_RUNBOOK.md`.
3. Optional, not blocking: the clean-hardware speed measurement (command in `reports/phase_2.md`).

## Things you should know before approving
- **A new result contradicts a statement in an earlier report.** `reports/phase_4.md` first said the event gain from abstention was "not shown" (two unpaired intervals overlapped). The paired comparison on the same filer-cluster resamples gives 0.100 (0.035 to 0.172), which excludes 0, so on dev the gain is distinguishable from zero. The report is corrected. This is still a dev result.
- **Dev results are optimistic by construction**: prompt v2, the E1 inherited-date allowance and V4r were set after looking at dev; the v2 event-type definitions are copied from the rules that define the silver labels.
- **Labels are silver** (AI-made, cross-checked by AI passes and code checks; not human-verified; one model family). Dev event-type agreement between the two independent AI passes is 84.8%, which is the rough ceiling for event-type accuracy.
- The injection test on dev was written by me after the verifiers (0/20 with verifiers is in-sample); the held-out 30 attacks were written blind, which is the real test.
- B1 (plain rules) beat the original LLM prompts on events and cause; with prompt v2 the 4B beats B1 on events point-wise, with overlapping intervals.
- The optional 2B-to-4B cascade was not built. Speed numbers were all measured with Claude Code and other apps open and swap in use.
- Two small process notes: my first 2B run crashed on my own coding error and was resumed; part of the 2B run overlapped with an analysis script of mine (timing contaminated).
