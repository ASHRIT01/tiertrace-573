import json,re,os
n=lambda s:re.sub(r"\s+"," ",s).strip()
items=json.load(open("items.json",encoding="utf-8"))
dec=json.load(open("decisions.json",encoding="utf-8"))
ids={d["item_id"] for d in dec}
print("missing",[i["item_id"] for i in items if i["item_id"] not in ids], "count",len(dec))
f={i["item_id"]:i["file"] for i in items}
from collections import Counter;print(Counter(d["decision"] for d in dec))
for d in dec:
    t=n(open("texts/"+os.path.splitext(f[d["item_id"]])[0]+".txt",encoding="utf-8").read())
    ok=n(d["quote"]) in t and len(d["quote"])<=300
    c=d.get("corrected")
    if c: ok = ok and n(c["quote"]) in t and c["date_text"] in c["quote"]
    if not ok: print("BAD",d["item_id"])
