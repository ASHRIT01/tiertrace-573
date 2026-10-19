import json, re, sys
d = json.load(open("decisions.json")); items = json.load(open("items.json"))
assert {i["item_id"] for i in items} == {x["item_id"] for x in d}
norm = lambda s: re.sub(r"\s+", " ", s).strip()
for x in d:
    it = next(i for i in items if i["item_id"] == x["item_id"])
    t = norm(open("texts/" + it["file"].rsplit(".",1)[0] + ".txt").read())
    print(x["item_id"], x["decision"], norm(x["quote"]) in t, len(x["quote"]) <= 300)
