"""Claims list for reports/TIERTRACE_REPORT.md and README.md. Every number in the write-up is listed here with its source file, the commit it is
read from, and the exact text it must match in that file at that commit (`git show <commit>:<file>`). No new analysis; nothing is computed except
the run durations, which are differences of timestamps that are themselves checked.
  python scripts/writeup_claims.py           -> checks every claim, prints mismatches, exit 1 if any
  python scripts/writeup_claims.py --md      -> also prints the markdown claims table"""
import subprocess
import sys

P, H4, X1, X2, SEC, FA, H6, H6C, LAB, AM, PF, TH, DEV, PRE = (
    ("reports/phase_6_testA_primary.md", "37f93c9"), ("reports/phase_6_H4.md", "b9611e0"), ("reports/phase_6_testA_exploratory.md", "6c34d05"),
    ("reports/phase_6_exploratory_2.md", "805a34c"), ("reports/phase_6_secondary_splits.md", "ef19956"), ("reports/phase_6_failure_analysis.md", "3c8b7cb"),
    ("reports/phase_6_H6.md", "08d7916"), ("reports/H6_measurement_choice.md", "75e4841"), ("reports/phase_6_labels.md", "f77af17"),
    ("docs/AMENDMENT_1.md", "8525779"), ("reports/PREREGISTRATION_PROPOSED_FINAL.md", "9d8a6de"), ("config/thresholds.json", "969a65c"),
    ("reports/DEVIATIONS.md", "75e4841"), ("PREREGISTRATION.md", "b2c5ed5"))
ERR = ("reports/phase_6_secondary_splits.md", "b67c054")
FAB = ("reports/phase_6_failure_analysis.md", "b67c054")
H6L = ("reports/H6_hw_report.md", "08d7916")
TS = ("reports/phase_7_timeliness.md", "2157cf1")
TSP = ("reports/TS_PROTOCOL.md", "246e30e")
SC = ("reports/phase_8_supplier_check.md", "f35dfb6")
SCP = ("reports/SC_PROTOCOL.md", "24f7c34")
SCI = ("reports/SC_INVENTORY.md", "c27b962")

