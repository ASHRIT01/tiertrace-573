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
- D-T2. Frozen code bug: `tt.labels.dates.parse_span` raises AttributeError ('tuple' object has no attribute 'year') on a year-less fuzzy date such as "mid-April" or "early October" (Test-A b02, Pass B labels of 23V483-6594 and 23V708-4418, both rule-conformant: "a date without a year is kept as written"). It crashes `label-compare`. The frozen files are NOT edited. `scripts/phase6_runner.py` wraps the labelling commands and makes that case (and, from b03, a calendar-invalid date such as 2023-09-31, which raises ValueError 'day is out of range for month' in `_point`) return None (what parse_span already returns for other dates it cannot parse) at runtime. **The same crash will occur in the unmodified scorer** (`prepare_gold` and `diagnose` call parse_span on gold date_text), so the frozen scorer cannot score a Test-A set that contains such gold events unless the same guard is applied; this needs the owner's decision before any scoring (Phase 6 step 4).
- D-P7. Pass B subagents are launched with an added line from b02 on: "Keep any helper script inside this directory too, and list it in files_seen.txt; do not write or read outside it." Subagents report that the project CLAUDE.md is loaded into their context automatically (not opened); it contains project rules only.

## Labelling-rule problems (logged, not fixed)
(filing id | problem)
- 23V253-4361 (Test-A b01): one sentence holds two actions ("An engineering review was initiated and, on March 21st, the seat supplier was contacted"); the rules give one event per sentence but do not say which action sets the type or whether the undated action is dated. Pass C marked it CONTESTED (D024). Not fixed.
- 23E009-8284 (Test-A b01): a date range "From September 2022, through January 2023" (review period): the rules give one event per distinct date and do not say whether a range is one date or two. Pass C kept the first date only (September 2022). Not fixed.
- 23V310-1286 (Test-A b01): "decides that a product safety defect exists" vs a committee recommendation: DECISION vs OTHER typing is arguable (D011 in Pass C notes); the rules' DECISION definition does not name an internal committee deciding that a defect exists. Not fixed.
- 23V558-1590 (Test-A b02): "had received three complaints between May 2023 and July 2023" can be read as a count over a window (not an event) or as complaints received (FILER_AWARENESS) at two dates; the rules do not settle it. Pass C: CONTESTED. Not fixed.
- 23V653-1716 (Test-A b02): "Engineer talked with design engineering to understand the history of the parts" is OTHER (a meeting) or INVESTIGATION_START (inquiry into cause); the type definitions do not settle it. Pass C: CONTESTED.
- 23V653, 23V690, 23V750 (Test-A b02): several A/B pairs label different sentences or dates of the same dated entry, so they are not competing labels for one event (Pass C: three CONTESTED items; also noted in b02 batch 3). The pairing in `tt/labels/agree.py` matches events by type+overlap, so such cases surface as "type differs"/"only in" items. A protocol limitation, not changed.
- Rules gap (b02, several filings): a sentence that reports both awareness and the start of an investigation (23V... D027/D029/D031) has no tie-break; Pass C chose FILER_AWARENESS ("awareness is the main clause"). Date ranges ("From X through Y" around an activity) are treated by Pass B/C as one event per date, which the rules support only for 'distinct dates in one sentence'.
- 23V787/24V164/24V143 etc. (Test-A b03): the frozen sentence splitter breaks "R. H. Sheppard" into fragments ("R.", "H.") and Pass C had to rule on fragments (D039/D040); a pointer such as "Chronology is provided as an attachment." is not recognised as a pointer. Rule text unaffected; tool limitations, not changed.
- 24V164-6230 (b03): A/B events matched against each other by the pairing code were two different bullets of the same entry (Pass C: two CONTESTED items). Same protocol limitation as in b02.
- 24E041/24V143/24V077 (b03): Pass C and B read 'U = NOT_REPORTED' for a pointer chronology whose cause mentions "the supplier" generically (the rules make an exception only for a NAMED company in the cause); Pass A had 'UNNAMED'. The rules do not say what U is when the chronology is a pointer and the cause refers to a supplier generically. Logged, not changed.
- 24E071/23V818 (b03): whether a supplier's own recall decision ("Weldon decided to conduct a safety recall") is DECISION or OTHER is not settled by the rules (DECISION is 'the decision to recall' without saying whose). Pass C ruled OTHER for a supplier's decision.
- D-T3. Pass A's S1 quote is built as "Name : <name>" (`draft.py`), which is not verbatim for the 2025+ Part 573 layout where the block reads "Name:\n<name>" (Q1 code check fails, seen in 24E071-6470 in b03; the 2025/2026 filings of Test-A/Test-B/unseen will show the same). Handled by a per-filing Pass A override of the S1 quote ("Name: <name>", status unchanged). For 24E071 the override was added after Pass B/C had run (S1 was agreed, so no item was affected; Pass A's S1 status is unchanged); from b04 the script prints the Pass A code checks right after Pass A so the override is made before Pass B.
- (Test-A b04) Pass C subagent for batch_2 read back its own long tool printout saved outside the batch directory (a file holding only batch texts; listed in its files_seen.txt) and used outside knowledge for one S2 call (D028, 24V556: 'Meritor' taken as the block company 'Cummins Drivetrain and Braking Systems', background knowledge not in the filing). Decision kept as made; flagged for the summary.
- 24V556-5723, 24V588 (b04): '09/03/2024- Revised recall schedule due to holiday.' could be a Part 573 amendment (NHTSA_FILING) or logistics (OTHER); Pass C: CONTESTED (D029). Rules do not say whether an amendment line without 'submitted to NHTSA' counts.
- 24V477-8229 (b04): 'Polestar decided the condition as critical concern' DECISION vs OTHER (D015 CONTESTED); 24V480-8563 'Ongoing analysis is focused on ...' status vs event (D023 CONTESTED).
- 24V217/24V480 (b04): in several A/B pairs one label took model years ("2022") or line-broken fragments ("December 2023 ...") as event dates; Pass C corrected them (10 NEITHER items in one batch). Pass A's year-less/fragment dates come from the frozen sentence splitter and date finder, unchanged.
- D-P8. From b05 the Pass A review sheet is printed in compact mode (block, cause start, auto draft with event list; no chronology text) to keep the session's reading load manageable. Pass A overrides for b05 onward are therefore based on the auto draft, not on a full read of each chronology; this lowers Pass A quality relative to b01-b04 (more items for Pass C).
- 24V789-9845 (b05): 'Cummins’ 573 filed with NHTSA; copy provided to Kenworth S&C.' fits both 'OTHER: a supplier's own filing' and 'SUPPLIER_NOTICE'; Pass C CONTESTED (D008).
- 24V820/24V789 etc. (b05): 'received reports ... and began to investigate' in one sentence: FILER_AWARENESS vs INVESTIGATION_START has no tie-break (same gap as b02).
- 24V949-7212 (b05): a customer-reported symptom sentence inside a header-dated entry: separate event or not, with which date/type, not settled (D025 CONTESTED).
- D-T3 (cont.). `scripts/phase6_fixq.py` applies the D-T3 S1/S2 block-quote fix mechanically (it only rewrites "Name : <name>" to "Name: <name>" in per-filing claim overrides for filings whose Pass A code check Q1 fails; statuses are untouched). First used in b06 (10 of 25 filings are 2025+ layout).
- 25V377-7112 (b06): the frozen sentence splitter cuts at "lbs." (weights) and Pass A/B produced fragments that Pass C had to rule out (D042-D045); 25V100/25V164: lists of dates after a sentence ("These occurred October 2023, June 2024, ...") become separate events in the auto draft. Splitter/date-finder limitations, not changed.
- 25V132-5563 (b06): 'Ford informed NHTSA of this concern' is neither a Part 573 submission nor a recall notice; Pass C ruled it not NHTSA_FILING. The rules' NHTSA_FILING definition ('submits or amends a Part 573 report, or informs NHTSA that it will recall') leaves 'informs NHTSA of a concern' unsettled.
- 25V598-1713 (b07, KTM): the chronology lines begin with a day number ("20. Jan 2023:", "11. Sept 2025: ..."). The frozen date finder and both labelers read them as month-only dates and attached the next line's reference number to the quote; Pass C corrected 15 of 16 items (NEITHER). The rules do not describe the 'D. Mon YYYY' format. Logged, not changed.
- 25V565/25V521/25V659 (b07): (D039) whether a planned action ('Inspection of field motor home to be performed.') is an event is not settled; one sentence stating both awareness and investigation start (D027) has no tie-break (same gap as b02/b05).
- b07 had the highest A-vs-B event disagreement so far (events agree 46.6%): Pass B labels more events per filing than Pass A's code draft (209 vs fewer); the Pass C agreement with A was 3.7%. This reflects Pass A's compact-sheet overrides (D-P8) as well as rule ambiguity.
- D-T3 (cont., b08). Some 2025+ blocks list several suppliers (e.g. 'Tier 1 ... Name: TriMark Corporation ... Tier 1 ... Name: Spartan Fire LLC'); Pass A's S1 name joins them ('TriMark Corporation Spartan Fire LLC'). For the 4 b08 filings the S1/S2 quote was set to the first supplier's Name line by a manual per-filing override; statuses unchanged.

