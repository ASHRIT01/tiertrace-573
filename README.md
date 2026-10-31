# TierTrace-573

[![DOI](https://zenodo.org/badge/1440585674.svg)](https://doi.org/10.5281/zenodo.23831372)

**All labels in this repository are silver labels: AI-made (code plus Claude models) and cross-checked by other AI passes. No human checked any label.**

TierTrace-573 extracts timeline events (supplier notice, awareness, investigation, decision, NHTSA filing) and supplier names from NHTSA Part 573 Safety Recall Reports. Each claim comes with a verbatim quote. A small local model (`qwen3.5:4b-q4_K_M` via Ollama) proposes the claims. Deterministic code then checks each one, and the agent keeps a claim only if every check passes and a second, differently sampled run agrees; otherwise it abstains. The study was preregistered (tag `freeze-v1`) and scored once against silver labels. The full write-up is [reports/TIERTRACE_REPORT.md](reports/TIERTRACE_REPORT.md).

## Headline results

Error rates are against silver labels, not checked by a human. Sources are given as `file@commit`; every number is in the claims list of the report (section 9).

| endpoint | tier | split | result | rule | verdict | source |
|---|---|---|---|---|---|---|
| **H1** event error, B2 (all claims) − agent (accepted) | **primary, preregistered** | Test-A (199) | **0.1352 [0.0855, 0.1924]**, coverage 0.533; error 0.402 → 0.267 | ≥ 0.05, CI lower > 0, coverage ≥ 0.40 | **PASS** | `reports/phase_6_testA_primary.md@37f93c9` |
| H2 cause reported or not (NR detection only) | secondary, preregistered | Test-A | 0.1350 [0.0803, 0.1977] | CI lower > 0 | PASS | same |
| H4 prompt-injection success after checks | secondary, preregistered | 30 attacks | 2/30 = 0.067; exact 95% upper bound 0.195 | ≤ 0.10 | PASS (point estimate; bound above 0.10) | `reports/phase_6_H4.md@b9611e0` |
| H5 event error, rule baseline B1 − B2 | secondary, preregistered | Test-A | 0.1092 [0.0308, 0.1765] | CI lower > 0 | PASS | `reports/phase_6_testA_primary.md@37f93c9` |
| H6 JSON-valid rate / p95 seconds per filing | secondary, preregistered | 100 dev filings | 1.000; p95 80.1 s including the cold-load call; p50 31.7 s; max 112.5 s (M2 8 GB, Terminal.app, other apps closed, as stated by the owner). H6 PASS on 100 dev filings with apps closed (p95 80.1 s); on Test-A filings with apps open, p95 was 130 s (run 1) / 184 s (run 2) (A13), so longer recent filings with other apps running can exceed 120 s. | ≥ 0.95; ≤ 120 s | PASS | `reports/phase_6_H6.md@08d7916` |
| H1-style delta | exploratory | Test-B (100) | **0.0327 [−0.0244, 0.0984]**: interval includes 0 | none | n/a | `reports/phase_6_secondary_splits.md@ef19956` |
| H1-style delta | exploratory | unseen-filer (98) | 0.0877 [0.0219, 0.1587] | none | n/a | same |
| H5-style B1 − B2 | exploratory | Test-B / unseen-filer | 0.1458 [0.0639, 0.2048] / **0.0877 [−0.0103, 0.1612]**: unseen interval includes 0 | none | n/a | same |
| TS-1 timeliness screen: self-reported decision-to-original-filing gap > 5 working days (screening signal, not a legal finding) | post-freeze protocol ts-protocol-1, silver reference | 305 defect filings | FLAGGED with RCDATE as filing date 19/305 = 0.062 [0.040, 0.095]; originals stratum 6/136 = 0.044 [0.020, 0.093] (CIs added after seeing results). The primary (PDF Submission Date, 104/305) is not interpretable as timing: amended versions carry the amendment date | none (descriptive) | n/a | `reports/phase_7_timeliness.md@2157cf1` |
| SC-1 supplier claims vs the filer-declared supplier (reference = filer's declaration, non-AI, not a reference standard) | post-freeze protocol sc-protocol-1 | 261 filings declaring an external supplier | agent (never saw the block, name masked): recall 18/261 = 0.069, precision 19/172 = 0.110 (accepted 14/70 = 0.200); silver S2 precision 92/113 = 0.814; components not run (no component claims) | none (descriptive) | n/a | `reports/phase_8_supplier_check.md@f35dfb6` |
| HA-1 small audit of accepted event claims (audited by the author, a single non-expert, n = 39; HA-01 practice item excluded) | post-freeze protocol ha-protocol-1; silver verdict compared, not a reference standard | 39 accepted Test-A claims, one per filing (estimates a random accepted claim from a random filing) | marked correct (date and type) 26/39 = 0.667 [0.510, 0.794]; date only 38/39 = 0.974 [0.868, 0.995]; marks vs silver agreement 30/39 = 0.769, kappa 0.449; repeats 8/8; exploratory prediction-powered estimate over the 536 claims 0.612 [0.452, 0.771] (not narrower); post hoc without HA-02 (n = 38): 26/38 = 0.684 [0.525, 0.809] | none (descriptive) | n/a | `reports/phase_9_human_audit.md@6d81416` |

## Quick start

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]" && pytest
ollama pull qwen3.5:4b-q4_K_M          # the frozen digest is d8b0f5e9760c…; Ollama 0.40.6 was used

# one filing: download (1 request/s, identifying user agent) and parse it
echo https://static.nhtsa.gov/odi/rcl/2024/RCLRPT-24V418-6316.PDF > one.txt
tt fetch-list --url-file one.txt --out data/raw
tt parse data/raw/RCLRPT-24V418-6316.PDF
```

`tt parse` prints the text-layer status, the sections found and the supplier block fields. It makes no model call.

There is no command that runs the agent on a single filing. The model runs over a labelled set with `tt dev-bench`, and PDFs are not in the repository. To rerun the H6 setting on the dev filings, build the campaign index from the NHTSA flat file (`tt flat-index`) and fetch the dev PDFs (`tt dev-fetch`). Then run:

```bash
tt dev-bench --model qwen3.5:4b-q4_K_M --labels data/labels/dev_silver_v1.json --prompt v2 --out runs/my_dev_run.jsonl
```

The Phase 6 test procedure is in `docs/PHASE6_RUNBOOK.md`.

## Repository map

| path | what |
|---|---|
| `tt/fetch/`, `tt/parse/` | polite NHTSA download; PDF text, section and supplier-block parsing |
| `tt/agent/` | prompt v2, output schema, the two-run agent and acceptance rule, injection harness |
| `tt/verify/` | deterministic verifiers (`verifier.py` V1–V5, `extra.py`) |
| `tt/baselines/` | B0 and B1 rule baselines |
| `tt/labels/` | silver-labelling pipeline (Pass A code, comparison, blind X/Y Pass C), blind guard |
| `tt/eval/` | frozen scorer (`endpoints`, `phase3`, `phase4`, `riskcov`, `diagnose`) and the amendment-1 wrapper `amend1.py` |
| `config/` | thresholds, run settings, labelling models, overrides, injection attacks, isolation slips |
| `data/splits/`, `data/labels/` | split ID lists; silver labels and labelling work files (PDFs are not committed) |
| `runs/` | model outputs, force-added and hashed (otherwise gitignored) |
| `reports/` | every report; start with `TIERTRACE_REPORT.md`, then `DEVIATIONS.md` |
| `docs/` | labelling rules, Pass B/C prompts, amendment 1, runbook |
| `PREREGISTRATION.md` | the frozen preregistration and freeze record |
| `scripts/` | Phase 6 runners, supervisor, analysis scripts, `writeup_claims.py` (checks every number in the write-up) |
| `LICENSE`, `LICENSE-DATA.md`, `CITATION.cff` | MIT for code; CC BY 4.0 for labels, run outputs and reports; citation metadata |

## Limitations

- **Silver labels only.** Nobody checked the labels; the only reading by a person is HA-1, 39 accepted claims marked by the author, a single non-expert (The notes were written by the author; an AI assistant rewrote their wording; one practice item was answered by the AI and one was discussed with it), and one rater is not a reference standard. Pass C sided with Pass B in 72–78% of items, and both are the same model family, so the labels are not independent evidence. No label-error rate is claimed.
- **Results are weaker beyond Test-A.** The check-and-abstain gain did not show clearly on Test-B (H1 interval includes 0), and the advantage over the rule baseline did not show clearly on unseen filers (H5 interval includes 0).
- **Event types are where errors concentrate.** Most wrong accepted claims have the right date but a different type. The agent's typing falls below the two labellers' agreement on Test-B and unseen filers.
- **Supplier claims** are few (13–20 accepted per split) and their error is 23–40%, with wide intervals.
- **H4 limits.** H4 has 30 attacks; the upper bound of 0.195 cannot rule out a true rate above 10%. An attack that makes the model return no events is invisible to every claim-level check.
- **Cause.** Only "cause reported or not" is scored, never the cause itself.
- **Speed.** H6 is one run on one machine, with the clean condition as stated by the owner. H6 PASS on 100 dev filings with apps closed (p95 80.1 s); on Test-A filings with apps open, p95 was 130 s (run 1) / 184 s (run 2) (A13), so longer recent filings with other apps running can exceed 120 s.
- **Wording.** Suppliers are "named in the filing as component manufacturer", never "responsible" for a recall.
- **SN-1 scope.** SN-1 is data collection only; no analysis has been done yet. Coverage is campaigns received 2020-01-01 to 2026-10-09, vehicle and equipment: 6,666 usable Part 573 PDFs (17 campaigns with no Part 573, 2 unusable). Tire and child-restraint campaigns are out of scope. PDFs are not redistributed; the repository holds NHTSA URLs and campaign IDs only.

## How to cite

```
Ashrit Kota (2026). TierTrace-573 (v1.0.0) [software and data]. Zenodo. https://doi.org/10.5281/zenodo.23831372
```

That DOI covers all versions. v1.0.0 specifically is https://doi.org/10.5281/zenodo.23831373.

Preregistration tag freeze-v1 (commit b2c5ed5); amendment-1 (commit 8525779). Report: reports/TIERTRACE_REPORT.md. Repository URL: https://github.com/ASHRIT01/tiertrace-573. See also CITATION.cff.

Related work: Astvansh, V., Ball, G., & Josefy, M. (2022). The Recall Decision Exposed: Automobile Recall Timing and Process Data Set. *Manufacturing & Service Operations Management*, 24(3), 1457–1473. https://doi.org/10.1287/msom.2022.1085

## Licence

- **Code:** MIT ([LICENSE](LICENSE)).
- **Silver labels, run outputs and reports:** CC BY 4.0 ([LICENSE-DATA.md](LICENSE-DATA.md)).
- **NHTSA source documents** (Part 573 filings, and the quotes from them inside the labels and outputs) are US-government records. We do not relicense them.
- **The MSOM dataset** (Astvansh, Ball & Josefy 2022) is not included or redistributed here.
