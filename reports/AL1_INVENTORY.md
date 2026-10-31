# AL-1 Step 0: amendment lineage inventory

Counts from listing metadata and a 5-PDF download probe. No chronology was opened or compared, no model was run, and nothing frozen changed.
Script: `scripts/al1_inventory.py`. Data: `reports/al1/AL1_INVENTORY.json`, `reports/al1/AL1_SAMPLE_PLAN.json` (sampled IDs and URLs), `reports/al1/AL1_PROBE.json`.

**Definition.** A "version" is one Part 573 document in the cached API listing, selected by the existing `tt.fetch.api.list_573` rule. Dates are the API's `loadDate`, which is the upload date and not the filing date. Year and type come from the flat file (RCDATE, RCLTYPECD), as in `reports/SN1_INVENTORY.md`.

## 1. Version counts

6,685 campaigns hold 14,219 Part 573 documents. **3,891 campaigns (58.2%) have >= 2 documents.**

Many documents share a load timestamp, so the table also counts distinct load days. Every timestamp tie falls on a single day, so 3,476 campaigns (52.0%) have >= 2 distinct load days. The other 415 campaigns with >= 2 documents have all of them on one day, so the listing gives no order for them.

| Per campaign | Documents: campaigns | Share | Distinct load days: campaigns | Share |
|---|---:|---:|---:|---:|
| 0 | 17 | 0.3% | 17 | 0.3% |
| 1 | 2,777 | 41.5% | 3,192 | 47.7% |
| 2 | 1,980 | 29.6% | 2,164 | 32.4% |
| 3 | 1,001 | 15.0% | 839 | 12.6% |
| 4 | 490 | 7.3% | 304 | 4.5% |
| 5 | 228 | 3.4% | 106 | 1.6% |
| 6 | 89 | 1.3% | 34 | 0.5% |
| 7 | 50 | 0.7% | 15 | 0.2% |
| 8 or more (max 16 documents, 13 days) | 53 | 0.8% | 14 | 0.2% |

Share of campaigns with >= 2 documents:

| Year | All: >= 2 / campaigns | Share | Vehicle | Share | Equipment | Share |
|---|---:|---:|---:|---:|---:|---:|
| 2020 | 462 / 867 | 53.3% | 404 / 782 | 51.7% | 58 / 85 | 68.2% |
| 2021 | 746 / 1,069 | 69.8% | 676 / 978 | 69.1% | 70 / 91 | 76.9% |
| 2022 | 681 / 1,030 | 66.1% | 598 / 933 | 64.1% | 83 / 97 | 85.6% |
| 2023 | 614 / 988 | 62.1% | 542 / 894 | 60.6% | 72 / 94 | 76.6% |
| 2024 | 598 / 1,059 | 56.5% | 524 / 950 | 55.2% | 74 / 109 | 67.9% |
| 2025 | 496 / 970 | 51.1% | 446 / 891 | 50.1% | 50 / 79 | 63.3% |
| 2026 (to 10-09) | 294 / 702 | 41.9% | 268 / 643 | 41.7% | 26 / 59 | 44.1% |
| **All** | **3,891 / 6,685** | **58.2%** | **3,458 / 6,071** | **57.0%** | **433 / 614** | **70.5%** |

Recent years are right-censored, because their campaigns have had less time to be amended.

Gap between first and last load date:

| Campaigns | n | Median (days) | Q1 | Q3 | IQR | Max |
|---|---:|---:|---:|---:|---:|---:|
| >= 2 documents (same-day groups count as 0) | 3,891 | 47 | 13 | 120 | 107 | 2,154 |
| >= 2 distinct load days | 3,476 | 55 | 24 | 138 | 114 | 2,154 |

## 2. Sample plan v1 (superseded by section 5, never fetched)

- **Frame:** >= 2 documents, excluding the union of `dev_ids`, `testA_ids`, `testA_labelled_ids`, `testB_ids` and `unseen_filer_ids` (1,500 distinct IDs). The labelled and unseen-filer lists are subsets of Test-A. The exclusion removes 697 campaigns, leaving **3,194**. The injection fixture lists no campaign IDs.
- **Draw:** 300 campaigns, random with seed 0, stratified by RCDATE year. Allocation is proportional to the frame, by largest remainder. The request did not specify the allocation; this is the rule Test-A used.
- **Overlap with the exclusions:** 0.

| Year | Frame | Sample |
|---|---:|---:|
| 2020 | 433 | 41 |
| 2021 | 714 | 67 |
| 2022 | 647 | 61 |
| 2023 | 417 | 39 |
| 2024 | 417 | 39 |
| 2025 | 337 | 32 |
| 2026 | 229 | 21 |
| **All** | **3,194** | **300** (266 V, 34 E) |

