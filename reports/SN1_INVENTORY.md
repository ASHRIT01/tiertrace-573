# SN-1 Step 0: data inventory

Counts and downloads only. No supplier blocks parsed, no network statistic computed, no model run. Nothing frozen changed.
Script: `scripts/sn1_inventory.py` (aggregates in `reports/sn1/SN1_INVENTORY.json`); fetcher: `scripts/sn1_fetch.py`.

## 1. Recall campaigns, RCDATE 2020-01-01 to latest

Source: `data/flat/FLAT_RCL_POST_2010.zip` (user-supplied, file dated 2026-10-18; 246,109 rows; latest RCDATE **2026-10-09**).
This file was not re-downloaded. If a fresher copy is wanted, replace it and rerun both scripts.
A campaign is the 6-character id (e.g. `24V418`); the flat file has one row per make/model/year/component.
Every campaign has a single RCLTYPECD across its rows.

**6,798 campaigns** since 2020-01-01.

| Year | Campaigns |
|---|---|
| 2020 | 881 |
| 2021 | 1,084 |
| 2022 | 1,051 |
| 2023 | 1,000 |
| 2024 | 1,073 |
| 2025 | 994 |
| 2026 (to 10-09) | 715 |

| RCLTYPECD | Campaigns |
|---|---|
| V (vehicle) | 6,071 |
| E (equipment) | 614 |
| T (tire) | 83 |
| C (child restraint) | 30 |

Year by type is in the JSON. **Scope choice:** "vehicle and equipment" was read as RCLTYPECD V and E, so the fetch set is
**6,685 campaigns**. The 113 tire and child-restraint campaigns (T, C) are listed above but are not being downloaded;
adding them is about 113 × 2 requests. Say if they should be in.

## 2. Part 573 report PDFs (RCLRPT, latest version)

URLs come from the existing `tt.fetch.api.list_573` (api.nhtsa.gov `safetyIssues/byNhtsaId`, "latest" = latest `loadDate`),
PDFs from `tt.fetch.nhtsa.PoliteFetcher` into the existing gitignored `data/cache/`. User-agent is the project's honest one
(`TierTrace-573 research crawler (contact: ...)`), no browser imitation. API and PDF calls share one clock, 1.05 s apart at minimum.
Already-cached API listings and PDFs are skipped without a request. A 401/403/429 stops the run. Failures go to `runs/sn1_failures.jsonl`.
Rerunning `python scripts/sn1_fetch.py` resumes. The log is `runs/sn1_fetch.log` (progress line every 100 campaigns).

Launched 2026-10-28 07:41 UTC in the background under `caffeinate -i`.

Snapshot at 2026-10-28 07:50 UTC (about 9 minutes in):

| | |
|---|---|
| PDFs in `data/cache` | 1,143 (1,103 before this phase, which were mostly 2015-2019 audit and test samples) |
| API listings in `data/api_cache` | 1,150 |
| Disk, `data/cache` / `data/api_cache` | 303 MB / 37 MB |
| Failures so far | 2, both "no Part 573 document in the API listing" (`20E002`, `20E051`); no HTTP errors, no blocks |

**Expected download time.** The rate limit alone would give about 3.8 h (6,685 campaigns × 2 requests at 1/s). Measured
throughput is far lower, about 4-7 campaigns per minute, because the project drive is a FAT (msdos) volume whose small
writes take 0.7-8 s each (the fetcher sits in uninterruptible disk wait; NHTSA responds in about 0.6 s). At that rate expect
**roughly 16-28 hours**. Average PDF size so far is about 0.27 MB, so the 6,685 PDFs should add about 1.8 GB (28 GB free).
Moving `data/cache` and `data/api_cache` to the internal disk would bring it near the 3.8 h floor; I have not done that
because it changes the cache location.

## 3. Investigations flat file

| | |
|---|---|
| URL | https://static.nhtsa.gov/odi/ffdd/inv/FLAT_INV.zip (dictionary: .../inv/INV.txt) |
| Downloaded | 2026-10-28 07:42 UTC, HTTP 200, project user-agent |
| Saved as | `data/inv/FLAT_INV_2026-10-28.zip` (4,303,076 bytes; contains `FLAT_INV.txt`, 390,689,692 bytes, member dated 2026-10-27), `data/inv/INV_2026-10-28.txt` (gitignored; hashes below) |
| SHA-256 zip | `eeebbb92e86305d06fd8c1a0c3d599785961a2dc3f8c7921b587e0cf23c193f7` |
| SHA-256 INV.txt | `04d3eef957004ff6d235ffbefe1ab270be27b72c1671ca5c3e8cfa96951bf8d2` |

- **Rows: 154,455** (all 11 fields). The file has one row per make/model/year, so this is not the investigation count.
- **Distinct investigations (NHTSA action numbers): 5,354.** 108 have a blank open date. Latest open date 2026-10-23.
- **Opened 2015 to now: 456 investigations** (2015: 65, 2016: 28, 2017: 33, 2018: 34, 2019: 34, 2020: 31, 2021: 35, 2022: 27, 2023: 42, 2024: 58, 2025: 37, 2026: 32).
- Investigations carrying a CAMPNO: 1,551 of all; **177 of the 456** opened since 2015.
- CAMPNO is 6 or 9 characters; it is normalised to the 6-character campaign id.
- **Join to the step-1 campaigns (6,798, any type): 171 distinct CAMPNO values**, from 106 investigations opened since 2015.
  168 of the 171 are V or E campaigns, i.e. inside the fetch set. All 171 come from investigations opened 2015 or later.
- 467 distinct campaign ids are linked from investigations opened since 2015; the other 296 are pre-2020 campaigns.
- Some old CAMPNO values are not recall-style ids (e.g. `00I002000`, `01I004000`); they cannot join and are ignored.

## Limits

- The recall flat file is the local copy of 2026-10-18; campaigns filed after 2026-10-09 are not in it.
- "Latest version" depends on the API's `loadDate`; campaigns with no Part 573 document in the API listing are logged as failures, not retried.
- The download figures above are a snapshot; the log and cache are the live record. Final counts will be appended when the run finishes.
