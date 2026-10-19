import json,re
items=json.load(open("items.json")); dec=json.load(open("decisions.json"))
ids={i["item_id"] for i in items}; files={i["item_id"]:i["file"] for i in items}
assert ids=={d["item_id"] for d in dec} and len(dec)==len(ids), "coverage"
n=lambda s:re.sub(r"\s+"," ",s).strip()
from collections import Counter
for d in dec:
    t=n(open("texts/"+files[d["item_id"]].replace(".PDF",".txt"),encoding="utf-8").read())
    qs=[d["quote"]]
    if "corrected" in d: qs.append(d["corrected"]["quote"])
    for q in qs:
        if n(q) not in t or len(q)>300: print("BAD",d["item_id"],q)
    if d["decision"]=="NEITHER": assert "corrected" in d
print(Counter(d["decision"] for d in dec))