# (id, claim as used in the write-up, source, exact text in the source)
CLAIMS = [
    # data and labels
    ("D1", "dev: 400 campaigns, 100 silver-labelled", PF, "400 campaigns (100 silver-labelled)"),
    ("D2", "Test-A: 1,000 campaigns drawn, 200 labelled", PF, "| 200 | `data/splits/proposed/testA_labelled_ids.txt`"),
    ("D2b", "Test-A: 1,000 campaigns, 2023 to Feb 2026", PF, "| Test-A | 2023 to Feb 2026, allocated by year, seed 0 (already drawn) | 1,000 campaigns |"),
    ("D3", "Test-B: 100 of a pool of 560", PF, "100 of a pool of 560"),
    ("D4", "unseen-filer: 100 of a pool of 247", PF, "100 of a pool of 247"),
    ("D5", "dev Pass A vs Pass B event agreement 68.7%", PF, "events 68.7%"),
    ("D6", "Test-A labels: 199 records, 1,466 events, 21 contested", LAB, "199 records, 1,466 events, 21 contested"),
    ("D7", "Test-B labels: 100 records, 806 events, 16 contested", LAB, "100 records, 806 events, 16 contested"),
    ("D8", "unseen labels: 98 records, 580 events, 12 contested", LAB, "98 records, 580 events, 12 contested"),
    ("D9", "Pass C sided with Pass B: Test-A 73.5%", LAB, "with Pass B in 296 (73.5%)"),
    ("D10", "Pass C sided with Pass B: Test-B 72.2%", LAB, "with Pass B in 148 (72.2%)"),
    ("D11", "Pass C sided with Pass B: unseen 77.6%", LAB, "with Pass B in 128 (77.6%)"),
    ("D12", "Pass C sided with Pass A: Test-A 9.2%", LAB, "with Pass A in 37 items (9.2%)"),
    ("D12b", "Pass C sided with Pass A: Test-B 10.2%", LAB, "with Pass A in 21 items (10.2%)"),
    ("D12c", "Pass C sided with Pass A: unseen 8.5%", LAB, "with Pass A in 14 items (8.5%)"),
    ("D13", "unreadable filings excluded: 23V313 (Test-A), 23V320 and 24V945 (unseen)", AM, "23V313 (Test-A), 23V320 and 24V945 (unseen-filer)"),
    ("D14", "isolation slips: 3 slips, 56 filings", DEV, "3 slips, 56 filings"),
    # preregistration
    ("R1", "H1 pass rule: delta >= 0.05", TH, '"delta_point_min": 0.05'),
    ("R2", "H1 pass rule: CI lower bound > 0", TH, '"delta_ci95_lower_gt": 0.0'),
    ("R3", "H1 pass rule: coverage >= 0.40", TH, '"coverage_min": 0.4'),
    ("R4", "H4 pass rule: attack success rate <= 0.10", TH, '"attack_success_rate_max": 0.1'),
    ("R5", "H6 pass rule: JSON-valid >= 0.95", TH, '"json_valid_min": 0.95'),
    ("R6", "H6 pass rule: p95 <= 120 s", TH, '"p95_seconds_max": 120'),
    ("R7", "bootstrap: 2,000 resamples, seed 0, filer cluster", TH, '"resamples": 2000'),
    ("R8", "dev reference for H1: 0.100 (0.035 to 0.172), coverage 50.9%", PF, "Delta 0.100 (0.035 to 0.172), coverage 50.9%"),
    ("R9", "Ollama version at freeze 0.40.6", PRE, "ollama version is 0.40.6"),
    ("R10", "agent model digest d8b0f5e9760c...", PRE, "digest d8b0f5e9760cd1682034f292d7ef72ec46f432149be0df7574bf2d6e92e38c04"),
    ("R11", "run 1 temperature 0 seed 0; run 2 temperature 0.5 seed 1; num_ctx 6144", PRE,
     "run 1 {'temperature': 0.0, 'seed': 0, 'presence_penalty': 0, 'num_ctx': 6144}; run 2 {'temperature': 0.5, 'seed': 1, 'presence_penalty': 0, 'num_ctx': 6144}"),
    ("R12", "H6 apps-open dev reference: 100% JSON-valid, p95 100-114 s", PF, "with apps open: 100%, p95 100-114 s"),
    ("R13", "CP bound with 0/30 successes would be 0.095", PF, "0/30 -> 0.095"),
    ("R14", "excluded gold events under amendment 1, Test-A: 27 of 1,445 (1.87%)", AM, "Test-A 27 of 1,445 non-contested gold events (1.87%, 11 filings)"),
    ("R15", "H6 verdict p95 includes the cold-load call (fixed before the run)", H6C, "The verdict p95 INCLUDES the first cold-load call"),
    # (a) preregistered, Test-A
    ("A1", "Test-A B2 event error 0.402 (1,005 claims)", P, "| B2 event error (all 1,005 claims) | 0.402 |"),
    ("A2", "Test-A agent accepted event error 0.267 (536 claims)", P, "| agent event error (536 accepted claims) | 0.267 |"),
    ("A3", "H1 delta 0.1352, 95% CI [0.0855, 0.1924]", P, "**0.1352**, 95% CI [0.0855, 0.1924]"),
    ("A4", "H1 coverage 0.533 (536/1005)", P, "0.533 (536/1005)"),
    ("A5", "H2 delta 0.1350, 95% CI [0.0803, 0.1977]", P, "delta 0.1350, 95% CI [0.0803, 0.1977]"),
    ("A6", "H2: B2 error 0.161, agent accepted 0.026, coverage 0.779", P, "B2 error 0.161 (199 claims); agent accepted error 0.026 (155 accepted, coverage 0.779)"),
    ("A7", "H5 (B1 - B2) 0.1092, 95% CI [0.0308, 0.1765]", P, "0.1092, 95% CI [0.0308, 0.1765]"),
    ("A8", "B1 event error 0.511 (624 claims)", P, "B1 0.511 (624 claims)"),
    ("A9", "run 2: 4 timeouts kept as missing", P, "Run 2 has 4 timeouts"),
    ("A10", "sensitivity runs: lowest H1 delta 0.1203 [0.072, 0.178]", P, "| bound: filings with an excluded gold event dropped | 0.1203 | [0.072, 0.178] |"),
    ("A11", "sensitivity runs: highest H1 delta 0.1455 [0.093, 0.207]", P, "| 0.1455 | [0.093, 0.207] |"),
    ("A12", "timeouts retried (sensitivity): H1 delta 0.1406, coverage 0.548", P, "| 0.1406 | [0.090, 0.197] | 0.548 |"),
    ("A13", "Test-A operational p95 (apps open): 130 s run 1, 184 s run 2", P, "p95 130 s (run 1), 184 s (run 2)"),
    ("A14", "H4: 2/30 = 0.067 after verifiers + agreement", H4, "**2/30 = 0.067**"),
    ("A15", "H4: exact one-sided 95% Clopper-Pearson upper bound 0.195", H4, "Clopper-Pearson upper bound: **0.195**"),
    ("A16", "H4 raw (no verifier): 11/30 = 0.367, bound 0.533", H4, "| 11/30 | 0.367 | 0.533 |"),
    ("A17", "H4 residual successes: suppress_events 2 of 6", H4, "| suppress_events | 2 | 2 | 2 |"),
    ("A18", "H4 flip_cause: 6 raw, 0 after verifiers", H4, "| flip_cause | 6 | 0 | 0 |"),
    ("A19", "empty event lists in Test-A run 1: 4 of 199 (2.0%)", X2, "**4 of 199 filings** (2.0%)"),
    ("A20", "suppress_events produced an empty list in 2 of 6 attacks", X2, "2 of 6 suppress_events attacks produced one"),
    ("A21", "H6 JSON-valid 1.000", H6, "| 1.000 | >= 0.95 | PASS |"),
    ("A22", "H6 p95 80.1 s including the cold-load call", H6, "| 80.1 | <= 120 | PASS |"),
    ("A23", "H6 p95 excluding the cold-load call 81.0 s", H6, "| 81.0 |"),
    ("A24", "H6 p50 31.7 s", H6, "| 31.7 / 31.7 |"),
    ("A25", "H6 max 112.5 s", H6, "| max s/filing | 112.5 |"),
    ("A26", "H6 cold-load call 65.0 s", H6, "cold-load call, 65.0 s"),
    ("A27", "H6 run: 100 dev filings", H6L, "filings=100"),
    ("A28", "H6 hardware: Apple M2, 8 GB, macOS 15.6.1, Ollama 0.40.6", H6, "Apple M2, 8 GB RAM, macOS 15.6.1, Ollama 0.40.6"),
    ("A29", "H6 clean condition as stated by the owner (Terminal.app, other apps closed)", H6C, "started from Terminal.app with caffeinate"),
    # (b) exploratory, secondary splits
    ("B1", "Test-B H1 delta 0.0327 [-0.0244, 0.0984]", SEC, "**0.0327 [-0.0244, 0.0984]**"),
    ("B2", "unseen H1 delta 0.0877 [0.0219, 0.1587]", SEC, "**0.0877 [0.0219, 0.1587]**"),
    ("B3", "Test-B H5 0.1458 [0.0639, 0.2048]", SEC, "**0.1458 [0.0639, 0.2048]**"),
    ("B4", "unseen H5 0.0877 [-0.0103, 0.1612]", SEC, "**0.0877 [-0.0103, 0.1612]**"),
    ("B5", "Test-B H2 0.2739 [0.1103, 0.4712]", SEC, "**0.2739 [0.1103, 0.4712]**"),
    ("B6", "unseen H2 0.1003 [0.0384, 0.1712]", SEC, "**0.1003 [0.0384, 0.1712]**"),
    ("B7", "accepted claims / coverage: Test-B 263 / 0.516, unseen 231 / 0.520", SEC, "| 263 / 0.516 | 231 / 0.520 |"),
    ("B8", "B2 event error: Test-B 0.386 [0.306, 0.456], unseen 0.417 [0.345, 0.503]", SEC, "| 0.386 [0.306, 0.456] | 0.417 [0.345, 0.503] |"),
    ("B9", "agent accepted error: Test-B 0.354 [0.244, 0.461], unseen 0.329 [0.258, 0.412]", SEC, "| 0.354 [0.244, 0.461] | 0.329 [0.258, 0.412] |"),
    ("B10", "B1 error: Test-B 0.532 (327 claims), unseen 0.504 (230 claims)", SEC, "| 0.532 (327 claims) [0.410, 0.639] | 0.504 (230 claims) [0.435, 0.565] |"),
    ("B11", "event claims B2: Test-B 510, unseen 444", SEC, "| event claims, B2 (all) | 1,005 | 510 | 444 |"),
    ("B12", "supplier claims accepted, Test-A: 20, error 0.400 [0.062, 0.655]", SEC, "20 (0.286); 0.400 [0.062, 0.655]"),
    ("B13", "supplier claims accepted, Test-B: 13, error 0.231 [0.000, 0.529]", SEC, "13 (0.371); 0.231 [0.000, 0.529]"),
    ("B14", "supplier claims accepted, unseen: 20, error 0.300 [0.000, 0.565]", SEC, "20 (0.526); 0.300 [0.000, 0.565]"),
    ("B15", "Test-B bounding run, rule b off: H1 0.0466 [-0.0223, 0.1362]", SEC, "H1 delta 0.0466 [-0.0223, 0.1362]"),
    ("B16", "Test-B bounding run, affected filings dropped: H1 0.0191 [-0.0392, 0.0750]", SEC, "H1 delta 0.0191 [-0.0392, 0.0750]"),
    ("B17", "Test-B ignored predictions 14 of 524 (2.7%)", SEC, "14 of 524 agent/B2 events (2.7%)"),
    ("B18", "run-2 missing on Test-B and unseen: 0", SEC, "| **0** | **0** |"),
    # (c) post hoc
    ("C1", "accepted claims scored wrong: Test-A 143 of 536, Test-B 93 of 263, unseen 76 of 231", FA, "| 536 / 143 (26.7%) | 263 / 93 (35.4%) | 231 / 76 (32.9%) |"),
    ("C2", "of those, date matches but type differs: 122 (85.3%), 80 (86.0%), 57 (75.0%)", FA, "| 122 (85.3%) | 80 (86.0%) | 57 (75.0%) |"),
    ("C3", "date-only view, Test-A: B2 0.142, accepted 0.039, delta 0.103 [0.051, 0.172]", FA, "| date only | 0.142 [0.087, 0.214] | 0.039 [0.022, 0.061] | 0.103 [0.051, 0.172] |"),
    ("C4", "date-only view, Test-B: B2 0.100, accepted 0.049, delta 0.051 [0.022, 0.090]", FA, "| date only | 0.100 [0.063, 0.146] | 0.049 [0.022, 0.079] | 0.051 [0.022, 0.090] |"),
    ("C5", "date-only view, unseen: B2 0.153, accepted 0.078, delta 0.075 [0.032, 0.135]", FA, "| date only | 0.153 [0.091, 0.238] | 0.078 [0.035, 0.137] | 0.075 [0.032, 0.135] |"),
    ("C6", "type agreement Test-A: labellers 0.788 [0.762, 0.812] (781/991)", FA, "0.788 [0.762, 0.812] (781/991)"),
    ("C7", "type agreement Test-A: agent 0.763 [0.725, 0.798] (393/515)", FA, "0.763 [0.725, 0.798] (393/515)"),
    ("C8", "type agreement Test-B: labellers 0.786 [0.748, 0.820] (397/505)", FA, "0.786 [0.748, 0.820] (397/505)"),
    ("C9", "type agreement Test-B: agent 0.680 [0.620, 0.735] (170/250)", FA, "0.680 [0.620, 0.735] (170/250)"),
    ("C10", "type agreement unseen: labellers 0.827 [0.788, 0.861] (340/411)", FA, "0.827 [0.788, 0.861] (340/411)"),
    ("C11", "type agreement unseen: agent 0.728 [0.664, 0.783] (155/213)", FA, "0.728 [0.664, 0.783] (155/213)"),
    ("C12", "Test-B Jayco: labellers 26/29, agent 6/18", FA, "| Jayco | 0.897 [0.736, 0.964] (26/29) | 0.897 [0.736, 0.964] (26/29) | 0.333 [0.163, 0.563] (6/18) |"),
    ("C13", "Test-B Ford: labellers 53/79, agent 11/31", FA, "| Ford | 0.671 [0.561, 0.764] (53/79) | 0.645 [0.533, 0.743] (49/76) | 0.355 [0.211, 0.531] (11/31) |"),
    ("C13b", "4 of the agent's 6 most frequent type confusions are among the labellers' 6", FA, "4 of the agent's 6 most frequent confusions are also among the labellers' 6 most frequent"),
    ("C14", "FILER_AWARENESS / INVESTIGATION_START: 6.4% of labeller disagreements (25 of 389)", FA, "| FILER_AWARENESS / INVESTIGATION_START | 25 | 6.4% |"),
    ("C15", "FILER_AWARENESS / INVESTIGATION_START: 20.8% of agent disagreements (54 of 260)", FA, "| FILER_AWARENESS / INVESTIGATION_START | 54 | 20.8% |"),
    ("C16", "most frequent pair INVESTIGATION_START / OTHER: labellers 32.9%, agent 39.2%", FA, "| INVESTIGATION_START / OTHER | 102 | 39.2% |"),
    ("C17", "most frequent labeller pair INVESTIGATION_START / OTHER 128 (32.9%)", FA, "| INVESTIGATION_START / OTHER | 128 | 32.9% |"),
    ("C18", "erratum: about 33% of Ford's chronology entries recur in another Ford filing; within-filing repeat share about 0", ERR, "about 33% of Ford's entries recur"),
    ("C19", "only 2 accepted-wrong claims are within-filing duplicates (unseen)", FAB, "only 2 accepted-wrong claims are duplicates, both in unseen-filer"),
    ("C20", "leave-Ford-out Test-B H1 delta 0.0496 [-0.0117, 0.1130], coverage 0.539", SEC, "0.0496 [-0.0117, 0.1130] at coverage 0.539"),
    ("C21", "Ford on Test-B: 85 of 510 claims, error 0.541; accepted 34 at 0.676", SEC, "Ford is 85 of 510 claims (16.7%) with 0.541 error, and its 34 accepted claims have 0.676 error"),
    ("C22", "tipping point: H1 point threshold fails at 24.9% of accepted-correct claims wrong (98 claims, 9.7% of labels)", X2, "fails first, at 24.9% (98 claims = 9.7% of labels)"),
    ("C23", "tipping point: CI lower bound reaches 0 at 26.7% (105 claims, 10.4% of labels)", X2, "26.7% of the accepted-correct claims are really wrong (105 claims = 10.4% of all 1005 event labels)"),
    ("C24", "Shapley: run-2 agreement 0.065 [0.038, 0.097]", X2, "run-2 agreement 0.065 [0.038, 0.097]"),
    ("C25", "Shapley: V3 unparseable date 0.031, E1 0.026", X2, "V3 unparseable-date 0.031 [0.013, 0.055], E1 0.026 [0.009, 0.045]"),
    ("C26", "filters alone: verifiers only delta 0.106 at coverage 0.659", X1, "| 662 | 0.659 | 0.296 | 0.106 [0.058, 0.160] |"),
    ("C27", "filters alone: run-2 agreement only delta 0.103 at coverage 0.714", X1, "| 718 | 0.714 | 0.299 | 0.103 [0.057, 0.155] |"),
    ("C28", "AURC (events) 0.269 [0.215, 0.332]", X1, "AURC 0.269 [0.215, 0.332]"),
    ("C29", "cluster t-bound: events upper bound 0.324", X2, "upper bound **0.324**"),
    ("C30", "cluster t-bound false-certification rate, events: lowest 0.0115", X2, "| 231/20000 | 0.0115"),
    ("C31", "cluster t-bound false-certification rate, events: highest 0.0273", X2, "| 546/20000 | 0.0273"),
    ("C32", "cluster t-bound false-certification rate, cause: lowest 0.0481", X2, "| 963/20000 | 0.0481"),
    ("C33", "cluster t-bound false-certification rate, cause: highest 0.2056", X2, "| 4111/20000 | 0.2056"),
    # TS-1 timeliness screen (post-freeze protocol ts-protocol-1, silver reference)
    ("T0", "TS-1 protocol fixed and committed before any gap was computed", TSP, "**Status: fixed before any gap is computed.**"),
    ("T1", "TS-1 population: 305 defect filings of 397; 92 noncompliance", TS, "**Population:** 305 defect filings (out of 397; 92 noncompliance filings are reported separately)."),
    ("T2", "TS-1 primary (Submission Date): FLAGGED 104/305 = 0.341 W[0.290, 0.396]", TS, "FLAGGED 104/305 = 0.341 W[0.290, 0.396] B[0.268, 0.418]"),
    ("T3", "TS-1: 98 of the 104 primary FLAGGED are amended versions; originals 6/136", TS, "98 of the 104 FLAGGED filings are processed from an amended version, against 6/136 among originals."),
    ("T4", "TS-1: Submission Date equals RCDATE in 15 of 169 amended versions and 131 of 136 originals", TS, "it equals RCDATE in only 15 of 169 amended versions, against 131 of 136 originals"),
    ("T5", "TS-1: RCDATE earlier than an amended version's Submission Date by a median of 35 calendar days", TS, "RCDATE is earlier by a median of 35 calendar days"),
    ("T6", "TS-1 RCDATE variant: FLAGGED 19/305 = 0.062 W[0.040, 0.095] B[0.033, 0.096]", TS, "RCDATE variant: FLAGGED 19/305 = 0.062 W[0.040, 0.095] B[0.033, 0.096]."),
    ("T7", "TS-1 originals stratum: FLAGGED 6/136 = 0.044 W[0.020, 0.093] B[0.013, 0.086]", TS, "originals stratum: FLAGGED 6/136 = 0.044 W[0.020, 0.093] B[0.013, 0.086]."),
    ("T8", "TS-1 RCDATE variant, pooled: gap_mid 5 [3-5] 6; agent coverage 126/305; bounds 0.049-0.649; kappa 0.809, PABAK 0.938 (n 121)", TS,
     "| pooled | 305 | 217 | 19/305 = 0.062 W[0.040, 0.095] B[0.033, 0.096] | 5 [3–5] 6 | 5 [3–5] 5 | 5 [3–5] 6 | 126/305 (0.413) | 15/126 (0.119) | 0.049 [0.026, 0.076] – 0.649 [0.562, 0.738] | 121 | 10,0,0; 1,104,2; 0,2,2 | 0.809 [0.611, 0.957] | 0.938 [0.874, 0.988] |"),
    ("T9", "TS-1 originals stratum, pooled: gap_mid 5 [3-5] 6; agent coverage 52/136; bounds 0.015-0.654; kappa 0.383, PABAK 0.912 (n 51, unstable)", TS,
     "| pooled | 136 | 99 | 6/136 = 0.044 W[0.020, 0.093] B[0.013, 0.086] | 5 [3–5] 6 | 4 [3–5] 5 | 5 [3–5] 6 | 52/136 (0.382) | 2/52 (0.038) | 0.015 [0.000, 0.040] – 0.654 [0.520, 0.779] | 51 | 0,0,0; 1,47,2; 0,0,1 | 0.383 [0.000, 1.000] | 0.912 [0.786, 1.000] (reference FLAGGED among n both: 0, fewer than 10: unstable) |"),
    ("T10", "TS-1: 88 of 305 defect filings have no usable DECISION date (silver)", TS, "88 of 305 defect filings (0.289) have no usable DECISION date"),
    ("T11", "TS-1: agent accepted, dated DECISION claim for 127/305 (0.416)", TS, "127/305 = 0.416"),
    ("T12", "TS-1: agent vs reference kappa 0.937 where both have a date (primary)", TS, "(Cohen's κ 0.937)"),
    ("T13", "TS-1 amendment TS-A1: 2 filings, 0 anchors affected", TS, "**Anchors using a year from context in them: 0**"),
    ("T14", "TS-1: 186 of 397 filings typed by the flat-file FMVSS proxy (2025+ form has no type field)", TS, "186 of 397 filings are typed by a flat-file FMVSS proxy"),
    # SC-1 supplier check (post-freeze protocol sc-protocol-1; reference = filer-declared supplier, non-AI, not ground truth)
    ("U0", "SC-1 protocol fixed before any claim was compared with the reference", SCP, "**Status: fixed before any claim is compared with the reference.**"),
    ("U1", "SC-1: supplier block parsed in 397/397 filings (portal 186, older 211)", SC, "Parse rate 397/397, with 0 failures, in both layouts: portal (186) and older (211)."),
    ("U2", "SC-1 strata: NAMED 255, OEM_SELF 47, OBTAINED_FROM 4, MULTIPLE 6, BLANK 85, PARSE_FAIL 0", SC, "| **all** | 255 | 47 | 4 | 6 | 85 | 0 |"),
    ("U3", "SC-1 population: 261 filings declare one or more external suppliers", SC, "**Population:** 261 filings declare one or more external suppliers"),
    ("U4", "SC-1: 52 of 65 Supplier-Type-OEM names are not the filer", SCI, "52 of the 65 OEM-typed names are not the filer"),
    ("U5", "SC-1: the agent's frozen input contains no supplier-block line in any filing", SC, "no block heading or field line appears in the agent's frozen input in any filing"),
    ("U6", "SC-1: agent supplier claims 226 (92 gate-accepted)", SC, "Agent run-1: 226 in total, of which 92 are gate-accepted."),
    ("U7", "SC-1 agent exact, pooled: recall 18/261 = 0.069; accepted 13/261; precision 19/172 = 0.110; accepted 14/70 = 0.200", SC,
     "| **pooled** | 261 | 18/261 = 0.069 W[0.044, 0.106] B[0.037, 0.110] | 13/261 = 0.050 W[0.029, 0.083] B[0.024, 0.085] | 19/172 = 0.110 W[0.072, 0.166] B[0.065, 0.168] | 14/70 = 0.200 W[0.123, 0.308] B[0.105, 0.317] |"),
    ("U8", "SC-1 silver exact, pooled: S2 recall 92/261 = 0.352; S1 precision 254/261 = 0.973; S2 precision 92/113 = 0.814", SC,
     "| **pooled** | 261 | 255/261 = 0.977 W[0.951, 0.989] B[0.958, 0.993] | 92/261 = 0.352 W[0.297, 0.412] B[0.268, 0.463] | 254/261 = 0.973 W[0.946, 0.987] B[0.953, 0.991] | 92/113 = 0.814 W[0.733, 0.875] B[0.723, 0.897] |"),
    ("U9", "SC-1 agent vs silver S2, pooled: 18 both / 0 agent only / 74 silver only / 169 neither", SC, "| **pooled** | agent all vs silver S2 | 18 | 0 | 74 | 169 |"),
    ("U10", "SC-1 containment, pooled: agent precision (accepted) 27/70", SC, "| token containment | **pooled** | 261 | 34/261 = 0.130 | 35/172 = 0.203 | 26/261 = 0.100 | 27/70 = 0.386 |"),
    ("U11", "SC-1 fuzzy tsr>=90, pooled: agent precision (accepted) 29/70", SC, "| fuzzy token_set_ratio ≥ 90 | **pooled** | 261 | 40/261 = 0.153 | 41/172 = 0.238 | 28/261 = 0.107 | 29/70 = 0.414 |"),
    ("U12", "SC-1 components not run: no component claims exist", SC, "**Not run: there are no component claims to check.**"),
    ("U13", "SC-1 amendment SC-A1: 23 of 26 Pass-C silver S2 claims fall in the population", SC, "**23 of these 26 claims fall in the population;**"),
    ("U14", "SC-1 post hoc: 24 of 261 population filings declare a short form of the filer's own name; 1 of 19 agent matches there", SC,
     "In 24 of 261 population filings"),
    ("U15", "SC-1 post hoc: 14 silver S1 quotes located out of block are first-match artefacts", SC, "**POST HOC diagnostic:** in all 14"),
    # cost, hardware, runs
    ("H1", "Test-A run 1: 12:48:52 to 16:10:07 (3 h 21 min)", DEV, "12:48:52 start, 16:10:07 done"),
    ("H2", "Test-A run 2: restart at 21:32:45 with 167 of 199 records", DEV, "RESTART 21:32:45 with 167 of 199 records"),
    ("H3", "Test-A run 2: four timeouts at 300 s", DEV, "four per-call timeouts at 300 s"),
    ("H3b", "Test-A run 2: one runner crash, no model call completed", DEV, 'one "model runner has unexpectedly stopped" at 2 s (RCLRPT-25V574-1873; no model call completed, no output)'),
    ("H3c", "Test-A run 2: the crashed record retried once", DEV, "RCLRPT-25V574-1873 re-run once with the frozen run-2 settings"),
    ("H4", "battery death: Low Power Sleep 2026-10-25 17:56:21 on battery at 1%", SEC, "Low Power Sleep at 2026-10-25 17:56:21 while on battery at 1% charge"),
    ("H4b", "the Mac rebooted at 19:22:49", SEC, "the machine rebooted at 19:22:49"),
    ("H4c", "Test-B run 2 restart 2026-10-27 11:48:06", SEC, "RESTART 2026-10-27 11:48:06"),
    ("H5", "Test-B run 1: 15:19:16 to 17:52:00 (2 h 33 min)", SEC, "| Test-B | 1 | 2026-10-25 15:19:16 | 2026-10-25 17:52:00 |"),
    ("H6", "Test-B run 2 after restart: 11:48:29 to 12:46:55 (58 min)", SEC, "START 11:48:29 | 2026-10-27 12:46:55"),
    ("H7", "unseen run 1: 12:47:02 to 13:39:30 (52 min)", SEC, "| unseen | 1 | 2026-10-27 12:47:02 | 2026-10-27 13:39:30 |"),
    ("H8", "unseen run 2: 13:39:32 to 14:30:00 (50 min)", SEC, "| unseen | 2 | 2026-10-27 13:39:32 | 2026-10-27 14:30:00 |"),
]


def main():
    bad, cache = [], {}
    for cid, claim, (f, c), needle in CLAIMS:
        if (f, c) not in cache:
            cache[f, c] = subprocess.run(["git", "show", f"{c}:{f}"], capture_output=True, text=True).stdout
        if needle not in cache[f, c]:
            bad.append(cid)
            print(f"MISMATCH {cid}: {claim!r} not found as {needle!r} in {f}@{c}")
    print(f"{len(CLAIMS)} claims checked, {len(bad)} mismatches")
    if "--md" in sys.argv:
        print("| # | claim | source | commit | matched text |\n|---|---|---|---|---|")
        for cid, claim, (f, c), needle in CLAIMS:
            print(f"| {cid} | {claim} | `{f}` | {c} | `{needle.replace('|', '¦')}` |")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
