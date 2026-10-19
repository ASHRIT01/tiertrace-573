# Preregistration (provisional; freeze before touching Test-A/Test-B)

Wording rule: results say "named in the filing as component manufacturer", never that a supplier "caused" a recall.

| ID | Hypothesis | Threshold |
|----|-----------|-----------|
| H1 | Masked-block parent-supplier recovery | Top-1 >= 0.80 where name is in chronology; >= +10 pts over B1 on full masked set |
| H2 | Verifier cuts confident-wrong outputs | >= 50% fewer vs. no verifier; <= 15 pts coverage lost |
| H3 | Timeline | Date exact-match F1 >= 0.90; median lag error <= 3 days (200 labelled) |
| H4 | Tier/locus labelling | Krippendorff alpha >= 0.70; agent macro-F1 >= 0.60 and +15 over keyword baseline |
| H5 | 4-bit 4B vs full precision | within 3 pts on H1, H3, H4 |
| H6 | (stretch) forward prediction | exploratory |

Headline metric: error among accepted claims vs. coverage (risk-coverage curve). Abstaining on everything is never success.
Splits and L1 labels: publish SHA-256 hashes here before any test run.

## DRAFT (not frozen): filing versions
A campaign can have several Part 573 report versions (e.g. 24V418 has three: loaded 2024-06-12, 2024-08-01, 2024-08-10).
All versions are stored and marked original (earliest loadDate) / latest. Default evaluation uses the LATEST version.
Note: the golden file 24V418-6316 is the middle version, not the latest.

## DRAFT 2026-10-18 (NOT frozen; owner to review and sign): scope revision after the data audit

Existing H1-H6 text and thresholds above are unchanged. This section proposes what the tasks mean now. New numeric thresholds are
left for the owner to set before freezing; none are invented here.

### Why (our own findings, 300 sampled latest-version filings, 2015-2026; all AI-checked, none human-verified)
- Of 300 filings, 78 name no supplier in the block and 19 name the filer itself; 203 name a different company (reports/mask_recover_size.md).
  Among those 203 the supplier's name appears in the cause or chronology in only **40 (20%; "extractive")**, as a short form only in 22,
  and **not at all in 141 (69%; "inferential")**. (An earlier count under the previous kind rule was 38 of 196 = 19%.)
- Named upstream suppliers are rare in the narrative: in a hand-check of 42 filings, only **1 (2%)** named a sub-tier / distributor / other
  supplier beyond the block supplier (95% Wilson interval about 0.4% to 12%); upstream involvement is mostly an unnamed reference ("their supplier").
  (reports/narrative_companies_handcheck.md; one reader, not double-labelled.)
- The "Tier of Supplier" field is absent from the form before 2025 (0% filled 2015-2024; 24% in 2025, 44% in 2026).
- Roughly a quarter of filings name no supplier in the block at all; the narrative is often a pointer or NR (86% have a substantive chronology).

### Scope
- **T2 (core): supplier claims with evidence and abstention.** A supplier is counted RECOVERED only if it is located in the narrative with
  a verbatim quote (verifier V1). If the narrative does not name the supplier, the correct output is **INSUFFICIENT**; a guess is an
  **unsupported claim even if it matches the block-named supplier**. Reported separately for extractive (name in cause/chronology),
  partial-only (short form) and inferential (name absent) cases, and separately for kind = external vs filer_affiliate; kind = filer_itself
  and blank-block filings are excluded from the supplier-recovery set (rule: tt/kind.py). Headline: error among accepted claims vs coverage.
- **T3 (core): dated events** with verbatim quotes; metrics as in H3.
- **T4 (reframed, secondary): upstream involvement is NAMED, UNNAMED or ABSENT** in the narrative, with a quote for NAMED and UNNAMED. Tier and
  failure-locus labels are not headline; they stay cut unless a codebook reaches the agreement threshold in H4.
- **T5 (prediction): cut.**

