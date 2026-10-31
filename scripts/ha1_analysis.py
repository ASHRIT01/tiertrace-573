"""HA-1 analysis: exactly the quantities fixed in reports/HA_PROTOCOL.md (tag ha-protocol-1). No model run. Reads audit/HA1_marks.txt (by item ID), the sample plan,
and the sealed answer key (silver verdicts). HA-01 is a practice item excluded from every result (reports/HA_AMENDMENTS.md), so the primary n is 39.
  python scripts/ha1_analysis.py   -> reports/ha1/HA1_RESULTS.json (printed too)"""
import json
import math
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Z = 1.96


def wilson(k, n, z=Z):
    if n == 0:
        return (float("nan"),) * 2
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def kappa(a, b, c, d):
    """2x2: a = both yes, b = human yes / silver no, c = human no / silver yes, d = both no."""
    n = a + b + c + d; po = (a + d) / n
    pe = ((a + b) * (a + c) + (c + d) * (b + d)) / n ** 2
    return (po - pe) / (1 - pe)


def marks():
    out = {}
    for l in open(ROOT / "audit" / "HA1_marks.txt", encoding="utf-8"):
        if l.startswith("#") or not l.strip():
            continue
        p = [x.strip() for x in l.split("|")]
        out[p[0]] = {"date": p[1].split("=", 1)[1], "type": p[2].split("=", 1)[1], "minutes": p[3].split("=", 1)[1], "note": p[4].split("=", 1)[1]}
    return out


def main():
    M = marks(); S = json.load(open(ROOT / "reports" / "ha1" / "HA1_SAMPLE.json"))
    key = json.load(open(ROOT / "audit" / "sealed" / "HA1_answer_key.json"))
    sil = {x["item"]: x["silver_correct"] for x in key["items"]}
    mean536 = key["mean_silver_correct_536"]
    F = S["frame_filings"]; N = S["population_claims"]
    ncl = S["accepted_claims_per_frame_filing"]
    by = {x["item"]: x for x in S["items"]}
    primary = [f"HA-{i:02d}" for i in range(2, 41)]                      # HA-01 excluded
    h = {i: int(M[i]["date"] == "yes" and M[i]["type"] == "yes") for i in primary}
    n = len(primary); R = {"n_primary": n, "excluded": ["HA-01"], "wording": "audited by the author, a single non-expert, n = 39"}
    # primary and sensitivity
    k = sum(h.values()); R["primary"] = {"correct": k, "n": n, "share": k / n, "wilson95": wilson(k, n)}
    kept = [i for i in primary if "unsure" not in (M[i]["date"], M[i]["type"])]
    ks = sum(h[i] for i in kept); R["sensitivity_excluding_unsure"] = {"correct": ks, "n": len(kept), "share": ks / len(kept), "wilson95": wilson(ks, len(kept)), "excluded_items": [i for i in primary if i not in kept]}
    # secondary: date only
    kd = sum(M[i]["date"] == "yes" for i in primary); R["date_only"] = {"yes": kd, "n": n, "share": kd / n, "wilson95": wilson(kd, n)}
    # human vs silver
    a = sum(h[i] and sil[i] for i in primary); b = sum(h[i] and not sil[i] for i in primary)
    c = sum((not h[i]) and sil[i] for i in primary); d = sum((not h[i]) and not sil[i] for i in primary)
    R["human_vs_silver"] = {"human_yes_silver_yes": a, "human_yes_silver_no": b, "human_no_silver_yes": c, "human_no_silver_no": d,
                            "agreement": (a + d) / n, "kappa": kappa(a, b, c, d), "silver_correct_in_sample": a + c,
                            "silver_correct_share_in_sample": (a + c) / n,
                            "marks_wrong_silver_right": [i for i in primary if not h[i] and sil[i]], "marks_right_silver_wrong": [i for i in primary if h[i] and not sil[i]],
                            "marks_wrong_total": [i for i in primary if not h[i]], "marks_wrong_silver_wrong": [i for i in primary if not h[i] and not sil[i]]}
    # repeats
    pairs = [(i, by[i]["repeat_of"]) for i in sorted(by) if by[i]["repeat_of"]]
    rep = {"pairs": [{"repeat": r, "original": o, "date": [M[o]["date"], M[r]["date"]], "type": [M[o]["type"], M[r]["type"]], "identical_note": M[o]["note"] == M[r]["note"]} for r, o in pairs]}
    rep["date_agree"] = sum(M[o]["date"] == M[r]["date"] for r, o in pairs); rep["type_agree"] = sum(M[o]["type"] == M[r]["type"] for r, o in pairs)
    rep["both_agree"] = sum(M[o]["date"] == M[r]["date"] and M[o]["type"] == M[r]["type"] for r, o in pairs); rep["of"] = len(pairs)
    rep["identical_notes"] = sum(p["identical_note"] for p in rep["pairs"]); rep["disagreeing"] = [(r, o) for r, o in pairs if (M[o]["date"], M[o]["type"]) != (M[r]["date"], M[r]["type"])]
    R["repeats"] = rep
    # minutes / unsure
    R["minutes"] = "not recorded" if all(M[i]["minutes"] == "NA" for i in M) else "partly recorded"
    R["unsure_marks_primary"] = {"DATE_OK": sum(M[i]["date"] == "unsure" for i in primary), "TYPE_OK": sum(M[i]["type"] == "unsure" for i in primary)}
    # exploratory PPI, protocol section E, with 40 replaced by the primary n = 39 (POST HOC consequence of excluding HA-01)
    w = {i: ncl[by[i]["file"]] for i in primary}
    dlt = [w[i] * (h[i] - int(sil[i])) for i in primary]
    th = mean536 + F / (N * n) * sum(dlt)
    se = F / (N * math.sqrt(n)) * statistics.stdev(dlt)
    hw = F / (N * n) * sum(w[i] * h[i] for i in primary)
    R["ppi"] = {"theta": th, "se": se, "ci95": [th - Z * se, th + Z * se], "mean_silver_536": mean536, "weighted_human_only": hw,
                "unweighted_with_silver": mean536 + sum(h[i] - int(sil[i]) for i in primary) / n, "F": F, "weights": {"min": min(w.values()), "max": max(w.values())},
                "silver_correct_536": round(mean536 * N), "n_used": n, "note": "protocol formula with 40 replaced by 39"}
    # POST HOC (not fixed by the protocol): claimed type of each audited claim, split by the author's verdict
    import csv
    ct = {r["ITEM"]: r["CLAIMED_TYPE"] for r in csv.DictReader(open(ROOT / "audit" / "HA1_sheet.csv", encoding="utf-8-sig"))}
    tab = {}
    for i in primary:
        c = tab.setdefault(ct[i], {"claims": 0, "marked_correct": 0}); c["claims"] += 1; c["marked_correct"] += h[i]
    R["post_hoc_by_claimed_type"] = tab
    json.dump(R, open(ROOT / "reports" / "ha1" / "HA1_RESULTS.json", "w"), indent=1, default=list)
    print(json.dumps(R, indent=1, default=list))


if __name__ == "__main__":
    main()
