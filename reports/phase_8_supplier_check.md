# Phase 8 (SC-1): agent and silver supplier claims checked against the filer's own declaration

**Reference = filer-declared supplier (non-AI, not ground truth).** The declared supplier is what the filer wrote under 49 CFR 573.6(c)(2)(iv). It may be a tier-1 assembler, the entity the part was obtained from, or the filer itself. **A match measures fidelity to the filer's declaration, not who really made the part, and a non-match is not an error by the filer.**

The computation follows the protocol fixed before any comparison (`reports/SC_PROTOCOL.md`, tag `sc-protocol-1`), with one amendment (SC-A1). No model was run, and nothing under `freeze-v1`, `amendment-1` or `ts-protocol-1` changed. Tests: `15 passed, 5 warnings in 0.80s` (`tests/test_sc_check.py`, run by the script before anything is written). Raw aggregates: `reports/sc/phase_8_supplier_check.json`. Aggregates only; no per-filer rows and no supplier names in any result table.

W = Wilson 95% CI; B = filer-cluster bootstrap 95% CI (2,000 resamples, seed 0); *unstable* = n < 20.

## Summary
**1. The reference and the population.**
- **Parsing:** the supplier block parses in 397/397 filings, in both layouts.
- **Population:** 261 filings declare one or more external suppliers (NAMED_SUPPLIER or MULTIPLE).
- **Other strata:** 47 OEM_SELF, 4 OBTAINED_FROM and 85 BLANK filings are reported as counts only.

**2. The agent never saw the supplier block.** Its frozen input is the cause and chronology, with the block name masked (Step 0). So its matches are recoveries from the narrative, not copies of the block.
- **All supplier claims:** exact match on 18/261 = 0.069 filings (recall) and 19/172 = 0.110 claims (precision).
- **Gate-accepted claims:** recall 13/261 = 0.050, precision 14/70 = 0.200.
- **Evidence location:** all agent evidence lies outside the block.
- **Why precision understates:** a correct sub-supplier named only in the narrative, and not in the block, counts as a non-match. Which companies the non-matching claims name was not tabulated.

**3. The silver labels against the declaration (the first non-AI check of the silver supplier labels).**
- **S1 (read from the block):** matches in 254/261 = 0.973 claims. This is circular by construction.
- **S2 (narrative claims):** match the declared supplier in 92/113 = 0.814 claims, and cover 92/261 = 0.352 population filings.

**4. Components: not run.** Neither the frozen agent schema nor the silver labels contain component claims. Only the reference's availability is reported.

## Inventory summary (`reports/SC_INVENTORY.md`, commit c27b962)
- **Supplier block:** one per filing in all 397. Parse rate 397/397, with 0 failures, in both layouts: portal (186) and older (211).
- **Agent input:** no block heading or field line appears in the agent's frozen input in any filing. The block name is masked wherever it appears.
- **Involved Components:** a name or part number is present in 390 of 397 filings, and flat-file MFR_COMP_NAME in 392 of 397. No new flat file was downloaded; the MFR_COMP fields are present (SHA-256 `d4c96957c1de88eb…`, member date 2026-10-18).
- **Supplier claims:**
  - Agent run-1: 226 in total, of which 92 are gate-accepted.
  - Silver: 312 S1 and 158 S2, SUPPORTED.
  - No claim stores a character offset, so quotes are located in the parsed text.

**Strata (supplier block)**

| split | NAMED_SUPPLIER | OEM_SELF | OBTAINED_FROM | MULTIPLE | BLANK | PARSE_FAIL |
|---|---|---|---|---|---|---|
| Test-A | 140 | 20 | 1 | 3 | 35 | 0 |
| Test-B | 60 | 15 | 1 | 3 | 21 | 0 |
| unseen-filer | 55 | 12 | 2 | 0 | 29 | 0 |
| **all** | 255 | 47 | 4 | 6 | 85 | 0 |

OEM_SELF is defined as a declared name normalising to the filer's name (protocol C). The instruction's literal rule, which also counts Supplier Type "OEM", is a sensitivity below.

## C(a)–(b): agent supplier claims, exact match (primary)
**Recall** is the share of population filings whose declared supplier set is matched by at least one agent claim. **Precision** is the share of agent supplier claims in population filings that match a declared name.

