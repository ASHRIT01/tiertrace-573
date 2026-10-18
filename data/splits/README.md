# Splits (IDs only)

Campaign ids drawn by tt/splits.py from the local flat-file index; seed 0. Dev: 2015-2022, 50 per year. Test-A: 2023-Feb 2026, allocated in proportion to eligible campaigns per year. The 300 audit-sample campaigns are excluded from both. V and E campaigns only. SHA-256 of each file is in SHA256SUMS. No Test-A filing has been downloaded or read.

```
{
 "dev_per_year": 50,
 "testA_alloc": {
  "2023": 315,
  "2024": 338,
  "2025": 309,
  "2026": 38
 },
 "eligible_by_year": {
  "2015": 928,
  "2016": 985,
  "2017": 857,
  "2018": 997,
  "2019": 926,
  "2020": 844,
  "2021": 1043,
  "2022": 1004,
  "2023": 963,
  "2024": 1034,
  "2025": 945,
  "2026": 677
 },
 "testA_window_pool": {
  "2023": 963,
  "2024": 1034,
  "2025": 945,
  "2026": 117
 }
}
```
