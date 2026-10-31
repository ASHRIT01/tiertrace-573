# AL-1 amendments to the protocol (tag `al1-protocol-1`)

Every change after the tag `al1-protocol-1` is listed here, with its date and reason. `reports/AL1_PROTOCOL.md` is not edited; where they differ, this file takes precedence.

## Amendment 1 (2026-10-31): global matching, evidence independence, date tags, ablation reporting

**No AL-1 outcome has been seen.** When this amendment was written and tagged (`al1-amendment-1`):
- the agent had not been run on any AL-1 filing, and `runs/al1/` did not exist;
- no lineage class, pair, label draw, ablation or timeliness result existed;
- no AL-1 chronology had been opened, parsed or compared. What had been read from the AL-1 PDFs is the listing metadata, the first bytes, the Submission Date line of page 1, and file hashes;
- the matcher had been run only on made-up version pairs.

This statement covers what the repository and these AI sessions hold. The owner made the decision to amend, and it was not based on any AL-1 result.

**Reason.** A check of the tagged protocol found that it lacked these design rules, which the owner wants preregistered.

| Rule | In the tagged protocol? | Closest section |
|---|---|---|
| (a) Global optimal one-to-one assignment, against a greedy baseline | No. F rule 5 is greedy, there is no combined cost, and the only hard limits are the theta and N thresholds | F, G |
| (b) Evidence independence, with and without | No. F rule 9 uses verbatim text to detect extraction misses, not to discount support | F |
| (c) Every lineage date tagged stated or inferred | No | D, F |
| (d) Ablation effects reported with intervals; no claimed improvement without support; simpler variant reported | No. J reports baselines with "no significance test" and has no ablations | J |

**How this relates to section M.** Section M says a result is POST HOC if it depends on anything decided after the tag. Read literally, that covers this amendment. The amendment does not remove that rule or hide the change:
- Results under this amendment are labelled **"pre-specified under al1-amendment-1 (amended after al1-protocol-1, before any outcome existed)"**, not plain "pre-specified".
- The tagged protocol's own matcher stays in the analysis as baseline G4, unchanged, and is reported beside the primary result on the same items.
- Section M applies in full to any change after `al1-amendment-1`.

**Unchanged:** the analysis sets (248 and 228), extraction and the frozen gate, theta = 0.6, N = 30, the five labels, the number of labelled items (72 + 8), the quotas, the seed, the endpoints in J and K except as stated here, and the wording rules.

### A1.1 Primary matcher: global assignment (replaces F rules 4 and 5)

`match_global` in `scripts/al1_lib.py` picks the one-to-one assignment with the lowest total cost, over each version and the next, using the Hungarian algorithm.

**Hard contradiction constraints.** A pair can never match if any of these holds:
1. quote-token overlap is below theta (0.6);
2. date distance is above N (30 calendar days);
3. both quotes cite recall numbers (`\d{2}[VECT]-?\d{3}`) and they have none in common.

**Cost of an allowed pair:**

    cost = 0.60 * (1 - overlap) + 0.15 * (types differ) + 0.25 * (date distance / N)

Each event may stay unmatched at a cost of 0.5. An allowed pair costs at most 0.64, less than leaving both events unmatched (1.0). Exact ties prefer closer list positions (1e-9 × position difference). **These weights are a judgement fixed without seeing any AL-1 event, not tuned.** A type difference does not forbid a match, since TYPE_CHANGE must stay possible. F's tokens, overlap, date distance, class rules and rule 9 are unchanged.

The label draw (section I) is stratified by the predicted class of `match_global`. Baselines and ablations are scored on those same items.

### A1.2 New baseline G4: greedy nearest match

`match_versions`, exactly as tagged in `al1-protocol-1` (F rules 1 to 9). It is the protocol's pre-specified result under its original matcher.

### A1.3 Evidence independence

A quote copied verbatim from an earlier version is the same evidence, not independent support (`tag_evidence`, `chain_support`).

- **Copied:** ignoring case, spaces and punctuation, the later quote stands in the earlier version's chronology or equals the earlier quote, or the pair is text-carried. An event in one version only has nothing to compare and is not copied.
- **Chains.** A chain follows one event through successive matched pairs. It reports `versions` (versions claiming it) and `independent` (`versions` minus its copied links), with and without the rule.
- **Endpoint.** The rule does not change any predicted class. Each copied pair gets `evidence_weight` = 1/m, where m is the number of copied pairs in its chain, so m copies count once. The J endpoint keeps its stated estimator (without the rule). The same estimator with these weights multiplied in is reported beside it (with the rule), along with the effect (A1.5).
- **Descriptive results.** Section H's counts are also reported both ways, for the share of events supported by two or more versions and by two or more independent pieces of evidence.
- **The frozen gate is not changed.** This rule applies only to lineage results.

### A1.4 Stated or inferred dates

Every lineage date carries a tag (`date_tag`).

- **stated:** the `date_text` stands in that version's chronology (ignoring case, spaces and punctuation), and `ts_lib.resolve` read it without borrowing a year from context, choosing between ambiguous readings, or capping it at the filing date.
- **inferred:** anything else, including a date the text does not hold.
- **Pair tag** (`pair_date_tag`): stated only if every event in the pair is tagged stated.

Section H reports class counts by tag. For DATE_CORRECTION, the shift distribution is reported for all pairs and for stated-only pairs. The author's sheet does not show the tag.

### A1.5 Ablations and how they are reported

Each is compared with the full matcher on the same labelled items, using the J weighted endpoint and the author's labels, on the primary set and again on the sensitivity set.

| Ablation | What is removed |
|---|---|
| A1 | Global assignment: greedy baseline G4 |
| A2 | Recall-number constraint (`recall_constraint=False`) |
| A3 | Type term in the cost (`w_type=0`) |
| A4 | Date term in the cost (`w_date=0`; N stays a hard limit) |
| A5 | Text guard, F rule 9 (`text_guard=False`) |
| A6 | Evidence rule: the estimator without it against the same estimator with it (A1.3) |
| A7 | Inferred dates: stated-only items against all items |

A variant's class for an item is the class of its row holding the same earlier event, else the same later event (`predict_for_item`).

**Reporting rule (`ablation_effect`):**
1. **Every ablation's effect on the primary endpoint** (full minus variant) is reported with a 95% interval: stratified bootstrap by predicted class, 2,000 resamples, seed 0. All are reported, whatever they show.
2. **No improvement is claimed unless the interval supports it.** The full version is called better only if the lower end is above 0.
3. **The simpler variant is reported if it works as well.** If the interval includes 0, the result is stated as "no supported difference", the simpler variant is named as working as well on this sample, and no benefit is claimed for the removed part. If the upper end is below 0, the variant is reported as better.
4. **No selection.** The primary matcher stays `match_global` whatever the ablations show. Adopting a variant would be a POST HOC change.

This replaces J's line "No significance test" for ablations. It still applies to baselines 1 to 3.

**Limits.**
- n = 72 is small, so most intervals are likely to include 0. That means "no supported difference", not "no difference".
- Items were drawn from the full matcher's classes, so a comparison on them may favour the full matcher. This is stated with the results.
- A1.3's chains and A7's subset may leave few items, and the item counts are reported.

### A1.6 Tests and files

`scripts/al1_lib.py` adds the functions above and keeps `match_versions`'s results as tagged. `tests/test_al1_matcher.py` adds tests on made-up version pairs only, including a brute-force check of the assignment and a case where global matching beats greedy.
