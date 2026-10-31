# HA-1 protocol: a small human audit of accepted event claims

**Status: fixed before the audit sheet is built.** This protocol, the draw script and the sample IDs are committed and tagged `ha-protocol-1` before the sheet exists. Any later change goes in `reports/HA_AMENDMENTS.md`, with its date and reason, and every result it affects is labelled **POST HOC**.

**Required wording for any result:** "audited by the author, a single non-expert; n = 40".

**Hard rules:**
- No model runs.
- Nothing under `freeze-v1`, `amendment-1`, `ts-protocol-1` or `sc-protocol-1` changes.
- Read-only use of the run outputs, the frozen gate decisions, the silver labels and the parsed text.

## A. Population and sample

**Population:** run-1 event claims accepted by the frozen gate on Test-A: 536 claims in 159 filings. This is the accepted set of H1, rebuilt with the frozen `agent.decide` through the amendment-1 wrapper at its primary settings. `scripts/ha1_draw.py` stops unless the count is exactly 536.

**Draw** (`scripts/ha1_draw.py`), using one generator, `random.Random(7)`, in this order:
1. `rng.sample(frame, 40)`, where the frame is the 159 filing names, sorted.
2. For each drawn filing, in drawn order, `rng.choice` over its accepted claims, sorted by run-1 event index.
3. `rng.sample(range(40), 8)` chooses the repeat items, then `rng.shuffle` sets their order. They become items 41 to 48.

Items 1 to 40 appear in drawn order, which is already random. The draw never reads a silver verdict.

**What the sample represents.** Filings hold between 1 and 17 accepted claims, and each filing contributes one claim. So the 40 items are not a simple random sample of the 536 claims: a claim in a filing with many accepted claims is less likely to be drawn. The primary result estimates "a random accepted claim from a random filing that has at least one". It must not be reported as the accuracy of the 536 claims. Section E gives the only estimate that targets the 536.

## B. What the auditor sees

The auditor (the owner, one person, not a domain expert) sees only:
- the filing ID and the NHTSA PDF URL;
- the claimed date (`date_text`) and the claimed event type;
- the verbatim evidence quote, exactly as run 1 gave it;
- the surrounding chronology text: up to 300 characters on each side of the quote, from the parsed, unmasked chronology, with whitespace collapsed and cuts moved to word boundaries.

The auditor does **not** see the silver label, the agent's status, the B1/B2 outputs or any score.

## C. What the auditor marks

For each item: `DATE_OK` (yes/no/unsure), `TYPE_OK` (yes/no/unsure), `MINUTES`, and an optional `NOTE`. "Correct" means correct as stated in the filing's own text, using the codebook `docs/HA1_CODEBOOK.md`. If the PDF and the parsed text differ, the PDF decides and the difference goes in `NOTE`.

The frozen rules define labels, not audit marks, so these marking instructions are new to HA-1:
- **DATE_OK = yes:** the claimed date is the date the filing gives this event under the frozen date rules (its own date, or the date of its dated entry). Differences of format do not matter.
- **DATE_OK = no:**
  - the date belongs to something else;
  - the date is coarser or finer than the text, or drops a qualifier the rules keep ("March 2020" for "early March 2020");
  - the sentence is undated prose, which has no date under the rules.
- **A year added to a year-less date:** yes if the year is unambiguous under the frozen rule, otherwise unsure.
- **TYPE_OK = no:** the type is wrong, or the sentence is not an event under the rules. Judge DATE_OK separately.
- **Boundary cases:** use unsure when the rules do not settle the type.

**Order of work.** The filled sheet is committed before the answer key is opened. No item is replaced or dropped. An unreachable PDF is judged from the shown text and noted.

## D. Primary and secondary results

A claim is **correct** when `DATE_OK` = yes and `TYPE_OK` = yes. Only items 1 to 40 count towards results; items 41 to 48 are used only for repeat consistency.

- **Primary:** the share of the 40 audited claims that are correct, with a Wilson 95% CI (z = 1.96). Unsure counts as not correct.
- **Sensitivity:** the same, excluding claims with unsure in either mark.
- **Secondary:**
  - The date-only share (`DATE_OK` = yes), with a Wilson 95% CI, where unsure counts as not correct.
  - The human verdict against the silver verdict on the same 40 claims, as a 2x2 table with Cohen's kappa. The silver verdict is the frozen scorer's right/wrong for that claim, at amendment-1 primary settings. The human verdict is the primary one.
  - Repeat consistency over the 8 pairs: exact agreement on `DATE_OK`, on `TYPE_OK`, and on both, reported as x of 8 with no CI.
- **Also reported:** total and median minutes, and the number of unsure marks.

## E. Exploratory: prediction-powered inference over the 536 claims

The predictor is the silver verdict, known for all 536 claims. Because of the one-per-filing design, the correction term is weighted by inverse inclusion probability. This weighting is part of this protocol's specification:

    theta = mean_silver_536 + (F / (536 * 40)) * sum_i n_i * (h_i - s_i)
    SE    = (F / (536 * sqrt(40))) * sd_i( n_i * (h_i - s_i) )
    95% interval: theta +/- 1.96 * SE

