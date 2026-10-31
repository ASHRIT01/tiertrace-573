# AL-1 protocol: amendment lineage of dated chronology events

**Status: fixed before any AL-1 filing is run through the agent and before any lineage result exists.** This protocol is committed and tagged `al1-protocol-1`. Any later change goes in `reports/AL1_AMENDMENTS.md`, with its date and reason, and every result it affects is labelled **POST HOC** (section M).

**Hard rules:**
- Nothing under `freeze-v1`, `amendment-1`, `ts-protocol-1`, `sc-protocol-1` or `ha-protocol-1` changes.
- Every event comes from the frozen agent and is AI-extracted, not human-verified.
- Aggregates only in output tables: no company names or recall numbers. Per-filing files stay in gitignored `runs/al1/`. Section B's lists and the author's sheet are the exceptions.

## A. Question

How do dated chronology events change between successive versions of one Part 573 filing, and how much does using the wrong version distort the TS-1 timeliness screen?

"Wrong version" means only "a different version from the one the analysis should use". It does not mean any filing is wrong.

## B. Analysis sets

Source of all campaign sets: `reports/al1/AL1_ORDER.json`, SHA-256 `29e181b5b064bf1cde6844b46377faf530b9462430ea79f98d839c1fce434f17`.

| Set | Rule | Campaigns | Documents | Successive pairs |
|---|---|---:|---:|---:|
| Ordered | `order_status` is `ORDERED` | 249 | | |
| **Primary** | Ordered minus `24V528`, whose latest listed document is NON_PDF | **248** | **712** | **464** |
| **Sensitivity** | Primary minus sets (a) and (b) below; a rerun of the primary analysis | **228** | 636 | |

**The 51 `ORDER_AMBIGUOUS` campaigns are reported as counts only.** They are not run through the agent and are in neither set.

**(a) Only the load timestamp separates versions (16).** Ordered campaigns where at least two usable versions share a Submission Date (`same_date_broken_by_load`):

20V016, 20V322, 21V155, 22E052, 22V307, 22V523, 23V380, 23V707, 23V797, 24V459, 24V661, 24V712, 24V833, 26E023, 26V519, 26V546

**(b) Submission Date order and load order disagree (12).** Campaigns where a version with a strictly earlier load timestamp has a strictly later Submission Date (`date_order_differs_from_load`):

- In the primary set, so dropped by the sensitivity rerun (8): 21V758, 21V841, 24V459, 24V661, 24V833, 25V080, 25V375, 26V546
- `ORDER_AMBIGUOUS`, so already outside the primary set (4): 20V059, 20V396, 21V189, 21V782

**Arithmetic.** Sets (a) and (b) share 4 primary campaigns (24V459, 24V661, 24V833, 26V546), so the rerun drops 16 + 8 - 4 = 20 distinct campaigns: 248 - 20 = 228. `24V528` is in neither set.

**Limit on "original".** The earliest version is the earliest one the NHTSA listing holds. `ORIGINAL_MISSING` is 0 in the 300, but the listing may not hold every version filed.

## C. Data handling

- **Case-colliding URLs.** `21V174`, `21V187` and `22V173` each list PDF URLs differing only in filename case. Any later all-versions fetch must store them as separate files on a case-insensitive disk. `22V173` is already handled in `~/tiertrace_al1_cache`; the other two are not in the current sample.
- **No OCR.** No OCR is run on the 4 no-text-layer PDFs (`22V173`, `25V063`, `25V680`, `26V219`). All 4 campaigns are `ORDER_AMBIGUOUS`, so they are outside both analysis sets.
- **PDFs.** Read-only from `~/tiertrace_al1_cache`; manifest `al1_manifest.json`, SHA-256 `000b497cb6c54457e5e034b6703ca49c921f798ad9430a06158d459599947511`. No PDF is committed.

## D. Extraction

**Model and settings: the frozen v1 agent and gate, exactly as in `freeze-v1`.** `config/run_settings.json` (SHA-256 `7a13cd4a37e391d672c1ad8c071d03cde0bdf62c30e8c50a4c4a00328f0edbb9`): model `qwen3.5:4b-q4_K_M`, prompt v2, thinking off, `num_ctx` 6144, 300 s timeout. Before the run, the model digest is checked against the frozen `d8b0f5e9760c...`; a mismatch stops the run.

Each of the 712 documents is extracted separately, with no knowledge of its other versions.