### Consequences to decide before freezing
- Expected size of the T2 extractive set in Test-A (about 1,000 filings) is about 130 (20% of about 680 filings naming a different
  company; very wide interval). H1's "at least 0.80 top-1 where the name appears in the chronology" would rest on about that many cases.
- H1 and H4 need restating in these terms (recovered-with-quote rate on extractive cases; unsupported-claim rate on inferential cases;
  NAMED/UNNAMED/ABSENT agreement). The owner sets the thresholds.
- Versions: the LATEST 573 version is the default evaluation document (see the earlier draft section).

## DRAFT 2026-10-18 (NOT frozen; owner to review): event inclusion and parse-failure handling

### Event-inclusion rule (T3 gold events)
- Gold events = **every dated event in the chronology**, each typed from the fixed list SUPPLIER_NOTICE, FILER_AWARENESS, INVESTIGATION_START,
  DECISION, NHTSA_FILING, OTHER, and each carrying a verbatim quote in which **the date text appears inside the quote** (the quote spans date and event).
- **Excluded:** remedy logistics (mailings to owners or dealers, remedy-vendor follow-ups, planned notification dates), and 'as of <date>' status
  statements (counts of claims or incidents as of a date). A date given only by reference ('that day') is not a dated event unless the date text
  is in the quote. Dates with no year are kept as written (the filing date gives the year); printed typos are kept as written and left to verifier V3.
- A chronology that is a pointer ('see attached ...') or NR has no gold events and is reported as NOT_REPORTED, not as zero events.
- Applied to the 30 dev label drafts: 98 events (was 90 before the rule and the date-in-quote check); 8 of 30 filings have no events.

### Upstream involvement (T4) status values
NAMED / UNNAMED / NONE_MENTIONED (the narrative is present and mentions no supplier-chain party) / NOT_REPORTED (the chronology is a pointer or NR, so
the narrative cannot settle it). A supplier that only helps with the remedy is not upstream.

### Parse-failure handling (DRAFT proposal; owner decides)
- Latest version empty or unreadable (seen: 18V155, Amendment 3 has 0 pages): fall back to the most recent earlier version that parses, and record the
  fallback in the ledger.
- No text layer (seen: 21V248, a scanned 'Defect Notice 573 Report'): exclude from scored tasks and report such filings as a separate 'unreadable' count
  in every results table; no OCR in v1. (Alternative for the owner: OCR them and report accuracy on them separately.)
- Excluded or fallback filings are never replaced by other filings after test results are seen.

## DRAFT 2026-10-19 (NOT frozen; owner to review): event and upstream rules (these refine the 2026-10-18 event-inclusion rule)

### E (T3 gold events): one event per dated sentence, date inherited from its entry
- The chronology is read sentence by sentence. A **dated sentence** carries a date of its own. An **entry** is a dated sentence plus the undated
  sentences that follow it, up to the next dated sentence (or, in a list, up to the next dated list item).
- **One event per sentence.** A sentence that reports an action or occurrence is one event. It takes its own date, or, if it has none, the date of its
  entry (the date is inherited). Each event is typed from the fixed list (SUPPLIER_NOTICE, FILER_AWARENESS, INVESTIGATION_START, DECISION,
  NHTSA_FILING, OTHER) and carries a verbatim single-sentence quote. An inherited-date event also stores its entry sentence, and the date text must
  appear inside that entry sentence, which must come at or before the event's sentence.
- A sentence that holds two dates is still one event, dated by the date of its own action (the first date given), not by a date it only mentions.
- **Not events:** descriptions with no action; statements of belief; 'as of' status statements and statements of no known incidents, complaints or
  injuries; remedy logistics (mailings, remedy-vendor emails, repairs of the affected vehicles); a pointer or NR chronology (it has no events and is
  reported NOT_REPORTED); a sentence under a heading with no date of its own (for example a 'Corrective Action' line).
