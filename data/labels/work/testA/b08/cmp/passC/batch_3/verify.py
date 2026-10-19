import json,re,os
items=json.load(open("items.json")); dec=json.load(open("decisions.json"))
norm=lambda s:re.sub(r"\s+"," ",s).strip()
ids={i["item_id"] for i in items}; d={x["item_id"]:x for x in dec}
print("missing",ids-set(d),"extra",set(d)-ids)
for i in items:
    t=norm(open("texts/"+os.path.splitext(i["file"])[0]+".txt").read())
    q=norm(d[i["item_id"]]["quote"])
    if q not in t or len(q)>300: print("BAD",i["item_id"])
from collections import Counter; print(Counter(x["decision"] for x in dec))
