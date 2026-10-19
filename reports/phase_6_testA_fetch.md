# Phase 6 Test-A (labelled, 200 campaigns): fetch ledger (2026-10-19)
- Listed: 200/200 campaigns have Part 573 documents (382 versions in all; latest version of each is evaluated); downloaded 200/200 latest versions; 0 failed; no 401/403/429/5xx. Fetch rate 1 request/s with the identifying user agent. API requests: 200.
- Multi-version campaigns: 100 have 1 version, 100 have 2 to 10.
- Readable (text layer, header parsed): 199. **Excluded as unreadable: 1** — 23V313 (`RCLRPT-23V313-1055.PDF`, 3 pages, 0 characters of text, scanned; the campaign has only one version, so the earlier-version fallback does not apply). No OCR in v1. It is counted as "unreadable" in every Test-A table and is never replaced.
- Note: `label-select` did not list 23V313 under its `unreadable` field (it skips a file whose header cannot be parsed before the length check), so `config/testA_selection.json` shows `"unreadable": []`; this ledger is the record. Logged in reports/DEVIATIONS.md (D-T1).
- Listing: `data/labels/work/testA/listing.jsonl`.
