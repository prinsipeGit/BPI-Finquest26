"""Map v4: M (thematic eligibility) and V (investment decision) exactly as fixed in ../RULES_v4.md (8 Oct 2026).
Input: st4.txt (stockanalysis.com statistics, 8 Oct 2026, checksum 3742345854). Output: universe4.json + printed funnel."""
import json, statistics as st
from universe4 import *

F = ['ccy', 'finccy', 'mcap', 'ev_abs', 'shares', 'vol', 'pe', 'fpe', 'pfcf', 'pocf', 'ev', 'evebit', 'evfcf', 'debt_ebitda', 'cov',
     'roic', 'wacc', 'ebitda', 'nc', 'debt', 'cash', 'ocf', 'capex', 'da', 'fcf', 'rev', 'dy', 'fcfy', 'revg3', 'epsg3', 'altz',
     'piotroski', 'beta', 'cur', 'ebitda_m', 'payout']
def num(s):
    s = s.strip().replace(',', '').replace('$', '')
    if s in ('', 'n/a', '-', 'Upgrade'): return None
    pct = s.endswith('%'); s = s.rstrip('%'); m = {'T': 1e12, 'B': 1e9, 'M': 1e6, 'K': 1e3}
    v = float(s[:-1]) * m[s[-1]] if s[-1] in m else float(s)
    return v / 100 if pct else v
raw = {}
for line in open('st4.txt').read().split('\n'):
    if not line: continue
    k, *v = line.split('|')
    d = dict(zip(F, v)); raw[k] = {f: (d[f] if f in ('ccy', 'finccy') else num(d[f])) for f in F}
    raw[k]['ccy'] = raw[k]['ccy'] or 'USD'

PRICE = {'AIRTEL': 11.43e12 / 6.10e9, 'TATAPOWER': 1.10e12 / 3.195e9, 'MAXH': 881.88e9 / 0.972e9}   # shares n/a on stockanalysis
SHOCK = {1: .15, 2: .10, 3: .15, 4: .30, 5: .60, 6: .35, 7: .50, 8: .25}
GOVERNANCE = {'ADANIPOWER': 'Adani group: US DOJ/SEC charges against group founder and executives (Nov 2024)',
              'ADANIGREEN': 'Adani group: US DOJ/SEC charges against group founder and executives (Nov 2024)',
              'ADPORTS': 'Adani group: US DOJ/SEC charges against group founder and executives (Nov 2024)'}
NO_PRICES = {'EAND': 'no price history in our sources (Abu Dhabi listing)'}
AUM = 1e9

rows = []
for key, t, ctry, gics, name, yh in L:
    d = raw[key]; ccy = d['ccy']
    usd = d['mcap'] / FX[ccy]
    px = PRICE.get(key) or (d['mcap'] / d['shares'] if d['shares'] else None)
    liq = d['vol'] * px / FX[ccy] * FX['PHP'] * 0.2 * 5 / AUM if (px and d['vol']) else None
    nd = -d['nc'] / d['ebitda'] if (d['ebitda'] and d['nc'] is not None) else None
    ebit_ratio = d['evebit'] / d['ev'] if (d['evebit'] and d['ev']) else None          # EBITDA / EBIT
    cov_s = None
    if d['cov'] is not None and ebit_ratio:
        cov_s = d['cov'] * (1 - SHOCK[t] * ebit_ratio)
    cy = None
    if d['ev_abs'] and d['ocf'] is not None:
        cy = ((d['ocf'] - d['da']) / d['ev_abs']) if d['da'] is not None else (d['fcf'] / d['ev_abs'] if d['fcf'] is not None else None)
    rows.append(dict(key=key, name=name, type=t, ctype=TYPES[t], role=ROLE[t], country=ctry, gics=gics, yahoo=yh, ccy=ccy,
                     usd_bn=round(usd / 1e9, 2), nd=None if nd is None else round(nd, 2), cov=d['cov'], cov_stress=None if cov_s is None else round(cov_s, 2),
                     ev=d['ev'], cash_yield=None if cy is None else round(cy, 4), roic=d['roic'], wacc=d['wacc'],
                     spread=None if d['roic'] is None or d['wacc'] is None else round((d['roic'] - d['wacc']) * 100, 2),
                     ocf_ebitda=None if not d['ebitda'] or d['ocf'] is None else round(d['ocf'] / d['ebitda'], 2),
                     dy=d['dy'] or 0.0, fpe=d['fpe'], pe=d['pe'], fcfy=d['fcfy'], revg3=d['revg3'], beta=d['beta'],
                     liq_cap=None if liq is None else round(min(liq, 1), 4), shock=SHOCK[t]))

for t in TYPES:
    ts = sorted([r for r in rows if r['type'] == t], key=lambda r: -r['usd_bn'])
    for i, r in enumerate(ts, 1): r['size_rank'] = i; r['in_universe'] = i <= 20 and r['usd_bn'] >= 1.0
    uni = [r for r in ts if r['in_universe']]
    med_nd = st.median([r['nd'] for r in uni if r['nd'] is not None])
    med_ev = st.median([r['ev'] for r in uni if r['ev'] is not None])
    for r in ts: r['type_med_nd'] = round(med_nd, 2); r['type_med_ev'] = round(med_ev, 2)