## Test-B batch 2 (b02)
- Pass B (opus) isolation: read the tool-captured stdout of `cat texts/*.txt`, a file outside the batch directory (self-logged). Content was the same filing texts.
- Pass C D016/D017 (Ford 26V236): CONTESTED because X and Y label different sentences (event-matching artefact, not a true disagreement). Rules unchanged.
- Rule ambiguity: date taken from a "Month(s):" section header vs. from the sentence itself (D036, D039, D040); Pass C resolved to the sentence. Rules not changed.
- Rule ambiguity: Ford CCRG referral typed INVESTIGATION_START vs FILER_AWARENESS (26V236); consistent within the batch only.

## Test-B batch 3 (b03)
- Pass B (opus) isolation: printing all texts at once made the tool save the output to a file outside the batch directory; the agent did not open it and re-printed in smaller groups.
- Rule problem: date ranges written "March and April 2026", "From November 2025, through June 2026", "5/5-6/2026" are split by the frozen code into two events (26V415, 26V405, 26V413); Pass B keeps one event with the full range. Pass C said the rules do not settle it. Not fixed. (26V405 handled with a dates override.)
- Rule problem: "built on or after <date>" production-window dates read as event dates (26V397, 26V419 Jan 13, 2026); Pass C treated them as window bounds.
- Rule problem: sentences after a blank line inside a dated entry (26V419) - inherit or undated; Pass C ruled undated.
- Rule problem: a block Name field that is only a pointer to an attachment (26V510 "See - Seat Belt Assembly Supplier.pdf"): S1 NOT_REPORTED (Pass B, Pass C) vs SUPPORTED (Pass A code). Pass A not changed; Pass C decided.
- Rule problem: cause stating a mechanism plus "still under investigation" (26V415): SUPPORTED vs INSUFFICIENT; Pass C CONTESTED.
- Pass C CONTESTED D002/D008/D014 (Ford/IMC, 26V369-26V374 + 26V397) and D042 (26V419) are event pairing artefacts (different sentences paired).
- Multi-supplier block 26V416: joined names; manual S1/S2 quote override (D-T3).

