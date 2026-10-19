# Phase 2 diagnosis (dev only; 2026-10-19)

All scores are **vs silver labels** (AI-made, cross-checked by independent AI passes and code checks; not human-verified; one model family throughout).
Test-A, Test-B and the other test splits were not opened. Every number below comes from code run in this session
(`tt/eval/diagnose.py`, `tt/eval/baselines_run.py`, `tt/eval/devscore.py`); raw outputs are the `reports/phase_2_*.json` files.
**All speed numbers: measured with Claude Code and other apps open (and swap use of 6-14 GB), not the clean hardware result.**
Prompt versions and every post-hoc change: `docs/PROMPT_LOG.md`.

## 1. Metric definitions
- **JSON-valid rate**: filings whose output parses and validates against the `Extraction` schema / 100.
- **Verifier pass rate**: filings with zero errors from `tt/verify/verifier.py` / 100 (per filing, not per claim; one bad claim fails the filing).
- **Unsupported-claim rate**: among filings whose silver S2 is not SUPPORTED (73; 3 CONTESTED skipped), the share where the model asserts at least one SUPPORTED supplier/sub-supplier/distributor. Per filing. It counts any such company, so listing the filer or another company named in the text counts against the model even when the text does name it.
- **S2 recovery**: among the 24 filings whose silver S2 is SUPPORTED, the share where a SUPPORTED supplier-role company matches the silver name and its quote is verbatim in the named section (k/n below).
- **Headline event F1** (the scorer's `event_f1`): silver events of the five headline types vs predicted events of those types; a match needs equal type and overlapping date spans; OTHER events and fuzzy dates excluded.
- **Date-only F1 / date+type F1 / type accuracy given date** (`event_split`): over ALL scored silver events (all six types incl. OTHER) vs all predicted events; one-to-one pairing on date-span overlap preferring equal type. date-only F1 ignores type; date+type F1 needs equal type; type accuracy = date+type matches / date-only matches.
- **Cause accuracy**: `cause_reported` equals (silver cause status == SUPPORTED). INSUFFICIENT counts as "not reported" (5 filings).

**The two event F1 families differ**: 0.21 / 0.235 are headline-only (five types); 0.15 / 0.16 are date+type over all six types.

## 2. Results, same 100 dev filings

| | B0 | B1 (rules) | 2B v1 | 4B v1 | 4B v2 |
|---|---|---|---|---|---|
| JSON-valid | 100% | 100% | 100% | 100% | 100% |
| Verifier pass rate | 75% | 82% | 13% | 2% | 17% (26% with `extra.py` layer) |
| S2 recovery name + verbatim quote | 0/24 | 1/24 | 11/24 | 11/24 | 11/24 |
| Unsupported-claim rate | 0/73 | 8/73 (11%) | 69/73 (94.5%) | 69/73 (94.5%) | 12/73 (16.4%) |
| Headline event F1 (P / R) | n/a (no events) | 0.399 (0.494 / 0.335) | 0.235 (0.195 / 0.296) | 0.211 (0.189 / 0.237) | 0.647 (0.595 / 0.708) |
| Date-only F1 (all events) | 0 | 0.638 | 0.754 | 0.752 | 0.802 |
| Date+type F1 (all six types) | 0 | 0.326 | 0.156 | 0.153 | 0.539 |
| Type accuracy given date matched | n/a | 51.1% | 20.6% | 20.4% | 67.1% |
| Cause accuracy | 70% | 95% | 94% | 98% | 95% |

S2 recovery with Wilson 95% (k/n): 4B v1 11/24 (27.9-64.9%), 2B v1 11/24 (27.9-64.9%), 4B v2 11/24 (27.9-64.9%), B1 1/24 (0.7-20.2%), B0 0/24 (0.0-13.8%).
Name-only recovery (quote not checked): 4B v1 17/24 (50.8-85.1%), 2B v1 16/24 (46.7-82.0%). The 11/24 for 4B and 2B is a coincidence (8 filings overlap).
Unsupported-claim rate Wilson 95%: 4B v1 69/73 (86.7-97.8%); B1 8/73 (5.7-20.2%).

**B1 beats both v1 models on events (0.399 vs 0.21/0.235) and on verifier pass rate (82% vs 2%/13%), and ties or beats them on cause accuracy against the 2B (95% vs 94%) but not the 4B (98%).** The models beat B1 only on S2 recovery (11/24 vs 1/24) and, on dates, on date-only F1 (0.75-0.80 vs 0.64). v1 lost on event type: the prompt gave no event-type definitions.
B1 provenance: its regexes and keyword lists (`tt/baselines/rules.py`) were written once, before B1 was first run on dev, and never changed afterwards, so they are not tuned on dev results. They were informed by the labeling rules, which I wrote while reading dev filings.
**Event-type ceiling**: the two independent AI labelers (Pass A vs Pass B) agree on type for 368 of 434 date-matched events = 84.8% (Wilson 95% 81.1-87.9%). Models in v1 reach 20%, B1 51%, 4B v2 67%.

## 3. Verifier audit (v1 outputs, vs silver; `tt/verify/verifier.py` unchanged)
Claim = company or event. *wrong* = no matching silver content (company: not a silver S1/S2/U name, and is the filer/affiliate or absent from the text; event: no silver event with an overlapping date, or a different type). *right* = matches silver. *unlabelled* = company named in the text that silver has no claim on. Precision = true rejects / (true + false rejects); recall = true rejects / all wrong claims (not caught by type errors, etc.).
V4 fired 0 times; V5 (path member not among companies) is per path member and has no silver label (4B 34, 2B 13); V6 does not exist in `verifier.py` (V1-V5 only). V7 and the extra verifiers are Phase 4.

| verifier | model | failed | true rejects | false rejects | unlabelled | precision | recall |
|---|---|---|---|---|---|---|---|
| V1 quote not found | 4B | 87 | 59 | 16 | 12 | 0.79 | 0.15 |
| V2a company not in text | 4B | 4 | 4 | 0 | 0 | 1.00 | 0.01 |
| V2b filer as supplier | 4B | 105 | 99 | 6 | 0 | 0.94 | 0.25 |
| V3 date | 4B | 58 | 41 | 17 | 0 | 0.71 | 0.10 |
| any | 4B | 228 | 181 | 35 | 12 | 0.84 | 0.46 |
| V1 | 2B | 117 | 72 | 23 | 22 | 0.76 | 0.16 |
| V2b | 2B | 88 | 82 | 6 | 0 | 0.93 | 0.18 |
| V3 | 2B | 92 | 75 | 17 | 0 | 0.82 | 0.17 |
| any | 2B | 268 | 205 | 41 | 22 | 0.83 | 0.45 |

Per-filing consistency check: my per-claim flags reproduce `verify()` error counts on all 100 filings for both models.
**V2 was not too strict**: 99 of 105 (4B) and 82 of 88 (2B) V2b rejections were claims silver does not support (94%/93%). The 6 + 6 false rejects are claims where the silver block supplier (S1) is the filer or an affiliate (silver has 7 such S1 labels of 58 SUPPORTED); `extra.py` stops V2 from rejecting a company equal to the block supplier.
V3 false rejects are valid dates the old parser cannot read: ranges ("April to May 2019"), month-only, year-less ("11/29"). V3's recall is low because it only sees unparseable dates; the real event errors are type errors, which no verifier here can catch.

## 4. Quote check
| outputs | quotes | pass: V1 as written (case-insensitive, whitespace) | pass: principled (whitespace, curly/straight quotes, dashes, line-break hyphenation, case-sensitive) |
|---|---|---|---|
| 4B v1 | 632 | 526 (83.2%) | 554 (87.7%) |
| 2B v1 | 763 | 625 (81.9%) | 657 (86.1%) |
| 4B v2 | 654 | 563 (86.1%) | 601 (91.9%) |

(The principled check also uses the original, unmasked section text with line breaks; the V1-as-written column is the verifier's own `locate`.) Residual failures (principled), 4B v1: paraphrase 66, wrong section 11, truncation/ellipsis 0, other 1. 2B v1: paraphrase 43, wrong section 44, other 19. 4B v2: paraphrase 49, wrong section 4. Of the 62 failing company/event quotes in 4B v1, 16 contain the literal mask token `[MASKED]`, which the model copied from its input; the verifier compares against unmasked text.
Residual examples (20, random seed 0, 4B v1; class | file | section | quote start) are in `reports/phase_2_diag_4b_v1.json` under `quote_residual_examples`: 17 paraphrase (e.g. "Charmac Trailers Inc. issued recall on September 17, 2015.", "[MASKED] confirmed that the steering wheels were built incorrectly ..."), 3 wrong section (a chronology quote from the cause or defect text).

## 5. V2 and S1
Silver S1 SUPPORTED labels: 58; supplier equals filer/affiliate: 7. V2b rejected 6 4B claims (6 for the 2B) that match a silver label.

## 6. Events: side by side (20 filings, 4B v1)
`reports/phase_2_side_by_side_4b_v1.md` (random sample, seed 0). Typical pattern: dates match, types do not (e.g. every event in one filing typed FILER_AWARENESS or DECISION).
Miss classes vs headline silver events (plus every unmatched prediction), counts of events:

| | matched | type mismatch (date overlaps, other type) | missing (no prediction at that date) | extra (prediction with no headline-event date match; includes events silver types OTHER) | date format (unparseable) |
|---|---|---|---|---|---|
| 4B v1 | 53 | 150 | 54 | 137 | 1 |
| 2B v1 | 69 | 144 | 44 | 179 | 9 |
| 4B v2 | 179 | 44 | 34 | 199 | 12 |

## 7. Filings over 120 s (v1 4B / 2B; v2 4B)
Cost tracks OUTPUT tokens (0.8k-3k at 12-14 tokens/s), not prompt length (0.4-0.7k). **Swap at the time of each call was not recorded: UNVERIFIED.** Swap used before runs: 6.3 GB (4B v1 start), 13.6 GB (2B start), 6.5 GB (4B v2 start), 13.3 GB when last read; macOS resizes swap, total ranged 5-15 GB. Another process (my own PDF analysis script) ran during part of the 2B run.
- 4B v1 (9 filings): 15V036-1855 193 s (570 prompt / 1659 out), 19V811-5724 173 s (505/1224), 20V202-4602 146 s (453/1148), 20E044-6457 131 s (639/1058), 20E065-6078 123 s (683/961), 21E060-9563 206 s (610/1714), 21E026-4426 168 s (685/1427), 22V744-5844 131 s (483/825), 22E081-1945 128 s (625/1081).
- 2B v1 (5): 18V293-6049 137 s (589/1866), 20E041-4869 211 s (388/3079), 17V584-2241 143 s (745/2088), 21E060-9563 126 s (610/1805), 21E026-4426 176 s (685/2481).
- 4B v2: none over 120 s except 21V415-8099 125 s, 19E009-4588 126 s, 16V798-6461 122 s, 18V293-6049 122 s (prompts 0.9-1.2k tokens).
Speed/gates (measured with Claude Code and other apps open): 4B v1 p50/p95 40.4/130.9 s (p95 gate FAIL); 2B v1 53.2/119.9 s including the first call, 53.2/126.1 excluding it (gate passes or fails depending on the convention); 4B v2 40.4/100.2 including, 40.4/114.0 excluding the first call (pass). JSON-valid 100% for all. No model fails both gates, so none is dropped and no other model is pulled. Generation speed 12.4 (4B v1), 14.1 (2B), 16.6 (4B v2) tokens/s.

## 8. Changes applied (each with before -> after, 4B, dev, vs silver; see `docs/PROMPT_LOG.md`)
| change | reason (from sections above) | before -> after |
|---|---|---|
| Prompt v2 rule 6: filer is not a supplier/distributor | 99/105 V2b rejections were correct; 136/203 4B company roles were DISTRIBUTOR | V2b rejections 105 -> 0; unsupported-claim rate 94.5% -> 16.4% |
| Prompt v2 event rules + type definitions (from `LABELING_RULES.md`) | no type definitions in v1; type accuracy 20% | headline F1 0.211 -> 0.647; date+type F1 0.153 -> 0.539; type accuracy 20.4% -> 67.1% |
| Prompt v2 rules 7-8 (mask token, contiguous verbatim quote) | 16/62 failing quotes contain `[MASKED]`; 66 paraphrases | principled quote pass 87.7% -> 91.9% |
| `tt/verify/extra.py` (V1 on masked text, V3 via span parser, V2 not for block supplier); `verifier.py` not edited | V3 false rejects 17/58; V1 mask token; V2 6 false rejects | v1 4B: verifier-pass filings 2 -> 6; v2 4B: 17 -> 26 |
Side effects: cause accuracy 98% -> 95% (4B); S2 recovery unchanged (11/24). v2 numbers are **optimistic by construction**: the type definitions come from the same rules that define the silver labels, v2 was designed after seeing v1 dev results, and the labels are silver. Not evidence of generalisation.
Still failing in v2 (not fixed, not justified yet): V5 path members (45 4B filings-level errors), `locus` SUPPORTED without evidence (32), 12 unparseable date texts, 9 order inconsistencies. The `locus`/`supply_path` fields are not part of the silver claims; Phase 4 should drop or redefine them rather than tune the prompt to pass V5.

## UNVERIFIED
Swap per call; correctness of any silver label; whether v2 generalises; the 2B under the v2 prompt (not run).
