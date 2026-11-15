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

## Prior-art wording note (2026-11-14; not a protocol change)

The novelty sentence in reports/AL1_PRIOR_ART.md section 4 is superseded by reports/AL1_PRIOR_ART_ADDENDUM.md (Timmerman & Bronselaer 2022).

## Amendment 2 (2026-11-14): extraction on Kaggle, model re-pulled, equivalence check

**No AL-1 outcome has been seen.** When this amendment was written and tagged (`al1-amendment-2`):
- the agent had not been run on any AL-1 filing, and `runs/al1/` did not exist;
- no lineage class, pair, label draw, ablation or timeliness result existed, and no AL-1 extraction output existed on any machine;
- no AL-1 chronology had been opened, parsed or compared. Since amendment 1, the only operations on AL-1 PDFs were SHA-256 checks of the cached files against `al1_manifest.json` and `AL1_FETCH.json` (959 of 959 verified, 2026-11-14; nothing re-fetched);
- the equivalence reference run (below) had not started, and no output existed for the 20 equivalence documents.

The owner made the decision to amend, and it was not based on any AL-1 result.

**Reason.** The external drive that held the working repository is unavailable. Lost with it: the original local model files (the Ollama blobs; only the manifest files remained on the internal disk), the dev run outputs (gitignored `runs/`), `data/dev_raw/`, and one unpushed commit, `f488d2a`, whose content (one line in this file) was restored on 2026-11-14 as the prior-art wording note above. Section D's plan to run about 23 h on the M2 is replaced by a Kaggle notebook.

### A2.1 Where the extraction runs
- **Kaggle notebook** (`kaggle/al1_extraction.ipynb`): Linux, one NVIDIA T4-class GPU, Ollama **0.40.6** (the official `ollama-linux-amd64.tar.zst`, SHA-256 `c164ab8b1b28e2a247c29719b8e404c423c5b83ae64c3ab4e59d50c7ff7fc5e0`, checked before use; any other version stops the run).
- **Same frozen code, prompts and settings**: `config/run_settings.json` (SHA-256 `7a13cd4a...`), prompt v2, thinking off, `num_ctx` 6144, run 1 temperature 0 seed 0, run 2 temperature 0.5 seed 1, 300 s timeout, the frozen gate through the amendment-1 wrapper. The notebook clones this repository at tag `al1-amendment-2` and checks every file hash in `data/FREEZE_MANIFEST.json` and the prompt, schema and user-message hashes before any model call.
- **Python environment.** The package versions of the freeze-v1 environment were never recorded and were lost with the drive. The environment was rebuilt on 2026-11-14 from `pyproject.toml` (Python 3.12.6); the resolved versions are fixed in `kaggle/requirements-lock.txt` and installed identically on Kaggle (Python 3.12.6 via uv). The 155 previously existing tests pass in it; the 18 that need `data/raw` or `data/dev_raw` skip. This environment may differ from the one that produced the v1 results (notably PyMuPDF, now 2.1), which every AL-1 report states.
- **One GPU, one Ollama server.** Splitting documents across two servers would change which request precedes which on each server and could not be shown to leave every document's output unchanged, so a second GPU, if present, is not used.
- **Order.** AL-1 documents run campaign by campaign in `config/al1_docs.json` order (sorted campaign IDs, versions in resolved order): run 1 on the campaign's versions, then run 2 on them, then the gate. One record per document per run, one gate record per document, and a progress file. The notebook prints counts only.
- **Sessions.** Each Kaggle session stops cleanly before an 11-hour budget is reached (no call starts unless it is expected to end in time) and writes its outputs; the next session resumes from them, attached as an input dataset. A session whose GPU model differs from the one of the session that passed the equivalence check stops.
- **Retry rule unchanged** (section D): a timeout is recorded and not retried; one retry after a runner crash; a missing run 1 leaves the document's pairs uncomputed, and a missing run 2 counts as "run 2 does not agree".

**Consequences.** Outputs may differ across hardware. **H6 latency claims do not apply to AL-1**, and section D's M2 compute estimate is void. **Every AL-1 report states where the extraction ran** (Kaggle, GPU model, driver, Ollama version, model digest, repository commit, from the notebook's environment record) and gives both equivalence shares (A2.3).

### A2.2 The model is pulled, and accepted only if identical
The model `qwen3.5:4b-q4_K_M` is pulled from the Ollama registry, on the Mac (done 2026-11-14) and on Kaggle, and is accepted only if:
1. the Ollama API digest equals the frozen `d8b0f5e9760cd1682034f292d7ef72ec46f432149be0df7574bf2d6e92e38c04`; and
2. every blob re-hashes to its digest: the blob named by the frozen digest (the registry manifest) re-hashes to it, and each blob it lists (config, projector, weights, template, license, params) exists with the listed size and re-hashes to its digest. The frozen weight blobs `a9d0a3e1...` and `e56a899b...` must be among them.