## Test-B batch 4 (b04)
- Pass B (opus) and Pass C batch_2 isolation: first `cat` of all texts overflowed and the tool saved the output outside the batch directory; neither agent opened that file and both re-read inside the directory.
- Rule problem: day-prefixed month-year dates ("16-Sep-2026 ...", "5-May-2026", "28-APR-2026 through 5-May-2026" in 26V644, 26V568) lose the day in Pass A code (date_text "Sep-2026"); Pass C corrected D032 to "5-May-2026". Same family as the KTM 25V598 format. Not fixed.
- Rule problem: "Late Aug-2026" - leading modifier dropped from date_text (D047, 26V644).
- Rule problem: "May and June 2026" - two dates or one range (D014/D016, 26V531); Pass C: two events. Contradicts the batch-3 reading of "March and April 2026" as one period in places; rules silent.
- Rule problem: meetings held to find root cause/scope (OTHER per rules vs INVESTIGATION_START) - D003 (26V518) and D027 (26V558 or 26V561) CONTESTED; D044 (26V638) review of reports aimed at planning part collection CONTESTED.
- Rule problem: control-bypass/production-window dates (26V577 Dec 27, 2025 - Jan 23, 2026) are window bounds, not events (Pass C D036/D037).
- Rule problem: a supplier's own Part 573 filing (Weldon, 26V521): typed OTHER by Pass C (D009).
- Pass A code bug seen again: "8/27/26: ... voted in favor" excluded as status statement (26V554), fixed by include override.
- Multi-supplier block 26V581 (Astotec / Joyson): joined names; manual S1 quote override (D-T3).

## Unseen-filer fetch
- D-T1 (again): 23V320 and 24V945 have no text layer (scanned); excluded and never replaced; see reports/phase_6_unseen_fetch.md. 98 of 100 labelled.