def decide(r):
    if not r['in_universe']: return 'Outside universe', f"size rank {r['size_rank']} in its type (top 20, US$1bn floor)"
    # M1 material exposure
    if r['gics'] not in QUALIFYING:
        seg = SEGMENT.get(r['key'])
        if not seg or seg[0] < 0.5:
            return 'Reject (M1)', (f"qualifying revenue {seg[0]*100:.0f}% < 50% ({seg[1]})" if seg else f"{r['gics']} is not a qualifying sub-industry")
    # M2 earns from the capacity
    if r['roic'] is None or r['roic'] <= 0: return 'Reject (M2)', f"ROIC {'n/a' if r['roic'] is None else f'{r['roic']*100:.1f}%'}: not yet earning from its capacity"
    if r['ocf_ebitda'] is None or r['ocf_ebitda'] <= 0: return 'Reject (M2)', 'operating cash flow not positive'
    # V1 debt service under stress
    if r['nd'] is not None and r['nd'] > 0:
        if r['cov_stress'] is None: return 'Watchlist (evidence)', 'interest cover not available'
        if r['cov_stress'] < 1.5: return 'Reject (V1)', f"stressed interest cover {r['cov_stress']:.2f}× < 1.5× (EBITDA −{int(r['shock']*100)}%; cover today {r['cov']:.2f}×)"
    # V2 leverage outlier
    if r['nd'] is not None and r['nd'] > r['type_med_nd'] + 2.0:
        return 'Reject (V2)', f"net debt/EBITDA {r['nd']:.2f}× vs type median {r['type_med_nd']:.2f}× (+2.0 limit)"
    # V3 investability
    if r['key'] in NO_PRICES: return 'Reject (V3)', NO_PRICES[r['key']]
    if r['liq_cap'] is not None and r['liq_cap'] < 0.01: return 'Reject (V3)', f"liquidity capacity {r['liq_cap']*100:.2f}% of NAV < 1%"
    # V4 governance
    if r['key'] in GOVERNANCE: return 'Reject (V4)', GOVERNANCE[r['key']]
    if r['ev'] is None or r['spread'] is None or r['cash_yield'] is None: return 'Watchlist (evidence)', 'valuation or return data missing'
    return 'Ranked', ''

for r in rows: r['stage'], r['why'] = decide(r)

def pct(vals, v, low):
    n = len(vals)
    if n == 1: return 1.0
    worse = sum(1 for x in vals if (x > v if low else x < v)); eq = sum(1 for x in vals if x == v) - 1
    return (worse + 0.5 * eq) / (n - 1)
for t in TYPES:
    ps = [r for r in rows if r['type'] == t and r['stage'] == 'Ranked']
    evs = [r['ev'] for r in ps]; cys = [r['cash_yield'] for r in ps]; sps = [r['spread'] for r in ps]
    for r in ps:
        r['val_pct'] = (pct(evs, r['ev'], True) + pct(cys, r['cash_yield'], False)) / 2
        r['qual_pct'] = pct(sps, r['spread'], False)
        r['merit'] = (r['val_pct'] + r['qual_pct']) / 2
        r['peers'] = len(ps); r['peer_med_ev'] = round(st.median(evs), 2); r['peer_med_spread'] = round(st.median(sps), 2)
        r['peer_med_cy'] = round(st.median(cys), 4)
    ps.sort(key=lambda r: (-r['merit'], -r['spread']))
    for i, r in enumerate(ps, 1):
        r['merit_rank'] = i
        if r['ocf_ebitda'] < 0.5: r['stage'], r['why'] = 'Watchlist (V5)', f"operating cash flow {r['ocf_ebitda']*100:.0f}% of EBITDA < 50%"
        elif r['ev'] > 2 * r['type_med_ev']: r['stage'], r['why'] = 'Watchlist (V6)', f"EV/EBITDA {r['ev']:.1f}× > 2× type median {r['type_med_ev']:.1f}×"
        elif r['merit'] < 0.5: r['stage'], r['why'] = 'Watchlist (V7)', f"merit {r['merit']:.2f} in bottom half of {len(ps)} ranked {TYPES[t].lower()}"
        else: r['stage'], r['why'] = 'Eligible', f"merit {r['merit']:.2f}, rank {i} of {len(ps)}"

json.dump(rows, open('universe4.json', 'w'), indent=1)
if __name__ == '__main__':
    from collections import Counter
    U = [r for r in rows if r['in_universe']]
    print('universe', len(U), Counter(r['stage'].split(' (')[0] for r in U), Counter(r['stage'] for r in U))
    for t in TYPES:
        print(f'\n== {TYPES[t]}')
        for r in sorted([r for r in U if r['type'] == t], key=lambda r: (r.get('merit_rank', 99), r['size_rank'])):
            if 'merit' in r:
                print(f"  #{r['merit_rank']:<2} {r['key']:<10}{r['country']} ${r['usd_bn']:7.1f}B EV {r['ev']:5.1f} cy {r['cash_yield']*100:5.1f}% spr {r['spread']:+6.1f} nd {r['nd']} covS {r['cov_stress']} merit {r['merit']:.2f} -> {r['stage']} {r['why'] if not r['stage']=='Eligible' else ''}")
            else:
                print(f"  -- {r['key']:<10}{r['country']} ${r['usd_bn']:7.1f}B {r['stage']}: {r['why']}")
