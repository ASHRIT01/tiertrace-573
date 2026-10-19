import json,re,os
items=json.load(open("items.json")); dec=json.load(open("decisions.json"))
ids={i["item_id"] for i in items}; did=[d["item_id"] for d in dec]
assert ids==set(did) and len(did)==len(set(did)), (ids^set(did))
fm={i["item_id"]:i["file"] for i in items}
n=lambda s:re.sub(r"\s+"," ",s).strip()
bad=0
for d in dec:
    t=n(open("texts/"+fm[d["item_id"]].replace(".PDF",".txt")).read())
    for q in [d["quote"]]+([d["corrected"]["quote"]] if "corrected" in d else []):
        if n(q) not in t or len(q)>300: print("BAD",d["item_id"],q); bad+=1
    assert d["decision"] in ("X","Y","NEITHER","CONTESTED")
from collections import Counter
print("bad",bad,Counter(x["decision"] for x in dec))
