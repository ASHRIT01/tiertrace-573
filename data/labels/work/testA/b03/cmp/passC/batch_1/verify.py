import json,re,os,collections
items=json.load(open("items.json")); dec=json.load(open("decisions.json"))
ws=lambda s:re.sub(r"\s+"," ",s).strip()
ids={d["item_id"] for d in dec}; need={i["item_id"] for i in items}
print("missing",need-ids,"extra",ids-need)
fm={i["item_id"]:i["file"] for i in items}
for d in dec:
    t=ws(open("texts/"+os.path.splitext(fm[d["item_id"]])[0]+".txt").read())
    qs=[d["quote"]]+([d["corrected"]["quote"]] if "corrected" in d else [])+([d["corrected"]["entry_quote"]] if "corrected" in d and "entry_quote" in d["corrected"] else [])
    for q in qs:
        if ws(q) not in t or len(q)>300: print("BAD",d["item_id"],len(q),q[:60])
print(collections.Counter(d["decision"] for d in dec))
