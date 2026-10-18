# Narrative gain (Week-2 go/no-go measure)

Rules (deterministic heuristics; precision UNVERIFIED):
```
deterministic; heuristics, precision UNVERIFIED -- see examples in the report):
 A  COMPANY. A capitalised name ending in a corporate suffix (Inc, LLC, Corp, Corporation, Company, Co,
    Ltd, Limited, GmbH, AG, S.A., LP, Industries, Group, Holdings) appears in cause+chronology and, after
    squashing suffixes, neither equals/contains nor is contained by the filer (PDF header or flat file
    MFGNAME) nor the block supplier name. Names without a corporate suffix are NOT detected, so A under-counts.
 B  DATED EVENT. The chronology contains a date (numeric m/d/y, yyyy-mm-dd, d-Mon-yyyy, 'Month d, yyyy', or 'Month yyyy') that is
    not the flat file's RCDATE, ODATE, BGMAN or ENDMAN.
 C  CAUSE. The PDF cause section has >=40 chars and is not NR (C1), or it is NR/blank but the chronology
    contains a causal cue (C2), AND the flat file's defect summary (DESC_DEFECT) contains no causal cue.
 GAIN = A or B or C.
```

Of 300 filings: A company 35, B dated event 243, C cause 192, any (GAIN) 274.

| year | n | A company | B dated event | C cause | GAIN |
|---|---|---|---|---|---|
| 2015 | 25 | 6 | 22 | 12 | 24 |
| 2016 | 25 | 5 | 18 | 14 | 19 |
| 2017 | 25 | 2 | 17 | 18 | 22 |
| 2018 | 25 | 3 | 21 | 14 | 21 |
| 2019 | 25 | 0 | 19 | 14 | 22 |
| 2020 | 25 | 4 | 18 | 14 | 20 |
| 2021 | 25 | 1 | 22 | 20 | 25 |
| 2022 | 25 | 1 | 18 | 17 | 24 |
| 2023 | 25 | 3 | 21 | 19 | 24 |
| 2024 | 25 | 3 | 22 | 14 | 25 |
| 2025 | 25 | 4 | 23 | 18 | 24 |
| 2026 | 25 | 3 | 22 | 18 | 24 |

## 10 random GAIN examples (seed 0; not cherry-picked)

- **RCLRPT-15V682-1265.PDF** (2015): A=[] B=['9/17/15', '9/18/15', '10/15/15'] C1=True C2=False
  - cause: 'According to Eaton, "A spacer assembly that lacks necessary clearance for the transmission\'s main shaft key causes the recall condition by forcing the main shaf'
  - chronology: '9/17/15 Eaton informs Volvo of a potential problem with transmissions they supply 9/18/15 Eaton provides additional information to Volvo. Volvo opens an investi'
- **RCLRPT-17V560-7694.PDF** (2017): A=[] B=['March 2017', 'September 2017'] C1=False C2=True
  - cause: 'NR'
  - chronology: 'In March 2017 a jib mast on an LS87 failed during end-of-line testing at the factory when exposed to the test load of 750 lb (1.5x rated capacity). After extens'
- **RCLRPT-19V411-9234.PDF** (2019): A=[] B=['May 14, 2019', 'May 20, 2019', 'May 22, 2019'] C1=True C2=False
  - cause: 'The airbag ECU could malfunction due to a capacitor that does not comply with product specification due to the manufacturing process.'
  - chronology: 'Ferrari was advised by the supplier about the possibility of a potentially defective airbag ECU on May 14, 2019. Ferrari requested additional information during'
- **RCLRPT-23V867-4491.pdf** (2023): A=[] B=[] C1=True C2=False
  - cause: 'A small number of vehicles have experienced thermal overload with smoke or fire occurring underneath the vehicle from the high-voltage battery. The root cause i'
  - chronology: 'Please see separate document for chronology.'
- **RCLRPT-17V162-7813.PDF** (2017): A=[] B=['June 2016', 'January 2017', 'December 22, 2016'] C1=False C2=False
  - cause: 'The windshield wiper systems were not properly secured during the manufacturing process at TMC.'
  - chronology: 'June 2016 – January 2017 – 10 individual Vehicle Owner Questionnaires were submitted to NHTSA. These VOQs were added as additional warranty data points in TMC’s'
- **RCLRPT-18E101-9523.PDF** (2018): A=[] B=['October 31, 2018', 'September 2017', 'October 2017'] C1=True C2=False
  - cause: 'Based on information provided by Kidde-Fenwal, the equipment specifications provided to its component supplier (Chemring) may not provide sufficient force to de'
  - chronology: 'On October 31, 2018, Kidde-Fenwal, Inc. notified Kidde Technologies, Inc., that it had observed low force output from a piston actuator that provides initiation'
- **RCLRPT-22V752-6117.PDF** (2022): A=[] B=['September 2022', 'July 2022', 'September 30, 2022'] C1=False C2=True
  - cause: 'NR'
  - chronology: 'In early September 2022, BMW became aware of a potential issue during testing when it was reported that three engines on a test bench exhibited signs of leakage'
- **RCLRPT-23E003-9685.PDF** (2023): A=[] B=['June 2018', 'May 2019'] C1=False C2=False
  - cause: 'NR'
  - chronology: '04/22 Comoto were notified that the sizes M, & XXL helmet manufactured in 2021 that were tested at ACT Lab USA were found to be noncompliant with FMVSS 218. 06/'
- **RCLRPT-23V184-8706.PDF** (2023): A=['Volvo Product Safety Working Group'] B=['2023-02-16', '2023-02-16', '2023-02-20'] C1=True C2=False
  - cause: 'During the vehicle manufacturing, the emergency window exits were incorrectly adjusted by Prevost technicians.'
  - chronology: '2023-02-16 Issue identified in production during an internal Prevost audit. 2023-02-16 Internal Prevost investigation was opened to identify the root cause and '
- **RCLRPT-23V176-2072.PDF** (2023): A=[] B=['February 21, 2023', 'March 15, 2023'] C1=True C2=False
  - cause: 'Due to an incorrect market-specific coding of instrument clusters for Puerto Rico and Canada, the "initial seat belt warning" function is not displayed as legal'
  - chronology: 'February 21, 2023: Porsche AG learned that some instrument clusters did not perform as expected during an internal check of the market-specific coding. Testing '