## Unseen-filer batch 1 (b01)
- Pass B and Pass C isolation: no outside reads reported.
- Rule problem: sentences listing several data dates ("warranty claims were received on 2022-03-30, 2022-07-21, ...", 23V475) yield one event per date unless ignore_dates is used; Pass C treated as non-event dates (D027).
- Rule problem: supplier's own awareness/decision (23V493 Cummins; D034, D035): DECISION is not limited to the filer; supplier awareness typed OTHER.
- Rule problem: routine quality-control test vs investigation (3M, 23E033; D005) - OTHER.
- Rule problem: cause "Defective part." - INSUFFICIENT (23V161, D021).
- Pass C CONTESTED D033 (23V481): pairing artefact (two sentences of one entry).

## Unseen-filer batch 2 (b02)
- Environment: macOS AppleDouble `._*` files appear next to the texts on the external drive; Pass B hit a non-UTF-8 `._` file in texts/, did not open it, and filtered it out. Pass C was told to ignore `._` files. No label content affected.
- Rule problem: a Pass A S2/U quote can be empty when the supplier is named in a sentence the splitter cut (24E051, USK Internacional "S.A. de C.V."); manual quote override.
- Rule problem: date ranges with "through" (24E024, "From February 17, 2023, through February 20, 2024") - one event or two (Pass C: two, D027); "a second date inside a data-supply sentence" (24E067 "data Cruise provided in 2023", D032).
- Rule problem: sentence after a dated entry line ("On Friday 5/31/2024 ...") is prose, not inherited (24E043, D029 NEITHER).
- Rule problem: record/inventory reviews to find the affected population - INVESTIGATION_START per Pass C (D008, D011, D015, D017, D024) but OTHER in Pass A in places.
- Rule problem: typo date "March12, 2024" (24V203) handled by a dates override.
- Rule problem: block names the filer while the narrative names the real maker (23V530 Chinook / Cummins, D004).

## Unseen-filer batch 3 (b03)
- Pass B and Pass C: no outside reads reported; `._` files ignored.
- Rule problem: "between X and Y" ranges (24V781 "9/27 - 10/10/2024", 25E037 "Between May 13 and May 21") - Pass C splits into one event per date (D014, D028, D029, D032) while Pass B/Pass A keep ranges or split inconsistently.
- Rule problem: Standing General Order incident reports to NHTSA are not Part 573 filings (25E037; D026 OTHER).
- Rule problem: deploying a software update to affected vehicles - remedy logistics vs occurrence (25E037, D030).
- Pass C CONTESTED D005, D013, D023 (24V524 etc.): pairing artefacts (different sentences paired as one event).
- Rule problem: header junk "Condition considered as a critical concern ... 2024-12-13;" in Polestar filings (24V939, 24V940) read as dated events.

## Unseen-filer batch 4 (b04)
- Pass C agents hit the account session rate limit mid-run (HTTP 429) and were resumed with SendMessage after the reset; they continued from their saved transcripts. No labels were changed by the interruption.
- Rule problem: an opening "On or around <date>" prose sentence followed by undated sentences (25V342): Pass A inherits the date, Pass C ruled undated (D021-D025 NEITHER).
- Rule problem: build/production dates as event dates ("March 2025" vehicle build, 26E004; D047).
- Rule problem: typo date "12/16/20205" (26E004; D049) kept as written.
- Rule problem: "finalizes recall remedy" lines (25V783, D045/D046): OTHER event vs remedy logistics; "As of ... N warranty claims" status sentence with a first-claim date (D030 CONTESTED).
- Rule problem: "identifies a condition and opens an investigation" in one sentence (D041 CONTESTED), same family as earlier awareness-plus-investigation.
- Pass C CONTESTED D008-D011 (25E058): pairing artefacts.
- Multi-supplier block 26V063: doubled name; manual S1 quote override (D-T3).

## Amendment 1 (tag amendment-1; docs/AMENDMENT_1.md)
- Scorer wrapper `tt/eval/amend1.py` (rules a, b, c; crash-only `parse_span` guard; bounding and sensitivity switches); frozen scorer files untouched. Resolves the open D-T2 scorer-crash issue for scoring.
- Definition of "excluded gold event" fixed as "date text present and no ISO span" AFTER the first dev re-score under the broader "or flagged date_inferred" reading changed one dev prediction (434 -> 433, 19V811-5724 '11-13-'); the broader reading is kept as the pre-declared sensitivity `inferred_too`. Fixed before any Test-A model output exists.
- `tt/leakcheck.py` already skipped `._*` files (line 68); a test now pins it. The runner reads the selection list only.
- Isolation slips listed in config/isolation_slips.json (3 slips, 56 filings; outside-knowledge case 24V556-5723).