- Operational choices that are mine and unreviewed: what counts as 'an action or occurrence' for an undated sentence, and the type chosen for it.
  Applying the rule to the 30 dev drafts changed 55 E labels (53 added, 2 removed; reports/rule_application_changes.md).
- Scoring: events are matched by **date + type**, not by quote span (tt/eval/devscore.py).

### U (T4): upstream involvement in the narrative (cause and chronology)
- **NAMED** if any supplier-chain company (a supplier, sub-supplier or distributor of the filer) is named in the cause or chronology. A filer's parent,
  affiliates, customers, regulators and internal committees are not supplier-chain companies. A supplier that only helps with the remedy is not
  upstream and does not make U NAMED on its own.
- **UNNAMED** if the narrative refers to a supplier, vendor or sub-supplier only generically (no company named).
- **NONE_MENTIONED** if the narrative is present and mentions no supplier-chain party.
- **NOT_REPORTED** if the chronology is a pointer or NR, so the narrative cannot settle it.
- Applying the rule to the 30 dev drafts changed 0 U labels.

## DRAFT 2026-10-19, Phase 0 (NOT frozen): rule fixes a-e (these amend the event rule above)
Labels are **silver labels: AI-made, cross-checked by independent AI passes and code checks. No label is human-verified.**
- **a. Date inheritance only inside a dated entry or bullet.** A dated entry starts at a sentence that begins with a date (no preposition such as
  'On'/'In' before it) or at a bullet item, and runs until the next entry or bullet or a blank line. An undated sentence inside it inherits the entry's
  date. An undated sentence in prose is stored with `date_inferred=true` and no date; it is **not scored**. (tt/labels/events.py)
- **b. A sentence with two distinct dates yields one event per date.** The first date takes the sentence's type; later dates are OTHER unless an
  override says otherwise. Dates that only bound a data range (production/build windows, 'ranging from', 'start of production through') are mentions,
  not event dates.
- **c. Date normalisation.** Strip 'On or about', 'approximately', 'around' (and leading on/in/by/since/during). Parse to {start, end, granularity:
  day | month | quarter | year | range | fuzzy}; 'mid-2017', 'mid-August 2017', 'early/late/end of/beginning of X' are fuzzy. A year-less date takes
  its year from context only if unambiguous: the one year of all fully dated expressions in the chronology, or, with none, the filing year provided the
  result is not after the filing date; otherwise `date_inferred=true`. (tt/labels/dates.py)
- **d. Event scoring.** A predicted event matches a gold event if the types are equal and the date spans overlap after widening both to the coarser
  granularity (day < month < quarter < year; ranges as is). Each gold event matches at most once. Fuzzy gold dates are scored separately (recall).
  Date-inferred gold events are not scored. (tt/eval/devscore.py)
- **e. Headline event metric** uses five types: FILER_AWARENESS, INVESTIGATION_START, DECISION, SUPPLIER_NOTICE, NHTSA_FILING. OTHER is reported
  separately.
- Per-filing judgment calls (exclusions with reasons, type corrections) live in config/event_overrides.json; they are AI decisions, unreviewed.

## FROZEN (see reports/PREREGISTRATION_PROPOSED_FINAL.md for the full text)
Code commit before freeze: 969a65cd2ab8471e5e63e98b4a004c55f8be622a

Primary endpoint (chosen by the owner): H1

