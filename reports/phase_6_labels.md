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
