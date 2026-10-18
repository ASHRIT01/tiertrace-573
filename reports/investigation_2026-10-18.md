# Investigation of two suspicious audit results (sample of 300 latest-version filings)

## (a) "Chronology filled 100% every year" -- real content, but the metric was too loose
The audit counted any non-empty string. Opened 5 PDFs with very short chronologies (16V493, 16E056, 18V052, 19V182, 16V375):
the source itself says `research`, `NR`, `See File: Recall H056 Chronology.`, `See attached chronology dated March 8, 2019.`,
`A recall letter was received from Ricon Corporation. 16E020`. Parser output matched the source in all 5. 24 of 300 are under 60 chars.
With a stricter rule (>=100 chars and not a pointer/NR), 257/300 (86%) have a substantive chronology (by year: 2015 23/25, 2016 19,
2017 21, 2018 21, 2019 21, 2020 20, 2021 22, 2022 18, 2023 22, 2024 22, 2025 24, 2026 24).
"See attached" chronologies are NOT inside the PDF (19V182 is 96k chars and does not contain it).

## (b) "Cause fill rate identical to supplier-name fill rate" -- not identical; coincidence at n=25
Overall: supplier named 222/300, cause stated 210/300. Cross-tab (supplier, cause): (yes,yes) 149, (yes,no) 73, (no,yes) 61,
(no,no) 17; weak negative association (phi about -0.11). They coincide in 3 of 12 years (2021, 2022, 2026), expected by chance with
25 filings per year. Cause not stated = 79 `NR` + 11 empty. Opened 5 of the 11 empty (25V667, 25V813, 25V653, 25V581, 25V472): in the
source the "Description of the cause:" line is blank, so it is the filer's own content, not a parser miss.
