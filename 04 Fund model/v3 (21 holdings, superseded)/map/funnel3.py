import json
from universe3 import *
def num(s):
    if s in ('', 'n/a', None): return None
    s = s.replace(',', ''); m = {'T': 1e12, 'B': 1e9, 'M': 1e6}
    return float(s[:-1])*m[s[-1]] if s[-1] in m else float(s)
raw = {}
for line in open('st3.txt').readlines() + open('st3_extra.txt').readlines():
    k, ccy, mc, sh, vol, nc, eb, cov, ev, roic, wacc = line.rstrip('\n').split('|')
    raw[k] = dict(ccy=ccy or 'USD', mcap=num(mc), shares=num(sh), vol=num(vol), nc=num(nc), ebitda=num(eb), cov=num(cov),
                  ev=num(ev), roic=num(roic), wacc=num(wacc))
PRICE = {'AIRTEL': 1833.9}
rows = []
for key, t, ctry, gics, name, yh in L:
    d = raw[key]; usd = d['mcap']/FX[d['ccy']]
    px = PRICE.get(key) or (d['mcap']/d['shares'] if d['shares'] else None)
    cap = d['vol']*px/FX[d['ccy']]*FX['PHP']*0.2*5/1e9 if px else None
    nd = -d['nc']/d['ebitda'] if d['ebitda'] else None
    r = dict(key=key, name=name, type=t, country=ctry, gics=gics, role=ROLE[t], yahoo=yh, usd_bn=round(usd/1e9, 2), nd=round(nd, 2),
             cov=d['cov'], ev=d['ev'], roic=d['roic'], wacc=d['wacc'], spread=None if d['roic'] is None else round(d['roic'] - d['wacc'], 2),
             liq_cap=None if cap is None else round(min(cap, 1), 4))
    rows.append(r)
# universe: 20 largest per type (US$1bn floor)
for t in TYPES:
    ts = sorted([r for r in rows if r['type'] == t], key=lambda r: -r['usd_bn'])
    for i, r in enumerate(ts, 1): r['size_rank'] = i; r['in_universe'] = i <= 20 and r['usd_bn'] >= 1.0
for r in rows:
    fails = []
    if not r['in_universe']: r['stage'] = 'Outside universe'; r['why'] = f"size rank {r['size_rank']} in its type (top 20 only)"; continue
    # M: theme fit
    if r['gics'] not in QUALIFYING:
        seg = SEGMENT.get(r['key'])
        if not seg or seg[0] < 0.5:
            r['stage'] = 'Fail M'; r['why'] = f"theme fit: {r['gics'].lower()}; qualifying revenue {seg[0]*100:.0f}% < 50% ({seg[1]})" if seg else f"theme fit: {r['gics']} not on list"; continue
    # V: gates
    dl = 6.0 if r['gics'] in (EU, MU_, WU, IPP, RE) else 4.0
    if r['nd'] > dl: fails.append(f"net debt/EBITDA {r['nd']:.2f}× > {dl:.1f}×")
    if r['cov'] is not None and r['cov'] < 2.5: fails.append(f"interest cover {r['cov']:.2f}× < 2.5×")
    if r['ev'] > 22.2: fails.append(f"EV/EBITDA {r['ev']:.1f}× > 22.2×")
    if r['liq_cap'] is not None and r['liq_cap'] < 0.01: fails.append(f"liquidity cap {r['liq_cap']*100:.2f}% < 1%")
    if fails: r['stage'] = 'Fail V gate'; r['why'] = '; '.join(fails); continue
    r['stage'] = 'Ranked'
# merit: within each type among gate passers, percentile of EV/EBITDA (low better) and ROIC-WACC (high better)
for t in TYPES:
    ps = [r for r in rows if r['type'] == t and r['stage'] == 'Ranked']
    n = len(ps)
    def pct(vals, v, low): # share of peers strictly worse
        worse = sum(1 for x in vals if (x > v if low else x < v)); eq = sum(1 for x in vals if x == v) - 1
        return (worse + 0.5*eq)/(n - 1) if n > 1 else 1.0
    evs = [r['ev'] for r in ps]; sps = [r['spread'] for r in ps]
    med_ev = sorted(evs)[n//2] if n % 2 else (sorted(evs)[n//2 - 1] + sorted(evs)[n//2])/2
    med_sp = sorted(sps)[n//2] if n % 2 else (sorted(sps)[n//2 - 1] + sorted(sps)[n//2])/2
    for r in ps:
        r['val_pct'] = pct(evs, r['ev'], True); r['qual_pct'] = pct(sps, r['spread'], False)
        r['merit'] = round((r['val_pct'] + r['qual_pct'])/2, 9); r['peer_med_ev'] = med_ev; r['peer_med_spread'] = med_sp; r['peers'] = n
    ps.sort(key=lambda r: -r['merit'])
    for i, r in enumerate(ps, 1): r['merit_rank'] = i
json.dump(rows, open('universe3.json', 'w'), indent=1)
for t in TYPES:
    print(f'\n== {TYPES[t]}')
    for r in sorted([r for r in rows if r['type'] == t and r.get('in_universe')], key=lambda r: (r['stage'] != 'Ranked', r.get('merit_rank', 99), r['size_rank'])):
        if r['stage'] == 'Ranked':
            print(f"  #{r['merit_rank']:<2} {r['key']:<11}{r['country']} ${r['usd_bn']:7.1f}B EV {r['ev']:5.1f} (med {r['peer_med_ev']:.1f}) ROIC-WACC {r['spread']:+6.2f} (med {r['peer_med_spread']:+.2f}) merit {r['merit']:.2f} liq {r['liq_cap']}")
        else:
            print(f"  -- {r['key']:<11}{r['country']} ${r['usd_bn']:7.1f}B {r['stage']}: {r['why']}")