```
LEAK CHECK: Test-A / Test-B / unseen-filer IDs in file names or contents under data/, runs/, reports/
  ID sets: Test-A 1000, Test-A labelled 200, Test-B 100, Unseen-filer 100 (union 1100)
  files scanned: data/ 2232, runs/ 28, reports/ 40; unreadable: 0
  LEAKS (a file or content of a test campaign) in non-excluded files: 0 file(s)  -> none
  WAIVER 24V284 [Test-A]: Downloaded and read as a parser golden file (config/golden_urls.txt, tests/test_golden.py, tests/test_layout.py) before the splits were final. In the Test-A list of 1,000 only; in no scored subset (not Test-A labelled, Test-B or unseen-filer). Files kept; never used in any analysis.
  CROSS-REFERENCES (test ID only mentioned inside another campaign's source document; not a file of that ID): 10
    data/api_cache/si_23V867.json: 23V626 [Test-A]
      ...circuit and battery failure. This \ufb01ling was assigned Recall No. 23V626. On December 13, 2023, Porsche Cars North America (Porsche) noti\ufb0...
    data/api_cache/si_25V224.json: 24V928 [Test-A]
      ...recall is NGDV_TSB_036. Vehicles that were previously recalled under 24V-928 will need to be inspected and possibly have the head unit replaced ag...
    data/audit_raw/RCLRPT-25V224-9205.PDF: 24V928 [Test-A]
      ...eceived a new head unit for the rearview camera display under Recall 24V-928 as well as new production vehicles until a production change was imp...
      ...er 2024, Oshkosh submitted a Noncompliance Information Report (Recall 24V-928) where vehicles may intermittently display a blank rear view camera...
    data/audit_raw/RCLRPT-25V782-3862.pdf: 24E099 [Test-A/Test-A labelled]
      ...nvolved: 6 Descriptive Information: New Way received NHTSA Recall No. 24E099 from Agility Fuel Solutions, LLC. which identified affected Agility f...
      ...volved: 32 Descriptive Information: New Way received NHTSA Recall No. 24E099 from Agility Fuel Solutions, LLC. which identified affected Agility f...
    data/audit_raw/RCLRPT-26V336-9398.pdf: 26E032 [Test-B]
      ..., including crash, fire, death, injury: According to Lippert's Recall 26E032: "Under certain operating conditions, if the bolt head fractures whil...
      ...amended date is within the 60-day limit. Related NHTSA Recall Number: 26E032 Description of Remedy Remedy Type: Replace Consumer Advisories: Do No...
    data/cache/static.nhtsa.gov_odi_rcl_2025_RCLRPT-25V224-9205.PDF: 24V928 [Test-A]
      ...eceived a new head unit for the rearview camera display under Recall 24V-928 as well as new production vehicles until a production change was imp...
      ...er 2024, Oshkosh submitted a Noncompliance Information Report (Recall 24V-928) where vehicles may intermittently display a blank rear view camera...
    data/cache/static.nhtsa.gov_odi_rcl_2025_RCLRPT-25V782-3862.pdf: 24E099 [Test-A/Test-A labelled]
      ...nvolved: 6 Descriptive Information: New Way received NHTSA Recall No. 24E099 from Agility Fuel Solutions, LLC. which identified affected Agility f...
      ...volved: 32 Descriptive Information: New Way received NHTSA Recall No. 24E099 from Agility Fuel Solutions, LLC. which identified affected Agility f...
    data/cache/static.nhtsa.gov_odi_rcl_2026_RCLRPT-26E042-9936.pdf: 26E022 [Test-B]
      ...he defect or noncompliance: Please reference IMPORTANT SAFETY RECALL: 26E022 from Q'Straint for further information. Our recall is duplicating the...
      ...Date: Jul 13, 2026 NHTSA Recall No.: 26E042 Manufacturer Recall No.: 26E022 The information contained in this report was submitted pursuant to 49...
    data/cache/static.nhtsa.gov_odi_rcl_2026_RCLRPT-26V336-9398.pdf: 26E032 [Test-B]
      ..., including crash, fire, death, injury: According to Lippert's Recall 26E032: "Under certain operating conditions, if the bolt head fractures whil...
      ...amended date is within the 60-day limit. Related NHTSA Recall Number: 26E032 Description of Remedy Remedy Type: Replace Consumer Advisories: Do No...
    data/raw/RCLRPT-26E042-9936.pdf: 26E022 [Test-B]
      ...he defect or noncompliance: Please reference IMPORTANT SAFETY RECALL: 26E022 from Q'Straint for further information. Our recall is duplicating the...
      ...Date: Jul 13, 2026 NHTSA Recall No.: 26E042 Manufacturer Recall No.: 26E022 The information contained in this report was submitted pursuant to 49...
  ID matches in EXCLUDED files (expected; reported separately, not part of the verdict):
    data/processed/campaigns.csv: Test-A 1000/1000, Test-A labelled 200/200, Test-B 100/100, Unseen-filer 100/100
      1100 IDs, sha256 of the sorted list ee1ffdbbe971ae0a
    data/splits/README.md: Test-A 1/1000, Test-A labelled 0/200, Test-B 0/100, Unseen-filer 0/100
      24V284
    data/splits/proposed/testA_labelled_ids.txt: Test-A 200/1000, Test-A labelled 200/200, Test-B 0/100, Unseen-filer 0/100
      200 IDs, sha256 of the sorted list 2fe9c5130d96f8b0
    data/splits/proposed/testB_ids.txt: Test-A 0/1000, Test-A labelled 0/200, Test-B 100/100, Unseen-filer 0/100
      100 IDs, sha256 of the sorted list bc83f176285ae561
    data/splits/proposed/unseen_filer_ids.txt: Test-A 100/1000, Test-A labelled 0/200, Test-B 0/100, Unseen-filer 100/100
      100 IDs, sha256 of the sorted list 1e4114e86c1afb8c
    data/splits/testA_ids.txt: Test-A 1000/1000, Test-A labelled 200/200, Test-B 0/100, Unseen-filer 100/100
      1000 IDs, sha256 of the sorted list 04edba216e3f6677
    reports/PREREGISTRATION_PROPOSED_FINAL.md: Test-A 4/1000, Test-A labelled 1/200, Test-B 2/100, Unseen-filer 0/100
      23V626, 24E099, 24V284, 24V928, 26E022, 26E032

FREEZE RECORD
  git commit (HEAD at freeze time, before the freeze commit): 969a65cd2ab8471e5e63e98b4a004c55f8be622a
  scorer code = tt/eval/endpoints.py, devscore.py and the tt/eval modules they import: devscore.py, diagnose.py, endpoints.py, phase3.py, phase4.py, riskcov.py
  sha256 agent_prompt_v2_system             a1464bfbb4b8b46b866bf9be9eec1233134faa63551ff93b2d2da4b9e4080708
  sha256 agent_output_schema                ba79b8053e35ca0bc61ce99951903eabc6df49fa8396fe97dc1eede169b237a3
  sha256 agent_user_message_template        751e7503e7fb4f311b5d7a91bd76103de50260424d13b627e1f2028bf0255459
  sha256 thresholds_file                    d1dc231747eba62d2274dbd923f34a9e58327fe61421c11eab636037ecfba64f
  sha256 verifier:verifier.py               e9c6a147d0921b60196a6fd212bd9440284dbb3db74c090ca8e971f5f045189e
  sha256 verifier:extra.py                  330ac1956154d447c212f0425dd8b21f3ff549949de1754940d627a574ddbb15
  sha256 preregistration_proposed_final     1026b8809bd81aeee9ec9efb01734751e40ea698269c955b3d3d48c1bc829dff
  sha256 scorer:devscore.py                 67a49fc047afa910c2ce66c3269d064e56abe0bde1d04b7cc9d6a46f84e07dcb
  sha256 scorer:diagnose.py                 e8892c89a487d9cce1fa5cf72ac122d6a2d355b1bd5f3909aa28a9a3deb690bf
  sha256 scorer:endpoints.py                c70ed9dfd71051078eeae7cd31fe9e30e86516984a5fb5f69fe2a29bb4cb3cf9
  sha256 scorer:phase3.py                   45daaef94c248a0b794e0e96d0bfe4e8d7f60cd5fe006599def7eb7f3ffd7ca5
  sha256 scorer:phase4.py                   dbb7472ea58fac4c54e73547efe8144846b651917836acf569e5468da99764b2
  sha256 scorer:riskcov.py                  9492242d3fde23ea0381e2f5691d64c0d50fce788a1e2892a5057d150fb97bd2
  thresholds status OWNER_APPROVED; primary endpoint H1 (chosen by the owner)

  Ollama: ollama version is 0.40.6
  model qwen3.5:4b-q4_K_M (agent): digest d8b0f5e9760cd1682034f292d7ef72ec46f432149be0df7574bf2d6e92e38c04; ollama-show sha256 82b81d8d8a7d944c; weight blobs re-hashed OK: True; Q4_K_M 4.2B
  model qwen3.5:2b-q8_0 (dev_only): digest 0689d44085e06d165161a8a9a1731344278cfb5aade63a3c3dbdb48ab54b130a; ollama-show sha256 e608641bc7678742; weight blobs re-hashed OK: True; Q8_0 1.9B

  seeds and options (config/run_settings.json, checked against the code):
    prompt v2, think False; run 1 {'temperature': 0.0, 'seed': 0, 'presence_penalty': 0, 'num_ctx': 6144}; run 2 {'temperature': 0.5, 'seed': 1, 'presence_penalty': 0, 'num_ctx': 6144}
    bootstrap {'resamples': 2000, 'seed': 0}; split seed 0; subset sizes {'testA_labelled': 200, 'testB': 100, 'unseen_filer': 100}; injection fixture seed 0
    code: {'run1_options': {'temperature': 0, 'seed': 0, 'presence_penalty': 0}, 'num_ctx_default': 6144, 'dev_bench_default_temperature': 0.0, 'dev_bench_default_seed': 0, 'bootstrap_resamples': 2000, 'bootstrap_seed': 0, 'draw_splits_seed': 0, 'phase6_subsets_seed': 0}

  labelling:
    Pass A prompt: NONE EXISTS. Pass A is code-assisted (tt/labels/draft.py, events.py, dates.py) plus per-filing overrides (config/event_overrides.json, config/claim_overrides.json), all hashed in the manifest; there is no stored Pass A prompt text to hash.
    Claude model, test pass_a_drafter: 'code (tt/labels/draft.py, events.py, dates.py) + per-filing overrides written by the Claude Code session (claude-sonnet-5-5 for test)'
    Claude model, test pass_b_labeller: 'claude-opus-5-5'
    Claude model, test pass_c_adjudicator: 'claude-opus-5-5'
    dev labels: not recorded: Claude via Claude Code (claude-opus-5-5 or claude-sonnet-5-5, switched during the work)
    dev heldout_attack_author: not recorded: Claude subagent, session model at the time
    (aliases as passed to the Agent tool; alias-to-version mapping cannot be proven from inside a subagent)
    sha256 PASS_B_PROMPT.txt        6cc1bca13fa534e7493ed5cebc08285cec82835db9e4dbb0d7685ab1ebec33c3
    sha256 PASS_C_PROMPT.txt        dac9fa2c414be3a71acf8b6eb8c53c870fac54a290d8bc9541845fc867d7698c
    sha256 LABELING_RULES.md        39b99cbabe6b8c9c100193837ee81574c3da48efc2ed22319a5684757a510876
    blind guard tt/labels/blind.py sha256 7cfd8f93b9ee6b0faaf2baca77fdd19e9effb10d059d3a421459ee187cdbd52b
```

