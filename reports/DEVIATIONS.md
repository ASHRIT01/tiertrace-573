# Deviations and labelling-rule problems (Phase 6)

Rules, prompts and scoring code are frozen (tag `freeze-v1`). Nothing below changes them. Silver labels: AI-made, not human-verified.
(The preregistration calls this file `reports/deviations.md`; it is the same file on this case-insensitive volume.)

## Procedure notes (not rule changes)
- D-P1. `scripts/phase6_batch.py` was added after the freeze as orchestration glue (batch slicing of the frozen ID lists, per-batch work directories, merging). It calls the frozen labelling commands unchanged. It is not in the freeze manifest.
- D-P2. `docs/PASS_B_PROMPT.txt` says "the 20 files"; batches are 25 filings (owner's instruction), so the count in the prompt text is substituted (20 -> number of files in the batch) together with {DIR}. The file itself is unchanged.
- D-P3. Pass A, B and C are run per batch of 25 filings; the Pass C item ids (D001...) restart in each batch and the final labels are the concatenation of the batches. The pipeline code is the same as for dev, where all 100 filings were one batch.
- D-P4. `.gitignore` extended for fetched test PDFs and scratch texts.

## Tool issues (logged, code not changed)
- D-T1. `label-select` silently drops a PDF whose header cannot be parsed (no text layer) instead of listing it as unreadable. Test-A: 23V313 (scanned, 0 characters, single version) is excluded as unreadable per the dev rule (no OCR, no fallback available); see reports/phase_6_testA_fetch.md.

## Labelling-rule problems (logged, not fixed)
(filing id | problem)
