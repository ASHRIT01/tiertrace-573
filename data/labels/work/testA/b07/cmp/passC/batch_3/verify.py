import json,re,os
items=json.load(open("items.json")); dec=json.load(open("decisions.json"))
ids={i["item_id"] for i in items}; got={d["item_id"] for d in dec}
print("missing",ids-got,"extra",got-ids,"n",len(dec))
c=lambda s:re.sub(r"\s+"," ",s).strip()
bad=0
for d in dec:
    f=[i for i in items if i["item_id"]==d["item_id"]][0]["file"]
    t=c(open("texts/"+os.path.splitext(f)[0]+".txt").read())
    qs=[d["quote"]]+([d["corrected"]["quote"]]+([d["corrected"]["entry_quote"]] if "entry_quote" in d["corrected"] else [])) if "corrected" in d else [d["quote"]]
    for q in qs:
        if c(q) not in t or len(q)>300: print("BAD",d["item_id"],q); bad+=1
from collections import Counter; print(Counter(d["decision"] for d in dec),"bad",bad)