**Run 1 supplies the claims; run 2 is also required.** The claims come from run 1 (temperature 0, seed 0). But the frozen gate accepts a claim only if no verifier fires and run 2 agrees (score >= 3, as in `scripts/ts_gate.py`), so run-1 settings alone cannot produce gate decisions. Each document therefore also gets run 2 (temperature 0.5, seed 1), used only as the gate's agreement filter. The gate goes through the amendment-1 wrapper, as in `ts_gate.py`.

**Events used.** Run-1 events accepted by the gate. Dates are re-parsed from `date_text` by `ts_lib.resolve` against that version's own Submission Date, following TS-1 section D. An event with no resolvable date is left out of matching and counted.

**Compute estimate on the M2.** Seconds per document are measured from the frozen runs on the 397 filings of Test-A, Test-B and unseen.

| | Seconds per document | 712 documents |
|---|---:|---:|
| Run 1, weighted mean over the three splits | 61.4 | 12.1 h |
| Run 2, weighted mean | 56.3 | 11.1 h |
| **Both runs (estimate)** | **117.7** | **23.3 h** |
| Fastest split's means (unseen) | 63.0 | 12.5 h |
| Slowest run means (Test-B run 1 + Test-A run 2) | 171.0 | 33.8 h |

**How it runs.** In the background under `caffeinate -i`, resumable like `scripts/phase6_run.py`: one JSONL record per document in `runs/al1/`, finished documents skipped on restart, and each start and restart logged. The runner prints only progress and timing. A timeout is recorded and not retried; one retry is allowed after a runner crash, as in Test-A run 2. A document with no run-1 extraction leaves its pairs uncomputed; a missing run 2 counts as "run 2 does not agree". Both counts are reported. The user is told before the run starts, so it does not collide with their memory measurements.

## E. Lineage labels

`NEW`, `UNCHANGED`, `DATE_CORRECTION`, `TYPE_CHANGE`, `RETRACTED`, defined in `docs/AL1_CODEBOOK.md`.

## F. Matcher

Implemented in `scripts/al1_lib.py`, `match_versions`. Deterministic. It compares each version with the **next** version only.

**Parameters, fixed now:** **theta = 0.6, N = 30 calendar days.**

**Why fixed now, with no DEV set.** A DEV subset would have to come out of the 248 and so change the fixed primary set, and tuning on it would need labels that do not exist. These values are therefore a judgement made without seeing any AL-1 event: more than half of the content words shared; a date moved by up to about a month. **There are no DEV IDs, and all 248 are evaluation campaigns.** Section H's grid shows how much the choice matters, and no value is selected from it.

**Rules:**
1. **Tokens.** Lower-case alphanumeric tokens of the evidence quote, as a set, without the fixed stop-word list, month names or numbers of 1 to 4 digits. So a changed date inside a quote does not lower the score.
2. **Overlap.** |A ∩ B| / min(|A|, |B|). If either side has fewer than 3 tokens, it is 1 for identical sets and 0 otherwise.
3. **Date distance.** Calendar days between the [lo, hi] intervals; 0 if they overlap.
4. **Candidates.** Event pairs with overlap >= theta and distance <= N.
5. **Alignment.** One-to-one and greedy: highest overlap, then smallest distance, then earliest positions.
6. **Class of a matched pair.** Different interval: DATE_CORRECTION (with `type_also_changed` if the type differs too). Same interval, different type: TYPE_CHANGE. Otherwise UNCHANGED.
7. **Unmatched earlier event.** RETRACTED, unless rule 9 applies.
8. **Unmatched later event.** NEW, unless rule 9 applies.
9. **Text guard (extraction misses).** The extractor can miss in one version an event it found in the other, which would look like a change. If an unmatched event's quote stands verbatim in the other version's chronology (ignoring case, spaces and punctuation), it is UNCHANGED with `text_carried` = true. The guard does not apply if that event had a same-quote claim beyond the date window; those stay RETRACTED and NEW.

**Known limits.** A date moved by more than N days reads as RETRACTED plus NEW. An event carried by rule 9 has its later date unchecked. The results report `text_carried` counts separately.

## G. Baselines

All in `scripts/al1_lib.py`, scored on the same labelled items as the matcher. A NO_PREDICTION counts as disagreement.

