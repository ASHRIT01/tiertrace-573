import json,re
items=json.load(open("items.json")); dec=json.load(open("decisions.json"))
ids={d["item_id"] for d in dec}; need={i["item_id"] for i in items}
print("missing",need-ids,"extra",ids-need)
c=lambda s:re.sub(r"\s+"," ",s).strip()
fm={i["item_id"]:i["file"] for i in items}
from collections import Counter
for d in dec:
    t=c(open("texts/"+fm[d["item_id"]].rsplit(".",1)[0]+".txt").read())
    if c(d["quote"]) not in t or len(d["quote"])>300: print("BAD",d["item_id"])
    if d["decision"]=="NEITHER" and "corrected" not in d: print("NOCORR",d["item_id"])
print(Counter(d["decision"] for d in dec))
