import json,re
items=json.load(open("items.json")); dec=json.load(open("decisions.json"))
ids={i["item_id"]:i for i in items}; seen=set()
norm=lambda s:re.sub(r"\s+"," ",s).strip()
for d in dec:
    seen.add(d["item_id"]); it=ids[d["item_id"]]
    t=norm(open("texts/"+it["file"].replace(".PDF",".txt")).read())
    ok=norm(d["quote"]) in t and len(d["quote"])<=300
    if not ok: print("BAD QUOTE",d["item_id"])
print("missing",set(ids)-seen,"extra",seen-set(ids))
from collections import Counter; print(Counter(d["decision"] for d in dec))
