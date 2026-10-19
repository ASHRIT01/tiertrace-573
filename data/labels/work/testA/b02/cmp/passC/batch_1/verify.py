import json, re, os, sys
d = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(d, "items.json")))
dec = json.load(open(os.path.join(d, "decisions.json")))
ws = lambda s: re.sub(r"\s+", " ", s).strip()
ids = {i["item_id"]: i for i in items}
ok = True
seen = set()
for x in dec:
    seen.add(x["item_id"])
    it = ids[x["item_id"]]
    txt = ws(open(os.path.join(d, "texts", it["file"].rsplit(".", 1)[0] + ".txt")).read())
    if ws(x["quote"]) not in txt or len(x["quote"]) > 300:
        ok = False; print("BAD QUOTE", x["item_id"], len(x["quote"]))
    if x["decision"] not in ("X", "Y", "NEITHER", "CONTESTED"):
        ok = False; print("BAD DECISION", x["item_id"])
    if x["decision"] == "NEITHER" and "corrected" not in x:
        ok = False; print("NO CORRECTED", x["item_id"])
missing = set(ids) - seen
if missing: ok = False; print("MISSING", missing)
from collections import Counter
print(Counter(x["decision"] for x in dec))
print("OK" if ok else "FAIL")
