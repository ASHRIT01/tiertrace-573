# AI-vs-AI agreement, not human verification

Set A = reports/dev_labels_draft.json (reference); set B = reports/blind_labels_ai.json. Both were produced by AI. Agreement here shows consistency between two AI passes, not correctness.
Filings compared: 5 (#3 15V658-6735., #8 16V870-6167., #12 17V819-6798., #15 18V293-6049., #29 22V374-1195.).
Filings in B with no counterpart in A (not compared): 17V407-6579., 19V843-1571., 20V369-2518., 21V020-7654..

Classes: **same** (all compared fields equal) / **detail** (agree on status, kind or event type; quote span, names list or date_text differs: 'fix') /
**substance** (status, kind or event type differs, or an event exists on one side only: 'no'). Rules: tt/eval/compare_labels.py.

| claim | units | same | differs in detail (fix) | differs in substance (no) |
|---|---|---|---|---|
| S1 | 5 | 5 | 0 | 0 |
| S2 | 5 | 3 | 2 | 0 |
| E | 31 | 24 | 4 | 3 |
| C | 5 | 2 | 3 | 0 |
| U | 5 | 3 | 1 | 1 |
| all | 51 | 37 | 10 | 4 |

## Every difference (A = draft, B = blind)

### E on #3 RCLRPT-15V658-6735.PDF: **substance** — event only in set B
- A: (none)
- B: 'September 22, 2015' INVESTIGATION_START — "September 22, 2015 - Airstream notified of a vehicle inverter smoking at a servicing dealership due to loose cabling connections on the positive side of the electrical system. Airstream opens an investigation on the issue."

### S2 on #8 RCLRPT-16V870-6167.PDF: **detail** — quote span/presence
- A: SUPPORTED — "ARC Automotive, the supplier of the inflator incorporated by Takata into the RSIAB module"
- B: SUPPORTED — "ARC Automotive, the supplier of the inflator incorporated by Takata into the RSIAB module, performed an incorrect off seam inboard weld on the inflator manifold."

### E on #8 RCLRPT-16V870-6167.PDF: **detail** — quote span
- A: 'November 16, 2016' OTHER — "On November 16, 2016, testing of the failed inflator by ARC, the supplier of the inflator to Takata, identified that the failed inflator had ruptured at its manifold as the result of an incorrect off seam inboard weld but that weld inspection, hydro burst testing"
- B: 'November 16, 2016' OTHER — "On November 16, 2016, testing of the failed inflator by ARC, the supplier of the inflator to Takata, identified that the failed inflator had ruptured at its manifold as the result of an incorrect off seam inboard weld"

### C on #8 RCLRPT-16V870-6167.PDF: **detail** — quote span/presence
- A: SUPPORTED — "performed an incorrect off seam inboard weld on the inflator manifold"
- B: SUPPORTED — "performed an incorrect off seam inboard weld on the inflator manifold. The off seam weld caused the inflator to rupture at the manifold."

### U on #8 RCLRPT-16V870-6167.PDF: **detail** — names: ['Takata', 'ARC Automotive'] vs ['Takata']
- A: NAMED ['Takata', 'ARC Automotive'] — "ARC Automotive, the supplier of the inflator incorporated by Takata into the RSIAB module"
- B: NAMED ['Takata'] — "ARC Automotive, the supplier of the inflator incorporated by Takata into the RSIAB module"

### E on #12 RCLRPT-17V819-6798.PDF: **substance** — event only in set B
- A: (none)
- B: 'November 2016' INVESTIGATION_START — "In November 2016, incorrect light distribution values were detected in certain vehicles within the assembly plant. Investigations were initiated to identify potentially affected vehicles."

### S2 on #15 RCLRPT-18V293-6049.PDF: **detail** — quote span/presence
- A: SUPPORTED — "The Shield supplier pre-sourcing evaluation did not fully evaluate supplier quality capability"
- B: SUPPORTED — "The Shield supplier pre-sourcing evaluation did not fully evaluate supplier quality capability and the presence of hydrogen embrittlement in the D-ring bolt."

### C on #15 RCLRPT-18V293-6049.PDF: **detail** — quote span/presence
- A: SUPPORTED — "did not fully evaluate supplier quality capability and the presence of hydrogen embrittlement in the D-ring bolt"
- B: SUPPORTED — "The Shield supplier pre-sourcing evaluation did not fully evaluate supplier quality capability and the presence of hydrogen embrittlement in the D-ring bolt."

### U on #15 RCLRPT-18V293-6049.PDF: **substance** — kind: NAMED vs UNNAMED
- A: NAMED ['Shield'] — "The Shield supplier pre-sourcing evaluation did not fully evaluate supplier quality capability"
- B: UNNAMED  — "04/02/2018 - 04/23/18 – Navistar initiates investigation to understand the scope of the issue with the supplier and their sub suppliers and the impact on International products."

### E on #29 RCLRPT-22V374-1195.PDF: **detail** — date_text: 'May 5, 2022' vs 'On or about May 5, 2022'
- A: 'May 5, 2022' FILER_AWARENESS — "On or about May 5, 2022, DTNA received a notification from its Engineering group that, while testing a specific DTNA owned vehicle that had not been sold to commerce, there was a situation that resulted in an unintended brake application."
- B: 'On or about May 5, 2022' FILER_AWARENESS — "On or about May 5, 2022, DTNA received a notification from its Engineering group that, while testing a specific DTNA owned vehicle that had not been sold to commerce, there was a situation that resulted in an unintended brake application."

### E on #29 RCLRPT-22V374-1195.PDF: **detail** — date_text: 'May 16' vs 'On or about May 16'
- A: 'May 16' OTHER — "On or about May 16, DTNA determined that the occurrence could occur on a population of 4 vehicles, as listed on the prior 573 report."
- B: 'On or about May 16' OTHER — "On or about May 16, DTNA determined that the occurrence could occur on a population of 4 vehicles, as listed on the prior 573 report."

### E on #29 RCLRPT-22V374-1195.PDF: **detail** — quote span; date_text: 'May 18, 2022' vs 'On or about May 18, 2022'
- A: 'May 18, 2022' DECISION — "On or about May 18, 2022, after DTNA verified the limited population of vehicles potentially subject to the defect to the extent necessary to declare a recall and file that 573 report, out of abundance of caution"
- B: 'On or about May 18, 2022' DECISION — "On or about May 18, 2022, after DTNA verified the limited population of vehicles potentially subject to the defect to the extent necessary to declare a recall and file that 573 report, out of abundance of caution, DTNA decided to conduct a voluntary safety recall campaign"

### E on #29 RCLRPT-22V374-1195.PDF: **substance** — event only in set A
- A: 'June 3, 2022' OTHER — "June 3, 2022, DTNA captured and repaired the 4 vehicles at DTNA’s own expense."
- B: (none)

### C on #29 RCLRPT-22V374-1195.PDF: **detail** — quote span/presence
- A: NOT_REPORTED — "NR"
- B: NOT_REPORTED — ""
