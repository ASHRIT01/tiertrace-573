# Phase 6 Test-A labelling log (silver labels: AI-made, not human-verified)
Per batch of 25 filings: Pass A (code + overrides by the Claude Code session, claude-sonnet-5-5), Pass B (opus subagent), Pass C (opus subagents, blind X/Y). Work dirs: data/labels/work/testA/bNN/.

| batch | filings | A-vs-B items (S1/S2/C/U/E) | E agree (A vs B) | Pass C X / Y / NEITHER / CONTESTED | C with A | C with B | override entries (events / claims) |
|---|---|---|---|---|---|---|---|
| b01 | 25 | 42 (0/2/1/1/38) | 91/158 = 57.6% | 16 / 21 / 4 / 1 | 3/42 = 7.1% (3/41 decided) | 34/42 = 81.0% (34/41 decided) | 11 files / 2 files |
(C picked version X in 16 and Y in 21 items while X was Pass A in 26 of 42 items, so the preference for B is not a position effect.)
