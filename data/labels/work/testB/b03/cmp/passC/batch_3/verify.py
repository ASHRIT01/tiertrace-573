import json,re,os,collections
d=json.load(open("decisions.json")); items=json.load(open("items.json"))
ids={i["item_id"]:i for i in items}
assert set(x["item_id"] for x in d)==set(ids) and len(d)==len(ids)
norm=lambda s:re.sub(r"\s+"," ",s).strip()
for x in d:
    f=os.path.join("texts",ids[x["item_id"]]["file"].replace(".pdf",".txt"))
    t=norm(open(f).read())
    ok = norm(x["quote"]) in t and len(x["quote"])<=300
    if "corrected" in x: ok = ok and norm(x["corrected"]["quote"]) in t
    if not ok: print("BAD",x["item_id"],len(x["quote"]))
print(collections.Counter(x["decision"] for x in d))
