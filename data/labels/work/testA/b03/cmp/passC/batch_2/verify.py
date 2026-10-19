import json, re, os, collections
d = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(d, "items.json"), encoding="utf-8"))
dec = json.load(open(os.path.join(d, "decisions.json"), encoding="utf-8"))
ws = lambda s: re.sub(r"\s+", " ", s).strip()
ids = {i["item_id"]: i for i in items}
got = {x["item_id"] for x in dec}
print("missing:", set(ids) - got, "extra:", got - set(ids))
for x in dec:
    f = ids[x["item_id"]]["file"].replace(".PDF", ".txt")
    t = ws(open(os.path.join(d, "texts", f), encoding="utf-8").read())
    q = ws(x["quote"])
    ok = q in t and len(x["quote"]) <= 300
    if not ok: print("BAD", x["item_id"], len(x["quote"]))
    assert x["decision"] in ("X", "Y", "NEITHER", "CONTESTED")
print(collections.Counter(x["decision"] for x in dec))
