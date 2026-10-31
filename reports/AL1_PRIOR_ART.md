# AL-1 prior-art check (gaps only)

**Result.** We opened nothing that does what AL-1 does: extract dated events from each successive version of one regulatory filing, match them across versions, and classify the changes. But the idea of AL-1 is not new. News revision work already classifies edits between versions, including updates to events and corrections, and temporal knowledge-graph tools already mark older facts as invalid. Any novelty claim therefore has to stay narrow (section 4).

**How this was searched.** All searches were general web searches run on 2026-10-31. No bibliographic database (Scopus, Web of Science, SSRN, Google Scholar) was searched systematically, and most sources were read only at abstract level. A negative result here means "not found in this scope", not "does not exist".

**Not redone.** An earlier pass already searched revision-aware event extraction, amended-filing event diffs, Part 573 NLP datasets and cross-document event coreference. Its closest findings are in section 3 as supplied by the owner; they were not reopened here.

## 1. Exact queries (2026-10-31)

| # | Gap | Mode | Query |
|---|---|---|---|
| 1 | SEC | extended | `SEC 8-K/A 10-K/A amended filings event-level diff extraction what changed between original and amendment NLP` |
| 2 | SEC | standard | `textual analysis of 10-K/A restatement amendments original versus amended disclosure changes machine learning extraction` |
| 3 | SEC | standard | `amended SEC filing 10-K/A compared with original filing text similarity changes study "10-K/A" empirical what amendments change` |
| 4 | FDA | extended | `FDA recall enforcement report amendments corrections changes over time analysis openFDA recall classification revision NLP` |
| 5 | FDA | standard | `medical device recall FDA MAUDE supplemental reports follow-up report changes event text versions analysis adverse event report amendments` |
| 6 | CPSC | standard | `CPSC recall notice corrections reannouncement amended recall data text analysis event extraction` |
| 7 | Knowledge graphs | extended | `temporal knowledge graph versioning event revision correction detection fact updated retracted across document versions` |
| 8 | Knowledge graphs, versions | extended | `event timeline extraction across successive versions of the same document, date changed event retracted, version-aligned event matching regulatory report amendment` |
| 9 | Wikipedia | extended | `Wikipedia revision history event mining extract events from edits timeline correction vs new information` |
| 10 | News | extended | `news article revision dataset classify edits correction versus new information NewsEdits fact updates` |

## 2. Sources opened

"Full text" means the PDF's text was extracted and searched for the relevant passages, not read line by line.

| Source | Read at | What it does | What it does not do |
|---|---|---|---|
| Spangher, Huang, Cho & May (2024), *NewsEdits 2.0*, arXiv 2411.18811 | Full text | **Closest method.** Compares sentence pairs across versions of a news article. A schema of edit intentions separates fact, style and narrative updates, including add/delete/update of events and a Correction label. Over 9,200 annotated pairs, then silver labels. | Labels sentence revisions, not extracted dated events. No date-correction or type-change class. News only. Predicts which facts will update, not how a version choice changes a downstream measure. |
| Spangher, Ren, May & Peng (2022), *NewsEdits*, NAACL, arXiv 2206.07106 | Abstract | 1.2 million articles and 4.6 million versions. Extracts Addition, Deletion, Edit and Refactor actions between versions. | No structured dated events or event-level change classes. News only. |
| Konovalov, Strauss, Ritter & O'Connor (2017), *Learning to Extract Events from Knowledge Base Revisions*, WWW | First page and passages | Uses Wikipedia infobox edit history as distant supervision to learn event extractors that predict knowledge-base updates. | Revisions are the training signal. It does not compare events across versions of a document or classify corrections. |
| OpenAI Cookbook, *Temporal agents with knowledge graphs* (reference date June 2025) | Partly verbatim, rest through a model summary | **Closest knowledge-graph mechanism.** Extracts time-stamped statements from earnings call transcripts, resolves dates, and an invalidation agent marks contradicted facts as outdated. | A tutorial, not a study. Compares statements across separate transcripts, not versions of one document. No evaluated class of change, no recall data. |
| Huwiler, Stockinger & Fürst (2025), *VersionRAG*, arXiv 2510.08109 | Abstract | Graph of version sequences and changes between document states; retrieval over 34 versioned technical documents, reporting 60% on implicit change detection. | Question answering on technical documents. No dated-event extraction described and no named change classes. |
| Finger, Cortes, Rigo & Ramos, *Narrative Consolidation*, arXiv 2512.18041 | Full text | Temporal Alignment Event Graph with SAME_EVENT links across "versions" of 169 canonical events. | Its versions are accounts of an event in the four Gospels, not successive versions of one filing. Goal is one merged text. No change classes. |
| Park (2026), *Graph-Native Cognitive Memory for AI Agents*, arXiv 2603.17244 | Abstract | Immutable memory revisions with formal belief-revision semantics. | Agent memory, not documents. Formal framework, not a change classifier. |
| de Martim (2026), *Beyond Probabilistic Similarity*, arXiv 2606.09724 | Abstract | Position paper on temporal failures of legal retrieval; proposes event reification. | No empirical work, no extraction or classification across versions. |
| openFDA, *Drug Enforcement* API documentation | Full page | States that FDA corrects past enforcement reports and that the data should not be used to track a recall's lifecycle. | Documentation, not analysis. Shows FDA amendments exist; does not study them. |
| FDA, *About MAUDE* | Full page | Follow-up reports are merged into the displayed record and each report's type lists its versions. | No version comparison. FDA warns against using the data to evaluate event rates or changes in them. |
| sec-api.io, *Form 8-K Files Dataset* | Page, part through a model summary | Vendor dataset. 8-K/A filings are separate records; the unit is the filing, not the event. | No diff or event-level comparison. The summary says amendments have no explicit pointer to their originals. |
| CPSC, *Recall Effectiveness Workshop: Recall Data* (2017), slides | Full slides | Descriptive correction rates for 865 closed recall cases. Here "correction" means fixing the product. | Nothing about amended recall records or text. |

