import json,re
norm=lambda s:re.sub(r"\s+"," ",s).strip()
items=json.load(open("items.json"));dec=json.load(open("decisions.json"))
ids={d["item_id"] for d in dec}
assert ids=={i["item_id"] for i in items} and len(dec)==len(items)
fm={i["item_id"]:i["file"] for i in items}
from collections import Counter
for d in dec:
    t=norm(open("texts/"+fm[d["item_id"]].replace(".PDF",".txt")).read())
    for q in [d["quote"]]+([d["corrected"]["quote"]] if "corrected" in d else []):
        if norm(q) not in t or len(q)>300: print("BAD",d["item_id"],len(q))
    if "corrected" in d: assert d["corrected"]["date_text"] in d["corrected"]["quote"]
print(Counter(d["decision"] for d in dec))
