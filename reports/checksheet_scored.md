# Checksheet scores: AI visual check, NOT human-verified

Scored 2026-10-18 by Claude, BEFORE any code change. Two methods, labelled per entry:
- **visual**: the PDF pages were rendered to images and read directly (15 filings: one per year 2015-2026 plus 3 extra stacked-layout 2025-26 filings; 5 of the 15 are stacked).
- **text-only**: marked by comparing the PARSED and SOURCE text windows in reports/checksheet.md; the PDF image was not looked at.
These are AI judgments. Nothing here shows the 90% parser bar is met; the most that can be said is "AI-checked".

## Counts per field

| field | visual (n=15) | text-only (n=35) | all 50 |
|---|---|---|---|
| supplier name | 15 OK / 0 WRONG | 35 OK / 0 WRONG | 50 OK / 0 WRONG |
| cause | 12 OK / 3 WRONG | 34 OK / 1 WRONG | 46 OK / 4 WRONG |
| chronology start | 15 OK / 0 WRONG | 35 OK / 0 WRONG | 50 OK / 0 WRONG |
| tier | 15 OK (blank/absent is correct before 2025; Tier 1 correct on #46, #50) | not marked (window shows 'heading not found' for old forms) | - |

All 4 WRONG marks are in the cause field and are text leakage, not wrong values: page-break marker 'Page 2' in #4, #6, #7 and page-header text in #46.
Chronology marked OK on 5 entries is a pointer or NR in the source (#10, #22, #24, #33, #37): the parser reproduced the source, but the field has no substance.

## Your first-pass findings, and what the check found

| your finding | AI check |
|---|---|
| page-break text ('Page 2') inside cause in #4, #6, #7 | confirmed: #4 and #7 visually (page boundary falls inside/after the cause), #6 from the text window |
| page-header text leaking into cause in #46 | confirmed visually: the true cause is one sentence on page 2; the parsed cause starts with the header block |
| blank cause in #44 | confirmed real: 'Description of the cause:' is visibly blank in the PDF, so the parser is right |
| chronology pointers in #10, #22, #24, #33, #37 | confirmed: all five are NR or 'see attached/separate document' in the source (parsed faithfully) |

## Per-entry marks

| # | file | method | supplier | cause | chronology | note |
|---|---|---|---|---|---|---|
| 1 | RCLRPT-15V370-6865.PDF | text-only | OK | OK | OK | cause is NR in source |
| 2 | RCLRPT-15V547-8443.PDF | text-only | OK | OK | OK |  |
| 3 | RCLRPT-15V619-6612.PDF | text-only | OK | OK | OK |  |
| 4 | RCLRPT-15V682-1265.PDF | visual | OK | WRONG | OK | 'Page 2' page-break marker inside the cause sentence (page 1 ends 'key out of', page 2 starts 'position.') |
| 5 | RCLRPT-15V872-7027.PDF | text-only | OK | OK | OK |  |
| 6 | RCLRPT-16V100-8801.pdf | text-only | OK (blank: Name NR) | WRONG | OK | 'Page 2' marker at the end of the cause (seen in the text window) |
| 7 | RCLRPT-16V268-2446.PDF | visual | OK | WRONG | OK | 'Page 2' marker at the end of the cause; block names an affiliate (Volvo Car Corporation) |
| 8 | RCLRPT-16V343-7282.PDF | text-only | OK | OK | OK | cause NR in source |
| 9 | RCLRPT-16V521-0781.PDF | text-only | OK (blank: Name NR) | OK | OK |  |
| 10 | RCLRPT-17V581-5957.PDF | visual | OK | OK | OK | chronology is literally 'NR' in the source: pointer/NR, faithfully parsed |
| 11 | RCLRPT-17V595-7604.PDF | text-only | OK | OK | OK |  |
| 12 | RCLRPT-17V814-7599.PDF | text-only | OK | OK | OK |  |
| 13 | RCLRPT-17V845-8639.PDF | text-only | OK (blank: Name NR) | OK | OK |  |
| 14 | RCLRPT-18V003-7205.PDF | visual | OK | OK | OK | cause 'N/A' in source |
| 15 | RCLRPT-18V361-6855.PDF | text-only | OK (blank: Name NR) | OK | OK |  |
| 16 | RCLRPT-18V405-6087.PDF | text-only | OK (blank: Name NR) | OK | OK |  |
| 17 | RCLRPT-18V908-5711.PDF | text-only | OK (blank: Name NR) | OK | OK |  |
| 18 | RCLRPT-19E071-8708.PDF | text-only | OK | OK | OK | cause NR in source |
| 19 | RCLRPT-19V069-1382.PDF | text-only | OK (blank: Name NR) | OK | OK |  |
| 20 | RCLRPT-19V146-9045.PDF | visual | OK | OK | OK |  |
| 21 | RCLRPT-19V671-3143.PDF | text-only | OK (blank: Name NR) | OK | OK |  |
| 22 | RCLRPT-20V012-2152.PDF | text-only | OK | OK | OK | chronology is a pointer ('see the attached ... full chronology'), faithfully parsed; cause NR |
| 23 | RCLRPT-20V222-8216.PDF | text-only | OK | OK | OK |  |
| 24 | RCLRPT-20V259-9360.PDF | text-only | OK (blank: Name NR) | OK | OK | chronology is a pointer ('Chronology on a separate document.'), faithfully parsed |
| 25 | RCLRPT-20V381-1401.PDF | text-only | OK | OK | OK |  |
| 26 | RCLRPT-20V668-5029.PDF | visual | OK | OK | OK |  |
| 27 | RCLRPT-21V232-3340.PDF | text-only | OK | OK | OK | block names an affiliate (Mercedes-Benz AG) |
| 28 | RCLRPT-21V289-7210.PDF | text-only | OK | OK | OK | cause NR in source |
| 29 | RCLRPT-21V332-7058.PDF | text-only | OK | OK | OK |  |
| 30 | RCLRPT-21V892-4129.PDF | visual | OK | OK | OK | cause mentions an unnamed sub-supplier |
| 31 | RCLRPT-22V144-8961.PDF | text-only | OK (blank: Name NR) | OK | OK |  |
| 32 | RCLRPT-22V355-9384.PDF | text-only | OK (blank: Name NR) | OK | OK |  |
| 33 | RCLRPT-22V445-7572.PDF | text-only | OK | OK | OK | chronology is a pointer, faithfully parsed; cause NR |
| 34 | RCLRPT-22V701-3469.PDF | visual | OK | OK | OK |  |
| 35 | RCLRPT-23V176-2072.PDF | visual | OK | OK | OK | block names an affiliate (Porsche AG) |
| 36 | RCLRPT-23V464-5088.PDF | text-only | OK | OK | OK | block names an affiliate (Mercedes-Benz AG) |
| 37 | RCLRPT-23V478-2832.PDF | text-only | OK | OK | OK | chronology is a pointer, faithfully parsed; cause NR |
| 38 | RCLRPT-23V728-8027.PDF | text-only | OK (blank: Name NR) | OK | OK |  |
| 39 | RCLRPT-24V043-9157.PDF | visual | OK | OK | OK | chronology has date typos (Jan 2023 after Dec 2023): a V3 case |
| 40 | RCLRPT-24V238-4544.PDF | text-only | OK | OK | OK | cause NR in source |
| 41 | RCLRPT-24V266-5647.PDF | text-only | OK | OK | OK | table shows only the first 200 chars of the cause: remainder not checked |
| 42 | RCLRPT-24V683-8541.PDF | text-only | OK | OK | OK | block names the filer itself |
| 43 | RCLRPT-25V095-1385.PDF | text-only | OK | OK | OK | block names the filer itself |
| 44 | RCLRPT-25V581-3944.pdf | visual | OK (blank) | OK (blank in source) | OK | stacked layout; cause line is visibly blank in the PDF; Name/Tier/Type blank |
| 45 | RCLRPT-25V755-3652.pdf | visual | OK | OK | OK | stacked layout; tier blank in source |
| 46 | RCLRPT-25V757-9752.pdf | visual | OK | WRONG | OK | stacked layout; page-header block text (U.S. Department of Transportation ... Manufacturer Name ... Submission Date) leaks into the start of the cause; Tier 1 / Other correct |
| 47 | RCLRPT-26V002-0368.pdf | text-only | OK | OK | OK | block names the filer itself; cause 'Still under investigation' |
| 48 | RCLRPT-26V061-2359.pdf | text-only | OK | OK | OK | block names the filer itself (Supplier Type OEM) |
| 49 | RCLRPT-26V241-8011.pdf | visual | OK | OK | OK | stacked layout; block names the filer itself |
| 50 | RCLRPT-26V365-8440.pdf | visual | OK | OK | OK | stacked layout; Tier 1 / OEM correct |