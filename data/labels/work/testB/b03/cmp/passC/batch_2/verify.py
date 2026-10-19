import json,re,sys,os
d=os.path.dirname(os.path.abspath(__file__))
dec=json.load(open(os.path.join(d,'decisions.json')))
items=json.load(open(os.path.join(d,'items.json')))
ws=lambda s:re.sub(r'\s+',' ',s).strip()
ids={i['item_id']:i for i in items}
assert set(ids)==set(x['item_id'] for x in dec) and len(dec)==len(items), "coverage"
ok=True
for x in dec:
    t=ws(open(os.path.join(d,'texts',ids[x['item_id']]['file'].rsplit('.',1)[0]+'.txt')).read())
    if ws(x['quote']) not in t or len(x['quote'])>300: ok=False; print("BAD",x['item_id'])
from collections import Counter; print(Counter(x['decision'] for x in dec), "ok" if ok else "FAIL")
