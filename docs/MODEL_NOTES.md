# Model notes (checked 2026-10-18)

## Qwen3.5 release and training cutoff
- The model card (huggingface.co/Qwen/Qwen3.5-4B) states **no training-data or knowledge cutoff**. It gives no release date either; its BibTeX entry says February 2026.
- A secondary source (toolhalla.ai, citing the Qwen repository news log) dates the first Qwen3.5 family release to 16 February 2026 and the 27B to 24 February 2026. **UNVERIFIED** (not read from the Qwen repository directly).
- Consequence: the true data cutoff is UNKNOWN and is probably earlier than the release. For memorisation checks, treat filings submitted **on or after 2026-03-01** (after the release month) as Test-B candidates. Test-A already ends 2026-02-28, so Test-A is not guaranteed free of training-data overlap and the Test-A vs Test-B gap stays the memorisation check.
- Local `ollama show qwen3.5:4b-q4_K_M` (Ollama 0.40.6): 4.2B parameters, Q4_K_M, context 262144, thinking supported with **default on**, default sampling temperature 1, top_p 0.95, top_k 20, presence_penalty 1.5. Our runs must pass `think=False` and `temperature=0` explicitly (tt/agent/run_dev.py does).

## Candidate small models for the dev bake-off (from the Ollama library tag pages; NOT pulled, NOT run)
| tag | download size | context shown | note |
|---|---|---|---|
| qwen3.5:4b-q4_K_M | 3.3 GB (installed) | 256K | main candidate |
| qwen3.5:2b-q8_0 | 2.7 GB (installed) | 256K | fallback |
| llama3.2:3b-instruct-q4_K_M (= llama3.2:3b) | 2.0 GB | 128K | |
| phi4-mini:3.8b-q4_K_M | 2.5 GB | 128K | its q8_0 and fp16 tags list a 4K context: not used |
| gemma3:4b-it-q4_K_M | 3.4 GB | 128K | text and image input |
Sizes are as listed on ollama.com on 2026-10-18; confirm after pulling. Structured-output reliability of each is untested.

## Harness (not run)
`tt/agent/run_dev.py` writes predictions for a model over dev filings with the block masked; `tt dev-score <preds.jsonl>` scores them against the dev label DRAFTS (JSON validity, verifier pass, S2 recovery with a located quote, unsupported-claim rate, event date F1, cause accuracy). The scorer is unit-tested on synthetic predictions only. Scores against unreviewed drafts are not gold results.
