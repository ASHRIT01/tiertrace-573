import json,re,os
d=json.load(open("decisions.json")); items=json.load(open("items.json"))
ids={i["item_id"] for i in items}; got=[x["item_id"] for x in d]
print("missing",ids-set(got),"dups",len(got)-len(set(got)))
norm=lambda s:re.sub(r"\s+"," ",s).strip()
fm={i["item_id"]:i["file"] for i in items}
for x in d:
    t=norm(open("texts/"+fm[x["item_id"]].rsplit(".",1)[0]+".txt").read())
    q=norm(x["quote"])
    if q not in t or len(x["quote"])>300: print("BAD",x["item_id"],len(x["quote"]))
    c=x.get("corrected")
    if c and norm(c["quote"]) not in t: print("BADCORR",x["item_id"])
from collections import Counter; print(Counter(x["decision"] for x in d))