| group | filings | recall: all claims | recall: gate-accepted | precision: all claims | precision: gate-accepted |
|---|---|---|---|---|---|
| Test-A | 143 | 9/143 = 0.063 W[0.033, 0.115] B[0.025, 0.114] | 5/143 = 0.035 W[0.015, 0.079] B[0.007, 0.074] | 9/101 = 0.089 W[0.048, 0.161] B[0.037, 0.165] | 5/32 = 0.156 W[0.069, 0.318] B[0.033, 0.320] |
| Test-B | 63 | 4/63 = 0.063 W[0.025, 0.152] B[0.015, 0.133] | 3/63 = 0.048 W[0.016, 0.131] B[0.000, 0.109] | 4/34 = 0.118 W[0.047, 0.266] B[0.029, 0.222] | 3/17 = 0.176 W[0.062, 0.410] B[0.000, 0.400] *unstable* |
| unseen-filer | 55 | 5/55 = 0.091 W[0.039, 0.196] B[0.021, 0.188] | 5/55 = 0.091 W[0.039, 0.196] B[0.021, 0.188] | 6/37 = 0.162 W[0.077, 0.311] B[0.048, 0.324] | 6/21 = 0.286 W[0.138, 0.500] B[0.083, 0.556] |
| portal layout | 119 | 8/119 = 0.067 W[0.034, 0.127] B[0.025, 0.128] | 5/119 = 0.042 W[0.018, 0.095] B[0.009, 0.088] | 9/88 = 0.102 W[0.055, 0.183] B[0.039, 0.187] | 6/36 = 0.167 W[0.079, 0.319] B[0.047, 0.333] |
| older layout | 142 | 10/142 = 0.070 W[0.039, 0.125] B[0.030, 0.124] | 8/142 = 0.056 W[0.029, 0.107] B[0.022, 0.105] | 10/84 = 0.119 W[0.066, 0.205] B[0.056, 0.191] | 8/34 = 0.235 W[0.124, 0.400] B[0.108, 0.406] |
| vehicle (V) | 229 | 14/229 = 0.061 W[0.037, 0.100] B[0.031, 0.101] | 10/229 = 0.044 W[0.024, 0.079] B[0.018, 0.077] | 15/142 = 0.106 W[0.065, 0.167] B[0.052, 0.168] | 11/54 = 0.204 W[0.118, 0.329] B[0.089, 0.340] |
| equipment (E) | 32 | 4/32 = 0.125 W[0.050, 0.281] B[0.028, 0.259] | 3/32 = 0.094 W[0.032, 0.242] B[0.000, 0.222] | 4/30 = 0.133 W[0.053, 0.297] B[0.030, 0.281] | 3/16 = 0.188 W[0.066, 0.430] B[0.000, 0.500] *unstable* |
| **pooled** | 261 | 18/261 = 0.069 W[0.044, 0.106] B[0.037, 0.110] | 13/261 = 0.050 W[0.029, 0.083] B[0.024, 0.085] | 19/172 = 0.110 W[0.072, 0.166] B[0.065, 0.168] | 14/70 = 0.200 W[0.123, 0.308] B[0.105, 0.317] |

Precision understates: a correct sub-supplier named only in the chronology counts as a non-match.

