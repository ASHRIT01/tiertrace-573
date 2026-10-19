import json, re, os, sys
d = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(d, "items.json")))
dec = json.load(open(os.path.join(d, "decisions.json")))
ws = lambda s: re.sub(r"\s+", " ", s).strip()
ids = {i["item_id"] for i in items}
assert ids == {x["item_id"] for x in dec}, "coverage"
fm = {i["item_id"]: i["file"] for i in items}
for x in dec:
    t = ws(open(os.path.join(d, "texts", fm[x["item_id"]].rsplit(".", 1)[0] + ".txt"), encoding="utf-8").read())
    assert len(x["quote"]) <= 300 and ws(x["quote"]) in t, x["item_id"]
print("OK", len(dec))
