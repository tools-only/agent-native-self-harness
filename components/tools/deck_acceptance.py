# program: on
# description: Read-only validation of the current rendered HTML earnings deck.
# tags: acceptance
import json

def run(state,args):
    d=json.load(open('artifacts/deck.json'))
    if len(d.get('slides',[])) != 15: return {'ok':False,'reason':'Expected exactly 15 canonical slides.'}
    for i,s in enumerate(d['slides']):
        if 'Source:' not in ' '.join(e.get('text','') for e in s.get('elements',[]) if e.get('kind')=='text'): return {'ok':False,'reason':'Slide missing figure citation: '+str(i+1)}
    r=json.load(open('results/renders/v004/receipt.json'))
    if r.get('slides')!=15 or r.get('warnings') or r.get('elements',{}).get('image',0)<2: return {'ok':False,'reason':'Render count, warnings, or inline visuals did not pass.'}
    h=open('results/renders/v004/deck.html').read().lower()
    if not all(x in h for x in ['@media print','keydown','prev','next']): return {'ok':False,'reason':'HTML offline navigation/print check did not pass.'}
    return {'ok':True,'reason':'Latest render: 15 slides, source cited, no bounds warnings, two embedded visuals, offline navigation and print pagination.'}
