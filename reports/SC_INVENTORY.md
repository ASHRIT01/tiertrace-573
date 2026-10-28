# SC-1 Step 0 inventory: supplier and component reference

**Reference = filer-declared supplier/component (non-AI, not ground truth).** This file has parsing, strata and field checks only: **no agent or silver claim was compared with the reference.** Only company names, supplier type and country are kept from the supplier block; address and telephone lines are never stored or printed, and the example blocks below redact them. No model was run, and nothing under `freeze-v1`, `amendment-1` or `ts-protocol-1` changed. Scripts: `scripts/sc_lib.py` (parsers, normalisation), `scripts/sc_gate.py` (reads the frozen gate decisions for supplier claims), `scripts/sc_inventory.py`. Raw output: `reports/sc/SC_INVENTORY.json`.

## 1. Supplier block: layouts, parser, parse rate
Text comes from the frozen `extract_text` followed by `clean`. The parser (`supplier_blocks`) works by regex and layout only:
- **Start:** a line that is only "Component Manufacturer", optionally preceded by "Supplier Identification :".
- **Fields:** `Tier of Supplier`, `Supplier Type`, `Name`, `Address`, `Country`. Each value is either on the label line (older layout, "Name : X") or on the following line(s) (portal layout, "Name:" then "X").
- **Records:** a new supplier record starts at a repeated Name, Tier or Type label.
- **Skipped:** repeated page-header lines of the portal form. Address values are skipped and never stored.
- **End:** the next section heading (Involved Components, Chronology, Description of Remedy, Component Name, …).

**Portal layout ("Component Manufacturer" … "Supplier Type:" … "Name:" … "Country:")**: 5 real examples (address and other lines redacted):

- Test-A: `Component Manufacturer / Tier of Supplier: / Supplier Type: / Name: / ICM Controls / Address: [redacted] / [lines redacted] / Country: / United States`
- Test-B: `Component Manufacturer / Tier of Supplier: / Tier 2 / Supplier Type: / Other / Name: / Samsung SDI Co., Ltd. / Address: [redacted] / [lines redacted] / Country: / Hungary`
- unseen-filer: `Component Manufacturer / Tier of Supplier: / Supplier Type: / Name: / RECARO Automotive North America, Inc. / Address: [redacted] / [lines redacted] / Country: / United States`
- unseen-filer: `Component Manufacturer / Tier of Supplier: / Supplier Type: / Other / Name: / Accauto Co., LTD / Address: [redacted] / [lines redacted] / Country: / Thailand`
- unseen-filer: `Component Manufacturer / Tier of Supplier: / Tier 1 / Supplier Type: / OEM / Name: / Knorr-Bremse / Address: [redacted] / [lines redacted] / Country: / Germany`

**Older layout ("Supplier Identification : Component Manufacturer")**: 5 real examples (address and other lines redacted):

- Test-A: `Supplier Identification : / Component Manufacturer / Name : CONTINENTAL AUTONOMOUS MOBILITY US / Address: [redacted] / [line redacted] / Country : United States`
- unseen-filer: `Supplier Identification : / Component Manufacturer / Name : 3M Company / Address: [redacted] / [line redacted] / Country : United States`
- Test-A: `Supplier Identification : / Component Manufacturer / Name : East Penn Manufacturing Co. / Address: [redacted] / [line redacted] / Country : United States`
- Test-A: `Supplier Identification : / Component Manufacturer / Name : Suburban Manufacturing Co / Address: [redacted] / [line redacted] / Country : United States`
- Test-A: `Supplier Identification : / Component Manufacturer / Name : Autocar LLC / Address: [redacted] / [line redacted] / Country : United States`

| split | layout | filings | block heading found | parsed (heading and a Name label) |
|---|---|---|---|---|
| Test-A | portal | 62 | 62 | 62/62 |
| Test-A | older | 137 | 137 | 137/137 |
| Test-B | portal | 100 | 100 | 100/100 |
| unseen-filer | portal | 24 | 24 | 24/24 |
| unseen-filer | older | 74 | 74 | 74/74 |

**Parse rate: 397/397. Failures: none.** Every filing has exactly one block heading.

