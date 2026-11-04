# program: on
# description: Builds an editable earnings slide scene from separate story data.
# tags: html-slides, earnings
import json

def run(state,args):
    story=args.get('story')
    if story is None: story=json.load(open(args.get('story_path','artifacts/story.json')))
    W,H=13.333333,7.5
    navy='10283F'; teal='087E83'; gold='D89B32'; ink='183247'; muted='5D7180'; pale='F1F5F6'; white='FFFFFF'; line='D9E2E6'
    slides=[]
    def txt(x,y,w,h,text,size=16,color=ink,bold=False,font='Segoe UI',align='left',valign='top'):
        return {'kind':'text','x':x,'y':y,'w':w,'h':h,'text':text,'size':size,'font':font,'color':color,'bold':bold,'align':align,'valign':valign,'margin':0.02}
    def rect(x,y,w,h,fill,shape='rect'):
        return {'kind':'shape','shape':shape,'x':x,'y':y,'w':w,'h':h,'fill':fill}
    for i,s in enumerate(story['slides']):
        es=[rect(0,0,W,H,white),rect(0,0,.14,H,teal),txt(.58,.34,9,.25,s.get('eyebrow','JPMORGAN CHASE  |  3Q21 EARNINGS').upper(),10,teal,True),txt(.58,.72,12.1,.62,s['title'],27,navy,True)]
        if i==0:
            es += [rect(.58,1.58,12.15,5.18,navy,'rounded_rect'),txt(.95,1.98,7.0,.35,s.get('subhead','THIRD QUARTER 2021'),12,'B4D8D7',True),txt(.95,2.52,6.5,1.34,s.get('lead',''),39,white,True),txt(.95,4.03,6.2,1.1,s.get('summary',''),17,'E3ECEE'),rect(7.8,2.02,.025,4.1,'496173')]
            for j,m in enumerate(s.get('metrics',[])[:3]):
                y=2.15+j*1.36; es += [txt(8.25,y,3.9,.53,m['value'],27,gold,True),txt(8.25,y+.54,3.9,.48,m['label'],13,white)]
        else:
            es += [txt(.62,1.48,11.9,.68,s.get('deckline',''),17,muted)]
            metrics=s.get('metrics',[])
            if metrics:
                n=len(metrics); gap=.18; cw=(12.1-gap*(n-1))/n; yy=2.42
                for j,m in enumerate(metrics):
                    x=.62+j*(cw+gap); es += [rect(x,yy,cw,1.35,pale,'rounded_rect'),rect(x,yy,.065,1.35,m.get('accent',teal)),txt(x+.19,yy+.17,cw-.34,.55,m['value'],24,m.get('color',navy),True),txt(x+.19,yy+.75,cw-.34,.48,m['label'],13,muted)]
            art=s.get('art')
            if art:
                es += [{'kind':'image','path':art['path'],'x':.68,'y':4.0,'w':3.45,'h':2.05}]
            rows=s.get('rows',[])
            if rows:
                top=4.02 if metrics else 2.55
                for j,row in enumerate(rows[:4]):
                    if art:
                        y=top+j*.68; es += [rect(4.42,y,8.12,.012,line),txt(4.5,y+.12,2.2,.4,row[0],13,ink,True),txt(6.78,y+.12,5.65,.48,row[1],13,muted)]
                    else:
                        y=top+j*.55; es += [rect(.66,y,12.0,.012,line),txt(.76,y+.12,3.3,.35,row[0],13,ink,True),txt(4.08,y+.12,8.25,.38,row[1],14,muted)]
            bars=s.get('bars',[])
            if bars:
                top=4.02 if metrics else 2.55; maxv=max(abs(b['value']) for b in bars) or 1
                for j,b in enumerate(bars[:4]):
                    y=top+j*.57; es += [txt(.77,y,2.3,.28,b['label'],12,ink,True),rect(3.1,y+.04,6.3*abs(b['value'])/maxv,.22,b.get('color',teal),'rounded_rect'),txt(9.65,y-.02,2.5,.34,b['display'],13,navy,True)]
            if s.get('callout'): es += [rect(.68,6.29,11.95,.48,'EAF3F2','rounded_rect'),txt(.87,6.38,11.55,.29,s['callout'],12,teal,True)]
        es += [rect(.58,7.06,12.15,.012,line),txt(.62,7.13,10.9,.2,s.get('citation',''),9,muted),txt(11.65,7.12,1.05,.2,f'{i+1:02d}  /  15',9,muted,True,'Segoe UI','right')]
        slides.append({'background':white,'elements':es})
    json.dump({'width':W,'height':H,'font':'Segoe UI','slides':slides},open('artifacts/deck.json','w'))
    return {'slides':len(slides),'path':'artifacts/deck.json','story_title':story.get('title','')}
