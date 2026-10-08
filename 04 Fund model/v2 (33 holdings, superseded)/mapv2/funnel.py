import json
from universe import *
def num(s):
    if s in ('','n/a',None): return None
    s=s.replace(',','');m={'T':1e12,'B':1e9,'M':1e6}
    return float(s[:-1])*m[s[-1]] if s[-1] in m else float(s)
raw={}
for line in open('st_raw.txt').readlines()+open('st_raw_extra.txt').readlines():
    k,ccy,mc,sh,vol,nd,cov,ev,path=line.rstrip('\n').split('|')
    raw[k]=dict(ccy=ccy,mcap=num(mc),shares=num(sh),vol=num(vol),nd=num(nd),cov=num(cov),ev=num(ev),path=path)
rows=[]
for key,t,ctry,gics,name,yh in L:
    d=raw[key]; usd=d['mcap']/FX[d['ccy']]
    price=d['mcap']/d['shares'] if d['shares'] else None
    adv_php=d['vol']*price/FX[d['ccy']]*FX['PHP'] if price else None
    cap=adv_php*0.2*5/1e9 if adv_php else None
    dlim=6.0 if gics=='Utilities' else 4.0
    debt_ok = d['nd'] is not None and d['nd']<=dlim and (d['cov'] is None or d['cov']>=2.5)
    price_ok = d['ev'] is not None and d['ev']<=22.2
    liq_ok = cap is None or cap>=0.01
    why=[]
    if not debt_ok:
        if d['nd']>dlim: why.append(f"net debt/EBITDA {d['nd']:.2f}x > {dlim:.1f}x")
        if d['cov'] is not None and d['cov']<2.5: why.append(f"interest cover {d['cov']:.2f}x < 2.5x")
    if not price_ok: why.append(f"EV/EBITDA {d['ev']:.1f}x > 22.2x")
    if not liq_ok: why.append(f"liquidity cap {cap*100:.2f}% < 1%")
    rows.append(dict(key=key,name=name,type=t,region=region(ctry),country=ctry,gics=gics,role=ROLE[t],yahoo=yh,
        usd_bn=round(usd/1e9,2),nd=d['nd'],cov=d['cov'],ev=d['ev'],liq_cap=None if cap is None else round(min(cap,1),4),
        fin_pass=debt_ok and price_ok and liq_ok,fin_fail=why))
json.dump(rows,open('longlist.json','w'),indent=1)
for t in TYPES:
    for r in ['Asia-Pacific','Europe','Americas']:
        cell=sorted([x for x in rows if x['type']==t and x['region']==r],key=lambda x:-x['usd_bn'])
        print(f"\n[{t} {TYPES[t]} | {r}]")
        for x in cell:
            lc='' if x['liq_cap'] is None else f"liq {x['liq_cap']*100:.1f}%"
            print(f"  {'PASS' if x['fin_pass'] else 'fail'} {x['key']:10s} {x['country']} ${x['usd_bn']:8.1f}B  {lc:12s} {'; '.join(x['fin_fail'])}")
