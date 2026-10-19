import json,re,os
d=json.load(open("decisions.json")); items=json.load(open("items.json"))
ids={i["item_id"] for i in items}; got={x["item_id"] for x in d}
print("missing",ids-got,"extra",got-ids)
fm={i["item_id"]:i["file"] for i in items}
n=lambda s:re.sub(r"\s+"," ",s).strip()
for x in d:
    t=n(open("texts/"+fm[x["item_id"]].replace(".PDF",".txt"),encoding="utf-8").read())
    ok=n(x["quote"]) in t
    if not ok or len(x["quote"])>300: print("BAD",x["item_id"],len(x["quote"]))
from collections import Counter; print(Counter(x["decision"] for x in d))