## C(c): silver supplier labels, exact match
| group | filings | recall: S1 + S2 | recall: S2 only (narrative) | precision: S1 (from the block) | precision: S2 (narrative) |
|---|---|---|---|---|---|
| Test-A | 143 | 140/143 = 0.979 W[0.940, 0.993] B[0.953, 1.000] | 46/143 = 0.322 W[0.251, 0.402] B[0.227, 0.435] | 139/143 = 0.972 W[0.930, 0.989] B[0.941, 0.994] | 46/60 = 0.767 W[0.646, 0.856] B[0.644, 0.877] |
| Test-B | 63 | 60/63 = 0.952 W[0.869, 0.984] B[0.895, 1.000] | 20/63 = 0.317 W[0.216, 0.440] B[0.191, 0.500] | 60/63 = 0.952 W[0.869, 0.984] B[0.895, 1.000] | 20/26 = 0.769 W[0.579, 0.890] B[0.583, 0.926] |
| unseen-filer | 55 | 55/55 = 1.000 W[0.935, 1.000] B[1.000, 1.000] | 26/55 = 0.473 W[0.347, 0.602] B[0.328, 0.644] | 55/55 = 1.000 W[0.935, 1.000] B[1.000, 1.000] | 26/27 = 0.963 W[0.817, 0.993] B[0.880, 1.000] |
| portal layout | 119 | 113/119 = 0.950 W[0.894, 0.977] B[0.909, 0.984] | 40/119 = 0.336 W[0.258, 0.425] B[0.222, 0.485] | 112/119 = 0.941 W[0.884, 0.971] B[0.896, 0.980] | 40/53 = 0.755 W[0.624, 0.851] B[0.583, 0.902] |
| older layout | 142 | 142/142 = 1.000 W[0.974, 1.000] B[1.000, 1.000] | 52/142 = 0.366 W[0.291, 0.448] B[0.270, 0.475] | 142/142 = 1.000 W[0.974, 1.000] B[1.000, 1.000] | 52/60 = 0.867 W[0.758, 0.931] B[0.788, 0.946] |
| vehicle (V) | 229 | 223/229 = 0.974 W[0.944, 0.988] B[0.952, 0.991] | 77/229 = 0.336 W[0.278, 0.400] B[0.252, 0.441] | 222/229 = 0.969 W[0.938, 0.985] B[0.946, 0.988] | 77/95 = 0.811 W[0.720, 0.877] B[0.711, 0.903] |
| equipment (E) | 32 | 32/32 = 1.000 W[0.893, 1.000] B[1.000, 1.000] | 15/32 = 0.469 W[0.309, 0.636] B[0.281, 0.690] | 32/32 = 1.000 W[0.893, 1.000] B[1.000, 1.000] | 15/18 = 0.833 W[0.608, 0.942] B[0.667, 1.000] *unstable* |
| **pooled** | 261 | 255/261 = 0.977 W[0.951, 0.989] B[0.958, 0.993] | 92/261 = 0.352 W[0.297, 0.412] B[0.268, 0.463] | 254/261 = 0.973 W[0.946, 0.987] B[0.953, 0.991] | 92/113 = 0.814 W[0.733, 0.875] B[0.723, 0.897] |

**Circularity of S1.** S1 is Pass A's reading of the block, so its precision is circular. Its non-matches are filings where Pass A's block name differs from this parser's, such as a joined multi-supplier name or a truncated name. **The informative silver figure is S2**: claims that the narrative names the declared supplier.

## D: in-block vs out-of-block evidence (exact match)
Each claim's quote is located in the parsed text: in-block, out-of-block, or not located (the quote is not verbatim).
- **Recall by location:** a filing counts if a matching claim with that kind of evidence exists.
- **Precision by location:** claims are partitioned by where their evidence lies.

