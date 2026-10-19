import json,re,collections,os
n=lambda s:re.sub(r"\s+"," ",s).strip()
items=json.load(open("items.json")); dec=json.load(open("decisions.json"))
ids={i["item_id"] for i in items}; got={d["item_id"] for d in dec}
print("missing",ids-got,"extra",got-ids,"dups",len(dec)-len(got))
fm={i["item_id"]:i["file"] for i in items}
for d in dec:
    t=n(open("texts/"+fm[d["item_id"]].replace(".pdf",".txt")).read())
    if n(d["quote"]) not in t or len(d["quote"])>300: print("BAD quote",d["item_id"])
    if "corrected" in d and n(d["corrected"]["quote"]) not in t: print("BAD corr",d["item_id"])
print(collections.Counter(d["decision"] for d in dec))
