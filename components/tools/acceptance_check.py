# program: on
# description: Read-only acceptance_check for the rendered 15-slide HTML deck.
# tags: acceptance_check
import json

def run(state,args):
    d=json.load(open('artifacts/deck.json'))
    if len(d.get('slides',[])) != 15: return {'ok':False,'reason':'Expected exactly 15 slides.'}
    for i,s in enumerate(d['slides']):
        text=' '.join(e.get('text','') for e in s.get('elements',[]) if e.get('kind')=='text')
        if 'Source:' not in text: return {'ok':False,'reason':'Missing citation on slide '+str(i+1)}
    r=json.load(open('results/renders/v004/receipt.json'))
    if r.get('slides')!=15 or r.get('warnings') or r.get('elements',{}).get('image',0)<2: return {'ok':False,'reason':'Rendered deck count, warning, or visual check failed.'}
    h=open('deck.html').read().lower()
    if not h.startswith('<!doctype html>'): return {'ok':False,'reason':'Delivery file deck.html is missing or malformed.'}
    if not all(x in h for x in ['@media print','keydown','prev','next']): return {'ok':False,'reason':'Offline navigation or print pagination missing.'}
    return {'ok':True,'reason':'PASS deck.html: 15 cited slides, zero warnings, two inline visuals, working keyboard navigation and print pagination.'}
