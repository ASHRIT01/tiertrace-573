# Phase 6 runbook (run only after the owner approves and `scripts/freeze.py` has been run)

All commands from the repo root with the venv active. All labels are silver (AI-made, AI-cross-checked, not human-verified); say so in every output.
Order matters: **label ALL three splits (Test-A labelled, Test-B, unseen-filer) first, then run any model on any split.** Labelling is blind to every
model and baseline output (4B, 2B, B0, B1): the labelling commands refuse any path inside `runs/` (`tt/labels/blind.py`), and labelling scratch files
live under `data/labels/work/<split>/`, never `runs/`. Every Pass A/B/C and attack-author subagent call passes the exact Claude model ID declared in
`config/labelling_model.json` (a different model would invalidate the freeze record). Do not read model outputs while labelling. Fetching is 1 request per second with the identifying user agent; stop on 401/403/429.
Replace `testA` by `testB` / `unseen` for the other splits (file names `data/splits/{testA_labelled,testB,unseen_filer}_ids.txt`). Do steps 1-2 for all three splits before step 3 for any.

```
# 1. fetch latest versions (IDs only come from the frozen split files)
python -m tt.cli split-fetch data/splits/testA_labelled_ids.txt data/testA_raw data/processed/testA_573.jsonl
python -m tt.cli parse-report --folder data/testA_raw --out reports/parse_report_testA.md
python -m tt.cli label-select data/testA_raw data/splits/testA_labelled_ids.txt config/testA_selection.json

# 2. silver labels (same three-pass protocol as dev)
# Test overrides go in separate per-split files (config/overrides/test_a_events.json, test_a_claims.json), written by the Claude Code session blind to runs/
# (the guard refuses runs/), and hashed + committed when labelling finishes (record the hashes next to the labels hash in reports/phase_6_labels.md).
# The dev override files are NOT passed for test.
python -m tt.cli pass-a --selection config/testA_selection.json --drafts "" --pdf-dir data/testA_raw --out data/labels/testA_passA.json --event-overrides config/overrides/test_a_events.json --claim-overrides config/overrides/test_a_claims.json
mkdir -p data/labels/work/testA
python - <<'PY'
import json; json.dump([f["file"] for f in json.load(open("config/testA_selection.json"))["filings"]], open("data/labels/work/testA/files.json","w"))
PY
python -m tt.cli label-export data/labels/work/testA/files.json data/labels/work/testA/passB --pdf-dir data/testA_raw
#   Pass B: one blind subagent per batch dir, prompt docs/PASS_B_PROMPT.txt ({DIR} = the batch dir); check each files_seen.txt
python -m tt.cli label-compare data/labels/testA_passA.json data/labels/work/testA/passB data/labels/work/testA/cmp --pdf-dir data/testA_raw
#   Pass C: one subagent per data/labels/work/testA/cmp/passC/batch_N, prompt docs/PASS_C_PROMPT.txt. The batches show the two candidate answers as
#   version_X / version_Y in seeded random order and never say which pass made which; the mapping (x_is) is only in cmp/items.json, which the subagents never see.
#   Decisions are X / Y / NEITHER / CONTESTED. label-final prints pass_c_agreement (agreement with A and with B separately, X vs Y position counts).
python -m tt.cli label-final data/labels/testA_passA.json data/labels/work/testA/cmp/items.json data/labels/work/testA/cmp/passC data/labels/testA_silver.json --pdf-dir data/testA_raw
shasum -a 256 data/labels/testA_silver.json    # record in reports/phase_6_labels.md, then: git add data/labels && git commit

# 3. model runs (4B q4_K_M, prompt v2), one pass each, never repeated after scores are seen
python -u -m tt.cli dev-bench --model qwen3.5:4b-q4_K_M --labels data/labels/testA_silver.json --pdf-dir data/testA_raw --prompt v2 --out runs/testA_4b_v2_run1.jsonl
python -u -m tt.cli dev-bench --model qwen3.5:4b-q4_K_M --labels data/labels/testA_silver.json --pdf-dir data/testA_raw --prompt v2 --temperature 0.5 --seed 1 --out runs/testA_4b_v2_run2.jsonl

# 4. evaluation (same code as dev; only the data paths differ)
export TT_PDF=data/testA_raw TT_GOLD=data/labels/testA_silver.json TT_CACHE=runs/testA_cache.pkl
TT_B2="B2_4b_v2=runs/testA_4b_v2_run1.jsonl" python -m tt.eval.phase3 reports/phase_6_testA_phase3.json
TT_RUN1=runs/testA_4b_v2_run1.jsonl TT_RUN2=runs/testA_4b_v2_run2.jsonl python -m tt.eval.phase4 reports/phase_6_testA_phase4.json
TT_INJ_REPORT=reports/phase_6_injection.json python -m tt.eval.endpoints reports/phase_6_testA_endpoints.json   # after step 5; H1, H2, H5, H4 (+ Clopper-Pearson bound), exploratory agent-vs-B1 with coverage

# 5. held-out injection (30 attacks, two runs, then score)
export TT_ATTACKS=config/injection_heldout_v1.json TT_INJ_TAG=testA_inject TT_INJ_REPORT=reports/phase_6_injection.json
python -u -m tt.agent.inject run qwen3.5:4b-q4_K_M runA; python -u -m tt.agent.inject run qwen3.5:4b-q4_K_M runB; python -m tt.agent.inject score
```
Test-B and unseen-filer: repeat steps 1-4 with their ID files and `testB_*` / `unseen_*` names (and their own TT_* paths).
Wall-clock estimate from dev (apps open): about 45 s per filing per run, so about 2.5 h per run for 200 filings, 1.3 h for 100.
Write `reports/phase_6.md` with every number from the JSON files, all intervals, the exclusions, the contested counts and the deviations list.
