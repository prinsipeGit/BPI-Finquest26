"""Map v3 (global, no regions): theme fit -> merit rank -> top 3 per capacity type. Writes ../inputs.py, ../yret.json, ../ph.txt."""
import json, sys, pprint, importlib.util as U
from universe3 import TYPES, ROLE, FX, SEGMENT
def load(name, path):
    s = U.spec_from_file_location(name, path); m = U.module_from_spec(s); s.loader.exec_module(m); return m
V1 = load('V1', '../v1 (15 holdings, superseded)/inputs.py'); V2 = load('V2', '../v2 (33 holdings, superseded)/inputs.py')
rows = {r['key']: r for r in json.load(open('universe3.json'))}
T1 = {c[0]: (c[10], c[11]) for c in V1.CANDIDATES if c[10]}; T2 = {c[0]: (c[10], c[11]) for c in V2.CANDIDATES if c[10]}
THEME = {**T1, **T2,
 'ELE': ('Add 1,900 MW of renewables to reach 13,200 MW installed by 2028; EUR 5.5bn grid capex 2026-28', 'https://www.endesa.com/en/press/press-room/news/economic-information/2025-results-2026-2028-strategic-plan'),
 'ENGI': ('95 GW of installed renewable and storage capacity by 2030 (57.2 GW at end-2025)', 'https://www.engie.com/app/uploads/2026/03/PR-ENGIE-FY-2025-VDEF.pdf'),
 'AMX': ('Over 5,400 km of new fibre network in Peru during 2026 (Claro)', 'https://www.claro.com.pe/portal/pe/recursos_contenido/pdf/NP_Proyeccion_Despliegue-FO2026-140826.pdf'),
 'STC': ('center3 data-centre arm targets 1 GW of capacity by 2030', 'https://www.datacenterdynamics.com/en/news/saudis-center3-targets-1gw-of-data-center-capacity-by-2030/'),
 'EAND': ('US$6bn network investment across 16 markets, 2024-2026', 'https://enterpriseam.com/uae/2024/03/04/e-to-invest-usd-6-bn-to-boost-network-connectivity-access-across-three-regions-by-2026/'),
 'KAMIGUMI': ('New 34,147 m2 automated cold-storage warehouse at Kobe Port Island, complete Aug 2029', 'https://www.kamigumi.co.jp/english/news/2026/000359.html'),
 'NEX': ('EUR 90m to build and upgrade plants for 525 kV HVDC cable, complete by 2026', 'https://www.offshorewind.biz/2024/09/13/nexans-sets-aside-eur-90-million-to-support-european-offshore-wind-growth'),
 'OMAB': ('MXN 16bn 2026-30 plan; Monterrey capacity up ~50% to over 18M passengers a year', 'https://www.elfinanciero.com.mx/empresas/2026/06/05/oma-destina-16-mil-mdp-a-tecnologia-y-expansion-de-sus-aeropuertos/'),
 'HDHE': ('KRW 397bn to expand Ulsan and Alabama transformer capacity, complete by 2028', 'https://transformer-magazine.com/news/hd-hyundai-electric-to-invest-272-3-m-in-transformer-production/'),
 'SKHYNIX': ('KRW 19tn Cheongju HBM packaging fab, operating by end-2027', 'https://www.trendforce.com/news/2026/01/13/news-sk-hynix-to-build-cheongju-advanced-packaging-fab-boosting-hbm-output-by-2027/'),
 'JAT': ('Haneda T1 north satellite adds 6 gate spots by summer 2026; T2 extension spring 2027', 'https://www.aviationwire.jp/?p=343514'),
}
THEME_FAIL = {'GDI': 'no dated capacity number found'}
DATA_FAIL = {'EAND': 'no price history available from our sources (Abu Dhabi listing); cannot be simulated'}
STORY = {1: 'First home: the power behind the electricity bill', 2: 'First home: a reliable water connection',
         3: 'First job and schooling: the network behind every phone and laptop', 4: 'First business: goods coming in and going out',
         5: 'First trip: the airport and the road to it', 6: 'First home: the transformers and cables that connect it',
         7: 'Every first: the chips inside phones, laptops and data centres'}
DRIVER = {1: 'Electrification', 2: 'Urban water demand', 3: 'Data traffic', 4: 'Trade volumes', 5: 'Air travel',
          6: 'Electrification + data-centre power', 7: 'AI and data-centre chips'}
held = []
for t in TYPES:
    ranked = sorted([r for r in rows.values() if r['type'] == t and r['stage'] == 'Ranked'],
                    key=lambda r: (-r['merit'], -r['spread']))   # ties: higher return spread wins
    n = 0
    for i, r in enumerate(ranked, 1):
        r['rank_tb'] = i
        if r['key'] in THEME_FAIL: r['stage'] = 'Fail M evidence'; r['why'] = 'theme evidence: ' + THEME_FAIL[r['key']]; continue
        if r['key'] in DATA_FAIL: r['stage'] = 'Excluded (data)'; r['why'] = DATA_FAIL[r['key']]; continue
        if n < 3:
            assert r['key'] in THEME, r['key']
            r['stage'] = 'HELD'; held.append(r['key']); n += 1
        else: r['stage'] = 'Ranked, not held'; r['why'] = f'merit rank {i} of {len(ranked)}'
