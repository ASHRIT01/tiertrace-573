import json,re
norm=lambda s:re.sub(r"\s+"," ",s).strip()
items=json.load(open("items.json"))
dec=json.load(open("decisions.json"))
ids={d["item_id"] for d in dec}
assert ids=={i["item_id"] for i in items} and len(dec)==len(items), "coverage"
f={i["item_id"]:i["file"] for i in items}
bad=0
for d in dec:
    t=norm(open("texts/"+f[d["item_id"]].replace(".pdf",".txt")).read())
    qs=[d["quote"]]+([d["corrected"]["quote"]] if "corrected" in d else [])
    for q in qs:
        if len(q)>300 or norm(q) not in t: print("BAD",d["item_id"],len(q)); bad+=1
    assert d["decision"] in ("X","Y","NEITHER","CONTESTED")
from collections import Counter
print("bad",bad,Counter(d["decision"] for d in dec))
