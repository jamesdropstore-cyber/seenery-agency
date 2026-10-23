import base64,json,html,os
D=os.path.dirname(os.path.abspath(__file__))
t=open(D+'/template.html',encoding='utf-8').read()
names=['n5','bp1','bp2','bp3','b_cheese','b_onion','b_gringo','b_taco','grill','hero','m_cheese','m_classic','m_gringo','m_melt']
css=':root{'+''.join(f'--i-{n}:url(data:image/webp;base64,{base64.b64encode(open(D+"/assets/"+n+".webp","rb").read()).decode()});' for n in names)+'}'
t=t.replace('/*IMAGES*/',css)
import glob
NF=len(glob.glob(D+'/w/[0-9]*.webp'))
CFG=json.load(open(D+'/tour.json'))
t=t.replace('/*ENGINE*/',open(D+'/engine.js',encoding='utf-8').read().replace('/*NF*/0',str(NF)).replace('/*TM*/[[0,0],[7,1]]',json.dumps(CFG['TM'])).replace('/*FX*/[[0,.5],[7,.5]]',json.dumps(CFG['FX'])).replace('/*CH*/[0,1,2,3,4,5.6]',json.dumps(CFG['CH'])).replace('/*CAPW*/[]',json.dumps(CFG['CAPW'])).replace('/*HOLD*/[3.9,4.75]',json.dumps(CFG['HOLD'])))
PAW='<svg viewBox="0 0 64 64" aria-hidden="true" fill="currentColor"><ellipse cx="32" cy="42" rx="15" ry="12.5"/><ellipse cx="14.5" cy="27" rx="5.6" ry="7.2" transform="rotate(-22 14.5 27)"/><ellipse cx="25" cy="18" rx="5.6" ry="7.6" transform="rotate(-8 25 18)"/><ellipse cx="39" cy="18" rx="5.6" ry="7.6" transform="rotate(8 39 18)"/><ellipse cx="49.5" cy="27" rx="5.6" ry="7.2" transform="rotate(22 49.5 27)"/></svg>'
t=t.replace('<!--PAW-->',PAW)
R=json.load(open(D+'/reviews.json',encoding='utf-8'))
def card(r,dup):
    n,d,q=r;a=' aria-hidden="true"' if dup else ''
    return f'<figure class="q{" dup" if dup else ""}"{a}><span class="st" aria-label="5 von 5 Sternen">★★★★★</span><blockquote>«{html.escape(q,quote=False)}»</blockquote><figcaption><span class="av">{html.escape(n[0])}</span><span><b>{html.escape(n)}</b><small>Google · {d}</small></span></figcaption></figure>'
t=t.replace('<!--REVIEWS-->',''.join(card(r,False) for r in R)+''.join(card(r,True) for r in R))
open(D+'/smash-burger-bear.html','w',encoding='utf-8').write(t)
print(round(len(t)/1e6,2),'MB')
