# component_manufacturer_kind (300 latest-version filings)

Rule (also in tt/kind.py):
```
deterministic; names compared after tt.norm.aliases.squash: lowercase, punctuation and corporate suffixes removed):
 blank           the block has no supplier name (NR, N/A, empty, or no block).
 filer_itself    the block name equals the filer name after squashing and singularising tokens (PDF header filer; flat-file
                 MFGNAME as fallback).
 filer_affiliate not filer_itself, and EITHER one name contains the other (usually a foreign parent vs its US subsidiary,
                 e.g. 'Mercedes-Benz AG' vs 'Mercedes-Benz USA'), OR both names contain an alias of the same group in config/affiliates.csv
                 (seed table, UNVERIFIED), OR they share a first significant word (>= 4 chars, not a generic word such as
                 'general', 'american', 'national', 'international', 'united', 'global', 'advanced', 'standard').
 external        everything else.
Known weaknesses: containment sometimes means the same entity ('Blue Bird' vs 'Blue Bird Body Company' is called an
affiliate); the shared-first-word test joins unrelated companies with a common brand word (e.g. Volvo Car and Volvo
Trucks are different groups); the group table is a hand-written seed; a name mentioned only by brand is not linked.
```

Counts: external 183, filer_itself 19, filer_affiliate 20, blank 78

| year | external | filer_itself | filer_affiliate | blank |
|---|---|---|---|---|
| 2015 | 18 | 1 | 0 | 6 |
| 2016 | 16 | 0 | 1 | 8 |
| 2017 | 14 | 0 | 0 | 11 |
| 2018 | 16 | 0 | 1 | 8 |
| 2019 | 18 | 1 | 1 | 5 |
| 2020 | 16 | 1 | 1 | 7 |
| 2021 | 18 | 1 | 2 | 4 |
| 2022 | 15 | 1 | 3 | 6 |
| 2023 | 14 | 1 | 5 | 5 |
| 2024 | 14 | 4 | 2 | 5 |
| 2025 | 14 | 3 | 1 | 7 |
| 2026 | 10 | 6 | 3 | 6 |

## 10 random examples (seed 0)

- **RCLRPT-26V392-6562.pdf** (2026) filer `Storyteller Overland` / block `Nations Starter & Alternator` -> **external** 
- **RCLRPT-25V719-9776.pdf** (2025) filer `Isuzu Motors Limited` / block `Grede Iron Foundry of Biscoe` -> **external** 
- **RCLRPT-23V867-4491.pdf** (2023) filer `Volkswagen Group of America, Inc.` / block `LG Energy Solution Ochang Plant` -> **external** 
- **RCLRPT-18E101-9523.PDF** (2018) filer `Kidde Technologies, Inc.` / block `Kidde-Fenwal, Inc.` -> **filer_affiliate** shared first word: kidde
- **RCLRPT-26V500-8724.pdf** (2026) filer `Honda (American Honda Motor Co.)` / block `Thai Honda Manufacturing Co., Ltd.` -> **filer_affiliate** same group: honda
- **RCLRPT-22V445-7572.PDF** (2022) filer `Toyota Motor Engineering & Manufacturing` / block `Hino Motors Manufacturing USA` -> **filer_affiliate** same group: toyota
- **RCLRPT-19V560-6114.PDF** (2019) filer `Gulf Stream Coach, Inc.` / block `Gulf Stream Coach, Inc.` -> **filer_itself** equal
- **RCLRPT-25V403-5235.pdf** (2025) filer `Ford Motor Company` / block `Ford Motor Company` -> **filer_itself** equal
- **RCLRPT-16V493-3979.PDF** (2016) filer `Heartland Trailer Mfg` / block `` -> **blank** no supplier name in block
- **RCLRPT-17V652-8824.PDF** (2017) filer `Ford Motor Company` / block `` -> **blank** no supplier name in block

## All 20 filer_affiliate calls (for checking)

- RCLRPT-16V268-2446.PDF: `Volvo Car USA LLC` vs `Volvo Car Corporation` (name contained in the other (parent or regional entity))
- RCLRPT-18E101-9523.PDF: `Kidde Technologies, Inc.` vs `Kidde-Fenwal, Inc.` (shared first word: kidde)
- RCLRPT-19V302-1497.PDF: `Fontaine Trailer Company` vs `Fontaine Heavy Haul` (shared first word: fontaine)
- RCLRPT-20V135-9139.PDF: `Volkswagen Group of America, Inc.` vs `Volkswagen AG` (name contained in the other (parent or regional entity))
- RCLRPT-21V124-1956.PDF: `Mercedes-Benz USA, LLC` vs `Mercedes-Benz AG` (name contained in the other (parent or regional entity))
- RCLRPT-21V232-3340.PDF: `Mercedes-Benz USA, LLC` vs `Mercedes-Benz AG` (name contained in the other (parent or regional entity))
- RCLRPT-22V509-7302.PDF: `Kia Motors America` vs `Kia Georgia, Inc.` (same group: hyundai_kia)
- RCLRPT-22V445-7572.PDF: `Toyota Motor Engineering & Manufacturing` vs `Hino Motors Manufacturing USA` (same group: toyota)
- RCLRPT-22V158-7744.PDF: `Kia Motors America` vs `Kia Corporation-Hwasung Assembly Plant` (same group: hyundai_kia)
- RCLRPT-23V601-9768.PDF: `Volkswagen Group of America, Inc.` vs `AUDI AG` (same group: volkswagen)
- RCLRPT-23V463-7435.PDF: `Mercedes-Benz USA, LLC` vs `Mercedes-Benz AG` (name contained in the other (parent or regional entity))
- RCLRPT-23V176-2072.PDF: `Porsche Cars North America, Inc.` vs `Dr. Ing. h. c. F. Porsche AG` (same group: volkswagen)
- RCLRPT-23V464-5088.PDF: `Mercedes-Benz USA, LLC` vs `Mercedes-Benz AG` (name contained in the other (parent or regional entity))
- RCLRPT-23V300-6564.PDF: `Hyundai Motor America` vs `HYUNDAI WIA Cor` (same group: hyundai_kia)
- RCLRPT-24V201-8194.PDF: `Jaguar Land Rover North America, LLC` vs `Jaguar Land Rover Limited` (name contained in the other (parent or regional entity))
- RCLRPT-24V691-8386.PDF: `Hyundai Motor America` vs `Hyundai Mobis Mexico` (same group: hyundai_kia)
- RCLRPT-25V373-7837.pdf: `Hyundai Motor America` vs `HYUNDAI MOBIS MEXICO` (same group: hyundai_kia)
- RCLRPT-26V002-0368.pdf: `Blue Bird Body Company` vs `Blue Bird` (name contained in the other (parent or regional entity))
- RCLRPT-26V601-9878.pdf: `Winnebago Industries, Inc.` vs `Winnebago Motorhomes` (shared first word: winnebago)
- RCLRPT-26V500-8724.pdf: `Honda (American Honda Motor Co.)` vs `Thai Honda Manufacturing Co., Ltd.` (same group: honda)