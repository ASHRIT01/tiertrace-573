import json,re,collections
items=json.load(open("items.json")); dec=json.load(open("decisions.json"))
ws=lambda s:re.sub(r"\s+"," ",s).strip()
ids={i["item_id"] for i in items}; got={d["item_id"] for d in dec}
print("missing",ids-got,"extra",got-ids,"dups",len(dec)-len(got))
fm={i["item_id"]:i["file"] for i in items}
for d in dec:
    t=ws(open("texts/"+fm[d["item_id"]].replace(".PDF",".txt")).read())
    ok=ws(d["quote"]) in t and len(d["quote"])<=300
    c=d.get("corrected")
    if c: ok = ok and ws(c["quote"]) in t and (not c.get("entry_quote") or ws(c["entry_quote"]) in t)
    if not ok: print("BAD",d["item_id"],len(d["quote"]))
print(collections.Counter(d["decision"] for d in dec))
