import json,re,os
b=os.path.dirname(os.path.abspath(__file__))
items=json.load(open(os.path.join(b,"items.json")))
dec=json.load(open(os.path.join(b,"decisions.json")))
ws=lambda s:re.sub(r"\s+"," ",s).strip()
ids={d["item_id"] for d in dec}
assert ids=={i["item_id"] for i in items} and len(dec)==len(items)
fm={i["item_id"]:i["file"] for i in items}
for d in dec:
    t=ws(open(os.path.join(b,"texts",fm[d["item_id"]].replace(".PDF",".txt"))).read())
    print(d["item_id"],d["decision"],ws(d["quote"]) in t, len(d["quote"])<=300)
