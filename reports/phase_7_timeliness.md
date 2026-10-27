# Phase 7 (TS-1): 5-working-day timeliness screen of Part 573 filings

**Silver reference (AI-generated, not human-verified).** This is a **descriptive screening signal, not a legal finding** about any filing or filer. It was computed under the protocol fixed before any gap was computed (`reports/TS_PROTOCOL.md`, tag `ts-protocol-1`), with one implementation amendment (TS-A1, below), which affects no anchor. No model was run and nothing under `freeze-v1` or `amendment-1` changed. Aggregates only; manufacturers are anonymised. Tests: `25 passed in 0.05s` (`tests/test_ts_screen.py`, run by the script before anything is written). Raw aggregates: `reports/ts/phase_7_timeliness.json`.

## Summary
**1. Population and primary result.**
- **Population:** 305 defect filings (out of 397; 92 noncompliance filings are reported separately).
- **Primary screen:** the silver reference gives a decision date for 217 of 305. FLAGGED 104/305 = 0.341 W[0.290, 0.396] B[0.268, 0.418], NOT_FLAGGED 106, INDETERMINATE 7, NO_DECISION_DATE 88. W = Wilson 95%, B = filer-cluster bootstrap 95%.

**2. The primary FLAGGED share is mostly a filing-date artefact. Read it with the pre-declared version and RCDATE results.**
- **Most processed PDFs are amended versions.** For 169 of 305 defect filings the processed PDF is a later, amended version.
- **Their Submission Date is not the initial filing date.** It equals RCDATE (NHTSA's received date for the Part 573 report) in only 15 of 169. RCDATE is earlier by a median of 35 calendar days, so that Submission Date is most likely the amendment's date.
- **FLAGGED by version:**
  - amended versions: 98 of 169;
  - original (only-version) filings, where Submission Date and RCDATE agree in 131 of 136: 6 of 136 (6/136 = 0.044 W[0.020, 0.093] B[0.013, 0.086]).
- **With RCDATE as the filing date** (a pre-declared sensitivity), the pooled reference has 19 FLAGGED of 305.
- **Not promoted.** Neither variant is promoted to the primary result (that would be post hoc). They are pre-declared and shown so the primary share is not misread.

**3. Coverage and agreement.**
- **Decision dates:** 88 of 305 defect filings (0.289) have no usable DECISION date in the silver reference.
- **Agent coverage:** the agent has an accepted, dated DECISION claim for 127 of 305.
- **Agreement where both have a date:** the agent and the reference agree closely (Cohen's κ 0.937). Both mostly read the same sentence.

## (a) Reference (silver), defect filings
Gaps are counted in working days (Mon–Fri, excluding observed federal holidays), from strictly after the decision date up to and including the filing date (the Submission Date). gap_min uses the latest possible decision day, gap_max the earliest, and gap_mid is their mean. Quantiles use linear interpolation and cover filings with a decision date only.

| split | N | with decision date | gap_mid median [IQR] p90 | gap_min median [IQR] p90 | gap_max median [IQR] p90 | AMBIGUOUS anchors | anchor precision |
|---|---|---|---|---|---|---|---|
| Test-A | 152 | 117 | 6 [4–33] 81.6 | 5 [4–31] 81.6 | 6 [4–34] 87.6 | 3 | day 115, month 2 |
| Test-B | 73 | 58 | 5 [5–12] 25 | 5 [5–11] 21.5 | 5 [5–12.8] 27.4 | 1 | day 55, month 3 |
| unseen-filer | 80 | 42 | 15 [5.2–53.8] 127.0 | 12.5 [5–53.8] 87.9 | 15 [5.2–61] 156.7 | 2 | day 41, year_part 1 |
| pooled | 305 | 217 | 6 [5–29] 65.8 | 5 [4–28] 65.8 | 6 [5–30] 77.2 | 6 | day 211, month 5, year_part 1 |

| split | FLAGGED | NOT_FLAGGED | INDETERMINATE | NO_DECISION_DATE |
|---|---|---|---|---|
| Test-A | 55/152 = 0.362 W[0.290, 0.441] B[0.267, 0.469] | 58/152 = 0.382 W[0.308, 0.461] B[0.268, 0.487] | 4/152 = 0.026 W[0.010, 0.066] B[0.006, 0.056] | 35/152 = 0.230 W[0.170, 0.303] B[0.155, 0.321] |
| Test-B | 19/73 = 0.260 W[0.173, 0.371] B[0.148, 0.379] | 37/73 = 0.507 W[0.395, 0.618] B[0.328, 0.660] | 2/73 = 0.027 W[0.008, 0.095] B[0.000, 0.077] | 15/73 = 0.205 W[0.129, 0.312] B[0.117, 0.333] |
| unseen-filer | 30/80 = 0.375 W[0.277, 0.485] B[0.260, 0.500] | 11/80 = 0.138 W[0.079, 0.230] B[0.058, 0.222] | 1/80 = 0.013 W[0.002, 0.067] B[0.000, 0.041] | 38/80 = 0.475 W[0.369, 0.583] B[0.333, 0.613] |
| pooled | 104/305 = 0.341 W[0.290, 0.396] B[0.268, 0.418] | 106/305 = 0.348 W[0.296, 0.403] B[0.254, 0.434] | 7/305 = 0.023 W[0.011, 0.047] B[0.007, 0.042] | 88/305 = 0.289 W[0.241, 0.342] B[0.220, 0.367] |

Share = k/N. W = Wilson 95%; B = filer-cluster bootstrap 95% (2,000 resamples, seed 0).

**Noncompliance filings (descriptive only; § 573.6(c)(6) asks for a chronology for defects only):**

| split | N | with decision date | FLAGGED | NOT_FLAGGED | INDETERMINATE | NO_DECISION_DATE |
|---|---|---|---|---|---|---|
| Test-A | 47 | 38 | 13 (0.277) | 23 (0.489) | 2 (0.043) | 9 (0.191) |
| Test-B | 27 | 26 | 11 (0.407) | 14 (0.519) | 1 (0.037) | 1 (0.037) |
| unseen-filer | 18 | 9 | 8 (0.444) | 1 (0.056) | 0 (0.000) | 9 (0.500) |
| pooled | 92 | 73 | 32 (0.348) | 38 (0.413) | 3 (0.033) | 19 (0.207) |

## (b) Agent (run-1 claims accepted by the frozen gate), defect filings
**Unknown** = no accepted DECISION claim (abstention), no qualifying date, or INDETERMINATE.
- **Manski lower bound:** every unknown counted as not flagged.
- **Manski upper bound:** every unknown counted as flagged.

| split | N | coverage (agent decision date) | abstained (no accepted DECISION claim) | NO_DECISION_DATE total | FLAGGED / NOT / INDET | complete-case FLAGGED share | Manski lower [B] | Manski upper [B] | reference FLAGGED share |
|---|---|---|---|---|---|---|---|---|---|
| Test-A | 152 | 72/152 = 0.474 W[0.396, 0.553] B[0.346, 0.596] | 79 | 80 | 33 / 38 / 1 | 33/72 = 0.458 W[0.348, 0.573] B[0.296, 0.640] | 0.217 [0.133, 0.321] | 0.750 [0.628, 0.858] | 0.362 |
| Test-B | 73 | 28/73 = 0.384 W[0.281, 0.498] B[0.263, 0.514] | 45 | 45 | 11 / 15 / 2 | 11/28 = 0.393 W[0.236, 0.576] B[0.192, 0.576] | 0.151 [0.062, 0.250] | 0.795 [0.685, 0.885] | 0.260 |
| unseen-filer | 80 | 27/80 = 0.338 W[0.243, 0.446] B[0.235, 0.450] | 53 | 53 | 20 / 7 / 0 | 20/27 = 0.741 W[0.553, 0.868] B[0.567, 0.917] | 0.250 [0.160, 0.355] | 0.912 [0.849, 0.974] | 0.375 |
| pooled | 305 | 127/305 = 0.416 W[0.362, 0.472] B[0.328, 0.502] | 177 | 178 | 64 / 60 / 3 | 64/127 = 0.504 W[0.418, 0.589] B[0.394, 0.621] | 0.210 [0.154, 0.272] | 0.803 [0.728, 0.868] | 0.341 |

**Bounds without INDETERMINATE as unknown** (INDETERMINATE counted as not flagged; the lower bound is unchanged): upper bound Test-A 0.743; Test-B 0.767; unseen-filer 0.912; pooled 0.793.

## (c) Agreement where both the reference and the agent have a decision date
| split | n both | identical interval [B] | same day, both day precision [B] | abs. diff of gap_mid (working days): median / p90 / max; share 0; share ≤ 5 | precision of agent FLAGGED [B] | recall [B] | Cohen's κ [B] | PABAK [B] | reference FLAGGED among n |
|---|---|---|---|---|---|---|---|---|---|
| Test-A | 71 | 0.972 [0.925, 1.000] | 0.958 [0.899, 1.000] | 0 / 0 / 6.5; 0.972; 0.986 | 0.969 [0.893, 1.000] | 1.000 [1.000, 1.000] | 0.973 [0.906, 1.000] | 0.979 [0.927, 1.000] | 31 |
| Test-B | 27 | 0.889 [0.731, 1.000] | 0.889 [0.731, 1.000] | 0 / 0.8 / 6; 0.889; 0.963 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.856 [0.614, 1.000] | 0.889 [0.700, 1.000] | 10 |
| unseen-filer | 24 | 0.875 [0.700, 1.000] | 0.792 [0.583, 0.958] | 0 / 1.4 / 10; 0.875; 0.958 | 0.944 [0.824, 1.000] | 1.000 [1.000, 1.000] | 0.895 [0.588, 1.000] | 0.938 [0.795, 1.000] | 17 |
| pooled | 122 | 0.934 [0.876, 0.979] | 0.910 [0.843, 0.961] | 0 / 0 / 10; 0.934; 0.975 | 0.967 [0.913, 1.000] | 1.000 [1.000, 1.000] | 0.937 [0.867, 0.986] | 0.951 [0.895, 0.989] | 58 |

3×3 flag tables (rows = reference, columns = agent; raw counts):

**Test-A**

| reference \ agent | FLAGGED | NOT_FLAGGED | INDETERMINATE |
|---|---|---|---|
| FLAGGED | 31 | 0 | 0 |
| NOT_FLAGGED | 0 | 38 | 0 |
| INDETERMINATE | 1 | 0 | 1 |

**Test-B**

| reference \ agent | FLAGGED | NOT_FLAGGED | INDETERMINATE |
|---|---|---|---|
| FLAGGED | 10 | 0 | 0 |
| NOT_FLAGGED | 0 | 15 | 2 |
| INDETERMINATE | 0 | 0 | 0 |

**unseen-filer**

| reference \ agent | FLAGGED | NOT_FLAGGED | INDETERMINATE |
|---|---|---|---|
| FLAGGED | 17 | 0 | 0 |
| NOT_FLAGGED | 1 | 6 | 0 |
| INDETERMINATE | 0 | 0 | 0 |

**pooled**

| reference \ agent | FLAGGED | NOT_FLAGGED | INDETERMINATE |
|---|---|---|---|
| FLAGGED | 58 | 0 | 0 |
| NOT_FLAGGED | 1 | 59 | 2 |
| INDETERMINATE | 1 | 0 | 1 |

High agreement here mostly means that the agent's accepted DECISION claim and the silver DECISION event quote the same chronology sentence. It says nothing about whether either date is the legally relevant one.

## (d) Pre-declared sensitivity runs (defect filings)
Status changes are measured against the primary over all N, in four categories (NO_DECISION_DATE included).

| variant | split | reference: changed / N (share) | reference FLAGGED / NOT / INDET / NO_DATE | agent: changed / N (share) | agent FLAGGED / NOT / INDET / NO_DATE |
|---|---|---|---|---|---|
| 1 calendar days | Test-A | 35/152 (0.230) | 90 / 25 / 2 / 35 | 19/152 (0.125) | 52 / 19 / 1 / 80 |
| 1 calendar days | Test-B | 32/73 (0.438) | 50 / 5 / 3 / 15 | 11/73 (0.151) | 22 / 4 / 2 / 45 |
| 1 calendar days | unseen-filer | 5/80 (0.062) | 35 / 6 / 1 / 38 | 4/80 (0.050) | 24 / 3 / 0 / 53 |
| 1 calendar days | pooled | 72/305 (0.236) | 175 / 36 / 6 / 88 | 34/305 (0.111) | 98 / 26 / 3 / 178 |
| 2 holidays not excluded | Test-A | 2/152 (0.013) | 57 / 56 / 4 / 35 | 2/152 (0.013) | 35 / 36 / 1 / 80 |
| 2 holidays not excluded | Test-B | 2/73 (0.027) | 21 / 35 / 2 / 15 | 0/73 (0.000) | 11 / 15 / 2 / 45 |
| 2 holidays not excluded | unseen-filer | 1/80 (0.013) | 31 / 10 / 1 / 38 | 0/80 (0.000) | 20 / 7 / 0 / 53 |
| 2 holidays not excluded | pooled | 5/305 (0.016) | 109 / 101 / 7 / 88 | 2/305 (0.007) | 66 / 58 / 3 / 178 |
| 3 earliest DECISION | Test-A | 4/152 (0.026) | 59 / 54 / 4 / 35 | 4/152 (0.026) | 37 / 34 / 1 / 80 |
| 3 earliest DECISION | Test-B | 4/73 (0.055) | 23 / 33 / 2 / 15 | 0/73 (0.000) | 11 / 15 / 2 / 45 |
| 3 earliest DECISION | unseen-filer | 0/80 (0.000) | 30 / 11 / 1 / 38 | 0/80 (0.000) | 20 / 7 / 0 / 53 |
| 3 earliest DECISION | pooled | 8/305 (0.026) | 112 / 98 / 7 / 88 | 4/305 (0.013) | 68 / 56 / 3 / 178 |
| 4 latest event of any type | Test-A | 27/152 (0.178) | 65 / 60 / 9 / 18 | 56/152 (0.368) | 64 / 45 / 9 / 34 |
| 4 latest event of any type | Test-B | 20/73 (0.274) | 30 / 33 / 9 / 1 | 35/73 (0.479) | 40 / 18 / 4 / 11 |
| 4 latest event of any type | unseen-filer | 29/80 (0.362) | 39 / 20 / 5 / 16 | 30/80 (0.375) | 38 / 14 / 1 / 27 |
| 4 latest event of any type | pooled | 76/305 (0.249) | 134 / 113 / 23 / 35 | 121/305 (0.397) | 142 / 77 / 14 / 72 |
| 5 lexicon event | Test-A | 57/152 (0.375) | 31 / 30 / 1 / 90 | 43/152 (0.283) | 21 / 17 / 1 / 113 |
| 5 lexicon event | Test-B | 34/73 (0.466) | 9 / 17 / 0 / 47 | 21/73 (0.288) | 3 / 4 / 0 / 66 |
| 5 lexicon event | unseen-filer | 21/80 (0.263) | 13 / 10 / 0 / 57 | 17/80 (0.212) | 8 / 8 / 0 / 64 |
| 5 lexicon event | pooled | 112/305 (0.367) | 53 / 57 / 1 / 194 | 81/305 (0.266) | 32 / 29 / 1 / 243 |
| 6 RCDATE as filing date | Test-A | 49/152 (0.322) | 9 / 104 / 4 / 35 | 29/152 (0.191) | 6 / 65 / 1 / 80 |
| 6 RCDATE as filing date | Test-B | 17/73 (0.233) | 3 / 51 / 4 / 15 | 9/73 (0.123) | 3 / 22 / 2 / 46 |
| 6 RCDATE as filing date | unseen-filer | 23/80 (0.287) | 7 / 33 / 2 / 38 | 14/80 (0.175) | 6 / 20 / 1 / 53 |
| 6 RCDATE as filing date | pooled | 89/305 (0.292) | 19 / 188 / 10 / 88 | 52/305 (0.170) | 15 / 107 / 4 / 179 |

Subsets (status changes do not apply; primary rule within the subset):

| subset | split | N | reference FLAGGED / NOT / INDET / NO_DATE | reference FLAGGED share | agent FLAGGED / NOT / INDET / NO_DATE |
|---|---|---|---|---|---|
| 7a original (only-version) filings | Test-A | 72 | 2 / 51 / 3 / 16 | 2/72 = 0.028 W[0.008, 0.096] B[0.000, 0.074] | 0 / 32 / 1 / 39 |
| 7a original (only-version) filings | Test-B | 38 | 2 / 27 / 2 / 7 | 2/38 = 0.053 W[0.015, 0.173] B[0.000, 0.139] | 1 / 10 / 2 / 25 |
| 7a original (only-version) filings | unseen-filer | 26 | 2 / 10 / 0 / 14 | 2/26 = 0.077 W[0.021, 0.241] B[0.000, 0.200] | 1 / 5 / 0 / 20 |
| 7a original (only-version) filings | pooled | 136 | 6 / 88 / 5 / 37 | 6/136 = 0.044 W[0.020, 0.093] B[0.013, 0.086] | 2 / 47 / 3 / 84 |
| 7b amended-version filings | Test-A | 80 | 53 / 7 / 1 / 19 | 53/80 = 0.662 W[0.554, 0.757] B[0.549, 0.763] | 33 / 6 / 0 / 41 |
| 7b amended-version filings | Test-B | 35 | 17 / 10 / 0 / 8 | 17/35 = 0.486 W[0.330, 0.644] B[0.290, 0.676] | 10 / 5 / 0 / 20 |
| 7b amended-version filings | unseen-filer | 54 | 28 / 1 / 1 / 24 | 28/54 = 0.519 W[0.389, 0.646] B[0.373, 0.655] | 19 / 2 / 0 / 33 |
| 7b amended-version filings | pooled | 169 | 98 / 18 / 2 / 51 | 98/169 = 0.580 W[0.505, 0.652] B[0.490, 0.665] | 62 / 13 / 0 / 94 |
| 8 type from document text only (FMVSS-proxy-typed dropped) | Test-A | 104 | 32 / 42 / 3 / 27 | 32/104 = 0.308 W[0.227, 0.402] B[0.193, 0.432] | 22 / 31 / 1 / 50 |
| 8 type from document text only (FMVSS-proxy-typed dropped) | Test-B | 0 | 0 / 0 / 0 / 0 | n/a (N = 0) | 0 / 0 / 0 / 0 |
| 8 type from document text only (FMVSS-proxy-typed dropped) | unseen-filer | 62 | 22 / 7 / 1 / 32 | 22/62 = 0.355 W[0.247, 0.479] B[0.228, 0.482] | 15 / 4 / 0 / 43 |
| 8 type from document text only (FMVSS-proxy-typed dropped) | pooled | 166 | 54 / 49 / 4 / 59 | 54/166 = 0.325 W[0.259, 0.400] B[0.235, 0.426] | 37 / 35 / 1 / 93 |

Every pre-declared variant ran. Variant 7 cannot use the original version's own Submission Date, because those PDFs were not downloaded; it reports the two strata instead, as the protocol fixed. Variant 8 is empty for Test-B, where every filing is typed by the FMVSS proxy.

## (e) Consistency audit (no ground truth), defect filings
| split | set | order inconsistency (FILER_AWARENESS ≤ INVESTIGATION_START ≤ DECISION ≤ filing) | any dated event after the filing date | DECISION more than 10 years before filing |
|---|---|---|---|---|
| Test-A | silver | 20/152 (0.132) W[0.087, 0.195] | 2/152 (0.013) W[0.004, 0.047] | 0/152 (0.000) W[0.000, 0.025] |
| Test-A | agent accepted | 9/152 (0.059) W[0.031, 0.109] | 0/152 (0.000) W[0.000, 0.025] | 0/152 (0.000) W[0.000, 0.025] |
| Test-B | silver | 11/73 (0.151) W[0.086, 0.250] | 3/73 (0.041) W[0.014, 0.114] | 0/73 (0.000) W[0.000, 0.050] |
| Test-B | agent accepted | 4/73 (0.055) W[0.022, 0.133] | 0/73 (0.000) W[0.000, 0.050] | 0/73 (0.000) W[0.000, 0.050] |
| unseen-filer | silver | 7/80 (0.087) W[0.043, 0.170] | 0/80 (0.000) W[0.000, 0.046] | 0/80 (0.000) W[0.000, 0.046] |
| unseen-filer | agent accepted | 2/80 (0.025) W[0.007, 0.087] | 0/80 (0.000) W[0.000, 0.046] | 0/80 (0.000) W[0.000, 0.046] |
| pooled | silver | 38/305 (0.125) W[0.092, 0.166] | 5/305 (0.016) W[0.007, 0.038] | 0/305 (0.000) W[0.000, 0.012] |
| pooled | agent accepted | 15/305 (0.049) W[0.030, 0.080] | 0/305 (0.000) W[0.000, 0.012] | 0/305 (0.000) W[0.000, 0.012] |

An order inconsistency means an event of an earlier type in the chain lies entirely after an event of a later type, or a DECISION lies after the filing date. Investigations can legitimately continue after awareness or decision entries, so this is a consistency flag, not an error count.

## (f) Descriptive
**How informative the screen is:** the share of defect filings whose latest dated event (on or before the filing date) is DECISION-typed.

| split | silver: k / filings with a dated event (N) | agent accepted: k / filings with a dated event (N) |
|---|---|---|
| Test-A | 94/137 (152) | 58/121 (152) |
| Test-B | 49/72 (73) | 25/62 (73) |
| unseen-filer | 24/66 (80) | 14/56 (80) |
| pooled | 167/275 (305) | 97/239 (305) |

**Submission Date vs RCDATE** (RCDATE − Submission Date, calendar days; defect filings):

| split | stratum | n | equal | RCDATE earlier | RCDATE later | min | p10 | median | p90 | max |
|---|---|---|---|---|---|---|---|---|---|---|
| Test-A | all | 152 | 77 (0.507) | 74 | 1 | -443 | -104.7 | 0 | 0 | 1 |
| Test-A | original | 72 | 71 (0.986) | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| Test-A | amended | 80 | 6 (0.075) | 74 | 0 | -443 | -232 | -41.5 | -4 | 0 |
| Test-B | all | 73 | 43 (0.589) | 28 | 2 | -85 | -33.8 | 0 | 0 | 7 |
| Test-B | original | 38 | 37 (0.974) | 1 | 0 | -5 | 0 | 0 | 0 | 0 |
| Test-B | amended | 35 | 6 (0.171) | 27 | 2 | -85 | -56.6 | -14 | 0 | 7 |
| unseen-filer | all | 80 | 26 (0.325) | 52 | 2 | -508 | -150.1 | -15 | 0 | 3 |
| unseen-filer | original | 26 | 23 (0.885) | 1 | 2 | -1 | 0 | 0 | 0 | 3 |
| unseen-filer | amended | 54 | 3 (0.056) | 51 | 0 | -508 | -216.3 | -38.5 | -3.3 | 0 |
| pooled | all | 305 | 146 (0.479) | 154 | 5 | -508 | -101.2 | -1 | 0 | 7 |
| pooled | original | 136 | 131 (0.963) | 2 | 3 | -5 | 0 | 0 | 0 | 3 |
| pooled | amended | 169 | 15 (0.089) | 152 | 2 | -508 | -187.0 | -35 | -0.8 | 7 |

**Strata (reference, primary rule, pooled defect filings):**

| field | value | N | FLAGGED | NOT_FLAGGED | INDETERMINATE | NO_DECISION_DATE |
|---|---|---|---|---|---|---|
| INFLUENCED_BY | (empty) | 1 | 0 (0.000) W[0.000, 0.793] | 1 (1.000) W[0.207, 1.000] | 0 (0.000) W[0.000, 0.793] | 0 (0.000) W[0.000, 0.793] |
| INFLUENCED_BY | MFR | 265 | 92 (0.347) W[0.292, 0.406] | 100 (0.377) W[0.321, 0.437] | 6 (0.023) W[0.010, 0.049] | 67 (0.253) W[0.204, 0.308] |
| INFLUENCED_BY | ODI | 39 | 12 (0.308) W[0.186, 0.464] | 5 (0.128) W[0.056, 0.267] | 1 (0.026) W[0.005, 0.132] | 21 (0.538) W[0.386, 0.684] |
| RCLTYPECD | E | 46 | 17 (0.370) W[0.245, 0.514] | 9 (0.196) W[0.107, 0.332] | 1 (0.022) W[0.004, 0.113] | 19 (0.413) W[0.283, 0.557] |
| RCLTYPECD | V | 259 | 87 (0.336) W[0.281, 0.395] | 97 (0.375) W[0.318, 0.435] | 6 (0.023) W[0.011, 0.050] | 69 (0.266) W[0.216, 0.323] |

**Manufacturers with at least 10 pooled defect filings** (3 of 149 filers; anonymised; reference, primary rule):

| manufacturer | N | FLAGGED | NOT_FLAGGED | INDETERMINATE | NO_DECISION_DATE |
|---|---|---|---|---|---|
| M1 | 22 | 2 | 17 | 0 | 3 |
| M2 | 12 | 0 | 12 | 0 | 0 |
| M3 | 10 | 5 | 4 | 0 | 1 |

## Amendments
**TS-A1 (2026-10-28)** (`reports/TS_AMENDMENTS.md`):
- **What it is:** the amendment-1 crash-only guard on the frozen date parser inside `chronology_years`, which crashed on an invalid calendar date.
- **Scope:** 2 filings (testA 1, unseen 1).
- **Effect:** it changes only the year context of those filings. **Anchors using a year from context in them: 0**, so no anchor, gap or flag depends on the amendment. The POST HOC label therefore covers nothing in the tables above.

## Limitations
- **Silver labels.** Every decision date is an AI-made silver label or an AI agent's claim; no human checked any of them. Pass C sided with Pass B in 72–78% of items, and both are the same model family.
- **Self-reported dates.** The screen measures the interval between the decision date the filer wrote in its chronology and the filing date. The legally relevant trigger can be when a defect *should have* been determined, which may be earlier than any chronology date. So the gap is at best a lower bound on the legally relevant interval, and it depends on how each filer words its chronology.
- **Filing-date artefact.** The processed PDF is the latest version. For amended versions, the Submission Date is generally later than RCDATE (section f), so the primary gap is longer than the initial-report gap for most of those filings. The original version's own date was not available (not downloaded).
- **Working-days assumption.** Part 573 does not define "working days". We assume Mon–Fri excluding observed federal holidays. The holiday table follows 5 U.S.C. 6103 and **omits one-off executive-order closures** and Inauguration Day. The holidays-not-excluded variant changes few statuses; the calendar-days variant changes many.
- **DECISION vs OTHER typing.** The DECISION/OTHER boundary is one of the most frequent type confusions, both between the labellers and between the agent and the labels (`reports/phase_6_failure_analysis.md` section e).
  - Some DECISION-typed events are a supplier's own decision, or a sentence that only inherits an entry-header date.
  - The lexicon and any-event variants show how much the anchor choice matters.
- **Defect vs noncompliance typing.** The 2025+ form has no type field, so 186 of 397 filings are typed by a flat-file FMVSS proxy. On the pre-2025 form, the proxy's DEFECT calls are 153/154 correct, but it misses 13 of 166 defects.
- **Small n.** Per-split counts are small, the cluster bootstrap intervals are wide, and only 3 manufacturers reach 10 defect filings.
- **Scope.** These are three samples drawn for the extraction study (2023 to mid-2026), not a census.

## Prior art
- **Closest regulatory analogue:** NHTSA's case-by-case timeliness and audit queries. One example is TQ14-001, whose consent order (May 2014) is on nhtsa.gov; another is AQ23-002, whose information requests are on static.nhtsa.gov. We found no aggregate across manufacturers published by NHTSA.
- **Closest method analogue:** Zhyrko, Han & Verberne (2026), "Time as Structure: Temporal Dependency Graphs for Verifiable Deadline Computation over Legal Documents", arXiv 2608.15270 (a preprint). Its design extracts dated facts with a model, then computes with a calendar engine.
- **Closest data analogue:** Astvansh, Ball & Josefy (2022), *MSOM* 24(3):1457–1473. It hand-codes recall timing (awareness to recall) for 2,120 recalls by 27 automakers, 2009–2018.
- **Search scope:** four general web searches on 2026-10-28, read at snippet or summary level only. No bibliographic database was searched systematically, and no paper was read in full.
- **The only claim made:** within this scope, we found no prior work that computes this gap across multi-manufacturer Part 573 filings. The method is not claimed to be new.