The SHA-256 of the local manifest file is not the criterion (on this Ollama version it differs from the API digest). Any failure stops the run. Result on the Mac, 2026-11-14: API digest equal; all 7 blobs re-hash; `ollama show` and modelfile hashes equal the frozen record.

### A2.3 Equivalence check (fixed now)
**Documents.** 20 campaigns from the SN-1 cache, drawn by `scripts/al1_lists.py`: the frame is every campaign with exactly one PDF in the SN-1 cache whose file begins with `%PDF`, minus every dev, Test-A, Test-A labelled, Test-B and unseen-filer campaign and minus the 300 AL-1 sample campaigns (frame: 5,119), then `random.Random(0).sample(sorted(frame), 20)`. Their cached PDFs are verified against the SN-1 manifest (SHA-256 `7686b2344fb9...`). None is an AL-1 filing. The 20 campaigns (`config/al1_equivalence.json`):

23V718, 24V171, 20V303, 22V382, 25V311, 25E062, 24E080, 22V791, 24V888, 23V365, 26V227, 22E097, 25V220, 21V336, 22V598, 21V340, 21E009, 26V601, 22V303, 25V585

**Reference.** A fresh M2 run of the full frozen pipeline (run 1, run 2, gate) on these 20 documents, on this Mac, **after** the tag `al1-amendment-2`, on AC power (checked first; a run on battery does not start), with `scripts/al1_extract.py --mode batch` (run 1 on all 20, then run 2 on all 20, then the gate). Its outputs are the M2 reference and go into the Kaggle bundle with their hashes. The original dev outputs that were planned as a reference were lost with the drive.

**Kaggle side.** The same command on the same 20 documents in the same order, in the first Kaggle session, before any AL-1 document.

**Metric** (`equivalence` in `scripts/al1_kaggle_lib.py`). The claims are run-1 event claims accepted by the gate. A claim on one machine is matched if the other machine accepted a claim in the same document with the same event type and the same date (`date_text` compared after lower-casing and removing everything but letters and digits), one-to-one within a document.
- share A = matched / M2-accepted claims (M2 claims also accepted on Kaggle);
- share B = matched / Kaggle-accepted claims (the reverse).

**Rule.** The AL-1 run continues only if **both shares are >= 0.85**. Otherwise it stops and the decision returns to the author; nothing is re-run, tuned or replaced. A zero denominator does not pass. **Both shares appear in every AL-1 report.**

### A2.4 New code (not frozen)
`scripts/al1_kaggle_lib.py` (hashes, model check, resume, budget, metric), `scripts/al1_extract.py` (runner: the frozen `run_dev.run` and the frozen gate exactly as in `scripts/ts_gate.py`, taking the document list from a file instead of a gold file), `scripts/al1_equiv_check.py`, `scripts/al1_lists.py` (writes `config/al1_docs.json`, 712 documents, and `config/al1_equivalence.json`), `scripts/al1_env.py` (environment record), `scripts/al1_bundle.py` (input bundle), `kaggle/requirements-lock.txt`, and `tests/test_al1_kaggle.py` (made-up records, blobs and PDFs only). No frozen file was changed.

**How this relates to section M.** As with amendment 1, results under this amendment are labelled **"pre-specified under al1-amendment-2 (amended after al1-protocol-1, before any outcome existed)"**, and section M applies in full to any change after `al1-amendment-2`.

**Unchanged:** everything in `al1-protocol-1` and amendment 1 not stated here, including the analysis sets (248 and 228), the 712 documents, the matcher and its parameters, the labels, the draw, the endpoints and the wording rules.

## Additional reproducibility check, added after al1-amendment-2, before any AL-1 outcome (2026-11-14)

**Disclosed check, no stop rule.** Specified by the owner after the tag `al1-amendment-2` and before any AL-1 outcome existed: for up to 20 filings (seed 0) whose committed v1 run record can be matched **by hash** to a PDF still in the SN-1 or AL-1 cache (never an AL-1 sample filing), re-run run 1 only in today's environment and report how many outputs are byte-identical to the committed v1 records and the share of v1 event claims reproduced with the same date and type.

**Result: not run, because no input can be matched by hash.** None of the 1,456 records in the 14 committed v1 run files (`runs/H6_clean_4b.jsonl` and the committed Test-A, Test-B and unseen run files; the other committed files under `runs/` are logs) holds a hash of its input document. They hold the file name only (fields: `file`, `extraction`, `seconds`, `model`, `options`, `think`, token counts and durations, `done_reason`, `truncated`, `prompt`, `raw`, and `error`/`timeout`/`id` on some). No other committed file records a SHA-256 of a v1 input PDF: the hashes in `data/labels/work/**/final_stats.json` are of label files, and `data/splits/SHA256SUMS` covers the ID lists. Matching by file name alone was not allowed by the specification, so no filing qualifies and no model call was made for this check.

