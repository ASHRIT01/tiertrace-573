# Page-furniture leakage fix: before and after

AI-checked, not human-verified. Fix: tt/parse/sections.py clean() removes the stacked-layout page-header block as one unit and
'Page N' / 'Page' + newline + 'N' / 'Page N of M' lines; parse_header() now reads the raw text. No special cases; verifier.py untouched.
Detector (tt/parse/leak.py) looks for page furniture in the final cause/chronology/defect/risk text, independently of the cleaning patterns.

## All 300 sampled filings (latest versions)

- Filings with leakage: **before 25, after 0**.
- Before, by kind: header block in risk 13, defect 3, cause 2; 'Page N' marker in cause 4, chronology 1, defect 1, risk 1.
- Regression check (old sections.py from git vs new, all 300): every changed section is a pure deletion (41 page markers, 21 header blocks); 0 other edits.
- Side finding: in 4 filings the block's parsed *country* contained a page marker (e.g. 'United States Page 2'); fixed. Supplier names unchanged.
- Field fill: 2015 cause fill 64% -> 60% (one cause section was only a leaked page marker).

## 20 fresh filings (not in the checksheet, the debug list or any earlier report; chosen before the fix)

10 had leakage before (1 page marker, 9 header block); 10 had none (regression control).

| file | before | after |
|---|---|---|
| RCLRPT-15V116-5346.PDF | risk:page_marker | none |
| RCLRPT-25V055-8002.pdf | risk:dot_header+header_fields | none |
| RCLRPT-26V161-4285.pdf | risk:dot_header+header_fields | none |
| RCLRPT-26V622-0796.pdf | defect:dot_header+header_fields | none |
| RCLRPT-25V373-7837.pdf | risk:dot_header+header_fields | none |
| RCLRPT-26V601-9878.pdf | risk:dot_header+header_fields | none |
| RCLRPT-25V305-2682.pdf | risk:dot_header+header_fields | none |
| RCLRPT-25V761-4355.pdf | risk:dot_header+header_fields | none |
| RCLRPT-26V181-3625.pdf | risk:dot_header+header_fields | none |
| RCLRPT-26V211-1872.pdf | cause:dot_header+header_fields | none |
| RCLRPT-24V351-2385.PDF | none | none |
| RCLRPT-25V188-2594.PDF | none | none |
| RCLRPT-24V375-6263.PDF | none | none |
| RCLRPT-21V440-7992.PDF | none | none |
| RCLRPT-17V592-8612.PDF | none | none |
| RCLRPT-18V207-5155.PDF | none | none |
| RCLRPT-20V708-7541.PDF | none | none |
| RCLRPT-16V455-4491.PDF | none | none |
| RCLRPT-26V452-8085.pdf | none | none |
| RCLRPT-21V744-1366.PDF | none | none |

Fresh 20: leaking before **10**, after **0**; the 10 clean controls stayed clean.

## Checksheet cases (tuned-on, NOT fresh)

#4 15V682, #6 16V100, #7 16V268 ('Page 2' in cause) and #46 25V757 (header block in cause): all four causes now read correctly (checked by printing the new cause).

## Limits

- The fresh sample has 1 page-marker case; the page-marker fix rests on that, the 300 scan and 3 checksheet cases.
- The detector only knows the furniture patterns I listed; other leakage would not be seen.
- Not rendered to images after the fix: marks are from the parsed text and the earlier visual check.