**Fetch estimate:**

| | |
|---|---:|
| Part 573 documents in the 300 campaigns | 883 |
| Already in `~/tiertrace_sn1_cache` (one per campaign) | 300 |
| **PDFs needed** | **583** |
| of which strictly earlier than the campaign's latest timestamp | 510 |
| of which tied with the latest timestamp | 73 |
| Already fetched by the probe (section 3) | 5 |
| Still to fetch | 578 |
| **Time at 1.05 s spacing** | **about 10.1 minutes** (578 × 1.05 s = 607 s, minimum) |
| Disk, at the SN-1 mean of 266 KB per PDF | about 154 MB |

The time is a floor. SN-1 ran at its floor (2.1 s for two requests), so it should be close. Only the PDF host is contacted, because all listings are cached. Target: `~/tiertrace_al1_cache`.

## 3. Download probe (5 campaigns)

The 5 campaigns are from the sample, one each from 2020, 2021, 2023, 2025 and 2026, chosen with seed 0 among campaigns with a strictly earlier version. Each fetch took the campaign's earliest uncached version, used the project user agent and a robots.txt check, and was spaced at least 1.05 s apart. Only the first four bytes were inspected, and the files were saved unopened to `~/tiertrace_al1_cache/cache`.

| Campaign | File | Loaded | HTTP | Content type | Bytes | `%PDF` header |
|---|---|---|---:|---|---:|---|
| 20V466 | RCLRPT-20V466-5022.PDF | 2020-08-22 | 200 | application/pdf | 213,532 | yes |
| 21V782 | RCLRPT-21V782-9448.PDF | 2021-10-13 | 200 | application/pdf | 236,574 | yes |
| 23V694 | RCLRPT-23V694-5195.PDF | 2023-10-25 | 200 | application/pdf | 213,989 | yes |
| 25E043 | RCLRPT-25E043-0159.pdf | 2025-07-15 | 200 | application/pdf | 458,364 | yes |
| 26V230 | RCLRPT-26V230-6760.pdf | 2026-04-21 | 200 | application/pdf | 295,502 | yes |

All 5 are downloadable, with no block. Five files cannot show the failure rate across the 578. SN-1 found NHTSA can return a 125-byte `NO SUCH ENTITY` body in place of a PDF, so the full fetch must check the header and not rely on the HTTP status. `24E028` and `24V528`, the two known cases, are not in plan v1.

**Correction (Step 0b):** the code did not pace the first PDF request against the robots.txt request just before it, so that one gap may have been under 1.05 s. This applies to this probe and to the Step 0b fetch run. Both code paths are now fixed.

## 4. Limits of the listing metadata

These matter for AL-1 and were not resolved here.

- **Tied timestamps.** 1,447 campaigns have at least one tied timestamp. Documents with the same timestamp cannot be ordered from the listing, and without opening them we cannot tell whether they are duplicates.
- **"Latest" is arbitrary for 859 campaigns in SN-1.** Their latest timestamp is tied, and `list_573` then takes whichever tied document the listing returned last. So the SN-1 PDF for these campaigns is one of a same-timestamp group, not a demonstrated latest version. 58 of the 300 sampled campaigns are affected. Nothing in SN-1 was changed.
- **No order at all in 27 sampled campaigns.** All their documents share one load day (337 in the frame). Requiring >= 2 distinct load days would shrink the frame to 2,857. The plan follows the requested >= 2 versions rule and keeps them.
- **Load date is a proxy for filing date.** 4,648 documents carry a date in their summary label. The absolute difference from the load date has a median of 3 days (IQR 2 to 7), and 3,635 (78.2%) are within 7 days. The maximum of 10,947 days suggests label typos.
- **Amendment labels mostly agree with load order.** Of 546 campaigns with >= 2 numbered amendments, 11 have a higher number loaded strictly before a lower one. In 159 campaigns the earliest document is labelled as an amendment (by array order among ties), so the original may be missing or tied.
- **No check of completeness.** The listing may not hold every version ever filed. 17 campaigns have no Part 573 document at all.

## 5. Step 0b: resample

**Reason:** version order must be knowable, and in 337 campaigns of the v1 frame every document shares one load day. Eligibility now requires >= 2 distinct load days.

| | Plan v1 (`AL1_SAMPLE_PLAN.json`) | Plan v2 (`AL1_SAMPLE_PLAN_v2.json`) |
|---|---|---|
| Eligibility | >= 2 documents | >= 2 documents on >= 2 distinct load days |
| Frame, after dev/test exclusions | 3,194 | **2,857** |
| Draw | 300, seed 0, proportional by RCDATE year | same |
| Sample, 2020 to 2026 | 41, 67, 61, 39, 39, 32, 21 | 41, 69, 60, 39, 39, 31, 21 |
| Vehicle / equipment | 266 / 34 | 269 / 31 |
| Documents | 883 | 956 |
| Status | Superseded, not fetched | **Fetched** |

