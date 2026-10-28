# SC-1 protocol: supplier claims checked against the filer's own declaration

**Status: fixed before any claim is compared with the reference.** This protocol is committed and tagged `sc-protocol-1` before any comparison. Any later change goes in `reports/SC_AMENDMENTS.md`, with its date and reason, and every result it affects is labelled **POST HOC**.

**Reference:** the filer-declared supplier/component (non-AI, not ground truth).

**Hard rules:**
- No model runs.
- Nothing under `freeze-v1`, `amendment-1` or `ts-protocol-1` changes.
- Read-only use of the run outputs, the frozen gate decisions, the silver labels, the parsed text and the NHTSA flat file.
- From the supplier block, keep only company names, supplier type and country. Phone numbers and street addresses are never stored or printed.
- Aggregate tables only, with no per-filer rows.

Inputs are described in `reports/SC_INVENTORY.md` (commit c27b962).

## A. Legal basis and what a match means

Quoted verbatim from the eCFR, 49 CFR § 573.6(c)(2)(iv), as of 2026-10-23 (fetched with the eCFR versioner API on 2026-10-28):

> "In the case of motor vehicles or items of motor vehicle equipment in which the component that contains the defect or noncompliance was manufactured by a different manufacturer from the reporting manufacturer, the reporting manufacturer shall identify the component and, if known, the component's country of origin (i.e. final place of manufacture or assembly), the manufacturer and/or assembler of the component by name, business address, and business telephone number. If the reporting manufacturer does not know the identity of the manufacturer of the component, it shall identify the entity from which it was obtained. If at the time of submission of the initial report, the reporting manufacturer does not know the country of origin of the component, the manufacturer shall ascertain the country of origin and submit a supplemental report with that information once it becomes available."

**What the declared supplier can be.** It may be a tier-1 assembler, a distributor or importer (the entity "from which it was obtained"), or the OEM itself. **A match therefore measures fidelity to the filer's declaration, not who really made the part.** A non-match is never described as an error by the filer; it is a "non-match".

**What a match is evidence of** (Step 0, item 6):
- **The agent never saw the block.** Its frozen input is the cause and chronology only, and the frozen block name is masked as `[MASKED]` wherever it occurs.
- **Agent matches:** an agent claim that matches the declared supplier comes from a narrative mention that the mask did not cover, such as a different spelling, the filer's own name, or a multi-supplier block that the frozen parser joined into one string.
- **Silver S1 matches are circular:** S1 is read from the block itself, so it matches by construction. Silver S2 claims come from the narrative.

## B. Name normalisation and matching

**Primary normalisation (no alias list),** `norm_name` in `scripts/sc_lib.py`:
1. Lowercase and strip accents (Unicode NFKD, combining marks removed).
2. Strip punctuation. Apostrophes and periods are deleted ("Q'Straint" → qstraint, "S.A." → sa), and every other non-alphanumeric character becomes a space ("DISTRIBUTION,CORP" → distribution corp).
3. Remove the phrase "s a de c v".
4. Remove the legal-form tokens {inc, incorporated, llc, ltd, limited, co, company, corp, corporation, plc, gmbh, ag, sa, sas, spa, srl, bv, nv, kk, oy, ab, as, sl, pty, pvt, private, de, cv, the}.
5. Collapse spaces.

**Matching rules:**
- **MATCH (primary):** the normalised strings are equal and not empty.
- **Containment (secondary, pre-declared):** one name's token set is a subset of the other's, and the shared tokens number ≥ 2 or are a single token of ≥ 5 characters.
- **Fuzzy (sensitivity only):** `token_set_ratio` ≥ 90 on the normalised strings. `rapidfuzz` is not installed and no package is added, so `scripts/sc_lib.py` reimplements rapidfuzz 3.x `fuzz.token_set_ratio` in pure Python. It is unit-tested against known rapidfuzz values.

**Aliases:** any alias list made after seeing results is POST HOC only.

## C. Units and metrics (supplier claims)

**Population:** filings in the NAMED_SUPPLIER and MULTIPLE strata (Step 0). Each filing's **declared set** is every declared name in its block except pointers. Filings in the other strata (OEM_SELF, OBTAINED_FROM, BLANK, PARSE_FAIL) are reported only as counts of claims, not as errors.

**OEM_SELF:**
- **Primary:** the single declared name normalises to a filer name, either a flat-file MFGNAME of the campaign or the PDF header "Manufacturer Name".
- **Why not the instruction's rule:** the instruction also counted Supplier Type "OEM". Step 0 showed that "OEM" is a supplier type in the portal form, and 52 of 65 OEM-typed names are not the filer.
- **Sensitivity:** the literal rule (type "OEM" also counts as OEM_SELF) re-runs C(a)–C(b) on its own NAMED_SUPPLIER and MULTIPLE strata.

