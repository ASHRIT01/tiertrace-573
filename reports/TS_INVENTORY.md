# TS-1 Step 0 inventory: timeliness screen inputs

**Silver reference (AI-generated, not human-verified).** This file has counts and field checks only: **no gap and no date difference was computed.** Aggregates only; no company names or recall numbers. It was produced by `scripts/ts_gate.py`, which reads the frozen gate decisions without changing them, and `scripts/ts_inventory.py` (raw output `reports/ts/TS_INVENTORY.json`). No model was run and nothing under `freeze-v1` or `amendment-1` changed.

## 1. Filings
| split | processed, readable filings | note |
|---|---|---|
| Test-A | 199 | 200 drawn; 1 had no text layer and was excluded (amendment 1) |
| Test-B | 100 | 100 drawn; all readable |
| unseen-filer | 98 | 100 drawn; 2 had no text layer and were excluded (amendment 1) |
| **all** | **397** | |

## 2. Submission date in the PDF text
The text comes from the frozen extractor (`tt.parse.pdf.extract_text`). Below are five real headers, one for each split and form layout. Every value except the date is redacted.

- Test-A, pre-2025 form (label : value on one line): `[redacted line] / Manufacturer Name: [redacted] / Submission Date : FEB 09, 2023 / NHTSA Recall No.: [redacted] / Manufacturer Recall No.: [redacted]`
- Test-A, 2025+ form (label and value on separate lines): `[redacted line] / Manufacturer Name: [redacted] / Submission Date: Jun 20, 2025 / NHTSA Recall No.: [redacted] / Manufacturer Recall No.: [redacted]`
- Test-B, 2025+ form (label and value on separate lines): `[redacted line] / Manufacturer Name: [redacted] / Submission Date: May 04, 2026 / NHTSA Recall No.: [redacted] / Manufacturer Recall No.: [redacted]`
- unseen-filer, pre-2025 form (label : value on one line): `[redacted line] / Manufacturer Name: [redacted] / Submission Date : MAY 02, 2023 / NHTSA Recall No.: [redacted] / Manufacturer Recall No.: [redacted]`
- unseen-filer, 2025+ form (label and value on separate lines): `[redacted line] / Manufacturer Name: [redacted] / Submission Date: Jun 26, 2025 / NHTSA Recall No.: [redacted] / Manufacturer Recall No.: [redacted]`

Regex: `Submission\s*Date\s*:\s*([A-Za-z]{3,9})\.?\s+(\d{1,2}),\s*(\d{4})`. It allows 1–2 digit days ("MAR 7, 2025") and 3–9 letter month names; the month is matched on its first three letters.

| split | pre-2025 form | 2025+ form | parsed | single occurrence in the text | one-digit day seen | equals frozen `parse_header` | equals silver `filing_date` |
|---|---|---|---|---|---|---|---|
| Test-A | 137 | 62 | 199/199 | 199 | 0 | 199 | 199 |
| Test-B | 0 | 100 | 100/100 | 100 | 0 | 100 | 100 |
| unseen-filer | 74 | 24 | 98/98 | 98 | 0 | 98 | 98 |

Parse rate: **397/397**. Failing layouts: none. Every processed filing holds exactly one Submission Date, and all three readings agree.

## 3. NHTSA flat file
- **File:** `data/flat/FLAT_RCL_POST_2010.zip` (member `FLAT_RCL_POST_2010.txt`); layout data/flat/RCL.txt (TAB-delimited, 29 fields, dates YYYYMMDD; last updated May 2025).
- **Column names** (from RCL.txt, as used by `tt/data/flat.py`): RECORD_ID, CAMPNO, MAKETXT, MODELTXT, YEARTXT, MFGCAMPNO, COMPNAME, MFGNAME, BGMAN, ENDMAN, RCLTYPECD, POTAFF, ODATE, INFLUENCED_BY, MFGTXT, RCDATE, DATEA, RPNO, FMVSS, DESC_DEFECT, CONEQUENCE_DEFECT, CORRECTIVE_ACTION, NOTES, RCL_CMPT_ID, MFR_COMP_NAME, MFR_COMP_DESC, MFR_COMP_PTNO, DO_NOT_DRIVE, PARK_OUTSIDE.
- **CAMPNO format** (letters shown as A, digits as 9, all rows): `99A999999` 244,431, `99A99A999` 1,678. A test campaign is `YYTNNN` plus 3 digits.
- **Join rule:** campaign id = the 6 characters after 'RCLRPT-' in the processed PDF file name (e.g. YYTNNN); flat-file rows with CAMPNO matching \d{2}[VECT]\d{6} whose first 6 characters equal it; one campaign has many rows (one per make/model/year), the first row by file order is used after checking the fields below are constant across rows.
- **Join rate:** Test-A 199/199, Test-B 100/100, unseen-filer 98/98. Fields that differ across a campaign's rows: RCDATE 0, RCLTYPECD 0, INFLUENCED_BY 0, FMVSS 0, RPNO 0.

