import json,re,sys
items=json.load(open('items.json'));d=json.load(open('decisions.json'))
ids={i['item_id'] for i in items}; got={x['item_id'] for x in d}
print('missing',ids-got,'extra',got-ids)
c=lambda s:re.sub(r'\s+',' ',s).strip()
for x in d:
    f=[i for i in items if i['item_id']==x['item_id']][0]['file'].replace('.PDF','.txt')
    t=c(open('texts/'+f).read()); q=c(x['quote'])
    print(x['item_id'],x['decision'],len(x['quote'])<=300, q in t)
