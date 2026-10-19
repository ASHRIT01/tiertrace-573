import json,re,os
d=json.load(open("decisions.json")); items=json.load(open("items.json"))
ids={i["item_id"] for i in items}; got={x["item_id"] for x in d}
print("missing",ids-got,"extra",got-ids)
f=lambda s:re.sub(r"\s+"," ",s).strip()
fm={i["item_id"]:i["file"] for i in items}
for x in d:
    stem=os.path.splitext(fm[x["item_id"]])[0]
    t=f(open("texts/"+stem+".txt",encoding="utf-8").read())
    ok=f(x["quote"]) in t and len(x["quote"])<=300
    if not ok: print("BAD",x["item_id"])
    if x["decision"]=="NEITHER" and "corrected" not in x: print("NOCORR",x["item_id"])
from collections import Counter; print(Counter(x["decision"] for x in d))