## Test-A model runs (2026-10-20)
- Run 1 (temperature 0, seed 0): 12:48:52 start, 16:10:07 done, 199/199 records, JSON-valid 100%, 0 call errors, no restart.
- Run 2 (temperature 0.5, seed 1): 16:10:10 start; interrupted; RESTART 21:32:45 with 167 of 199 records already in the file (resume=True, frozen settings); done 22:12:05, 199 records, JSON-valid 0.9749, 5 call errors.
- The 5 run-2 errors (all before the restart, lines 160, 164, 165, 166, 167 of the file): four per-call timeouts at 300 s (RCLRPT-25V507-9357, 25V544-9834, 25V562-5431, 25V565-4354; no model output retained) and one "model runner has unexpectedly stopped" at 2 s (RCLRPT-25V574-1873; no model call completed, no output). No record had an invalid-JSON output.
- RETRY (owner rule: only records where no model call completed): RCLRPT-25V574-1873 re-run once with the frozen run-2 settings (temperature 0.5, seed 1, prompt v2, num_ctx 6144, timeout 300 s) by scripts/phase6_retry.py; it returned valid JSON on attempt 1 and replaced the failed record at line 167. The other 198 lines are unchanged (checked). The four timeouts were NOT retried. Original file kept as runs/testA_4b_v2_run2.pre_retry.jsonl (sha256 7ecd9fba...).
- Counts before -> after the retry: run 2 JSON-valid 194 -> 195 of 199 (97.49% -> 97.99%); call errors 5 -> 4 (all timeouts). Run 1 unchanged (199/199).
- Frozen handling of the four remaining run-2 failures: tt.eval.diagnose/phase4 read a run-2 record without an extraction as `None`, so "run 2 agrees" is false for that filing's run-1 claims (they cannot be accepted); run-2 claims are never scored. No rule was changed.
- (2026-10-20) Sensitivity retry of the four run-2 timeouts (RCLRPT-25V507-9357, 25V544-9834, 25V562-5431, 25V565-4354), once, frozen run-2 settings, after the primary endpoints file was committed: separate file runs/testA_4b_v2_run2.retry_timeouts.jsonl (4/4 valid JSON), never merged into runs/testA_4b_v2_run2.jsonl; scoring-only copy runs/testA_4b_v2_run2.sens_with_retry.jsonl. H1 verdict unchanged (PASS, delta 0.1406 vs 0.1352 primary).
- (2026-10-20) Primary Test-A scoring done once via `python -m tt.eval.amend1 endpoints|phase3|phase4|report`; sensitivity variants in reports/phase_6_testA_sens/ (scripts/phase6_sens.py). The rule-c trigger (excluded gold events 2.72% of dated gold events) required the two bounding runs; they are included.
- (2026-10-21) H4 held-out injection run (30 attacks, runA/runB, frozen settings) scored once; report reports/phase_6_H4.md.
- (2026-10-25) EXPLORATORY analyses 2 (d)-(g) on Test-A outputs, scoring only: reports/phase_6_exploratory_2.md; the (f) cluster-sum t-bound failed its validity check (false-certification rate above 0.01 in every scenario) and is reported as not valid; nothing frozen changed.

## Secondary splits (2026-10-25 to 2026-10-27)
- RESTART of Test-B run 2 (2026-10-27 11:48:06): the Mac entered Low Power Sleep on battery at 1% charge on 2026-10-25 17:56:21 (pmset) and rebooted 19:22:49, killing the runner and Ollama; run 2 had written no record. Resumed on AC power under scripts/phase6_supervise.sh with Ollama 0.40.6 and qwen3.5:4b-q4_K_M digest d8b0f5e9760c checked. Backups runs/testB_4b_v2_run{1,2}.pre_resume_20261027_114805.jsonl. No other restart; no timeouts, crashes or invalid outputs on Test-B or unseen-filer.
- Test-B and unseen-filer scored once with the amendment-1 wrapper (exploratory); Test-B exceeded the 2% ignored-prediction line (14 of 524) so the two bounding runs were added (reports/phase_6_testB_sens/). A descriptive diagnosis of Test-B's small H1 delta (Ford/Jayco concentration, one post hoc leave-one-cluster diagnostic) is in reports/phase_6_secondary_splits.md; nothing was changed or rerun.
