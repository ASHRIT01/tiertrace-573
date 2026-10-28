"""SN-1 Step 0 inventory: counts only (no supplier parsing, no network statistics).
  python scripts/sn1_inventory.py -> reports/sn1/SN1_INVENTORY.json"""
import io
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tt.data.flat import FIELDS, campaign_id  # noqa: E402

FLAT, INV = "data/flat/FLAT_RCL_POST_2010.zip", "data/inv/FLAT_INV_2026-10-28.zip"


def rows(zpath, n):
    with zipfile.ZipFile(zpath) as z, z.open(z.namelist()[0]) as raw:
        for line in io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline=""):
            f = line.rstrip("\r\n").split("\t")
            if len(f) == n:
                yield f


camps, maxd, nrows = {}, "", 0
for f in rows(FLAT, 29):
    r = dict(zip(FIELDS, f)); nrows += 1
    maxd = max(maxd, r["RCDATE"])
    cid = campaign_id(r["CAMPNO"])
    if r["RCDATE"] >= "20200101" and cid:
        c = camps.setdefault(cid, {"rcdate": r["RCDATE"], "types": set()})
        c["types"].add(r["RCLTYPECD"])
by_year, by_type, by_yt = Counter(), Counter(), Counter()
for c in camps.values():
    t = "/".join(sorted(c["types"])); y = c["rcdate"][:4]
    by_year[y] += 1; by_type[t] += 1; by_yt[(y, t)] += 1
ve = {k for k, c in camps.items() if c["types"] <= {"V", "E"}}

inv, ids_all, odates = {}, set(), []
nrow_inv = 0
for f in rows(INV, 11):
    nrow_inv += 1
    a, od, cn = f[0], f[6], f[8].strip()
    ids_all.add(a)
    i = inv.setdefault(a, {"odate": od, "camps": set()})
    if cn:
        i["camps"].add(campaign_id(cn if len(cn) == 9 else cn + "000") or "?" + cn)
op15 = {a: i for a, i in inv.items() if i["odate"] >= "20150101"}
linked = {c for i in inv.values() for c in i["camps"]}
linked15 = {c for i in op15.values() for c in i["camps"]}
res = {
    "flat_rows": nrows, "flat_max_rcdate": maxd, "campaigns_since_2020": len(camps),
    "by_year": dict(sorted(by_year.items())), "by_type": dict(by_type),
    "by_year_type": {f"{y}/{t}": n for (y, t), n in sorted(by_yt.items())}, "ve_campaigns": len(ve),
    "inv_rows": nrow_inv, "inv_distinct_actions": len(inv), "inv_min_odate": min(i["odate"] for i in inv.values()),
    "inv_max_odate": max(i["odate"] for i in inv.values()),
    "inv_opened_2015_on_actions": len(op15), "inv_blank_odate_actions": sum(1 for i in inv.values() if not i["odate"]),
    "inv_actions_with_campno": sum(1 for i in inv.values() if i["camps"]),
    "inv_opened_2015_with_campno": sum(1 for i in op15.values() if i["camps"]),
    "inv_by_open_year_2015_on": dict(sorted(Counter(i["odate"][:4] for i in op15.values()).items())),
    "distinct_campno_all": len(linked), "distinct_campno_opened2015": len(linked15),
    "campno_join_all_campaigns": len(linked & set(camps)), "campno_join_ve_campaigns": len(linked & ve),
    "campno_opened2015_join_campaigns": len(linked15 & set(camps)),
    "campno_opened2015_join_ve": len(linked15 & ve),
    "actions_opened2015_joining_campaigns": sum(1 for i in op15.values() if i["camps"] & set(camps)),
    "campno_malformed": sorted(c for c in linked if c.startswith("?"))[:10],
}
Path("reports/sn1").mkdir(parents=True, exist_ok=True)
Path("reports/sn1/SN1_INVENTORY.json").write_text(json.dumps(res, indent=1, default=list))
print(json.dumps(res, indent=1))
