# Mask-and-recover test-set size

Rules:
```
M1 exact   : the block supplier name, normalised (NFKC, lowercase, whitespace), is a substring of the narrative.
 M2 squash  : the name with corporate suffixes and punctuation removed (e.g. 'zf', 'allison transmission') occurs
              as whole words in the narrative squashed the same way (>= 2 chars).
 M3 alias   : any alias-table alias with the same parent id occurs as in M2.
 SELF       : (checked first) component_manufacturer_kind == filer_itself (tt/kind.py: equal after squashing and singularising);
              excluded from the task. Foreign-parent / regional / group-member names (kind == filer_affiliate) STAY in the
              task and are reported separately.
 M4 partial : (reported separately) only the first significant word of the squashed name (>= 4 chars) occurs
              as a whole word, e.g. 'Allison' for 'Allison Transmission Inc.'.
EXTRACTIVE = M1 or M2 or M3. PARTIAL-ONLY = M4 and not EXTRACTIVE. The rest are INFERENTIAL (name absent).
Masking for the task must remove all of M1-M4 occurrences in every section the model sees.
```

Of 300 filings: 78 have no supplier name in the block, 19 name the filer itself, 203 name a different company.
Among those 203: **extractive 40** (name in cause/chronology), partial-only 22, **inferential 141** (name absent from cause/chronology).
Alias-table matches (M3): 0 (the seed table has only 5 aliases, so M3 is a floor).

| year | filings | no block name | block = filer | extractive (M1-M3) | partial only | inferential |
|---|---|---|---|---|---|---|
| 2015 | 25 | 6 | 1 | 6 | 3 | 9 |
| 2016 | 25 | 8 | 0 | 4 | 2 | 11 |
| 2017 | 25 | 11 | 0 | 1 | 3 | 10 |
| 2018 | 25 | 8 | 0 | 5 | 2 | 10 |
| 2019 | 25 | 5 | 1 | 1 | 1 | 17 |
| 2020 | 25 | 7 | 1 | 3 | 2 | 12 |
| 2021 | 25 | 4 | 1 | 4 | 2 | 14 |
| 2022 | 25 | 6 | 1 | 3 | 0 | 15 |
| 2023 | 25 | 5 | 1 | 5 | 1 | 13 |
| 2024 | 25 | 5 | 4 | 5 | 0 | 11 |
| 2025 | 25 | 7 | 3 | 2 | 4 | 9 |
| 2026 | 25 | 6 | 6 | 1 | 2 | 10 |

By kind (extractive / partial-only / inferential):

- external (183): 35 / 20 / 128
- filer_affiliate (20): 5 / 2 / 13

## Reconciliation: earlier report said 26 'block = filer'; now 19

Earlier rule: squashed name contained in / containing the filer name. Now: equal after squashing and singularising tokens. 26 - 8 + 1 = 19.

Moved OUT of 'filer itself' (kind = filer_affiliate; they stay in the task): 8
- RCLRPT-16V268-2446.PDF: filer `Volvo Car USA LLC` vs block `Volvo Car Corporation` (name contained in the other (parent or regional entity))
- RCLRPT-20V135-9139.PDF: filer `Volkswagen Group of America, Inc.` vs block `Volkswagen AG` (name contained in the other (parent or regional entity))
- RCLRPT-21V124-1956.PDF: filer `Mercedes-Benz USA, LLC` vs block `Mercedes-Benz AG` (name contained in the other (parent or regional entity))
- RCLRPT-21V232-3340.PDF: filer `Mercedes-Benz USA, LLC` vs block `Mercedes-Benz AG` (name contained in the other (parent or regional entity))
- RCLRPT-23V463-7435.PDF: filer `Mercedes-Benz USA, LLC` vs block `Mercedes-Benz AG` (name contained in the other (parent or regional entity))
- RCLRPT-23V464-5088.PDF: filer `Mercedes-Benz USA, LLC` vs block `Mercedes-Benz AG` (name contained in the other (parent or regional entity))
- RCLRPT-24V201-8194.PDF: filer `Jaguar Land Rover North America, LLC` vs block `Jaguar Land Rover Limited` (name contained in the other (parent or regional entity))
- RCLRPT-26V002-0368.pdf: filer `Blue Bird Body Company` vs block `Blue Bird` (name contained in the other (parent or regional entity))

Of these, 7 are a foreign parent / regional entity (Volvo Car Corporation, Volkswagen AG, Mercedes-Benz AG x4, Jaguar Land Rover Limited) and 1 (Blue Bird) is probably the same entity (known miss of the containment rule).

Moved IN to 'filer itself' (singular/plural variant): 1
- RCLRPT-26V388-5998.pdf: filer `Daimler Trucks North America, LLC` vs block `Daimler Truck North America`

## 10 random examples of the name ALSO appearing in the narrative (seed 0)

- **RCLRPT-24V356-8426.PDF** (2024) block name `Freedman Seating` -> M1 match `Freedman Seating`; also in defect section: True
  - ...nr . on 5/17/2024 we were informed by freedman seating about a recall on the go-es foldaway seats. freedman supplied documen...
- **RCLRPT-21V375-1845.PDF** (2021) block name `Dometic` -> M1 match `Dometic`; also in defect section: True
  - ...he smell . tiny idahomes was recently informed of a recall on certain dometic 3 burner stoves. dometic became aware of warranty leak claims in may ...
- **RCLRPT-15V310-0723.PDF** (2015) block name `Dana Driveshaft Manufacturing LLC` -> PARTIAL match `dana`; also in defect section: False
  - ...h received the part 577 owner notification letter for this issue from dana for two affected trucks owned and registered to kenworth. on april 7,...
- **RCLRPT-23V627-3070.PDF** (2023) block name `Carefree of Colorado` -> M1 match `Carefree of Colorado`; also in defect section: False
  - ...stigated the field failures with assistance from the awning supplier, carefree of colorado. during the investigation winnebago and carefree identified 18 incide...
- **RCLRPT-21V330-3480.PDF** (2021) block name `Cummins, Inc.` -> M2 match `cummins`; also in defect section: False
  - ...il 30, 2021, eldorado national-california received communication from cummins about recall 21e-032 for their l9 and isx12 engines. on may 4, 2021, ...
- **RCLRPT-25V761-4355.pdf** (2025) block name `Q'Straint` -> M1 match `Q'Straint`; also in defect section: True
  - ...ndera motors confirmed receipt of nhtsa recall campaign # 25e063 from q'straint on 10/29/2025. removal of affected parts from inventory and the produ...
- **RCLRPT-19V146-9045.PDF** (2019) block name `Luxfer Canada Ltd` -> M2 match `luxfer canada`; also in defect section: True
  - ...ired one tank per unit. this tank was available and we purchased from luxfer canada inc. we purchased these tanks including valves, but did not specify t...
- **RCLRPT-15V641-7589.PDF** (2015) block name `Fontaine Fifth Wheel Company` -> PARTIAL match `fontaine`; also in defect section: True
  - ...operator misuse. according to fontaine, the cumulative damage observed is the result of the failure of opera...
- **RCLRPT-15V619-6612.PDF** (2015) block name `Henderson Wheel & Supply` -> M1 match `Henderson Wheel & Supply`; also in defect section: False
  - ...of torsion arm and torsion bar/beam. see mfg of axle for more info. . henderson wheel & supply did all tests and decision making on applying for recall....
- **RCLRPT-23V601-9768.PDF** (2023) block name `AUDI AG` -> M2 match `audi`; also in defect section: False
  - ...nr . february 13, 2019: the audi product safety committee receives a report about the issue and the po...