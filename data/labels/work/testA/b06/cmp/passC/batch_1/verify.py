import json, os, re, collections
D = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(D,"items.json")))
dec = json.load(open(os.path.join(D,"decisions.json")))
c = lambda s: re.sub(r"\s+"," ",s).strip()
dm = {d["item_id"]:d for d in dec}
assert set(dm)=={i["item_id"] for i in items}, "coverage"
bad=0
for i in items:
    d=dm[i["item_id"]]
    assert d["decision"] in ("X","Y","NEITHER","CONTESTED")
    assert len(d["quote"])<=300
    t=c(open(os.path.join(D,"texts",os.path.splitext(i["file"])[0]+".txt")).read())
    if c(d["quote"]) not in t: print("QUOTE MISS",i["item_id"]); bad+=1
print("bad",bad, collections.Counter(d["decision"] for d in dec))
