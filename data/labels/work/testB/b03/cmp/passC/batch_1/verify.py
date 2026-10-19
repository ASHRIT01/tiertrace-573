import json, re, os
b = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(b,"items.json")))
dec = json.load(open(os.path.join(b,"decisions.json")))
norm = lambda s: re.sub(r"\s+"," ",s).strip()
ids = {i["item_id"] for i in items}; dids = [x["item_id"] for x in dec]
assert ids == set(dids) and len(dids)==len(set(dids)), "coverage"
fm = {i["item_id"]: i["file"] for i in items}
bad = 0
for x in dec:
    t = norm(open(os.path.join(b,"texts",fm[x["item_id"]].rsplit(".",1)[0]+".txt")).read())
    if norm(x["quote"]) not in t or len(x["quote"])>300: print("BAD", x["item_id"]); bad+=1
    assert x["decision"] in ("X","Y","NEITHER","CONTESTED")
from collections import Counter
print("ok" if not bad else "fail", Counter(x["decision"] for x in dec))