| file | sha256 |
|---|---|
| config/affiliates.csv | 0d11d4d12c9f9efbf599e87e010d61a559b7b46772802a3a549b962f065538b5 |
| config/aliases.csv | 709cab6728e7b9b40db61dc846ae5edefb33506f2afa10a5a9043c23c7e089cd |
| config/claim_overrides.json | 52db5639ba498481be0513e87749e88797ca1b0d014bf2b3a43f87c3b733720e |
| config/event_overrides.json | 0a6dea306291293f266468583b8b880152f51852438351fa598d057355f8bafc |
| config/injection_heldout_v1.json | 4e70564571994eae4527d4a745916703322772422de40722d2da302e22e28a1c |
| config/labelling_model.json | 661c178894b2e37c505bb5535f605574291e65e1fe6692367d57b004c69b0a61 |
| config/model.yaml | 55e3e9b42e20a3adec9adab940c2c28f6f7ead65de3963ead5e2805690e8fb58 |
| config/run_settings.json | 7a13cd4a37e391d672c1ad8c071d03cde0bdf62c30e8c50a4c4a00328f0edbb9 |
| config/thresholds.json | d1dc231747eba62d2274dbd923f34a9e58327fe61421c11eab636037ecfba64f |
| data/labels/dev_silver_v1.json | d17a30a4c710e1aadb46fb773f2b4759cea49eea3ba5457279ae3441be46f35e |
| data/labels/passA_v1.json | 16eac53ae910e4ae5eccbcee0a43b9961fc44de25d393b69c4366408d7e6818b |
| data/labels/passB_v1.json | 0ebb01880cb619e788c335df3137dd8a95ca7ded1fcd374738950b960b337f99 |
| data/labels/passC_decisions_v1.json | 80f40fe1e75f3631ef416f6ce776f634e20c74541041da4bba681b5d7a8d2da2 |
| docs/LABELING_RULES.md | 39b99cbabe6b8c9c100193837ee81574c3da48efc2ed22319a5684757a510876 |
| docs/LABELS.md | e1dcac7e4d1701873cafe332dd09cef5b5467e4c50b6fabbc7e53c26e3ee9b4f |
| docs/PASS_B_PROMPT.txt | 6cc1bca13fa534e7493ed5cebc08285cec82835db9e4dbb0d7685ab1ebec33c3 |
| docs/PASS_C_PROMPT.txt | dac9fa2c414be3a71acf8b6eb8c53c870fac54a290d8bc9541845fc867d7698c |
| docs/PHASE6_RUNBOOK.md | 85c47f615571461acbf38a4da5ed43719afbdc416b302ee17d3f5f420d494447 |
| docs/PROMPT_LOG.md | 5802c8bbc22c930a242b698f227d108eab34e1be9c34858705c2b07508c167d8 |
| reports/PREREGISTRATION_PROPOSED_FINAL.md | 1026b8809bd81aeee9ec9efb01734751e40ea698269c955b3d3d48c1bc829dff |
| scripts/freeze.py | 127b9aa03c2df0ce159dbe40d31dd9950c02a7e09bd0865cf2550c1cb9f623fa |
| tt/agent/agent.py | 63bc1ddaf96bac7de8ea03c13e3e815770fa3d9facf0ddf73e2fb8eed233214f |
| tt/agent/inject.py | affab587c0b19b393a58b448098938b018ae703cac1f55dd053aa1b49859fec4 |
| tt/agent/run_dev.py | 13be7b03cdcb3908e1b9cb20954fe31b0f22a2a40adcc070051ea545e73571da |
| tt/agent/schemas.py | 1ad98617688ac686db79564fc1a29166f8f6aa7dd36bf0912c8e70662d40bf76 |
| tt/baselines/rules.py | c8107810fe9b1d8471732d76978777fe0bb5dd82f0707756157585bdbb2ee397 |
| tt/cli.py | 20b41b1b8597438401260c4fdc291ceb57e40bfce1495dd10bb63273d5b5b9b9 |
| tt/eval/devscore.py | 67a49fc047afa910c2ce66c3269d064e56abe0bde1d04b7cc9d6a46f84e07dcb |
| tt/eval/diagnose.py | e8892c89a487d9cce1fa5cf72ac122d6a2d355b1bd5f3909aa28a9a3deb690bf |
| tt/eval/endpoints.py | c70ed9dfd71051078eeae7cd31fe9e30e86516984a5fb5f69fe2a29bb4cb3cf9 |
| tt/eval/phase3.py | 45daaef94c248a0b794e0e96d0bfe4e8d7f60cd5fe006599def7eb7f3ffd7ca5 |
| tt/eval/phase4.py | dbb7472ea58fac4c54e73547efe8144846b651917836acf569e5468da99764b2 |
| tt/eval/riskcov.py | 9492242d3fde23ea0381e2f5691d64c0d50fce788a1e2892a5057d150fb97bd2 |
| tt/kind.py | 745b16cdbb3f08708288efc9f4f8465ab8a6a3c7998599f83317b716542183ac |
| tt/labeldraft.py | ae749b0468f7c350548e6e58dec3ecd8596f0bef882e9fbfe57aedd2856990ec |
| tt/labels/agree.py | 616c61a4dbb95f91b23b4d5d266860f2e280b39eebf86cba6f4aa1d740c1c74c |
| tt/labels/blind.py | 7cfd8f93b9ee6b0faaf2baca77fdd19e9effb10d059d3a421459ee187cdbd52b |
| tt/labels/dates.py | 17836b82a3a468203ed37bf21e39b721d889ecc904081691e199f3c8a5c97a04 |
| tt/labels/draft.py | 3e6d2d4e2528bb09e5aa6c18e620e94b4158ce891140d95f998434b7f4f14c0d |
| tt/labels/events.py | 750f96f3fda992c1aaa9f2e5631f262b9498130b8b6e8ce30b28e4919b44cfc1 |
| tt/labels/pipeline.py | 1240fdc4212c26b2110233749f81f5b0922902eefcd1acd15a7060e01bd7b085 |
| tt/labels/protocol.py | b5618bfda67abbc3aae8117fcd2eb9d970ea2064e7e648d7c9454bdbc2e4fcb7 |
| tt/labels/schema.py | 3ed842383918ed322f4f4b0c1f2380d40c59265d1e2c13caaf79fe80f6e7645a |
| tt/labels/texts.py | 74aaddfdd1842516e4d33dd5c46aa44c1c62fb4a50f8f7bc840ace34be2a3212 |
| tt/leakcheck.py | 5d20b145ec64b413da5c74ce533410de8ca3da9c8d30786ac609b4b0e22078fe |
| tt/norm/aliases.py | 743f811d3e37b85b4afbd497cc39dee8ff084a4cb5e340bcea85611523abe056 |
| tt/parse/block.py | b489a75f3b79edbc6c2e314753c5e4b7f2dee8187ea3b1b7fdfc787033013c8f |
| tt/parse/pdf.py | 85a92ea6d8fbabcbf3420d4640c5cf0ce1dc2c374bd7b7a8db82eef3afc93c97 |
| tt/parse/sections.py | 898727fe0abfab8dd5d5592fb3133eb38f04b85e8570fed9555cf57309d560f1 |
| tt/verify/dates.py | 6dedf1dfccb21bd43f81fcdf4522d37e491749bb1d88fe0bcf8a9f50f3559d57 |
| tt/verify/extra.py | 330ac1956154d447c212f0425dd8b21f3ff549949de1754940d627a574ddbb15 |
| tt/verify/verifier.py | e9c6a147d0921b60196a6fd212bd9440284dbb3db74c090ca8e971f5f045189e |
| data/splits/dev_ids.txt | f11841a831213bcaa2ca2887cf8c2939dab4de41a23cc6bffd7fdaf269ea645a |
| data/splits/testA_ids.txt | 89a89a5add390049da15e9f55955d512157fed3f2d4f127cf6f30a2b900c9fa1 |
| data/splits/testA_labelled_ids.txt | 0bc380cc2ef6faa4f9cdf77cec8f239572084384728586420ab6a7dc147482b1 |
| data/splits/testB_ids.txt | f9e12f2976ba891f921cb969ed923041bb2134c6bc2a33f5aa55ee032c4236e6 |
| data/splits/unseen_filer_ids.txt | fd7174f9f9968cabeb87e5f7fca7beafb1459ee3518fb946a432074b1dcddbe4 |
