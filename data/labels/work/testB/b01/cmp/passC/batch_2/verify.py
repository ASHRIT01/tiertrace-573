import json,re,sys,os
d=os.path.dirname(os.path.abspath(__file__))
items=json.load(open(os.path.join(d,'items.json')))
dec=json.load(open(os.path.join(d,'decisions.json')))
c=lambda s:re.sub(r'\s+',' ',s).strip()
ids={i['item_id'] for i in items}; got={x['item_id'] for x in dec}
print('missing',ids-got,'extra',got-ids)
fm={i['item_id']:i['file'] for i in items}
for x in dec:
    t=c(open(os.path.join(d,'texts',fm[x['item_id']].rsplit('.',1)[0]+'.txt')).read())
    ok=c(x['quote']) in t and len(x['quote'])<=300
    print(x['item_id'],x['decision'],'OK' if ok else 'FAIL')
