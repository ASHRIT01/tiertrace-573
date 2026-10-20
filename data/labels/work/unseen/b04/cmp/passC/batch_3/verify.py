import json,re,os
d=json.load(open('decisions.json')); it=json.load(open('items.json'))
assert {x['item_id'] for x in d}=={x['item_id'] for x in it}, 'coverage'
f={x['item_id']:x['file'] for x in it}
n=lambda s:re.sub(r'\s+',' ',s).strip()
for x in d:
    t=n(open('texts/'+os.path.splitext(f[x['item_id']])[0]+'.txt').read())
    print(x['item_id'],x['decision'],n(x['quote']) in t, len(x['quote']))