## 2. Supplier strata
Precedence: PARSE_FAIL > BLANK > MULTIPLE > OEM_SELF > OBTAINED_FROM > NAMED_SUPPLIER.
- **BLANK:** the name is empty, NR or N/A, or is a pointer to an attachment ("See - … .pdf": 2 filings).
- **MULTIPLE:** two or more different normalised names.
- **OBTAINED_FROM:** Supplier Type "Distributor", or distributor or obtained-from wording in the name.

| split | layout | NAMED_SUPPLIER | OEM_SELF | OBTAINED_FROM | MULTIPLE | BLANK | PARSE_FAIL |
|---|---|---|---|---|---|---|---|
| Test-A | portal | 41 | 3 | 1 | 3 | 14 | 0 |
| Test-A | older | 99 | 17 | 0 | 0 | 21 | 0 |
| Test-B | portal | 60 | 15 | 1 | 3 | 21 | 0 |
| unseen-filer | portal | 12 | 3 | 2 | 0 | 7 | 0 |
| unseen-filer | older | 43 | 9 | 0 | 0 | 22 | 0 |
| **Test-A** | all | 140 | 20 | 1 | 3 | 35 | 0 |
| **Test-B** | all | 60 | 15 | 1 | 3 | 21 | 0 |
| **unseen-filer** | all | 55 | 12 | 2 | 0 | 29 | 0 |
| **all** | all | 255 | 47 | 4 | 6 | 85 | 0 |

**OEM_SELF: why the literal rule is not used.** The instruction defined OEM_SELF as "Supplier Type 'OEM', or the name normalises to the filer's MFGNAME". In the portal form, though, "OEM" is a supplier type for original-equipment suppliers:

| Supplier Type | declared name = a filer name | declared name ≠ filer |
|---|---|---|
| OEM | 13 | 52 |
| Other | 1 | 15 |
| Distributor | 0 | 5 |
| (blank) | 33 | 203 |

- **Most OEM-typed names are external suppliers:** 52 of the 65 OEM-typed names are not the filer (they include large external parts makers).
- **Primary definition:** to avoid dropping them, OEM_SELF is the single declared name normalising to a filer name, either a flat-file MFGNAME of the campaign or the PDF header "Manufacturer Name". MFGNAME is truncated to 40 characters.
- **The literal rule** (Supplier Type OEM also counts as OEM_SELF) is kept as a pre-declared sensitivity. Its strata would be: Test-A NAMED_SUPPLIER 125, OEM_SELF 35, OBTAINED_FROM 1, MULTIPLE 3, BLANK 35; Test-B NAMED_SUPPLIER 39, OEM_SELF 36, OBTAINED_FROM 1, MULTIPLE 3, BLANK 21; unseen-filer NAMED_SUPPLIER 47, OEM_SELF 21, OBTAINED_FROM 1, BLANK 29.

## 3. Involved Components block
The parser (`component_records`) reads `Component Name [n]`, `Component Description` and `Component Part Number`, either with "label : value" on one line or the label followed by the value line.

| split | layout | filings | PRESENT (a name or part number) | BLANK | PARSE_FAIL | records | filings with a component name | filings with a part number |
|---|---|---|---|---|---|---|---|---|
| Test-A | portal | 62 | 62 | 0 | 0 | 206 | 62 | 55 |
| Test-A | older | 137 | 137 | 0 | 0 | 206 | 137 | 123 |
| Test-B | portal | 100 | 99 | 1 | 0 | 177 | 98 | 93 |
| unseen-filer | portal | 24 | 24 | 0 | 0 | 41 | 24 | 20 |
| unseen-filer | older | 74 | 68 | 6 | 0 | 125 | 68 | 64 |

## 4. NHTSA flat file
- **File:** `data/flat/FLAT_RCL_POST_2010.zip` (member `FLAT_RCL_POST_2010.txt`, member date 2026-10-18), SHA-256 `d4c96957c1de88eb415fb4b6fcd532dbb567a00782268618b279c9a67c063c74`.
- **Column names:** RECORD_ID, CAMPNO, MAKETXT, MODELTXT, YEARTXT, MFGCAMPNO, COMPNAME, MFGNAME, BGMAN, ENDMAN, RCLTYPECD, POTAFF, ODATE, INFLUENCED_BY, MFGTXT, RCDATE, DATEA, RPNO, FMVSS, DESC_DEFECT, CONEQUENCE_DEFECT, CORRECTIVE_ACTION, NOTES, RCL_CMPT_ID, MFR_COMP_NAME, MFR_COMP_DESC, MFR_COMP_PTNO, DO_NOT_DRIVE, PARK_OUTSIDE.
- **No download.** MFR_COMP_NAME, MFR_COMP_DESC and MFR_COMP_PTNO are present, so nothing was downloaded and the old file is unchanged.
- **Join rule:** campaign id = 6 characters after 'RCLRPT-' in the PDF file name; flat rows whose CAMPNO (\d{2}[VECT]\d{6}) starts with it; all rows kept, distinct values per field.