| group | set | claims: in-block / out-of-block / not located | recall: in-block evidence | recall: out-of-block evidence | precision: in-block | precision: out-of-block | precision: not located |
|---|---|---|---|---|---|---|---|
| Test-A | agent, all | 0 / 85 / 16 | 0/143 = 0.000 | 6/143 = 0.042 | 0/0 | 6/85 = 0.071 | 3/16 = 0.188 *unstable* |
| Test-A | agent, accepted | 0 / 32 / 0 | 0/143 = 0.000 | 5/143 = 0.035 | 0/0 | 5/32 = 0.156 | 0/0 |
| Test-A | silver S1 | 138 / 5 / 0 | 134/143 = 0.937 | 5/143 = 0.035 | 134/138 = 0.971 | 5/5 = 1.000 *unstable* | 0/0 |
| Test-A | silver S2 | 0 / 60 / 0 | 0/143 = 0.000 | 46/143 = 0.322 | 0/0 | 46/60 = 0.767 | 0/0 |
| Test-B | agent, all | 0 / 33 / 1 | 0/63 = 0.000 | 4/63 = 0.063 | 0/0 | 4/33 = 0.121 | 0/1 = 0.000 *unstable* |
| Test-B | agent, accepted | 0 / 17 / 0 | 0/63 = 0.000 | 3/63 = 0.048 | 0/0 | 3/17 = 0.176 *unstable* | 0/0 |
| Test-B | silver S1 | 59 / 4 / 0 | 56/63 = 0.889 | 4/63 = 0.063 | 56/59 = 0.949 | 4/4 = 1.000 *unstable* | 0/0 |
| Test-B | silver S2 | 0 / 26 / 0 | 0/63 = 0.000 | 20/63 = 0.317 | 0/0 | 20/26 = 0.769 | 0/0 |
| unseen-filer | agent, all | 0 / 36 / 1 | 0/55 = 0.000 | 5/55 = 0.091 | 0/0 | 6/36 = 0.167 | 0/1 = 0.000 *unstable* |
| unseen-filer | agent, accepted | 0 / 21 / 0 | 0/55 = 0.000 | 5/55 = 0.091 | 0/0 | 6/21 = 0.286 | 0/0 |
| unseen-filer | silver S1 | 50 / 5 / 0 | 50/55 = 0.909 | 5/55 = 0.091 | 50/50 = 1.000 | 5/5 = 1.000 *unstable* | 0/0 |
| unseen-filer | silver S2 | 0 / 27 / 0 | 0/55 = 0.000 | 26/55 = 0.473 | 0/0 | 26/27 = 0.963 | 0/0 |
| **pooled** | agent, all | 0 / 154 / 18 | 0/261 = 0.000 | 15/261 = 0.057 | 0/0 | 16/154 = 0.104 | 3/18 = 0.167 *unstable* |
| **pooled** | agent, accepted | 0 / 70 / 0 | 0/261 = 0.000 | 13/261 = 0.050 | 0/0 | 14/70 = 0.200 | 0/0 |
| **pooled** | silver S1 | 247 / 14 / 0 | 240/261 = 0.920 | 14/261 = 0.054 | 240/247 = 0.972 | 14/14 = 1.000 *unstable* | 0/0 |
| **pooled** | silver S2 | 0 / 113 / 0 | 0/261 = 0.000 | 92/261 = 0.352 | 0/0 | 92/113 = 0.814 | 0/0 |

- **Agent:** has no in-block evidence, as expected; its input contains no block.
- **Silver S1:** 14 S1 quotes are located out of block. **POST HOC diagnostic:** in all 14 the quote's text ("Name : X") also matches the page header's "Manufacturer Name : X", which comes first; and all 14 also occur inside the block. Their out-of-block status is an artefact of the first-match rule, not narrative evidence. Only the **S2** out-of-block matches are informative silver evidence.

## C(d): agent vs silver, per population filing (exact match)
| group | comparison | agent ✓ / silver ✓ | agent ✓ / silver ✗ | agent ✗ / silver ✓ | agent ✗ / silver ✗ |
|---|---|---|---|---|---|
| Test-A | agent all vs silver S1 S2 | 9 | 0 | 131 | 3 |
| Test-A | agent all vs silver S2 | 9 | 0 | 37 | 97 |
| Test-A | agent accepted vs silver S1 S2 | 5 | 0 | 135 | 3 |
| Test-A | agent accepted vs silver S2 | 5 | 0 | 41 | 97 |
| Test-B | agent all vs silver S1 S2 | 4 | 0 | 56 | 3 |
| Test-B | agent all vs silver S2 | 4 | 0 | 16 | 43 |
| Test-B | agent accepted vs silver S1 S2 | 3 | 0 | 57 | 3 |
| Test-B | agent accepted vs silver S2 | 3 | 0 | 17 | 43 |
| unseen-filer | agent all vs silver S1 S2 | 5 | 0 | 50 | 0 |
| unseen-filer | agent all vs silver S2 | 5 | 0 | 21 | 29 |
| unseen-filer | agent accepted vs silver S1 S2 | 5 | 0 | 50 | 0 |
| unseen-filer | agent accepted vs silver S2 | 5 | 0 | 21 | 29 |
| **pooled** | agent all vs silver S1 S2 | 18 | 0 | 237 | 6 |
| **pooled** | agent all vs silver S2 | 18 | 0 | 74 | 169 |
| **pooled** | agent accepted vs silver S1 S2 | 13 | 0 | 242 | 6 |
| **pooled** | agent accepted vs silver S2 | 13 | 0 | 79 | 169 |

**Reading.** The off-diagonal cells are the disagreements.
- **Agent ✓ / silver ✗ never occurs:** every filing the agent recovers is also covered by silver.
- **Agent ✗ / silver S2 ✓ is large.** Part of it is the evaluation masking: wherever the narrative spells the supplier exactly as the frozen block name, the agent's input showed `[MASKED]` instead, while the silver S2 labeller saw the name. How much of the cell this explains was not quantified, so the cell is not read as agent failure.