**Agent supplier claims:** run-1 companies with role SUPPLIER, SUB_SUPPLIER or DISTRIBUTOR and status SUPPORTED (frozen `agent.supplier_claims`).
- **All:** every such claim.
- **Gate-accepted:** frozen `agent.decide` kind S2 with score ≥ 3, extracted read-only by `scripts/sc_gate.py`. On Test-A the 4 run-2 timeouts mean no claim from those filings is accepted, exactly as in H1.

**Silver supplier claims:** S1 and S2 with status SUPPORTED. The name is the text of the `label` after the first ": ".

**Metrics:**
- **(a) Filing-level recall:** the share of population filings whose declared set is matched by ≥ 1 agent supplier claim. Computed for all claims and for gate-accepted claims only.
- **(b) Claim-level precision:** the share of agent supplier claims in population filings that match any declared name, for all claims and for accepted claims. **Precision understates:** a correct sub-supplier that is named only in the chronology, not in the block, counts as a non-match.
- **(c) Silver:** the same (a) and (b) for the silver labels, all claims (silver has no gate). This is the first non-AI check of the silver supplier labels.
- **(d) Agent vs silver:** per population filing, a 2×2 table of agent matches (yes/no) against silver matches (yes/no), for agent-all and agent-accepted. The off-diagonal cells are the disagreements, split by which side matches the reference. It is shown with silver = S1 + S2 and with silver = S2 only.

**Intervals:**
- Wilson 95% CI and a filer-cluster bootstrap 95% CI, using the frozen `tt.eval.riskcov.cluster_bootstrap` (2,000 resamples, seed 0). Clusters are filer names, lower-cased with whitespace collapsed.
- Recall resamples filings; precision resamples claims by their filing's cluster.
- Any cell with n < 20 is labelled **unstable**.

**Levels:** primary = exact MATCH. The containment and fuzzy levels repeat C(a)–(c) as sensitivity tables.

## D. Circularity: where the evidence lies

**Locating each claim:**
- **Block span:** the [start, end) character span of the supplier block in the frozen cleaned text (`supplier_blocks`, Step 0).
- **Quote location:** each claim's quote is found with `locate_quote`, which is whitespace-insensitive and lets `[MASKED]` match a short run.
- **Labels:** a claim is **in-block** if its located span lies inside a block span, **out-of-block** if it is located elsewhere, and **not located** otherwise.

**Reporting:**
- Metrics (a), (b) and (c) are reported separately for in-block and out-of-block evidence.
- For recall, a filing counts as recalled in-block (or out-of-block) if a matching claim with that kind of evidence exists.
- For precision, claims are partitioned by evidence location.
- **The out-of-block matches are the informative ones.** Step 0 showed that agent quotes cannot come from the block, and that silver S1 quotes are taken from it.

## E. Components

**Not run.** The reference exists: Involved Components records (a name or part number) in 390 of 397 filings, and flat-file MFR_COMP_NAME in 392 of 397. But **neither the frozen agent schema nor the silver labels contain any component claim** (Step 0 item 5), so nothing can be compared.

The matching rule is recorded here for any later use:
- an agent component claim matches if its normalised text equals or contains the PDF component name;
- or its part number, after stripping spaces and dashes, equals a declared part number;
- or it equals or contains a flat-file MFR_COMP_NAME value.

The fuzzy sensitivity would use token_set_ratio ≥ 90. Results are reported as "not run (no component claims)".

## F. Stratification and reporting

- **Strata:** every metric in C is stratified by split (Test-A, Test-B, unseen-filer, pooled), by layout (portal, older), and by RCLTYPECD (V, E).
- **Instability:** cells with n < 20 are labelled unstable.
- **Completeness:** results are reported whatever they show.
- **Tables:** aggregates only, with no per-filer rows. Supplier names appear only in the Step 0 examples, never in result tables.

## G. Prior art and wording

- **The reference** is the filer's declaration under 49 CFR 573.6(c)(2)(iv).
- **The OIG figure, as context only.** The owner reports that the DOT Office of Inspector General (2018) found this information missing in 16.2% (±8.5%) of 2012–2016 initial reports. Two web searches on 2026-10-29 did not find the OIG report, so the figure is **owner-supplied and unverified here**. It is cited as context only, with that label.
- **Wording:** a non-match is never called an error by the filer. Suppliers are "declared in the filing", never "responsible".

## H. Files
- `scripts/sc_lib.py` (parsers, normalisation, matching, quote location), `scripts/sc_gate.py`, `scripts/sc_inventory.py`.
- `scripts/sc_check.py` and `tests/test_sc_check.py` (Step 2). The tests must pass before any result is written.
- Output: `reports/phase_8_supplier_check.md`, with raw aggregates in `reports/sc/phase_8_supplier_check.json`.
