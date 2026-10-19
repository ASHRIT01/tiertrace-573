# Prompt and extraction-pipeline version log

Every change made after looking at dev results is listed here with its reason. All dev-only; Test-A was never opened.
Scores are "vs silver labels" (AI-made, cross-checked by AI passes and code checks; not human-verified).

| version | date | change | seen dev results first? | reason |
|---|---|---|---|---|
| v1 (`SYSTEM`) | written before 2026-10-19 (dev-bench stage) | original system prompt: verbatim quotes, SUPPLIER/SUB_SUPPLIER/DISTRIBUTOR only if named, NR rule, abstain | no | initial design |
| v2 (`SYSTEM_V2`, `--prompt v2`) | 2026-10-19 | adds rule 6 (filer is not a supplier/distributor), 7 ([MASKED] is not a company name), 8 (quote = one contiguous verbatim passage), 9 (one event per sentence, dates copied as written incl. ranges, definitions of the six event types taken from `docs/LABELING_RULES.md`) | **yes**: v1 4B and 2B outputs scored against silver | diagnosis: 99 of 105 (4B) / 82 of 88 (2B) V2 filer-as-supplier rejections were correct; 136 of 203 4B company roles were DISTRIBUTOR (mostly the filer); type accuracy given a matched date was about 20%; the v1 prompt contained no event-type definitions; 16 of 62 failing 4B quotes contain the mask token |

Non-prompt pipeline changes made after seeing dev results (2026-10-19):
- `tt/verify/extra.py` (new layer; `tt/verify/verifier.py` is not edited): quotes checked against the masked text the model saw; V3 uses the span date parser (ranges, month-only, year-less dates are valid); V2 filer-as-supplier not raised for a company equal to the block-reported supplier.
- `tt/eval/devscore.py`: silver-label support (S2 name from `name` field, contested S2 skipped); `tt.labels.protocol.prepare_gold` builds spans, drops contested events.
- Runner: 300 s timeout, truncation flag, `--resume`, progress flush (no change to model inputs).

Tuning rule: changes are justified by the diagnosis, not by maximising any pass rate. Because v2's event-type definitions are copied from the same
rules the silver labels follow, v2 dev scores are optimistic by construction and must not be read as generalisation.