- F = 159.
- n_i is the filing's number of accepted claims (`accepted_claims_per_frame_filing` in `reports/ha1/HA1_SAMPLE.json`).
- h_i and s_i are the human and silver verdicts, each 1 if correct and 0 if not.
- sd is the sample standard deviation. Unsure counts as not correct.

Two comparison lines are reported with it:
- the same weighted estimator without silver: `(F / (536 * 40)) * sum_i n_i * h_i`;
- the unweighted form: `mean_silver_536 + mean_i(h_i - s_i)`, labelled as ignoring the design.

**n = 40 is small and the interval may barely shrink.** Weights of up to 17 make the normal approximation rough. This line is exploratory and does not replace the primary result.

## F. Limits declared in advance

- **One non-expert auditor** who is also the author. There is no second reader and no inter-rater figure.
- **The auditor is not fully blind.** They know every item was accepted by the gate, and they know the published aggregate silver error of the accepted set (0.267). They cannot be blinded to either.
- **The repeats are visible as repeats.** Each filing appears once in items 1 to 40 and the repeats come last, so a repeat can be recognised by its filing ID and position. The consistency figure is therefore an upper-leaning check, not a test of independent re-judgement.
- **Silver and human verdicts are not the same test.** The frozen scorer accepts date spans that overlap after widening to the coarser granularity and never matches fuzzy gold dates, while section C compares the date as stated. Disagreements may reflect this and are not automatically silver errors.
- **Silver labels are AI-made.** Agreement with silver is not evidence of truth in either direction.

## G. Inputs (SHA-256)

- `runs/testA_4b_v2_run1.jsonl`: `1979a89b69e45e86362681b17e8a93dbeb8f90a3a6d0be169bdb0fbd806832f8`
- `runs/testA_4b_v2_run2.jsonl`: `a5705ea365dbd19b1258f5e2967ae2843324af8b95e920f45a3ea62821d12ee3`
- `data/labels/testA_silver.json`: `c8b637830c2e46753241cebd33b1043917f8832f03da41238b1d1d9aae180950`
- `runs/testA_cache.pkl`: `5506d2c14cda126178f07746b4cf8e9ec32d0a70a137f0e00fbfbd33e46de928`
- `docs/LABELING_RULES.md`: `39b99cbabe6b8c9c100193837ee81574c3da48efc2ed22319a5684757a510876`

## H. Sample IDs

Seed 7. Event index is the 0-based position in the run-1 `events` list. Full file names are in `reports/ha1/HA1_SAMPLE.json`.

| item | filing | event index | repeat of |
|---|---|---|---|
| HA-01 | 24V631-8870 | 0 |  |
| HA-02 | 23V699-7039 | 2 |  |
| HA-03 | 24V949-7212 | 0 |  |
| HA-04 | 23V217-6513 | 2 |  |
| HA-05 | 23V310-1286 | 0 |  |
| HA-06 | 25V651-2933 | 3 |  |
| HA-07 | 23V405-2388 | 5 |  |
| HA-08 | 24V820-7053 | 2 |  |
| HA-09 | 25V836-1434 | 13 |  |
| HA-10 | 23V238-8204 | 4 |  |
| HA-11 | 25V470-8715 | 4 |  |
| HA-12 | 24E030-1138 | 4 |  |
| HA-13 | 23V123-8136 | 1 |  |
| HA-14 | 23V383-8713 | 10 |  |
| HA-15 | 25V102-4724 | 1 |  |
| HA-16 | 25V027-7244 | 2 |  |
| HA-17 | 23V289-4389 | 6 |  |
| HA-18 | 24V039-2530 | 3 |  |
| HA-19 | 23V396-2407 | 4 |  |
| HA-20 | 25V032-4431 | 3 |  |
| HA-21 | 23V253-4361 | 2 |  |
| HA-22 | 23V558-1590 | 1 |  |
| HA-23 | 24E083-7160 | 0 |  |
| HA-24 | 25V659-2787 | 14 |  |
| HA-25 | 26V062-8099 | 0 |  |
| HA-26 | 26V059-8421 | 0 |  |
| HA-27 | 24E068-9308 | 1 |  |
| HA-28 | 23V186-7351 | 0 |  |
| HA-29 | 23V650-5650 | 2 |  |
| HA-30 | 24V476-9574 | 3 |  |
| HA-31 | 25V744-2593 | 2 |  |
| HA-32 | 23V656-4926 | 0 |  |
| HA-33 | 24V352-8650 | 0 |  |
| HA-34 | 25V640-8730 | 8 |  |
| HA-35 | 24V448-4950 | 0 |  |
| HA-36 | 23V703-2054 | 1 |  |
| HA-37 | 24V438-1492 | 1 |  |
| HA-38 | 25E064-2115 | 3 |  |
| HA-39 | 24V706-2031 | 3 |  |
| HA-40 | 25V702-0345 | 1 |  |
| HA-41 | 24V476-9574 | 3 | HA-30 |
| HA-42 | 24E083-7160 | 0 | HA-23 |
| HA-43 | 23V558-1590 | 1 | HA-22 |
| HA-44 | 23V253-4361 | 2 | HA-21 |
| HA-45 | 24V438-1492 | 1 | HA-37 |
| HA-46 | 23V310-1286 | 0 | HA-05 |
| HA-47 | 23V656-4926 | 0 | HA-32 |
| HA-48 | 23V703-2054 | 1 | HA-36 |
