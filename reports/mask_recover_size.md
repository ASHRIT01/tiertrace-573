# Mask-and-recover test-set size

Rules:
```
M1 exact   : the block supplier name, normalised (NFKC, lowercase, whitespace), is a substring of the narrative.
 M2 squash  : the name with corporate suffixes and punctuation removed (e.g. 'zf', 'allison transmission') occurs
              as whole words in the narrative squashed the same way (>= 2 chars).
 M3 alias   : any alias-table alias with the same parent id occurs as in M2.
 SELF       : (checked first) the block supplier is the filer itself (same after squashing); excluded from the task.
 M4 partial : (reported separately) only the first significant word of the squashed name (>= 4 chars) occurs
              as a whole word, e.g. 'Allison' for 'Allison Transmission Inc.'.
EXTRACTIVE = M1 or M2 or M3. PARTIAL-ONLY = M4 and not EXTRACTIVE. The rest are INFERENTIAL (name absent).
Masking for the task must remove all of M1-M4 occurrences in every section the model sees.
```

Of 300 filings: 78 have no supplier name in the block, 26 name the filer itself, 196 name a different company.
Among those 196: **extractive 38** (name in cause/chronology), partial-only 22, **inferential 136** (name absent from cause/chronology).
Alias-table matches (M3): 0 (the seed table has only 5 aliases, so M3 is a floor).

| year | filings | no block name | block = filer | extractive (M1-M3) | partial only | inferential |
|---|---|---|---|---|---|---|
| 2015 | 25 | 6 | 1 | 6 | 3 | 9 |
| 2016 | 25 | 8 | 1 | 3 | 2 | 11 |
| 2017 | 25 | 11 | 0 | 1 | 3 | 10 |
| 2018 | 25 | 8 | 0 | 5 | 2 | 10 |
| 2019 | 25 | 5 | 1 | 1 | 1 | 17 |
| 2020 | 25 | 7 | 2 | 2 | 2 | 12 |
| 2021 | 25 | 4 | 3 | 4 | 2 | 12 |
| 2022 | 25 | 6 | 1 | 3 | 0 | 15 |
| 2023 | 25 | 5 | 3 | 5 | 1 | 11 |
| 2024 | 25 | 5 | 5 | 5 | 0 | 10 |
| 2025 | 25 | 7 | 3 | 2 | 4 | 9 |
| 2026 | 25 | 6 | 6 | 1 | 2 | 10 |

## 10 random examples of the name ALSO appearing in the narrative (seed 0)

- **RCLRPT-16V375-8173.PDF** (2016) block name `Ricon Corporation` -> M1 match `Ricon Corporation`; also in defect section: False
  - ...ir holes in the knuckle link arm. . a recall letter was received from ricon corporation. 16e020...
- **RCLRPT-21V332-7058.PDF** (2021) block name `Cummins Inc.` -> M2 match `cummins`; also in defect section: False
  - ...service. . on april 30, 2021, e-one, inc. received communication from cummins about recall 21e-032 for their l9 and isx12 engines. on may 4, 2021, ...
- **RCLRPT-20V222-8216.PDF** (2020) block name `Freedman Seating Company` -> M1 match `Freedman Seating Company`; also in defect section: True
  - ... innovations received notification of recall #20e-004 on 4/13/20 from freedman seating company and began identifying parts and vehicles potentially affected by the ...
- **RCLRPT-21V375-1845.PDF** (2021) block name `Dometic` -> M1 match `Dometic`; also in defect section: True
  - ...he smell . tiny idahomes was recently informed of a recall on certain dometic 3 burner stoves. dometic became aware of warranty leak claims in may ...
- **RCLRPT-23V491-9834.PDF** (2023) block name `CUMMINS, INC.` -> M2 match `cummins`; also in defect section: False
  - ...nr . 05/03/2023 - cummins sales representative informed adaptive mobility systems of their prod...
- **RCLRPT-23V267-9881.PDF** (2023) block name `WARN Industries, Inc.` -> M2 match `warn industries`; also in defect section: False
  - ...ed an email from choon lee nhtsa senior safety recall specialist that warn industries was performing recall 22e101. after confirmation from choon lee we pr...
- **RCLRPT-24V830-7473.PDF** (2024) block name `MERITOR` -> M1 match `MERITOR`; also in defect section: True
  - ...nr . 10/21/2024- international receives notification from meritor that 79 suspect front steer drive (fsd) axle assemblies may have been...
- **RCLRPT-15V641-7589.PDF** (2015) block name `Fontaine Fifth Wheel Company` -> PARTIAL match `fontaine`; also in defect section: True
  - ...operator misuse. according to fontaine, the cumulative damage observed is the result of the failure of opera...
- **RCLRPT-15V619-6612.PDF** (2015) block name `Henderson Wheel & Supply` -> M1 match `Henderson Wheel & Supply`; also in defect section: False
  - ...of torsion arm and torsion bar/beam. see mfg of axle for more info. . henderson wheel & supply did all tests and decision making on applying for recall....
- **RCLRPT-24V356-8426.PDF** (2024) block name `Freedman Seating` -> M1 match `Freedman Seating`; also in defect section: True
  - ...nr . on 5/17/2024 we were informed by freedman seating about a recall on the go-es foldaway seats. freedman supplied documen...