| field | exists | meaning (RCL.txt) | what the joined campaigns hold |
|---|---|---|---|
| RCDATE | yes | Part 573 Defect/Noncompliance Report Received Date | 397/397 present, YYYYMMDD |
| INFLUENCED_BY | yes | Recall Initiated By (MFR/OVSC/ODI) | MFR 349, ODI 42, OVSC 5, (empty) 1 |
| RCLTYPECD | yes | Vehicle, Equipment, Child Restraint, Or Tire Part 573 Defect/Noncompliance Report | V 341, E 56; codes the product type (V/E/C/T), NOT defect vs noncompliance |
| FMVSS | yes | Federal Motor Vehicle Safety Standard Number | non-empty 104/397 |
| RPNO | yes | Regulation Part Number | non-empty 0/397 |
| defect/noncompliance indicator | **no** | — | none: no flat-file column states defect vs noncompliance (FMVSS gives a standard number, which defect reports can also carry) |

## 4. Defect vs noncompliance
Sources checked:
- **(a) Report text header (pre-2025 form only):** "Description of Defect :" or "Description of Noncompliance :".
- **(b) The 2025+ form:** it has one combined heading, "Description of the defect or noncompliance:", and **no type field**.
- **(c) NHTSA document titles in the version listing:** "Defect Notice 573 Report" or "Noncompliance Notice 573 Report" on any version.
- **(d) The flat file has no type field.** The only proxy is FMVSS: empty → defect, non-empty → noncompliance.

| split | header DEFECT | header NONCOMPLIANCE | header absent (2025+ form) | title DEFECT | title NONCOMPLIANCE | title absent | flat FMVSS empty | flat FMVSS non-empty |
|---|---|---|---|---|---|---|---|---|
| Test-A | 104 | 33 | 62 | 55 | 15 | 129 | 144 | 55 |
| Test-B | 0 | 0 | 100 | 0 | 0 | 100 | 73 | 27 |
| unseen-filer | 62 | 12 | 24 | 41 | 5 | 52 | 76 | 22 |

Cross-checks where two sources exist (all splits): header DEFECT vs flat FMVSS proxy DEFECT 153; header DEFECT vs flat FMVSS proxy NONCOMPLIANCE 13; header NONCOMPLIANCE vs flat FMVSS proxy DEFECT 1; header NONCOMPLIANCE vs flat FMVSS proxy NONCOMPLIANCE 44; header vs title: DISAGREE 2; header vs title: agree 114.

The header and the NHTSA title disagree on 2 filings; the header is used.

**Which source decides:** the report text header when present. Otherwise the NHTSA document title, which never decided a filing here: every filing with a title also has a header. Otherwise the flat-file FMVSS proxy.

| split | DEFECT by header | NONCOMPLIANCE by header | DEFECT by FMVSS proxy | NONCOMPLIANCE by FMVSS proxy |
|---|---|---|---|---|
| Test-A | 104 | 33 | 48 | 14 |
| Test-B | 0 | 0 | 73 | 27 |
| unseen-filer | 62 | 12 | 18 | 6 |

**The proxy's limits.** Every 2025+-form filing is typed by the proxy: 186 of 397, and all 100 Test-B filings. On the 211 pre-2025-form filings, the proxy matches the header as follows:
- Proxy DEFECT: 153 of its 154 calls are header DEFECT.
- Header DEFECT: 13 of 166 would be called NONCOMPLIANCE by the proxy, because a defect report can cite an FMVSS.
- Header NONCOMPLIANCE: 1 of 45 would be called DEFECT.

So the proxy mostly errs by leaving defect filings out of the defect population.

## 5. What the events store
- **Silver labels:** date_text (raw, as written; for an entry-header date the header text), span (ISO start/end; stored only for Pass A items), quote, type, flags inherited_date/date_inferred/contested.
- **Agent claims:** date_text (raw), type, status, evidence.quote, evidence.section; no ISO date; acceptance from the frozen gate (score >= 3).

