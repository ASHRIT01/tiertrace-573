import json,re
norm=lambda s:re.sub(r"\s+"," ",s).strip()
items=json.load(open("items.json",encoding="utf-8"))
dec=json.load(open("decisions.json",encoding="utf-8"))
ids={d["item_id"] for d in dec}
print("missing",[i["item_id"] for i in items if i["item_id"] not in ids])
fm={i["item_id"]:i["file"] for i in items}
for d in dec:
    t=norm(open("texts/"+fm[d["item_id"]].rsplit(".",1)[0]+".txt",encoding="utf-8").read())
    qs=[d["quote"]]+([d["corrected"]["quote"],d["corrected"]["entry_quote"]] if "corrected" in d else [])
    for q in qs:
        if norm(q) not in t or len(q)>300: print("BAD",d["item_id"],q[:60])
from collections import Counter;print(Counter(d["decision"] for d in dec))
