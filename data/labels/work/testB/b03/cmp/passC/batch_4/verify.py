import json,re,sys
d=json.load(open('decisions.json')); it=json.load(open('items.json'))
ids={i['item_id']:i for i in it}
assert set(ids)=={x['item_id'] for x in d}, 'coverage'
c=lambda s:re.sub(r'\s+',' ',s).strip()
for x in d:
    t=c(open('texts/'+ids[x['item_id']]['file'].rsplit('.',1)[0]+'.txt').read())
    print(x['item_id'],x['decision'],c(x['quote']) in t, len(x['quote']))
