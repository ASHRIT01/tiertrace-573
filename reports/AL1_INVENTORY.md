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

## 2. Sample plan (not fetched)

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

All 5 are downloadable, with no block. Five files cannot show the failure rate across the 578. SN-1 found NHTSA can return a 125-byte `NO SUCH ENTITY` body in place of a PDF, so the full fetch must check the header and not rely on the HTTP status. `24E028` and `24V528`, the two known cases, are not in the sample.

## 4. Limits of the listing metadata

These matter for AL-1 and were not resolved here.

- **Tied timestamps.** 1,447 campaigns have at least one tied timestamp. Documents with the same timestamp cannot be ordered from the listing, and without opening them we cannot tell whether they are duplicates.
- **"Latest" is arbitrary for 859 campaigns in SN-1.** Their latest timestamp is tied, and `list_573` then takes whichever tied document the listing returned last. So the SN-1 PDF for these campaigns is one of a same-timestamp group, not a demonstrated latest version. 58 of the 300 sampled campaigns are affected. Nothing in SN-1 was changed.
- **No order at all in 27 sampled campaigns.** All their documents share one load day (337 in the frame). Requiring >= 2 distinct load days would shrink the frame to 2,857. The plan follows the requested >= 2 versions rule and keeps them.
- **Load date is a proxy for filing date.** 4,648 documents carry a date in their summary label. The absolute difference from the load date has a median of 3 days (IQR 2 to 7), and 3,635 (78.2%) are within 7 days. The maximum of 10,947 days suggests label typos.
- **Amendment labels mostly agree with load order.** Of 546 campaigns with >= 2 numbered amendments, 11 have a higher number loaded strictly before a lower one. In 159 campaigns the earliest document is labelled as an amendment (by array order among ties), so the original may be missing or tied.
- **No check of completeness.** The listing may not hold every version ever filed. 17 campaigns have no Part 573 document at all.
