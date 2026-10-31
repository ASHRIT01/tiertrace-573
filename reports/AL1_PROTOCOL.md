# AL-1 protocol (amendment lineage)

**Status: incomplete.** This file holds only the rules fixed so far. The rest of the protocol follows the prior-art check. No chronology has been opened, parsed or compared.

Source of all campaign sets: `reports/al1/AL1_ORDER.json`, SHA-256 `29e181b5b064bf1cde6844b46377faf530b9462430ea79f98d839c1fce434f17`.

## Analysis sets

| Set | Rule | Campaigns |
|---|---|---:|
| Ordered | `order_status` is `ORDERED` | 249 |
| **Primary** | Ordered minus `24V528`, whose latest listed document is NON_PDF | **248** |
| **Sensitivity** | Primary minus sets (a) and (b) below; a rerun of the primary analysis | **228** |

The 51 `ORDER_AMBIGUOUS` campaigns are in neither set.

**(a) Only the load timestamp separates versions (16).** Ordered campaigns where at least two usable versions share a Submission Date (`same_date_broken_by_load`):

20V016, 20V322, 21V155, 22E052, 22V307, 22V523, 23V380, 23V707, 23V797, 24V459, 24V661, 24V712, 24V833, 26E023, 26V519, 26V546

**(b) Submission Date order and load order disagree (12).** Campaigns where a version with a strictly earlier load timestamp has a strictly later Submission Date (`date_order_differs_from_load`):

- In the primary set, so dropped by the sensitivity rerun (8): 21V758, 21V841, 24V459, 24V661, 24V833, 25V080, 25V375, 26V546
- `ORDER_AMBIGUOUS`, so already outside the primary set (4): 20V059, 20V396, 21V189, 21V782

**Arithmetic.** Sets (a) and (b) share 4 primary campaigns (24V459, 24V661, 24V833, 26V546), so the rerun drops 16 + 8 - 4 = 20 distinct campaigns: 248 - 20 = 228. `24V528` is in neither set.

## Data handling

- **Case-colliding URLs.** `21V174`, `21V187` and `22V173` each list PDF URLs differing only in filename case. Any later all-versions fetch must store them as separate files on a case-insensitive disk. `22V173` is already handled in `~/tiertrace_al1_cache`; the other two are not in the current sample.
- **No OCR.** No OCR is run on the 4 no-text-layer PDFs (`22V173`, `25V063`, `25V680`, `26V219`). All 4 campaigns are `ORDER_AMBIGUOUS`, so they are outside both analysis sets.
