import json,re
items=json.load(open("items.json")); dec=json.load(open("decisions.json"))
c=lambda s:re.sub(r"\s+"," ",s).strip()
ids={i["item_id"] for i in items}; assert ids=={d["item_id"] for d in dec} and len(dec)==len(ids)
fm={i["item_id"]:i["file"] for i in items}; bad=0
for d in dec:
    t=c(open("texts/"+fm[d["item_id"]].rsplit(".",1)[0]+".txt").read())
    if c(d["quote"]) not in t or len(d["quote"])>300: print("BAD",d["item_id"]); bad+=1
    if d["decision"]=="NEITHER" and c(d["corrected"]["quote"]) not in t: print("BADCORR",d["item_id"]); bad+=1
from collections import Counter; print(Counter(d["decision"] for d in dec), "bad",bad)
