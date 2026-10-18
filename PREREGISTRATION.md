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
