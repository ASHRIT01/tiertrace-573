import json,re,sys
d=json.load(open('decisions.json'));it=json.load(open('items.json'))
assert {x['item_id'] for x in d}=={x['item_id'] for x in it}, 'coverage'
n=lambda s:re.sub(r'\s+',' ',s).strip()
for x in d:
    t=n(open('texts/'+[i for i in it if i['item_id']==x['item_id']][0]['file'].rsplit('.',1)[0]+'.txt').read())
    ok=n(x['quote']) in t and len(x['quote'])<=300
    if 'corrected' in x: ok=ok and n(x['corrected']['quote']) in t
    print(x['item_id'],x['decision'],ok)
