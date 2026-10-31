# Phase 9: HA-1 small audit of accepted event claims

**Wording for every figure below: audited by the author, a single non-expert, n = 39** (the DATE_OK and TYPE_OK judgements; see Provenance of the marks). The marks are one person's reading of the filing text with the codebook (`docs/HA1_CODEBOOK.md`). They are not a reference standard, and the silver labels they are compared with are AI-made and are not one either.

*Tier: post-freeze protocol `ha-protocol-1` (tag `8a649c2`, commit `06296f3`, fixed before the audit sheet was built). No model run. Nothing frozen changed. Marks committed in `55fdd1a` before the sealed key was opened; the practice-item exclusion is recorded in `reports/HA_AMENDMENTS.md` (`8c24800`).*

## What was audited

- **Population:** the 536 run-1 event claims that the frozen gate accepted on Test-A (159 filings with at least one).
- **Sample:** 40 filings drawn at random (seed 7), one accepted claim per filing, plus 8 of them repeated at the end. HA-01 was a practice item: the AI gave its reading before the author marked it. **It is excluded from every result, so the primary n is 39**, and it has no repeat.
- **What the sample estimates:** it estimates a random accepted claim from a random filing. Filings hold 1 to 17 accepted claims and each contributes one, so it does not estimate the share of the 536 claims that are correct. Section 4 is the only line that targets the 536.
- **Marks:** DATE_OK and TYPE_OK (yes, no, unsure). A claim counts as correct only if both are yes; unsure counts as not correct. **Per-item time was not recorded** (MINUTES is NA for every item), so no time is reported and none is estimated.

## Provenance of the marks

- **(a)** DATE_OK and TYPE_OK were judged by the author. MINUTES was not recorded (NA for every item).
- **(b)** The notes were written by the author; an AI assistant rewrote their wording. They are not used as evidence and are not quoted.
- **(c)** HA-01 was answered by the AI (a practice item, excluded from all results, recorded in `reports/HA_AMENDMENTS.md`). HA-02 was also discussed with the AI assistant: the assistant gave item-specific guiding questions and confirmed the author's reading of the sentence, but did not give the marks. This became known **after** the results were seen, so the sensitivity row without HA-02 (section 5) is POST HOC.
- The marking process was not observed.
- The notes are identical in all 8 repeat pairs. Because an AI assistant rewrote the notes' wording, that observation is uninformative about re-judgement.

## 1. Primary and secondary results (as fixed by the protocol)

| quantity | value | Wilson 95% CI |
|---|---|---|
| **Primary:** claims with DATE_OK = yes and TYPE_OK = yes | 26/39 = 0.667 | [0.510, 0.794] |
| Sensitivity: same, excluding claims with an unsure mark (HA-38) | 26/38 = 0.684 | [0.525, 0.809] |
| Date only (DATE_OK = yes; unsure counts as not correct) | 38/39 = 0.974 | [0.868, 0.995] |

- **Unsure marks:** 1 DATE_OK and 0 TYPE_OK among the 39.
- **Where the shortfall is:** nearly all of it is the type mark. Of the 13 claims not marked correct, 12 have DATE_OK = yes and TYPE_OK = no, and 1 (HA-38) has DATE_OK = unsure and TYPE_OK = no.

## 2. The author's marks against the silver verdict (2x2, same 39 claims)

The silver verdict is the frozen scorer's right/wrong for the claim (amendment-1 primary settings). The marks' verdict is the primary one.

| | silver right | silver wrong |
|---|---|---|
| marks: correct | 23 | 3 |
| marks: not correct | 6 | 7 |

- **Agreement:** 30/39 = 0.769. **Cohen's kappa = 0.449** (point value; the protocol fixed no interval for it).
- **Marks say the claim is wrong, silver says right (6):** HA-02, HA-15, HA-16, HA-27, HA-36, HA-38.
- **Marks say the claim is correct, silver says wrong (3):** HA-22, HA-32, HA-33.
- **Both say wrong (7):** HA-04, HA-12, HA-13, HA-34, HA-35, HA-37, HA-40.
- **All 13 claims the marks do not accept:** HA-02, HA-04, HA-12, HA-13, HA-15, HA-16, HA-27, HA-34, HA-35, HA-36, HA-37, HA-38, HA-40.
- **Direction:** the marks are the stricter reader on this sample. Silver rates 29 of the 39 as right; the marks rate 26.
- **A caveat on what a disagreement means:** the frozen scorer accepts date spans that overlap after widening to the coarser granularity, while the marks compare the date as stated (protocol section F). A disagreement is not automatically a silver error.

## 3. Repeat-item consistency (8 pairs)

