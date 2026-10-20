# Phase 6 silver labels: hashes and summary (silver labels: AI-made, not human-verified)
Labelling is blind to runs/ (guard `tt/labels/blind.py`); no model or baseline has been run on any test filing. Models as declared in the freeze: Pass A = code + per-filing overrides by the Claude Code session (claude-sonnet-5-5), Pass B = opus subagents, Pass C = opus subagents (blind X/Y order). Aliases as passed to the Agent tool; alias-to-version mapping cannot be proven.

## Test-A labelled (200 campaigns; 199 readable; 23V313 excluded as unreadable)
| file | SHA-256 |
|---|---|
| config/overrides/test_a_events.json | 88bf83c9fd31e327a94389f3ddab83cf7cc80462ef52520aa22be71036314558 |
| config/overrides/test_a_claims.json | 2e0e1b996f1da198018ddaeee71683b4911fd3982597ad08cc27d7736256445e |
| data/labels/testA_passA.json | f77e9135067969233dce6e58870696e42fbf78d7e0eb8ade34dd1ac8f495f940 |
| data/labels/testA_passB.json | 97d7d60c25081b60bfe53bd2ddefe5980b39897235568b45171ce69b8227b8a3 |
| data/labels/testA_passC_items.json | 153bf2bd4f9d902ef9418c1dc6f9ea178cfc67e06089b80bc62853893e1562c2 |
| data/labels/testA_passC_decisions.json | 0d2603cebb2b3922f097706564c6ab555f4b8d0b67f412734142577ee448d3f7 |
| **data/labels/testA_silver.json** | **c8b637830c2e46753241cebd33b1043917f8832f03da41238b1d1d9aae180950** |

199 records, 1,466 events, 21 contested items (excluded from scoring), 0 code-check failures (Q1-Q4). Pass C items 403 (events 357, S2 19, U 15, C 11, S1 1). Pass C decisions: X 157, Y 176, NEITHER 49, CONTESTED 21. Translated back to the passes: Pass C sided with Pass A in 37 items (9.2%), with Pass B in 296 (73.5%), corrected both in 49 (12.2%), contested 21 (5.2%).
Per-batch numbers: reports/phase_6_testA_labelling_log.md. Deviations and rule problems: reports/DEVIATIONS.md.

## Test-B (100 campaigns; 100 readable)
| file | SHA-256 |
|---|---|
| config/overrides/test_b_events.json | 1eda8447c5ae82cc5ca607466f8aaede6f777327fec4367da8ce3741a7d48bab |
| config/overrides/test_b_claims.json | 990d80b6e9d7d265225879566661c53c128efd425cd50161851c291314de5236 |
| data/labels/testB_passA.json | 56eb660b2960ababf217e2b9232f53845a5bd9027517dad615d384d043b08db1 |
| data/labels/testB_passB.json | 085e50ff115bd532ba489f586f0f514680ea494f9864d4411f2fd5bf19af68d0 |
| data/labels/testB_passC_items.json | 7fdaece147aa4ae367aa2ea38d49448072169cc6842989865b48df05c36668c2 |
| data/labels/testB_passC_decisions.json | ad1441a56e9ef4a2ed016933be4f3c57bd0f57b15c2ac052fccb4ed0d306b31b |
| **data/labels/testB_silver.json** | **96e1f793d759766ce565b34f9e4a675d3f4f8ed505ae5c06b2d01589082004c2** |

100 records, 806 events, 16 contested items (excluded from scoring), 0 code-check failures. Pass C items 205 (events 180, U 10, S2 9, C 5, S1 1). Pass C decisions: X 61, Y 108, NEITHER 20, CONTESTED 16. Pass C sided with Pass A in 21 items (10.2%), with Pass B in 148 (72.2%), corrected both in 20, contested 16.

## Unseen-filer (100 campaigns; 98 readable; 23V320 and 24V945 excluded as unreadable)
| file | SHA-256 |
|---|---|
| config/overrides/unseen_events.json | eb9fcc377e5d645323f3d80edcb8f050b2c0c1d6f0ff1c71623715012db1b451 |
| config/overrides/unseen_claims.json | 14b55beb2e9ab1fec67723e9fbb44842b14e0ad3af815ff5bf44c0f0bd29da82 |
| data/labels/unseen_passA.json | b1db81440e50437a14f9a64200dba78f09af4ab8278837420b7faeac19680083 |
| data/labels/unseen_passB.json | ef70bf2cb9de00a9fa5d6ce9c65d3a72671eddd75037ebe25780093f813adaa5 |
| data/labels/unseen_passC_items.json | 26d41738fa35eeb86b5fa193a0de708f441b8e358c40dcad18507e276cdeb834 |
| data/labels/unseen_passC_decisions.json | 7dca147e5d3cb0a731714b51634baefb5af9738ca769af07b864c1fe6d450d7f |
| **data/labels/unseen_silver.json** | **86f669683547bea16422241dec42f418e79d6d155d55a163fb52e0edf4abae07** |

98 records, 580 events, 12 contested items (excluded from scoring), 0 code-check failures. Pass C items 165 (events 143, U 14, C 4, S2 4). Pass C decisions: X 48, Y 94, NEITHER 11, CONTESTED 12. Pass C sided with Pass A in 14 items (8.5%), with Pass B in 128 (77.6%), corrected both in 11, contested 12.
Per-batch numbers: reports/phase_6_testB_labelling_log.md, reports/phase_6_unseen_labelling_log.md.
