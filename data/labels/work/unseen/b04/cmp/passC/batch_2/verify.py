import json,re,collections
items=json.load(open("items.json")); D=json.load(open("decisions.json"))
ids={i["item_id"] for i in items}; got=[d["item_id"] for d in D]
print("missing",ids-set(got),"extra",set(got)-ids,"dups",len(got)-len(set(got)))
fm={i["item_id"]:i["file"] for i in items}
n=lambda s:re.sub(r"\s+"," ",s).strip()
for d in D:
    t=n(open("texts/"+fm[d["item_id"]].rsplit(".",1)[0]+".txt",encoding="utf-8").read())
    ok=n(d["quote"]) in t and len(d["quote"])<=300
    c=d.get("corrected")
    if c and c["quote"]: ok=ok and n(c["quote"]) in t
    if not ok: print("BAD",d["item_id"],len(d["quote"]))
    if d["decision"]=="NEITHER" and not c: print("NOCORR",d["item_id"])
print(collections.Counter(d["decision"] for d in D))
