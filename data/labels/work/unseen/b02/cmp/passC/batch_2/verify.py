import json,re,collections
d=json.load(open("decisions.json")); items=json.load(open("items.json"))
ids={i["item_id"] for i in items}; got=[x["item_id"] for x in d]
print("missing",ids-set(got),"extra",set(got)-ids,"dups",len(got)-len(set(got)))
fm={i["item_id"]:i["file"] for i in items}
c=lambda s:re.sub(r"\s+"," ",s).strip()
for x in d:
    t=c(open("texts/"+fm[x["item_id"]].replace(".PDF",".txt"),encoding="utf-8").read())
    ok=c(x["quote"]) in t and len(x["quote"])<=300
    cq=x.get("corrected",{}).get("quote")
    if cq: ok=ok and c(cq) in t
    if not ok: print("BAD",x["item_id"])
print(collections.Counter(x["decision"] for x in d))
