import json,re,os
b=os.path.dirname(os.path.abspath(__file__))
items=json.load(open(os.path.join(b,"items.json")))
D=json.load(open(os.path.join(b,"decisions.json")))
fm={i["item_id"]:i["file"] for i in items}
assert sorted(fm)==sorted(d["item_id"] for d in D), "coverage"
n=lambda s:re.sub(r"\s+"," ",s).strip()
from collections import Counter
for d in D:
    t=n(open(os.path.join(b,"texts",fm[d["item_id"]].replace(".PDF",".txt"))).read())
    qs=[d["quote"]]+([d["corrected"]["quote"]] if "corrected" in d else [])
    for q in qs:
        if n(q) not in t or len(q)>300: print("BAD",d["item_id"],len(q))
print(Counter(d["decision"] for d in D))
