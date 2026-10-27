# H6 measurement choice (fixed before any H6 measurement)
The frozen H6 (valid JSON >= 0.95, p95 <= 120 s, clean hardware) does not name the filings or say how to treat the first call.
- Command: the reports/phase_2.md dev-bench on the 100 dev filings (qwen3.5:4b-q4_K_M, prompt v2, temperature 0).
- Output: runs/H6_clean_4b.jsonl, log in reports/H6_hw_report.md.
- The verdict p95 INCLUDES the first cold-load call (the stricter reading); p95 without it is also reported.
- Clean condition: Claude Code, VS Code and other apps closed; Chrome Remote Desktop session disconnected (its host service stays installed, idle); AC power; started from Terminal.app with caffeinate.
