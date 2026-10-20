import json,re,collections
norm=lambda s:re.sub(r"\s+"," ",s).strip()
items=json.load(open("items.json")); dec=json.load(open("decisions.json"))
ids={d["item_id"] for d in dec}; print("missing",[i["item_id"] for i in items if i["item_id"] not in ids], "n",len(dec))
fm={i["item_id"]:i["file"] for i in items}
for d in dec:
    t=norm(open("texts/"+fm[d["item_id"]].rsplit(".",1)[0]+".txt").read())
    for q in [d["quote"]]+([d["corrected"]["quote"]] if "corrected" in d else []):
        if norm(q) not in t or len(q)>300: print("BAD",d["item_id"],q[:60])
print(collections.Counter(d["decision"] for d in dec))
