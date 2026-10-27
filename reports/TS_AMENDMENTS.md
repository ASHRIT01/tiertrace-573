# TS-1 amendments to the protocol (tag `ts-protocol-1`)

The protocol requires every change made after the tag to be listed here, with its date and reason, and the results it affects to be labelled POST HOC. Silver reference (AI-generated, not human-verified).

## TS-A1 (2026-10-28): crash-only guard on the frozen date parser inside `chronology_years`

- **What happened.** On its first run, `scripts/ts_screen.py` stopped while loading inputs, before any anchor, gap or flag was computed and before any output file existed. The frozen `tt.labels.dates.parse_span`, called by the frozen `tt.labels.events.chronology_years`, raised `ValueError: day is out of range for month` on an invalid calendar date in 2 chronologies (1 Test-A, 1 unseen-filer). This is the known D-T2 crash in `reports/DEVIATIONS.md`.
- **Change.** `scripts/ts_screen.py` imports `tt.eval.amend1`, which applies the amendment-1 crash-only guard (`safe_parse_span`) at import: a date that would crash returns `None`, exactly as for any other date the parser cannot read. This is the same guard used for all Phase 6 scoring, and the labelling runs used an equivalent guard (`scripts/phase6_runner.py`). Nothing that did not crash changes.
- **Effect.** It affects only the set of chronology years used to give year-less dates a year (protocol D) in those 2 filings. The protocol's definitions are unchanged.
- **POST HOC label.** Because it came after the tag, the results that depend on it are labelled POST HOC: the year context of these 2 filings. The report gives the number of anchors in these 2 filings that used a year taken from context. If that number is 0, no anchor, gap or flag depends on the amendment.
