import json,re,os,collections
dec=json.load(open("decisions.json"))
items=json.load(open("items.json"))
ids={i["item_id"] for i in items}
assert ids=={d["item_id"] for d in dec} and len(dec)==len(ids), "coverage"
ws=lambda s:re.sub(r"\s+"," ",s).strip()
fmap={i["item_id"]:i["file"] for i in items}
for d in dec:
    t=ws(open("texts/"+os.path.splitext(fmap[d["item_id"]])[0]+".txt",encoding="utf-8").read())
    assert len(d["quote"])<=300, d["item_id"]
    if ws(d["quote"]) not in t: print("MISSING",d["item_id"])
print(collections.Counter(d["decision"] for d in dec))