| split | campaigns | joined | MFR_COMP_NAME: campaigns with a value (median / max distinct values) | MFR_COMP_DESC | MFR_COMP_PTNO |
|---|---|---|---|---|---|
| Test-A | 199 | 199 | 199 (1 / 8) | 191 (1 / 12) | 189 (1 / 70) |
| Test-B | 100 | 100 | 98 (1 / 6) | 97 (1 / 22) | 93 (1 / 22) |
| unseen-filer | 98 | 98 | 95 (1 / 3) | 92 (1 / 8) | 92 (1 / 21) |

## 5. What the claims store
- **Agent:** companies[]: name, role (SUPPLIER/SUB_SUPPLIER/DISTRIBUTOR count as supplier claims), status, evidence.section (cause/chronology/components/defect), evidence.quote; NO character offset; gate decision from the frozen agent.decide (scripts/sc_gate.py).
- **Silver:** claims S1 (block reports a component manufacturer; section 'block') and S2 (the narrative names that supplier; section cause/chronology): id, label (contains the name after ': '), status, quote, section; NO character offset; no gate.
- **Components:** neither the frozen agent schema (tt/agent/schemas.py) nor the silver labels contain component claims. Component metrics (protocol E) therefore have no claims to score.

**Locating quotes.** No claim stores a character offset. A quote is located in the parsed text by `locate_quote` (`scripts/sc_lib.py`), which is whitespace-insensitive and lets a `[MASKED]` token stand for the masked name.

| count | Test-A | Test-B | unseen-filer | all |
|---|---|---|---|---|
| agent supplier claims (all) | 109 | 50 | 67 | 226 |
| agent supplier claims (gate-accepted) | 35 | 20 | 37 | 92 |
| agent quote located in parsed text | 91 | 49 | 65 | 205 |
| agent quote contains [MASKED] | 29 | 16 | 15 | 60 |
| silver S1 SUPPORTED | 164 | 79 | 69 | 312 |
| silver S1 quote located in parsed text | 164 | 79 | 69 | 312 |
| silver S2 SUPPORTED | 77 | 41 | 40 | 158 |
| silver S2 quote located in parsed text | 77 | 41 | 40 | 158 |

**Agent claims** are companies with role SUPPLIER, SUB_SUPPLIER or DISTRIBUTOR and status SUPPORTED; acceptance follows the frozen gate (score ≥ 3). **Silver claims** are S1 (the block's component manufacturer, read from the block) and S2 (the narrative names that supplier), SUPPORTED only. Silver has no gate. Agent quotes that cannot be located are not verbatim, which is the same failure V1 rejects.

## 6. Does the agent's input contain the supplier block?
**No, in either layout.** How this was checked: the frozen tt.agent.run_dev.build_user rebuilt for every filing (no model call): 'CAUSE:' + cause + 'CHRONOLOGY:' + chronology, block name masked.

| split | layout | filings | input contains a block heading or block field line | input contains [MASKED] | a declared name appears verbatim (case-insensitive) in the input |
|---|---|---|---|---|---|
| Test-A | portal | 62 | 0 | 9 | 6 |
| Test-A | older | 137 | 0 | 15 | 14 |
| Test-B | portal | 100 | 0 | 16 | 17 |
| unseen-filer | portal | 24 | 0 | 5 | 6 |
| unseen-filer | older | 74 | 0 | 10 | 12 |

**What this means:**
- **The agent never sees the block.** It reads only the cause and chronology, with the frozen block name masked wherever it appears.
- **So an agent claim matching the declared supplier cannot have been copied from the block.** Such a claim comes from a narrative mention that the mask did not catch: a different spelling, or a multi-supplier name the frozen parser joined.
- **A declared name can still appear unmasked** in the input when it is also the filer's own name (OEM_SELF), or when it is spelled differently from the frozen block name.
- **The silver S1 claims are read from the block itself** (circular by construction). Silver S2 claims come from the narrative.