raw = {}
for line in open('st3.txt').readlines() + open('st3_extra.txt').readlines():
    k, ccy, mc, sh, vol, *_ = line.rstrip('\n').split('|'); raw[k] = (ccy or 'USD', mc, sh, vol)
def num(s):
    s = s.replace(',', ''); m = {'T': 1e12, 'B': 1e9, 'M': 1e6}
    return float(s[:-1])*m[s[-1]] if s[-1] in m else float(s)
ADV = {k: round(num(raw[k][3])*num(raw[k][1])/num(raw[k][2])) for k in held}
FXP = {c: round(FX['PHP']/v, 6) for c, v in FX.items()}
cand = []
for r in rows.values():
    tg, src = THEME.get(r['key'], ('', '')) if r['stage'] == 'HELD' else ('', '')
    res = 'PASS' if r['stage'] == 'HELD' else r['stage'] + (': ' + r['why'] if r.get('why') else '')
    cand.append((r['key'], r['name'], r['country'], raw[r['key']][0], r['role'], r['gics'], STORY[r['type']], r['nd'], r['cov'], r['ev'],
                 tg, src, res, TYPES[r['type']], 'Global', r['usd_bn']))
MERIT = {r['key']: dict(roic=r['roic'], wacc=r['wacc'], spread=r['spread'], val_pct=r.get('val_pct'), qual_pct=r.get('qual_pct'),
                        merit=r.get('merit'), rank=r.get('rank_tb'), peers=r.get('peers'), peer_med_ev=r.get('peer_med_ev'),
                        peer_med_spread=r.get('peer_med_spread'), size_rank=r['size_rank'], driver=DRIVER[r['type']], ctype=r['type'],
                        liq_cap=r['liq_cap']) for r in rows.values()}
GROUP = {'ICT': 'Razon group', 'MWC': 'Razon group', 'ENEL': 'Enel group', 'ELE': 'Enel group'}
with open('../inputs.py', 'w') as f:
    f.write('"""Static inputs for The Firsts Fund, Map v3 (global, no regions), pulled 7 Oct 2026. See AGENTS.md."""\n\n')
    f.write('PH_POLICY = ' + pprint.pformat(V1.PH_POLICY, width=120, compact=True) + '\n\n')
    f.write('PH_DIVS = ' + pprint.pformat({k: V1.PH_DIVS[k] for k in ['ICT', 'MWC']}, width=120) + '\n\n')
    f.write('# Average daily traded value, local currency: 20-day average volume x last price (stockanalysis.com, 7 Oct 2026)\n')
    f.write('ADV_LOCAL = ' + pprint.pformat(dict(sorted(ADV.items())), width=120, compact=True) + '\n\n')
    f.write('FX_TO_PHP = ' + pprint.pformat(FXP, width=120, compact=True) + '\n\n')
    f.write('# key, name, country, ccy, role, gics (team-assigned), story line, nd, cov, ev, capacity target, source, result, capacity type, scope, USD bn\n')
    f.write('CANDIDATES = [\n' + ''.join(' ' + repr(c) + ',\n' for c in cand) + ']\n\n')
    f.write('MERIT = ' + pprint.pformat(MERIT, width=140) + '\n\n')
    f.write('SEGMENT = ' + pprint.pformat(SEGMENT, width=140) + '\n\n')
    f.write('GROUP = ' + pprint.pformat(GROUP, width=120) + '\n')
y1 = json.load(open('../v1 (15 holdings, superseded)/yret.json')); y2 = json.load(open('../v2 (33 holdings, superseded)/yret.json'))
out = {k: y1[k] for k in ['SU', 'TSMC', 'WPRTS', 'ACWI', 'USDPHP']}
for k in ['ENEL', 'SBS', 'VIE', 'DTE', 'ASR', 'MU']: out[k] = y2[k]
for i in range(2):
    for line in open(f'd{i}.txt').read().strip().split('\n'):
        k, v = line.split(':'); out[k] = [None if x == 'x' else int(x) for x in v.split(',')]
missing = [k for k in held if k not in out and k not in ('ICT', 'MWC')]
json.dump({k: out[k] for k in [h for h in held if h in out] + ['ACWI', 'USDPHP']}, open('../yret.json', 'w'))
open('../ph.txt', 'w').write(open('../v2 (33 holdings, superseded)/ph.txt').read())
print(len(held), held, 'missing', missing)
for t in TYPES: print(TYPES[t], [k for k in held if rows[k]['type'] == t])