28 campaigns are in both plans. Plan v2 has 0 overlap with the dev and test IDs. `24V528` is in plan v2.

## 6. Step 0b: fetch

| | |
|---|---:|
| Part 573 documents in the 300 campaigns | 956 |
| Fetched over HTTP, accepted (status 200 and `%PDF`) | 655 |
| Copied from the SN-1 cache, SHA-256 verified against the SN-1 manifest | 299 |
| Reused from the Step 0 probe | 1 |
| **NON_PDF** | **1** |
| PDF requests | 657 |
| Successful retries | 0 |
| 401, 403, 429 | 0 |
| Network errors | 0 |
| Main run | 07:11:57 to 07:23:49 UTC, 2026-10-31 (11 min 52 s) |
| Files on disk / bytes | 959 / 234,054,598 |

- **NON_PDF:** `RCLRPT-24V528-5855.PDF`, the campaign's latest listed document. Both tries returned HTTP 200 and 125 bytes, beginning `<html><title>NO SUCH ENTITY</title><body>There is no such recall id or contact id. Please check and `. The SN-1 copy is the same kind of reply, so it was not reused.
- **Probe leftovers:** 4 files from the Step 0 probe are not in plan v2 (`20V466`, `23V694`, `25E043`, `26V230`). They remain on disk and are marked `in_sample: false` in the manifest, which is why the disk holds 959 files and the sample 955.
- **Case collision:** `22V173` lists two different documents, `RCLRPT-22V173-7909.pdf` and `RCLRPT-22V173-7909.PDF`. This disk is case-insensitive, so the main run treated the second as already cached. It was then fetched separately (HTTP 200, different bytes) and saved as `..._RCLRPT-22V173-7909__casevariant.PDF`. Across all listings, 3 campaigns have such URL pairs (`21V174`, `21V187`, `22V173`), and any future fetch of all versions must handle them.

**Manifest:** `~/tiertrace_al1_cache/al1_manifest.json`, SHA-256 `000b497cb6c54457e5e034b6703ca49c921f798ad9430a06158d459599947511`.

## 7. Step 0b: ordering metadata

Only the `Submission Date` line of page 1 was kept. Page text was matched in memory and discarded, and no chronology was read, parsed or compared. Versions are ordered by Submission Date, then load timestamp. A remaining tie makes the campaign ORDER_AMBIGUOUS. A usable document with no readable date also does, because it cannot be placed by the rule.

| Status | Campaigns |
|---|---:|
| **Ordered** | **249** |
| of which every listed document is a usable PDF | 248 |
| of which one document is NON_PDF (`24V528`) | 1 |
| **ORDER_AMBIGUOUS** | **51** |
| same date and same load timestamp, different bytes | 47 |
| no readable Submission Date (no text layer) | 4 |
| **ORIGINAL_MISSING** | **0** |
| **NON_PDF** (1 document) | **1** |
| **Total** | **300** |

ORIGINAL_MISSING and NON_PDF are flags and overlap the order statuses.

| Year | Sample | Ordered |
|---|---:|---:|
| 2020 | 41 | 34 |
| 2021 | 69 | 57 |
| 2022 | 60 | 51 |
| 2023 | 39 | 31 |
| 2024 | 39 | 30 |
| 2025 | 31 | 26 |
| 2026 | 21 | 20 |

Notes:

- **Documents:** of 955 usable PDFs, 951 have exactly one Submission Date and 4 have no text layer on page 1 (`22V173`, `25V063`, `25V680`, `26V219`). No OCR was run.
- **ORIGINAL_MISSING rule:** a campaign is flagged if every document tied for earliest is labelled as an amendment. Ties need this rule because their array order is arbitrary. Literally taking the first document in the listing would flag 12 campaigns, and 22 have an amendment label somewhere in the earliest load-timestamp group, but none has only amendment labels there. For the 4 no-date campaigns the check uses load order. The flag does not detect missing intermediate amendments, and the 159 in section 4 came from array order and overstates the same way.
- **The 47 tied campaigns:** the tie touches the latest position in 17, the earliest in 15, and only middle positions in 15. All have at least 2 distinct positions.
- **Tiebreak:** in 16 ordered campaigns, at least two versions share a Submission Date and only the load timestamp separates them.
- **Date versus load order:** the two disagree in 12 campaigns.
- **`24V528`:** its order covers only its 2 usable documents. The missing one is the latest listed, so the campaign has no usable latest version.
