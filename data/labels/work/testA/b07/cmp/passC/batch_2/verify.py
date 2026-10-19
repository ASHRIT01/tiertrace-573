import json,re,collections
dec=json.load(open("decisions.json")); items=json.load(open("items.json"))
ids={i["item_id"] for i in items}; got={d["item_id"] for d in dec}
print("missing",ids-got,"extra",got-ids)
col=lambda s:re.sub(r"\s+"," ",s).strip()
f={i["item_id"]:i["file"] for i in items}
for d in dec:
    t=col(open("texts/"+f[d["item_id"]].rsplit(".",1)[0]+".txt").read())
    if col(d["quote"]) not in t or len(d["quote"])>300: print("BAD",d["item_id"],len(d["quote"]))
    if d["decision"]=="NEITHER" and col(d["corrected"]["quote"]) not in t: print("BADCORR",d["item_id"])
print(collections.Counter(d["decision"] for d in dec))
