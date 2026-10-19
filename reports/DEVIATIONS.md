# Deviations and labelling-rule problems (Phase 6)

Rules, prompts and scoring code are frozen (tag `freeze-v1`). Nothing below changes them. Silver labels: AI-made, not human-verified.
(The preregistration calls this file `reports/deviations.md`; it is the same file on this case-insensitive volume.)

## Procedure notes (not rule changes)
- D-P1. `scripts/phase6_batch.py` was added after the freeze as orchestration glue (batch slicing of the frozen ID lists, per-batch work directories, merging). It calls the frozen labelling commands unchanged. It is not in the freeze manifest.
- D-P2. `docs/PASS_B_PROMPT.txt` says "the 20 files"; batches are 25 filings (owner's instruction), so the count in the prompt text is substituted (20 -> number of files in the batch) together with {DIR}. The file itself is unchanged.
- D-P3. Pass A, B and C are run per batch of 25 filings; the Pass C item ids (D001...) restart in each batch and the final labels are the concatenation of the batches. The pipeline code is the same as for dev, where all 100 filings were one batch.
- D-P5. Pass A override effort is lighter than for dev: for each test batch the session reads the review sheet (text + auto draft) and writes overrides only for clear errors (wrong supply-chain party, obvious event-type errors, splitter fragments). Pass A is therefore closer to the raw code draft than the dev Pass A was, so more items go to Pass C. The count of override entries per batch is in the batch reports.
- D-P6. Pass B batch 1 (b01) wrote and ran its own helper script from the shared scratchpad (outside its batch directory) and logged it in files_seen.txt; it reports opening nothing else outside the batch (one oversized shell output was saved by the tool outside the batch; it was not opened). The prompt text did not forbid helper scripts. From the Pass C calls onward the prompt text is followed by one line: "Keep any helper script inside this batch directory too, and list it in files_seen.txt; do not write or read outside it." (Pass C prompt file unchanged.)
- D-P4. `.gitignore` extended for fetched test PDFs and scratch texts.

## Tool issues (logged, code not changed)
- D-T1. `label-select` silently drops a PDF whose header cannot be parsed (no text layer) instead of listing it as unreadable. Test-A: 23V313 (scanned, 0 characters, single version) is excluded as unreadable per the dev rule (no OCR, no fallback available); see reports/phase_6_testA_fetch.md.

## Labelling-rule problems (logged, not fixed)
(filing id | problem)
- 23V253-4361 (Test-A b01): one sentence holds two actions ("An engineering review was initiated and, on March 21st, the seat supplier was contacted"); the rules give one event per sentence but do not say which action sets the type or whether the undated action is dated. Pass C marked it CONTESTED (D024). Not fixed.
- 23E009-8284 (Test-A b01): a date range "From September 2022, through January 2023" (review period): the rules give one event per distinct date and do not say whether a range is one date or two. Pass C kept the first date only (September 2022). Not fixed.
- 23V310-1286 (Test-A b01): "decides that a product safety defect exists" vs a committee recommendation: DECISION vs OTHER typing is arguable (D011 in Pass C notes); the rules' DECISION definition does not name an internal committee deciding that a defect exists. Not fixed.