## Pre-declared sensitivity analyses
| level / population | group | filings | agent recall (all) | agent precision (all) | agent recall (accepted) | agent precision (accepted) | silver recall (S1 + S2) | silver S2 recall | silver S2 precision |
|---|---|---|---|---|---|---|---|---|---|
| token containment | Test-A | 143 | 15/143 = 0.105 | 15/101 = 0.149 | 10/143 = 0.070 | 10/32 = 0.312 | 133/143 = 0.930 | 44/143 = 0.308 | 44/60 = 0.733 |
| token containment | Test-B | 63 | 7/63 = 0.111 | 7/34 = 0.206 | 6/63 = 0.095 | 6/17 = 0.353 *unstable* | 60/63 = 0.952 | 21/63 = 0.333 | 21/26 = 0.808 |
| token containment | unseen-filer | 55 | 12/55 = 0.218 | 13/37 = 0.351 | 10/55 = 0.182 | 11/21 = 0.524 | 52/55 = 0.945 | 26/55 = 0.473 | 26/27 = 0.963 |
| token containment | **pooled** | 261 | 34/261 = 0.130 | 35/172 = 0.203 | 26/261 = 0.100 | 27/70 = 0.386 | 245/261 = 0.939 | 91/261 = 0.349 | 91/113 = 0.805 |
| fuzzy token_set_ratio ≥ 90 | Test-A | 143 | 18/143 = 0.126 | 18/101 = 0.178 | 10/143 = 0.070 | 10/32 = 0.312 | 143/143 = 1.000 | 52/143 = 0.364 | 52/60 = 0.867 |
| fuzzy token_set_ratio ≥ 90 | Test-B | 63 | 10/63 = 0.159 | 10/34 = 0.294 | 8/63 = 0.127 | 8/17 = 0.471 *unstable* | 63/63 = 1.000 | 22/63 = 0.349 | 22/26 = 0.846 |
| fuzzy token_set_ratio ≥ 90 | unseen-filer | 55 | 12/55 = 0.218 | 13/37 = 0.351 | 10/55 = 0.182 | 11/21 = 0.524 | 55/55 = 1.000 | 27/55 = 0.491 | 27/27 = 1.000 |
| fuzzy token_set_ratio ≥ 90 | **pooled** | 261 | 40/261 = 0.153 | 41/172 = 0.238 | 28/261 = 0.107 | 29/70 = 0.414 | 261/261 = 1.000 | 101/261 = 0.387 | 101/113 = 0.894 |
| exact, literal OEM rule (Supplier Type OEM = OEM_SELF) | Test-A | 128 | 7/128 = 0.055 | 7/89 = 0.079 | 5/128 = 0.039 | 5/31 = 0.161 | 125/128 = 0.977 | 42/128 = 0.328 | 42/53 = 0.792 |
| exact, literal OEM rule (Supplier Type OEM = OEM_SELF) | Test-B | 42 | 2/42 = 0.048 | 2/15 = 0.133 *unstable* | 2/42 = 0.048 | 2/5 = 0.400 *unstable* | 39/42 = 0.929 | 10/42 = 0.238 | 10/11 = 0.909 *unstable* |
| exact, literal OEM rule (Supplier Type OEM = OEM_SELF) | unseen-filer | 47 | 4/47 = 0.085 | 4/29 = 0.138 | 4/47 = 0.085 | 4/15 = 0.267 *unstable* | 47/47 = 1.000 | 22/47 = 0.468 | 22/22 = 1.000 |
| exact, literal OEM rule (Supplier Type OEM = OEM_SELF) | **pooled** | 217 | 13/217 = 0.060 | 13/133 = 0.098 | 11/217 = 0.051 | 11/51 = 0.216 | 211/217 = 0.972 | 74/217 = 0.341 | 74/86 = 0.860 |

The pooled rows of the containment and fuzzy levels, with CIs:

- **containment:** agent recall (all) 34/261 = 0.130 W[0.095, 0.177] B[0.087, 0.190]; agent precision (all) 35/172 = 0.203 W[0.150, 0.270] B[0.139, 0.276]; agent precision (accepted) 27/70 = 0.386 W[0.280, 0.503] B[0.265, 0.516]; silver S2 precision 91/113 = 0.805 W[0.723, 0.868] B[0.683, 0.917].
- **fuzzy_tsr90:** agent recall (all) 40/261 = 0.153 W[0.115, 0.202] B[0.103, 0.218]; agent precision (all) 41/172 = 0.238 W[0.181, 0.307] B[0.172, 0.319]; agent precision (accepted) 29/70 = 0.414 W[0.306, 0.531] B[0.298, 0.547]; silver S2 precision 101/113 = 0.894 W[0.824, 0.938] B[0.823, 0.955].

## Claims in the other strata (counts only, not errors)
| stratum | filings | agent claims (all) | agent claims (accepted) | silver S1 + S2 claims |
|---|---|---|---|---|
| NAMED_SUPPLIER | 255 | 169 | 68 | 367 |
| OEM_SELF | 47 | 24 | 7 | 89 |
| OBTAINED_FROM | 4 | 3 | 2 | 6 |
| MULTIPLE | 6 | 3 | 2 | 7 |
| BLANK | 85 | 27 | 13 | 1 |

## Components (protocol E)
**Not run: there are no component claims to check.** The frozen agent schema (`tt/agent/schemas.py`) has no component field, and the silver labels have no component claims.

The reference exists and is reported for completeness:
- **Involved Components:** a name or part number in 390 of 397 filings, with component names in 389 and part numbers in 355.
- **Flat file:** MFR_COMP_NAME in 392 of 397, MFR_COMP_DESC in 380, MFR_COMP_PTNO in 374.

The matching rule and the fuzzy threshold (token_set_ratio ≥ 90) are fixed in the protocol for any later component extractor.

## POST HOC diagnostics (added after seeing results; no protocol change)
- **Short forms of the filer's own name.** In 24 of 261 population filings, the declared name is a short form of the filer's own name ("X" for "X Industries, Inc.": token containment with a filer name). The pre-declared exact OEM_SELF rule leaves them in NAMED_SUPPLIER.
  - Agent matches inside them: 1 of 19 matching claims, and 1 of 18 recalled filings.
  - So the agent's matches are not mainly the filer naming itself.
- **Silver S1 outside the block:** 14 S1 quotes are located out of block by the first-match rule; all 14 also occur inside the block (section D).

## Amendments
**SC-A1 (2026-10-29)** (`reports/SC_AMENDMENTS.md`). The 26 Pass-C-decided silver S2 claims store their name in `name`, not in `label`. The script stopped on them before any comparison, and the name is now read from `name`. **23 of these 26 claims fall in the population;** the silver S2 results that include them are labelled POST HOC per the protocol rule.

## Limitations
- **Declared ≠ actual maker.** The reference is what the filer declared: an assembler, a distributor or the filer itself. A match is fidelity to that declaration, not identification of the true manufacturer. A non-match is not a filer error.
- **Masking and circularity.**
  - The agent saw neither the block nor the masked block name, so its recall is bounded by narrative mentions that the mask missed. Agent vs silver comparisons mostly reflect this.
  - Silver S1 is read from the block (circular). Only out-of-block S2 evidence is independent of the reference.
- **Small accepted n.** Gate-accepted agent claims in the population number 70 pooled, and 17–32 per split, so the intervals are wide; cells with n < 20 are marked unstable.
- **Parse failures.** None in the 397 filings, but the parser was written on these filings' layouts, and two pointer names ("See … .pdf") are counted as BLANK.
- **Normalisation.** No alias list was used. Short forms and parent-subsidiary names ("Bosch" vs "Robert Bosch LLC") match only at the containment level. 24 population filings declare a short form of the filer's own name (POST HOC).
- **Quote location.** It takes the first occurrence of the quote; for 14 silver S1 quotes that is the page header (section D). Agent quotes that are not verbatim cannot be located.
- **Flat-file vintage.** The flat file is from 2026-10-18 (RCL.txt layout last updated May 2025). It was used here for MFGNAME (the OEM_SELF test) and for component availability only.
- **Prior-art context.** The owner reports that the DOT OIG (2018) found the component-manufacturer information missing in 16.2% (±8.5%) of 2012–2016 initial reports. That figure is owner-supplied and was not verified here (protocol G). In these 397 filings, the block names no supplier in 85 (BLANK).
