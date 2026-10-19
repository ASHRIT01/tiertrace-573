import json,re,sys,os
d=os.path.dirname(os.path.abspath(__file__))
items=json.load(open(os.path.join(d,'items.json')))
dec=json.load(open(os.path.join(d,'decisions.json')))
c=lambda s:re.sub(r'\s+',' ',s).strip()
ids={i['item_id']:i for i in items}
assert set(ids)==set(x['item_id'] for x in dec) and len(dec)==len(items)
for x in dec:
    stem=ids[x['item_id']]['file'].rsplit('.',1)[0]
    t=c(open(os.path.join(d,'texts',stem+'.txt'),encoding='utf-8').read())
    ok=c(x['quote']) in t and len(x['quote'])<=300
    if x['decision']=='NEITHER':
        ok=ok and c(x['corrected']['quote']) in t and c(x['corrected']['entry_quote']) in t
    assert x['decision'] in ('X','Y','NEITHER','CONTESTED')
    if not ok: print('BAD',x['item_id'])
from collections import Counter
print(Counter(x['decision'] for x in dec))
