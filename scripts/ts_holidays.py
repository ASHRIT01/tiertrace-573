"""TS-1: write data/holidays_us_federal.csv from the 5 U.S.C. 6103 rules coded in scripts/ts_lib.py (holiday_rows). Deterministic.
  python scripts/ts_holidays.py"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ts_lib import HOLIDAY_YEARS, holiday_rows  # noqa: E402

rows = holiday_rows()
with open("data/holidays_us_federal.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["observed", "holiday", "actual", "shifted"])
    w.writeheader()
    w.writerows(rows)
print(len(rows), "rows,", HOLIDAY_YEARS.start, "-", HOLIDAY_YEARS.stop - 1)
