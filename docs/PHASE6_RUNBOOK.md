# Phase 6 runbook (run only after the owner approves and `scripts/freeze.py` has been run)

All commands from the repo root with the venv active. All labels are silver (AI-made, AI-cross-checked, not human-verified); say so in every output.
Order matters: **label first, then run models.** Do not read model outputs while labelling. Fetching is 1 request per second with the identifying user agent; stop on 401/403/429.
Replace `testA` by `testB` / `unseen` for the other splits (file names `data/splits/{testA_labelled,testB,unseen_filer}_ids.txt`).

```
# 1. fetch latest versions (IDs only come from the frozen split files)
python -m tt.cli split-fetch data/splits/testA_labelled_ids.txt data/testA_raw data/processed/testA_573.jsonl
python -m tt.cli parse-report --folder data/testA_raw --out reports/parse_report_testA.md
python -m tt.cli label-select data/testA_raw data/splits/testA_labelled_ids.txt config/testA_selection.json

# 2. silver labels (same three-pass protocol as dev)
python -m tt.cli pass-a --selection config/testA_selection.json --drafts "" --pdf-dir data/testA_raw --out data/labels/testA_passA.json
python - <<'PY'
import json; json.dump([f["file"] for f in json.load(open("config/testA_selection.json"))["filings"]], open("runs/testA_files.json","w"))
PY
python -m tt.cli label-export runs/testA_files.json runs/testA_passB --pdf-dir data/testA_raw
#   Pass B: one blind subagent per batch dir, prompt docs/PASS_B_PROMPT.txt ({DIR} = the batch dir); check each files_seen.txt
python -m tt.cli label-compare data/labels/testA_passA.json runs/testA_passB runs/testA_cmp --pdf-dir data/testA_raw
#   Pass C: one subagent per runs/testA_cmp/passC/batch_N, prompt docs/PASS_C_PROMPT.txt
python -m tt.cli label-final data/labels/testA_passA.json runs/testA_cmp/items.json runs/testA_cmp/passC data/labels/testA_silver.json --pdf-dir data/testA_raw
shasum -a 256 data/labels/testA_silver.json    # record in reports/phase_6_labels.md, then: git add data/labels && git commit

# 3. model runs (4B q4_K_M, prompt v2), one pass each, never repeated after scores are seen
python -u -m tt.cli dev-bench --model qwen3.5:4b-q4_K_M --labels data/labels/testA_silver.json --pdf-dir data/testA_raw --prompt v2 --out runs/testA_4b_v2_run1.jsonl
python -u -m tt.cli dev-bench --model qwen3.5:4b-q4_K_M --labels data/labels/testA_silver.json --pdf-dir data/testA_raw --prompt v2 --temperature 0.5 --seed 1 --out runs/testA_4b_v2_run2.jsonl

# 4. evaluation (same code as dev; only the data paths differ)
export TT_PDF=data/testA_raw TT_GOLD=data/labels/testA_silver.json TT_CACHE=runs/testA_cache.pkl
TT_B2="B2_4b_v2=runs/testA_4b_v2_run1.jsonl" python -m tt.eval.phase3 reports/phase_6_testA_phase3.json
TT_RUN1=runs/testA_4b_v2_run1.jsonl TT_RUN2=runs/testA_4b_v2_run2.jsonl python -m tt.eval.phase4 reports/phase_6_testA_phase4.json

# 5. held-out injection (30 attacks, two runs, then score)
export TT_ATTACKS=config/injection_heldout_v1.json TT_INJ_TAG=testA_inject TT_INJ_REPORT=reports/phase_6_injection.json
python -u -m tt.agent.inject run qwen3.5:4b-q4_K_M runA; python -u -m tt.agent.inject run qwen3.5:4b-q4_K_M runB; python -m tt.agent.inject score
```
Test-B and unseen-filer: repeat steps 1-4 with their ID files and `testB_*` / `unseen_*` names (and their own TT_* paths).
Wall-clock estimate from dev (apps open): about 45 s per filing per run, so about 2.5 h per run for 200 filings, 1.3 h for 100.
Write `reports/phase_6.md` with every number from the JSON files, all intervals, the exclusions, the contested counts and the deviations list.
