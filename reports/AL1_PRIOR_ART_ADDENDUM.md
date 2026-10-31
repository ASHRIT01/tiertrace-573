# AL-1 prior-art addendum (2026-10-31)

Follow-up to `reports/AL1_PRIOR_ART.md`, which is not edited. This addendum takes precedence where they differ.

**Result: the paper is no longer UNVERIFIED, and it weakens the novelty wording further.** Its change categories are close to the AL-1 labels. The sentence in section 3 here replaces the one in that report.

## 1. How it was opened

The paper was marked UNVERIFIED because ScienceDirect returned HTTP 403. A legitimate open copy was found; no block was worked around.

| Step | Result |
|---|---|
| Search: `"Automated monitoring of online news accuracy with change classification models" preprint arXiv authors` (extended) | Found the ScienceDirect and ResearchGate pages, and a stray arXiv ID |
| Search: `change classification online news error corrections 21,129 changes annotated dataset monitoring news accuracy Information Processing and Management 2023` (extended) | Same paper; no preprint |
| ResearchGate | HTTP 403; not retried |
| arXiv 1909.02164 | A different paper (TabFact); not related |
| Crossref API | Title, authors, DOI 10.1016/j.ipm.2022.103105, CC BY 4.0 |
| OpenAlex API | Lists an open copy in the Ghent University repository |
| **Ghent University repository**, `biblio.ugent.be/publication/8770058`, file 8770062 | **Opened.** A 22-page PDF, CC BY 4.0, published version |

**Read at:** the PDF's text was extracted and searched for the relevant passages, and the abstract and the category table (Table 3) were read. It was not read line by line.

## 2. What the paper does and does not do

**Timmerman, Y., & Bronselaer, A. (2022). Automated monitoring of online news accuracy with change classification models. *Information Processing & Management*, 59(6), 103105.**

**What it does.** It compares successive versions of online news articles from six Flemish newspapers, collected over two years. A subset of 21,129 atomic changes is annotated by automated and human annotation. Its supervised classifiers detect corrections of objective, subjective and linguistic errors.

Its Table 3 defines nine categories of atomic change. The six read in full:
- correction of an objective error, where typical errors explicitly include "wrong dates";
- correction of a subjective error;
- correction of a linguistic error;
- addition or clarification of information;
- deletion of information;
- update of information, where old information is replaced by more recent information.

It also has content-neutral reformulation and displacement of information; the ninth category was not read.

**How close the categories are:**

| AL-1 label | Nearest category in the paper |
|---|---|
| NEW | Addition or clarification of information |
| RETRACTED | Deletion of information |
| DATE_CORRECTION | Correction of an objective error, which includes wrong dates, though it is broader |
| UNCHANGED | No close category; it labels changes, and content-neutral reformulation is the nearest |
| TYPE_CHANGE | None |

**What it does not do, as far as the extracted text shows:**
- It classifies changed text, not structured dated events from each version, and does not match events across versions.
- It is about news. A search of the text for "regulat" finds nothing, and every "recall" hit checked is the evaluation metric.
- It does not measure how using one version rather than another changes a downstream measure.

**One difference matters for AL-1.** The paper calls these error corrections, because its goal is news accuracy. The AL-1 protocol does not say the earlier date was wrong.

## 3. Effect on the novelty wording

This is the closest taxonomy found. Classifying changes between versions of a text, including corrected dates, additions, deletions and updates, is established work. AL-1's differences are the unit (dated events extracted by an agent, not changed text), the domain (regulatory filings) and the downstream measure (the timeliness screen).

**This sentence replaces the one in `reports/AL1_PRIOR_ART.md`, section 4:**

> We found no prior work that extracts dated events from each successive version of one regulatory filing and classifies how they change between versions (search scope: twelve general web searches on 2026-10-31 covering SEC amendments, FDA and CPSC recall corrections, temporal knowledge-graph versioning and event correction, and Wikipedia and news revisions, plus an earlier web search pass on revision-aware event extraction, amended-filing event diffs, Part 573 NLP datasets and cross-document event coreference; no bibliographic database was searched systematically and most sources were read at abstract level). The closest prior dataset is Astvansh, Ball & Josefy (2022), who manually coded one Part 573 chronology per recall; the closest methods are from news, where Spangher et al. (2024; NewsEdits 2.0) classify sentence-level edits and Timmerman & Bronselaer (2022) classify atomic changes between article versions, including corrected dates, additions, deletions and updates.

The AL-1 label set must be described as an adaptation of this existing work, not as a new taxonomy.

## 4. Still UNVERIFIED

Everything else marked UNVERIFIED in `reports/AL1_PRIOR_ART.md` section 3 stays so, including Revisionista.PT, WikipEvent and DBpedia-TKG.
