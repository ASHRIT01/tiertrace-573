"""POST HOC sensitivity row for HA-1: the primary analysis without HA-02 (n = 38). Derived only from reports/ha1/HA1_RESULTS.json (already committed);
it does not read the marks file or the sealed key. HA-02's verdicts come from that file: marked not correct, date_yes (date-only count minus the one unsure
item), silver right.
  python scripts/ha1_sensitivity_ha02.py   -> reports/ha1/HA1_SENSITIVITY_HA02.json"""
import json
from pathlib import Path

import ha1_analysis as A

ROOT = Path(__file__).resolve().parents[1]
R = json.load(open(ROOT / "reports" / "ha1" / "HA1_RESULTS.json"))
V = R["human_vs_silver"]
assert "HA-02" in V["marks_wrong_total"] and "HA-02" in V["marks_wrong_silver_right"]
n = R["primary"]["n"] - 1
k = R["primary"]["correct"]                                   # HA-02 was not marked correct
kd = R["date_only"]["yes"] - 1                                # HA-02 had DATE_OK = yes (the only unsure date is HA-38)
a, b, c, d = V["human_yes_silver_yes"], V["human_yes_silver_no"], V["human_no_silver_yes"] - 1, V["human_no_silver_no"]
out = {"n": n, "excluded": ["HA-01", "HA-02"], "label": "POST HOC",
       "primary": {"correct": k, "n": n, "share": k / n, "wilson95": A.wilson(k, n)},
       "date_only": {"yes": kd, "n": n, "share": kd / n, "wilson95": A.wilson(kd, n)},
       "human_vs_silver": {"human_yes_silver_yes": a, "human_yes_silver_no": b, "human_no_silver_yes": c, "human_no_silver_no": d,
                           "agreement": (a + d) / n, "kappa": A.kappa(a, b, c, d)}}
json.dump(out, open(ROOT / "reports" / "ha1" / "HA1_SENSITIVITY_HA02.json", "w"), indent=1)
print(json.dumps(out, indent=1))
