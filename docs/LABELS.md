# Dev silver labels (v1)

**These are silver labels: AI-made, cross-checked by independent AI passes and code checks. No human has verified them.**
They must be called "silver labels" in every report, README and paper table. Scores against them are "vs silver labels".

File: `data/labels/dev_silver_v1.json` (100 dev filings; SHA-256 `d17a30a4c710e1aadb46fb773f2b4759cea49eea3ba5457279ae3441be46f35e`).
Not frozen. Test splits were not used.

## Procedure
1. **Pass A** (`data/labels/passA_v1.json`): code-assisted AI draft (`tt/labels/draft.py`) with per-filing AI corrections from `config/*overrides.json`; rules in `docs/LABELING_RULES.md`.
2. **Pass B** (`data/labels/passB_v1.json`): five independent subagents, each in a fresh directory holding only its 20 filing texts and the rules. Each logged the files it opened (`files_seen.txt`); all ten pass logs (B and C) list only files inside the batch directory (plus the Pass C prompt). Format-only normalisation applied: an empty `section` on an empty quote becomes `any`.
3. **Mechanical comparison** (`tt/labels/agree.py`) of A vs B per claim; 113 disagreement items.
4. **Pass C** (`passC_items_v1.json`, `passC_decisions_v1.json`): five adjudicator subagents saw only the filing text, the rules and both versions per item. Each chooses A, B, NEITHER (with a corrected label) or CONTESTED and quotes the deciding text. Final labels = Pass A with Pass C decisions applied (`tt/labels/protocol.py`).
5. **Code checks** (`tt/labels/schema.py`) on Pass B and on the final labels: quote verbatim in the named section, date inside quote (or inherited entry quote), schema-valid, quote required except NOT_REPORTED/NONE_MENTIONED. 0 failures on both.

CONTESTED items (16) are listed in each record's `contested` field and are excluded from scoring; contested events carry `contested: true`.

## Known weaknesses
- All passes (A, B, C) come from one model family and share its biases; agreement is not independent evidence of correctness.
- Pass C sees A and B labelled "version A / version B" and was told not to favour either by position; this is not verified.
- Event typing is the weakest part: many disagreements are A typing OTHER what B/C typed INVESTIGATION_START, and A/B quoting different sentences of one entry.
- S1 is nearly mechanical (block text), so its agreement is uninformative about difficulty.