## 3. Not opened, or supplied by the owner

Everything here is **UNVERIFIED**. It may be mentioned only with that mark, and nothing is claimed about it.

| Source | Status | Why it matters |
|---|---|---|
| *Automated monitoring of online news accuracy with change classification models*, ScienceDirect S0306457322002060 | HTTP 403. Snippet only. | **Possibly the closest taxonomy.** The snippet lists categories for correcting an error, adding information and updating information. Read it before any novelty sentence is published. |
| Revisionista.PT, Springer 978-3-030-45442-5_59 | Login redirect. Snippet only. | News changes classed as undisclosed correction, disclosed correction or disclosed update. |
| WikipEvent, Springer 978-3-319-11746-1_7 | Login redirect. Snippet only. | Event structures from Wikipedia edit history. |
| DBpedia-TKG (Leipzig PDF) | TLS certificate error. Snippet only. | Temporal graphs from every Wikipedia revision. |
| *Classifying Restatements*, EconBiz record | Bot-protection page. Snippet only. | Classifies restatements by language in announcements. |
| Other results seen as snippets only (never opened): Hasan et al. 2021; Harvard Wikipedia revision paper; *Extracting Event-Related Information from Article Updates in Wikipedia*; *Automatically Classifying Edit Categories in Wikipedia Revisions*; SemEval-2015 Task 4; Critical Audit Matter paper (gaexcellence.com); Cognee explainer | Not opened | Listed so the search record is complete. |
| Astvansh, Ball & Josefy (2022), MSOM 24(3):1457-1473 | Owner's earlier pass, not reopened | Closest prior dataset: manually coded one Part 573 chronology per recall, with supplier involvement, 2009-2018. |
| StreamSum (arXiv 2606.12807), CohTP (ACL 2026), TimelineAgent (EMNLP 2026) | Owner's earlier pass, not reopened | Revision-aware summarisation; event matching across documents, not across versions of one filing. |

## 4. What this does to the novelty wording

**What weakens the claim:**
- Classifying what changed between document versions, including corrections and event updates, already exists for news (NewsEdits 2.0). The AL-1 label set is an adaptation, not a new idea.
- Marking a fact outdated when a newer statement contradicts it already exists (the OpenAI Cookbook's invalidation agent).
- A UNVERIFIED paper may hold a closer taxonomy of corrections versus updates.
- The SEC gap is only weakly covered. Web search returned EDGAR filings and vendors rather than research, and an accounting-literature database might find what this did not.

**Not claimed:** a new method, a new task, or that this is the first study of revised filings.

**The only sentence allowed:**

> We found no prior work that extracts dated events from each successive version of one regulatory filing and classifies how they change between versions (search scope: ten general web searches on 2026-10-31 covering SEC amendments, FDA and CPSC recall corrections, temporal knowledge-graph versioning and event correction, and Wikipedia and news revisions, plus an earlier web search pass on revision-aware event extraction, amended-filing event diffs, Part 573 NLP datasets and cross-document event coreference; no bibliographic database was searched systematically and most sources were read at abstract level). The closest prior dataset is Astvansh, Ball & Josefy (2022), who manually coded one Part 573 chronology per recall; the closest method is NewsEdits 2.0 (Spangher et al., 2024), which classifies sentence-level edits in news.