HA-41 to HA-48 repeat eight of the audited claims. Exact agreement between the repeat and its original: **DATE_OK 8/8, TYPE_OK 8/8, both 8/8.** No interval is given.
- **Weak evidence:** repeats were recognisable as repeats (protocol section F). This is a check that the marks were entered consistently, not a test of independent re-judgement. The identical notes in the pairs are uninformative about re-judgement (see Provenance of the marks).

## 4. Exploratory: prediction-powered estimate over all 536 accepted claims

Protocol section E, with the silver verdict as the predictor and the correction weighted by each filing's number of accepted claims (F = 159; sample weights 1 to 13). The protocol's 40 is replaced by n = 39 (**POST HOC**: a consequence of excluding HA-01).

| estimate of the share of the 536 claims that are correct | value |
|---|---|
| Silver alone (393/536) | 0.733 |
| **Prediction-powered, weighted** | **0.612, 95% interval [0.452, 0.771]** (SE 0.081) |
| Same weighted estimator without silver | 0.715 |
| Unweighted form with silver (ignores the design) | 0.656 |

**n = 39 is small and the interval did not shrink:** its width is 0.319, against 0.284 for the primary Wilson interval. Weights up to 13 make the normal approximation rough. The four estimates span 0.612 to 0.733, a spread that 39 claims cannot resolve. This line is exploratory and does not replace the primary result.

## 5. POST HOC (not fixed by the protocol before computing)

- **n = 39 and the formula's n:** the exclusion of HA-01 was recorded after the marks were entered and before the key was opened (`8c24800`); the substitution of 39 for 40 in section 4 is the same consequence.
- **Claimed type of the 39 audited claims, by the author's verdict:**

| claimed type | claims | marked correct |
|---|---|---|
| DECISION | 14 | 12 |
| FILER_AWARENESS | 9 | 7 |
| INVESTIGATION_START | 9 | 3 |
| OTHER | 6 | 4 |
| NHTSA_FILING | 1 | 0 |

  Descriptive only. With 1 to 14 claims per type, no rate here is interpretable, and the table was made after seeing the marks.
- **The silver verdict within the sample:** 29/39 = 0.744 right, against 393/536 = 0.733 over the whole accepted set. This only shows the sample is not unusual on silver; no test was run.
- **Sensitivity without HA-02 (n = 38).** HA-02 was discussed with the AI assistant (see Provenance of the marks), which became known after the results were seen. The primary result stays at n = 39; this row does not replace it.

| quantity | n = 39 (primary, as fixed) | n = 38 (POST HOC, HA-02 excluded) |
|---|---|---|
| marked correct | 26/39 = 0.667 [0.510, 0.794] | 26/38 = 0.684 [0.525, 0.809] |
| date only | 38/39 = 0.974 [0.868, 0.995] | 37/38 = 0.974 [0.865, 0.995] |
| agreement with silver (kappa) | 30/39 = 0.769 (0.449) | 30/38 = 0.789 (0.490) |

  **The story does not change.** The correct rate moves by 0.017, the intervals overlap almost completely, and the date-only share is 0.974 in both. HA-02 was one of the six claims the marks rejected and silver accepted, so removing it lifts the agreement slightly. The n = 38 figure 26/38 equals the unsure-excluded figure in section 1 by coincidence: they come from different exclusions. The sensitivity was derived from the committed results only (`scripts/ha1_sensitivity_ha02.py`).

Everything else above was fixed in `reports/HA_PROTOCOL.md` before the sheet existed.

## 6. Limits

- **One rater, not an expert, who is also the author.** There is no second reader and no inter-rater figure. The marking process was not observed, and the provenance of the marks is as stated in Provenance of the marks: an AI assistant rewrote the notes' wording, HA-01 was answered by the AI, and HA-02 was discussed with it.
- **Small n:** 39 claims, one per filing. The intervals are wide: the primary interval spans 0.28.
- **Not blind:** the author knew every item had passed the gate and knew the published silver error of the accepted set (0.267).
- **Silver comparison:** silver labels are AI-made, one model family, and Pass C sided mostly with Pass B (`docs/AMENDMENT_1.md`). Agreement or disagreement with silver is not evidence of which is right.
- **Estimand:** a random accepted claim from a random filing, not the 536 claims.
- **Per-item time not recorded.**
- **HA-01 excluded** as a practice item; **HA-02 discussed** with the AI assistant (POST HOC sensitivity in section 5).
- **Scope:** this is Test-A, one agent, one set of frozen prompts. Nothing here says anything about a named company; suppliers and filers appear in the audit only as parts of the filing text.
- **Nothing is changed in the frozen result.** H1 and its silver-based error stay as committed.
