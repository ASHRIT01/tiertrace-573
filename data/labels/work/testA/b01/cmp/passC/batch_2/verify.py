import json,re
items=json.load(open("items.json")); dec=json.load(open("decisions.json"))
norm=lambda s:re.sub(r"\s+"," ",s).strip()
ids={i["item_id"] for i in items}; got={d["item_id"] for d in dec}
print("missing",ids-got,"extra",got-ids, "n",len(dec))
fm={i["item_id"]:i["file"] for i in items}
from collections import Counter; print(Counter(d["decision"] for d in dec))
for d in dec:
    t=norm(open("texts/"+fm[d["item_id"]].replace(".PDF",".txt")).read())
    qs=[d["quote"]]
    if "corrected" in d: qs+= [d["corrected"]["quote"], d["corrected"].get("entry_quote","")]
    for q in qs:
        if q and norm(q) not in t: print("BAD",d["item_id"],q[:60])
    if len(d["quote"])>300: print("LONG",d["item_id"])
print("ok")
