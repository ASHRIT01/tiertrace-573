import json,re
norm=lambda s:re.sub(r"\s+"," ",s).strip()
items=json.load(open("items.json")); d=json.load(open("decisions.json"))
fm={i["item_id"]:i["file"] for i in items}
assert set(fm)==set(x["item_id"] for x in d) and len(d)==len(fm), "coverage"
for x in d:
    t=norm(open("texts/"+fm[x["item_id"]].rsplit(".",1)[0]+".txt").read())
    ok=norm(x["quote"]) in t and len(x["quote"])<=300
    if "corrected" in x:
        c=x["corrected"]; ok=ok and norm(c["quote"]) in t and norm(c.get("entry_quote",""))in t
    print(x["item_id"],x["decision"],"OK" if ok else "FAIL")
from collections import Counter; print(Counter(x["decision"] for x in d))