| count | Test-A | Test-B | unseen-filer |
|---|---|---|---|
| silver events (all) | 1466 | 806 | 580 |
| silver events contested (dropped) | 21 | 16 | 11 |
| silver non-contested | 1445 | 790 | 569 |
| — with raw date text | 991 | 527 | 436 |
| — undated (no date text, no span) | 454 | 263 | 133 |
| — with stored ISO span | 757 | 416 | 340 |
| — ISO span only (no raw date text) | 0 | 0 | 0 |
| — raw date text but no stored span | 234 | 111 | 96 |
| — with evidence quote | 1445 | 790 | 569 |
| — DECISION (all) | 180 | 95 | 63 |
| — DECISION with raw date text | 170 | 93 | 58 |
| — DECISION quote cites a different recall number | 2 | 1 | 2 |
| agent filings with valid run-1 output | 199 | 100 | 98 |
| agent filings with valid run-2 output | 195 | 100 | 98 |
| agent run-1 events | 1006 | 524 | 445 |
| agent run-1 events with raw date text | 1006 | 524 | 445 |
| agent run-1 events with evidence quote | 1006 | 524 | 445 |
| agent run-1 DECISION (any gate outcome) | 170 | 97 | 62 |
| agent accepted events | 537 | 264 | 231 |
| agent accepted DECISION | 111 | 48 | 34 |
| agent accepted DECISION with raw date text | 111 | 48 | 34 |
| agent accepted DECISION quote cites a different recall number | 2 | 0 | 0 |

**What this means for the screen:**
- **No event is ISO-only.** Every event with a stored ISO span also has its raw date text.
- **The stored span is incomplete.** It is missing for every Pass-C-decided item (Test-A 229, Test-B 111, unseen 94) and for 7 Pass A items whose text the frozen parser could not read (Test-A 5, unseen 2). The screen therefore re-parses `date_text` for both the silver labels and the agent with one parser.
- **Quotes are present on every event**, so the different-recall-number rule (protocol E) can run.
- **Agent counts:** they are run-1 events and their acceptance by the frozen gate (score ≥ 3), the same set as H1. On Test-A, the 4 filings with a run-2 timeout have no accepted claim.

## 6. Original vs amended version
**Knowable for every filing** from the NHTSA version listing (`is_original`, `n_versions`). Only the latest version was downloaded and none of the originals of multi-version campaigns is cached, so the original's own Submission Date is **not** available.

| split | processed PDF is the original (only version) | processed PDF is a later (amended) version | processed is the latest |
|---|---|---|---|
| Test-A | 99 | 100 | 199 |
| Test-B | 55 | 45 | 100 |
| unseen-filer | 30 | 68 | 98 |

For a later version, the PDF's Submission Date may be the amendment's date rather than the original filing date. That matters for any filing-date anchor; the protocol handles it (TS_PROTOCOL.md section C and the version sensitivity).

## 7. Raw date-text formats
Each non-empty date text was classified by the TS parser (`scripts/ts_lib.py`, `date_format`), independently of any filing date:
- **full_date:** a day with a year.
- **numeric_ambiguous:** a numeric date that reads validly as both mm/dd and dd/mm.
- **yearless:** a day or month with no year.
- **week:** "CW51/2020" or "week of …".
- **early_mid_late:** of a month or a year.
- **quarter, year, range** (two dates), and **unparsed.**

Silver = non-contested events. Agent = run-1 events accepted by the frozen gate.

| split | set | full_date | numeric_ambiguous | month | yearless | week | early_mid_late | quarter | year | range | unparsed | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Test-A | silver, all types | 622 | 49 | 153 | 60 | 3 | 16 | 0 | 4 | 82 | 2 | 991 |
| Test-A | silver, DECISION | 153 | 6 | 5 | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 170 |
| Test-A | agent accepted, all types | 389 | 30 | 50 | 24 | 0 | 5 | 0 | 2 | 37 | 0 | 537 |
| Test-A | agent accepted, DECISION | 104 | 3 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 111 |
| Test-B | silver, all types | 317 | 30 | 91 | 38 | 0 | 7 | 0 | 1 | 43 | 0 | 527 |
| Test-B | silver, DECISION | 84 | 3 | 5 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 93 |
| Test-B | agent accepted, all types | 187 | 17 | 29 | 3 | 0 | 3 | 0 | 0 | 25 | 0 | 264 |
| Test-B | agent accepted, DECISION | 44 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 48 |
| unseen-filer | silver, all types | 303 | 29 | 46 | 22 | 0 | 6 | 0 | 4 | 25 | 1 | 436 |
| unseen-filer | silver, DECISION | 47 | 4 | 0 | 6 | 0 | 1 | 0 | 0 | 0 | 0 | 58 |
| unseen-filer | agent accepted, all types | 182 | 14 | 14 | 11 | 0 | 3 | 0 | 1 | 6 | 0 | 231 |
| unseen-filer | agent accepted, DECISION | 28 | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 34 |

The 3 unparsed silver texts are a typo year, "throughout" used as a range word, and "the months leading up to …". None is a DECISION date. Every agent date text parses.
