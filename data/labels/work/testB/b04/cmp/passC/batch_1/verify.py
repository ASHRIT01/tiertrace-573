import json,re,os
b=os.path.dirname(os.path.abspath(__file__))
items=json.load(open(os.path.join(b,"items.json")))
dec=json.load(open(os.path.join(b,"decisions.json")))
ws=lambda s:re.sub(r"\s+"," ",s).strip()
ids={d["item_id"] for d in dec}
assert ids=={i["item_id"] for i in items} and len(dec)==len(items)
fm={i["item_id"]:i["file"] for i in items}
bad=0
for d in dec:
    t=ws(open(os.path.join(b,"texts",fm[d["item_id"]].rsplit(".",1)[0]+".txt")).read())
    for q in [d["quote"]]+([d["corrected"]["quote"]] if "corrected" in d else []):
        if ws(q) not in t or len(q)>300: print("BAD",d["item_id"],q); bad+=1
    assert d["decision"] in ("X","Y","NEITHER","CONTESTED")
from collections import Counter
print("bad",bad,Counter(d["decision"] for d in dec))
