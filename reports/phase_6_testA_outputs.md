# Phase 6 Test-A model outputs (not scored, not inspected)
Frozen model qwen3.5:4b-q4_K_M, prompt v2, think off, num_ctx 6144, 199 filings (23V313 unreadable, excluded). Runner scripts/phase6_run.py; amendment-1.
| file | records | SHA-256 |
|---|---|---|
| runs/testA_4b_v2_run1.jsonl | 199 | 1979a89b69e45e86362681b17e8a93dbeb8f90a3a6d0be169bdb0fbd806832f8 |
| runs/testA_4b_v2_run2.jsonl (after the one retry) | 199 | a5705ea365dbd19b1258f5e2967ae2843324af8b95e920f45a3ea62821d12ee3 |
| runs/testA_4b_v2_run2.pre_retry.jsonl (as the run ended) | 199 | 7ecd9fbabf0847b2d0cc65fa479636aa1fb857100d1b536b00e0622a3f42e24a |
Run 1: JSON-valid 199/199. Run 2: 195/199 after the retry (194/199 before), 4 timeouts. Restart log: runs/testA_run_log.txt (sha256 of the file at this commit is in git).