1. **Earliest-version-only** (`single_version_predict`, with that version's events). One version shows no change, so it can only say UNCHANGED, for an event it contains (same theta and N), and otherwise gives NO_PREDICTION.
2. **Latest-version-only.** The same, with the latest version's events.
3. **Text-diff + date rule, no event extraction** (`textdiff_classify`, `textdiff_predict`). Chronology text is split into lines and sentences. The first date in each segment comes from a regex and is read by `ts_lib.resolve`. The matcher's overlap and date rules then apply. It has no types, so it can never say TYPE_CHANGE. A pair takes the class of the segment that best matches its quote at overlap >= theta.

Baselines 1 and 2 agree with the author only where the author says UNCHANGED, by construction. They set a floor; they are not rival systems.

## H. Descriptive results (no human labels)

All AI-extracted, not human-verified, and labelled so:
- Class counts and shares over all pairs, per filing and per successive pair, with `text_carried` shown separately.
- The share of campaigns with at least one pair of each class.
- For DATE_CORRECTION: median, IQR and maximum shift in calendar days.
- Run failures, undated events and accepted-claim counts per version.
- **Parameter grid:** class shares at theta in {0.5, 0.8} and at N in {7, 90, 365}, changing one at a time. Descriptive only. No value is selected.
- All of the above again on the sensitivity set.

## I. Human labels

**Who.** The author, a single non-expert. There is no second reader and no inter-rater figure.

**Items.** **n = 72 cross-version pairs from the 248 evaluation campaigns, plus 8 hidden repeats, so 80 rows.**

**Why 72.** It lies in the suggested 60-80 range and a single person can finish it. At 80% agreement, the overall Wilson interval at n = 72 is 0.700 to 0.880. A class of 14 gives 0.524 to 0.924 at about 79%, which is wide, so per-class results are rough. Every quota is at least 10, the minimum for an F1 (section J).

**Draw** (`draw_items`, seed 0), stratified by the matcher's predicted class at theta = 0.6, N = 30, using `random.Random(0)` in the order written there.

| Predicted class | Quota |
|---|---:|
| DATE_CORRECTION | 16 |
| TYPE_CHANGE | 14 |
| RETRACTED | 14 |
| NEW | 14 |
| UNCHANGED | 14 |
| **Total** | **72** |

- A class short of its quota contributes all its pairs, and the shortfall goes to the class with the most undrawn pairs.
- The inclusion probability (drawn / population, by class) is recorded in `reports/al1/AL1_LABEL_DRAW.json` before the sheet is built.
- 8 of the 72 are repeated and all 80 rows are shuffled together, so repeats do not sit at the end.
- Text-carried pairs stay in the UNCHANGED stratum. Rare classes are deliberately oversampled, which section J corrects for.

**What the author sees.** Item number; the two versions' file IDs and NHTSA URLs; for each side the date text, type and quote; and up to 300 characters of chronology around it in **both** versions. A one-sided pair shows the other version's chronology with no claim. The author does not see the predicted class, baselines, scores or stratum. A one-sided pair may still hint at NEW or RETRACTED; this cannot be hidden.

**Marks.** A plain-text file, `audit/AL1_marks.txt`, as in HA-1. Allowed labels: the five classes, NOT_SAME_EVENT, UNSURE.

```
AL-01 | LABEL=DATE_CORRECTION | MINUTES=NA | NOTE=
```

- The marks file is committed before the answer key is opened. No item is replaced.
- **The AI must not discuss individual items.** Any item discussed with an AI before it is marked, or whose reading came from an AI, is **excluded** from all results and logged in the amendments file.
- **Notes are optional.** If an AI rewords a note, that is recorded.
- **Time per item** is recorded only if measured; otherwise "not recorded".

## J. Primary endpoint

**Agreement of the matcher's class with the author's label**, on first-instance items.

**Scoring.** NOT_SAME_EVENT and UNSURE count as disagreement. A sensitivity excludes them.

**Reported:**
- **Per predicted class:** k/n with a Wilson 95% interval (z = 1.96). This is the matcher's precision for that class.
- **Per-class counts:** the full table of predicted class against author label.
- **Overall, unweighted:** k/n with a Wilson 95% interval, labelled "as sampled, rare classes oversampled".
- **Overall, weighted:** a Horvitz-Thompson estimate using the inclusion probabilities (`weighted_agreement`), with a stratified bootstrap 95% interval (2,000 resamples, seed 0). This estimates agreement over all matcher pairs.
- **F1 only for classes with >= 10 labelled pairs**, counted by the author's label, computed with the same weights. Otherwise "not computed, n < 10".
- **Repeat consistency:** exact label agreement over the 8 pairs, as x of 8, with no interval.
- **Baselines:** the same tables on the same items. No significance test.
- **Sensitivity set:** all of the above restricted to items from the 228. Items are not redrawn, and the result is labelled as a subset.

Pairs from one campaign are not independent, so Wilson intervals may be too narrow. The number of campaigns contributing items is reported.

## K. Secondary endpoint

**Of TS-1 timeliness flags, the share that change when the original version (or RCDATE) is used instead of the latest submission.**

**These are not the published TS-1 flags.** Those 397 filings are dev and test IDs, excluded from AL-1, and only one version of each is cached. This endpoint applies the frozen TS-1 rule to the AL-1 primary set.

**Rule.** TS-1 sections B to G from `scripts/ts_lib.py` (SHA-256 `4e8878825c12a03ccf8ceb2caf2a7a45cf0bd0b713bdb765350371af0862e89b`, holiday table `cb00b3ac48d335e16abbfea456985153a396b4f353dd2bfcf8ad920b47d0df81`), including the TS-A1 guard: agent anchor from gate-accepted claims, FLAGGED, NOT_FLAGGED, INDETERMINATE or NO_DECISION_DATE. **Defect filings only**, typed by TS-1 section G.

| Screen | Events from | Filing date |
|---|---|---|
| **L (reference)** | Latest version | Latest version's Submission Date |
| **O** | Earliest listed version | Earliest listed version's Submission Date |
| **R** | Latest version | Flat-file RCDATE |

**Reported:**
- **Primary figure:** of campaigns FLAGGED under L, the share with a different status under O, and separately under R. Each with a Wilson 95% interval and a filer-cluster bootstrap interval (`tt.eval.riskcov.cluster_bootstrap`, 2,000 resamples, seed 0).
- The same change share over all defect filings, with the full 4 × 4 status tables L vs O and L vs R.
- All of it again on the sensitivity set.

**Instability note.** TS-1's agent had an accepted, dated DECISION claim for only 127 of 305 defect filings, so FLAGGED counts here may be small. If fewer than 10 campaigns are FLAGGED under L, the report says the estimate is unstable. No threshold or pool is changed to raise the count.

## L. Wording rules

- **Labels:** "labelled by the author, a single non-expert; n = [number of items counted]".
- **Silver labels:** "AI-made, not human-verified". This analysis uses no new silver labels; the same words apply to agent output and to any silver label cited.
- **No company is called late or at fault.** The words are "FLAGGED", "NOT_FLAGGED", "INDETERMINATE" and "screening signal", as in TS-1. A change between versions is not an admission or an error. A supplier is "named in the filing", never "responsible" or "caused".
- **Class names describe change only.** DATE_CORRECTION does not say the earlier date was wrong, and RETRACTED does not say the filer withdrew anything on purpose.
- **Any novelty sentence** has the form "we found no prior work that ... (search scope: ...)", with the scope taken from `reports/AL1_PRIOR_ART.md` section 4 and naming Astvansh, Ball & Josefy (2022) as the closest prior dataset. That report's closest-method note on NewsEdits 2.0 stays with it. No claim of a new method is made.

## M. Post hoc and deviations

**A result is POST HOC if it depends on anything decided after the tag `al1-protocol-1`**, including:
- any change to the sets, models, settings, gate, parameters, matcher rules, baselines, draw or endpoints;
- any code fix after real AL-1 output has been seen, even a bug fix (the matcher has been tested on synthetic pairs only, so this may happen);
- any analysis not listed here, or any grid value promoted to primary.

**Rule.** Every deviation goes in `reports/AL1_AMENDMENTS.md` at the time it happens, with its date, reason and affected results. The affected results are labelled POST HOC wherever they appear, with the pre-specified result next to them where it can still be computed. Results are reported whatever they show. A pre-specified analysis that cannot run is listed as "not run", with the reason.

## N. Limits declared in advance

- **Extraction noise can look like change.** Each version gets its own model call, and the gate rejects many claims. Rule 9 catches only verbatim carry-overs, so NEW and RETRACTED may be inflated. That is why the human check oversamples them.
- **No event ground truth.** The author is one non-expert who is also the study's author.
- **The sample excludes dev and test IDs**, so it is not a random sample of all campaigns.
- **Only campaigns with knowable order are in the set**: multi-version campaigns with at least 2 load days and resolved order.
- **Prior art is a limited web search** (`reports/AL1_PRIOR_ART.md`).

## O. Files

- `scripts/al1_lib.py`, `tests/test_al1_matcher.py` (synthetic pairs only).
- `docs/AL1_CODEBOOK.md`, `reports/AL1_PRIOR_ART.md`, `reports/AL1_INVENTORY.md`.
- Written at execution: the extraction runner and analysis script, `reports/al1/AL1_LABEL_DRAW.json`, `audit/AL1_sheet.*`, `audit/AL1_marks.txt`, `audit/sealed/AL1_answer_key.json`, `reports/AL1_RESULTS.md`, `reports/AL1_AMENDMENTS.md`.
