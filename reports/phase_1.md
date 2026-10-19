# Phase 1 report: dev silver labels

All labels are **silver labels: AI-made, cross-checked by independent AI passes and code checks. Not human-verified.**
Numbers below come from `tt.labels.agree.compare` and `tt.labels.protocol.apply_c` run in this session.

## What changed
Pass A for 100 dev filings; Pass B by 5 blind subagents; A-vs-B comparison; Pass C by 5 adjudicator subagents; final labels
`data/labels/dev_silver_v1.json` (SHA-256 `d17a30a4c710e1aadb46fb773f2b4759cea49eea3ba5457279ae3441be46f35e`); `docs/LABELS.md`. Nothing frozen.

## Pass A vs Pass B agreement (before adjudication)
| claim | agree/units | rate | Wilson 95% |
|---|---|---|---|
| S1 | 100/100 | 100.0% | 96.3–100.0% |
| S2 | 93/100 | 93.0% | 86.3–96.6% |
| C | 99/100 | 99.0% | 94.6–99.8% |
| U | 97/100 | 97.0% | 91.5–99.0% |
| E (scored events) | 368/536 | 68.7% | 64.6–72.4% |
| E headline types | 201/275 | 73.1% | 67.6–78.0% |

Event unit = one paired event, or one unpaired event on either side (a pair with equal dates and different types counts as 2 disagreeing units).

## Pass C
113 items: 66 event type differs, 21 only in A, 15 only in B, 7 S2, 3 U, 1 C.
Decisions: A 14, B 77, NEITHER 6, CONTESTED 16 (11 E, 3 S2, 1 U, 1 C). Most CONTESTED events are A and B quoting different sentences of one entry.
B won 77 of 113, mostly event type (A typed OTHER where B/C typed INVESTIGATION_START or similar), so Pass A was the less accurate pass on events.

## Final labels
Code checks: 0 failures. 591 events; 16 contested items excluded from scoring.
S1: 58 SUPPORTED / 42 NOT_REPORTED. S2: 24 SUPPORTED / 39 INSUFFICIENT / 37 NOT_REPORTED. Cause: 70/5/25 SUPPORTED/INSUFFICIENT/NOT_REPORTED.
U: 25 NAMED, 19 UNNAMED, 46 NONE_MENTIONED, 10 NOT_REPORTED.

## UNVERIFIED / caveats
- Correctness of any label against the truth: UNVERIFIED (no human review; one model family throughout).
- Subagents' `files_seen.txt` are self-reported; I checked their content, not the sandbox.
- Two Pass C agents noted `files_seen` formatting slips (bare names); content was consistent.
