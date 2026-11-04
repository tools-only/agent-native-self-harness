# program: on
# description: Copies the latest validated self-contained renderer HTML to the requested delivery filename.
# tags: html-export
def run(state,args):
    src=args.get('source','results/renders/v004/deck.html')
    dst=args.get('destination','deck.html')
    data=open(src,'r',encoding='utf-8').read()
    open(dst,'w',encoding='utf-8').write(data)
    return {'source':src,'destination':dst,'bytes':len(data),'self_contained':True}
