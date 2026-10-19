# Phase 6 Test-A labelling log (silver labels: AI-made, not human-verified)
Per batch of 25 filings: Pass A (code + overrides by the Claude Code session, claude-sonnet-5-5), Pass B (opus subagent), Pass C (opus subagents, blind X/Y). Work dirs: data/labels/work/testA/bNN/.

| batch | filings | A-vs-B items (S1/S2/C/U/E) | E agree (A vs B) | Pass C X / Y / NEITHER / CONTESTED | C with A | C with B | override entries (events / claims) |
|---|---|---|---|---|---|---|---|
| b01 | 25 | 42 (0/2/1/1/38) | 91/158 = 57.6% | 16 / 21 / 4 / 1 | 3/42 = 7.1% (3/41 decided) | 34/42 = 81.0% (34/41 decided) | 11 files / 2 files |
(C picked version X in 16 and Y in 21 items while X was Pass A in 26 of 42 items, so the preference for B is not a position effect.)
| b02 | 25 | 48 (S1/S2/C/U/E = 0/2/1/1/44) | 91/162 = 56.2% | 17 X / 23 Y / 3 NEITHER / 5 CONTESTED | 7/48 = 14.6% | 33/48 = 68.8% | checks 0 fail; 178 events; overrides: 19 event-file entries, 8 claim-file entries |
| b03 | 25 | 40 (S1/S2/C/U/E = 0/3/3/2/32) | 65/118 = 55.1% | 12 X / 22 Y / 4 NEITHER / 2 CONTESTED | 4/40 = 10.0% | 30/40 = 75.0% | checks 0 fail (after the D-T3 S1-quote override); 158 events; overrides: 14 event-file entries, 7 claim-file entries |
| b04 | 25 | 41 (S1/S2/C/U/E = 0/3/1/3/34) | 83/130 = 63.8% | 16 X / 10 Y / 12 NEITHER / 3 CONTESTED | 5/41 = 12.2% | 21/41 = 51.2% | checks 0 fail; 169 events; overrides: 16 event-file entries, 7 claim-file entries |
| b05 | 25 | 26 (S1/S2/C/U/E = 0/0/2/1/23) | 78/116 = 67.2% | 9 X / 12 Y / 3 NEITHER / 2 CONTESTED | 3/26 = 11.5% | 18/26 = 69.2% | checks 0 fail; 151 events; overrides: 16 event-file entries, 7 claim-file entries (review sheet without chronology text from b05, COMPACT mode) |
| b06 | 25 | 48 (S1/S2/C/U/E = 0/2/2/2/42) | 102/168 = 60.7% | 23 X / 23 Y / 1 NEITHER / 1 CONTESTED | 6/48 = 12.5% | 40/48 = 83.3% | checks 0 fail; 202 events; overrides: 18 event-file entries, 5 claim-file entries + 10 mechanical S1/S2 quote fixes (D-T3) |
| b07 | 25 | 82 (S1/S2/C/U/E = 0/3/1/2/76) | 102/219 = 46.6% | 26 X / 33 Y / 17 NEITHER / 6 CONTESTED | 3/82 = 3.7% | 56/82 = 68.3% | checks 0 fail; 227 events; overrides: 17 event-file entries, 7 claim-file entries + 27 mechanical quote fixes (D-T3) |