**Limitation stated in every AL-1 report.** The v1 results (freeze-v1) were produced with package versions that were never recorded; AL-1 runs with the versions in `kaggle/requirements-lock.txt` (Python 3.12.6, PyMuPDF 2.1, ollama-python 0.6.3), and whether today's environment reproduces the v1 outputs could not be checked, because the v1 run records hold no input hash. Results are labelled "pre-specified under al1-amendment-2".

## Amendment 3 (2026-11-15): the Kaggle equivalence check failed; the AL-1 extraction runs on the M2

**No AL-1 outcome has been seen.** When this amendment was written and tagged (`al1-amendment-3`):
- the agent had not been run on any AL-1 filing on any machine: Kaggle session 1 stopped after the equivalence check, before any AL-1 document (its output archive holds no `al1/` folder), and `runs/al1/` did not exist;
- no lineage class, pair, label draw, ablation or timeliness result existed;
- the only model outputs in existence were on the 20 equivalence documents, which are not AL-1 filings.

**Kaggle session 1 (amendment 2, as specified).** Tesla T4 (GPU 0 of two; driver 580.178.04), Linux, Python 3.12.6, Ollama 0.40.6, model digest `d8b0f5e9760c...`, repository commit `e5cc4fe`; every pre-check passed (Ollama build hash, tag commit and pinned files, the 57 frozen files and the prompt, schema and template hashes, package lock, model digest and all 7 blobs, bundle and PDF hashes). Result on the 20 equivalence documents: **M2 accepted 63, Kaggle accepted 55, matched 47; share M2 -> Kaggle 0.746, share Kaggle -> M2 0.855.** The first is below the 0.85 rule, so the run stopped as specified. Diagnostics, hash comparisons only: the user messages sent to the model were identical on both machines for 20 of 20 documents, so the difference arises in the model computation, not in PDF parsing; the run-1 extraction was byte-identical to the M2's for 9 of 20 documents, run 2 for 1 of 20. Record: `reports/al1/AL1_EQUIV_KAGGLE.json` (counts and hashes; the archive, SHA-256 `8191e0f16c0e47120fdeca7de9288e7ccae2c1c1a66833048e259d1be3831dfd`, is kept out of git).

**Author's decision.** Kaggle is not used. The AL-1 extraction runs on the M2, the hardware of the frozen v1 runs, in resumable sessions. **The Kaggle result (both shares and the counts above) is reported in every AL-1 report.**

### A3.1 How the M2 run works
- Same frozen code, prompts, settings and gate as amendment 2 A2.1, with the environment of `kaggle/requirements-lock.txt` (Python 3.12.6) and the model accepted under A2.2 (digest and every blob re-hashed at the start of each session, `--blobs-dir`).
- `scripts/al1_extract.py --docs config/al1_docs.json --pdf-dir <the 712 PDFs, verified against config/al1_docs.json> --out-dir runs/al1 --mode campaign --stop-at-campaign-boundary --deadline <session end>`, under `caffeinate -i`, on AC power (checked before each session; a session on battery does not start).
- **Sessions.** Each session has a time budget set when it starts (the first: 4.5 hours). New option `--stop-at-campaign-boundary`: the deadline is checked only before a campaign, and the campaign starts only if all its remaining calls are expected to fit (mean call time so far, or 120 s before any call, plus 60 s); a session therefore stops between campaigns. Resume, the retry rule (section D) and the counts-only output are as in amendment 2. The Ollama server is left running between sessions.
- **H6** latency claims are still not made from AL-1 runs.

### A3.2 M2 self-reproducibility check (fixed now, before it runs)
The 20 equivalence documents are run again on this Mac with the identical frozen pipeline and the same command as the reference (`--mode batch`), into a new folder `runs/al1_equiv_m2_rerun/`, and the two shares of A2.3 are computed against the existing M2 reference (`scripts/al1_equiv_check.py`, reference gate SHA-256 `00905caf...`).

**Fixed interpretation.** If **both shares are >= 0.95**, the M2 reproduces itself and the Kaggle gap is read as a hardware effect. If either is **below 0.95**, run-to-run variation exists on one machine, and this is stated as a **limitation of the gate in every AL-1 report**, with both shares. Either way the AL-1 run on the M2 goes ahead; this check has no stop rule.

### A3.3 Files
`scripts/al1_kaggle_lib.py` (`Budget.can_start` takes a number of calls), `scripts/al1_extract.py` (`--stop-at-campaign-boundary`), `tests/test_al1_kaggle.py` (2 tests on made-up records), `reports/al1/AL1_EQUIV_KAGGLE.json`. No frozen file changed. Results are labelled **"pre-specified under al1-amendment-3 (amended after al1-protocol-1, before any outcome existed)"**; section M applies in full to any change after `al1-amendment-3`.

**Unchanged:** everything else in `al1-protocol-1` and amendments 1 and 2, including the 712 documents, the gate, the matcher, the labels, the draw and the endpoints.
