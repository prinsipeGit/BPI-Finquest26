"""Builds ../v2/inputs.py and ../v2/yret.json from the Map v2 long-list (st_raw.txt), theme research and price chunks."""
import json, sys, pprint
sys.path.insert(0, '..')
import importlib.util as _u
_s = _u.spec_from_file_location('V1', '../v1 (15 holdings, superseded)/inputs.py'); V1 = _u.module_from_spec(_s); _s.loader.exec_module(V1)
from universe import L, FX, TYPES, ROLE, region
rows = {r['key']: r for r in json.load(open('longlist.json'))}

MILESTONE = {1: 'Housing (power), Business', 2: 'Housing (water)', 3: 'Education (connectivity), Business',
             4: 'Transport (ports), Business', 5: 'Travel (airports)', 6: 'Housing (grid equipment), Business',
             7: 'Education (chips for devices and data centres), Business'}
MS_OVERRIDE = {'JSEXP': 'Transport (roads)', 'ZJEXP': 'Transport (roads)', 'DG': 'Transport (roads), Travel (airports)'}
v1 = {c[0]: c for c in V1.CANDIDATES}
THEME = {  # key: (target, source) -- researched 7 Oct 2026; v1 targets reused where the company was already verified
 'ADANIPOWER': ('Installed generation capacity to 30,670 MW by 2030', 'https://www.tndindia.com/adani-power-targets-over-30-gw-installed-capacity-by-2030/'),
 'ENEL': ('2026-28 plan: installed capacity from ~68 GW to over 80 GW by 2028', 'https://www.teleborsa.it/AMP/News/2026/02/23/enel-il-50percent-dei-capex-per-rinnovabili-e-in-europa-capacita-installata-salira-a-80-gw-17.html'),
 'CEG': ('Restart the 837 MW Crane Clean Energy Center as early as 2027', 'https://world-nuclear-news.org/articles/crane-clean-energy-centre-on-line-for-ahead-of-schedule-restart'),
 'SO': ('US$81B capital plan 2026-2030, led by new gas generation', 'https://prodadmin.pgjonline.com/news/2026/february/southern-co-expands-81-billion-spending-plan-as-data-center-demand-drives-gas-generation-growth'),
 'VIE': ('Double operated desalination capacity from 1.4 million m3/day by 2030', 'https://www.veolia.com/en/our-media/press-releases/veolia-global-champion-sustainable-desalination-set-double-its-operated'),
 'AWK': ('US$19-20B of regulated system investment 2026-2030', 'https://s26.q4cdn.com/750150140/files/doc_presentations/2026/Mar/10/March-2026-Investor-Presentation.pdf'),
 'SBS': ('About R$70B of works to universalise water and sewage by 2029', 'https://www.infomoney.com.br/mercados/sabesp-supera-metas-de-novas-ligacoes-e-reforca-plano-de-universalizar-ate-2029/'),
 'CHMOB': ('100 EFLOPS of AI computing power by 2028', 'https://www.scmp.com/business/article/3328842/china-mobile-aims-triple-ai-computing-power-using-homegrown-chips-2028'),
 'AIRTEL': ('Nxtra data-centre capacity doubled to 400 MW by 2026', 'https://w.media/nxtra-planning-200-mw-data-center-in-hyderabad/'),
 'DTE': ('Fibre to every household and business in Germany by 2030', 'https://report.telekom.com/annual-report-2024/management-report/group-strategy/investments.html'),
 'SCMN': ('FTTH coverage 60% by end-2026, 75-80% by 2030', 'https://www.rcrwireless.com/?p=428496'),
 'VZ': ('More than 30 million fibre passings by 2028', 'https://www.verizon.com/about/news/feed/verizon-updates-broadband-strategy-bring-more-choice-flexibility-and-value-millions'),
 'TMUS': ('12-15 million households passed with fibre by end-2030', 'https://www.sec.gov/Archives/edgar/data/1283699/000119312524221282/d845022dex991.htm'),
 'JSEXP': ('Widen a 10.5 km G2 section from 6 to 10 lanes (RMB 2.9B), open in 2027', 'https://paper.cnstock.com/html/2024-08/28/content_1959114.htm'),
 'ZJEXP': ('Widen 25.2 km of the Zhajiasu Expressway to 8 lanes (RMB 7.3B) by 2028', 'https://m.thepaper.cn/detail/30699391'),
 'AENA': ('EUR 13B 2027-31 airport plan; network capacity above 358M passengers by 2031', 'https://www.travelextra.ie/spanish-government-approves-e13000m-airport-investment-plan/'),
 'PAC': ('Guadalajara airport expansion to 40M passengers a year by 2029', 'https://elceo.com/negocios/gap-remodela-aeropuerto-de-guadalajara-para-llegar-a-40-millones-de-pasajeros/'),
 'ASR': ('Cancun T4 phase-2 expansion fully operational by end-2028', 'https://www.marketbeat.com/instant-alerts/grupo-aeroportuario-del-sureste-q2-earnings-call-highlights-2026-07-24/'),
 'MELCO': ('New Marugame plant doubles C-GIS switchgear output by FY2027', 'https://www.mitsubishielectric.co.jp/ja/pr/2025/pdf/0807-b.pdf'),
 'SAMSUNG': ('Pyeongtaek P5, over 1.5x the capacity of P4, completion targeted 2030', 'https://trendforce.com/news/2026/08/20/news-samsung-to-break-ground-on-krw-6t-onyang-hbm-fab-in-sept-p5-eyes-triple-fab-shift-as-expansion-accelerates'),
 'IFX': ('EUR 5B Dresden Smart Power Fab, production start 2026', 'https://www.powerelectronicsnews.com/infineon-is-on-track-with-the-smart-power-fab-in-dresden-production-is-set-to-begin-in-2026'),
 'STM': ('EUR 5B Catania SiC campus: 15,000 wafers a week at full build-out by 2033', 'https://www.datacenterdynamics.com/en/news/stmicroelectronics-to-build-5bn-silicon-carbide-campus-in-italy-receives-funding-from-eu-chips-act'),
 'MU': ('Idaho Fab 1 DRAM output from 2027; aim for 40% of DRAM made in the US', 'https://www.trendforce.com/news/2025/06/13/news-micron-to-invest-200b-in-u-s-amid-trumps-reshoring-drive-targeting-40-dram-made-in-america/'),
}
for k in ['NTPC', 'ADPORTS', 'ICT', 'MWC', 'IBE', 'DG', 'SU', 'SIE', 'HITACHI', 'TSMC', 'MER', 'TEL', 'CNVRG', 'PGRID', 'WPRTS']:
    THEME[k] = (v1[k][10], v1[k][11])
THEME_FAIL = {'GDI': 'FAIL Theme: no dated capacity number found',
              'ORA': 'FAIL Theme: 2026-30 plan gives a capex ratio, no dated capacity number'}

# walk each cell by size; the two largest that pass all four tests are held
held, result = set(), {}
cells = {}
for key, t, ctry, gics, name, yh in L:
    cells.setdefault((t, region(ctry)), []).append(key)
for (t, reg), keys in cells.items():
    keys.sort(key=lambda k: -rows[k]['usd_bn']); n = 0
    for rank, k in enumerate(keys, 1):
        r = rows[k]
        if not r['fin_pass']:
            result[k] = 'FAIL ' + '; '.join(r['fin_fail']); continue
        if k in THEME_FAIL: result[k] = THEME_FAIL[k]; continue
        if n < 2 and k in THEME: result[k] = 'PASS'; held.add(k); n += 1; continue
        result[k] = f'BENCH: passed Debt, Price and Liquidity; not among the two largest passers in its cell'

raw = {}
for line in open('st_raw.txt').readlines()+open('st_raw_extra.txt').readlines():
    k, ccy, mc, sh, vol, *_ = line.rstrip('\n').split('|'); raw[k] = (ccy, mc, sh, vol)
def num(s):
    s = s.replace(',', ''); m = {'T': 1e12, 'B': 1e9, 'M': 1e6}
    return float(s[:-1])*m[s[-1]] if s[-1] in m else float(s)
PRICE_OVERRIDE = {'AIRTEL': 1833.9}  # stockanalysis lacks share count; Yahoo last price
ADV = {}
for k in held:
    ccy, mc, sh, vol = raw[k]
    px = PRICE_OVERRIDE.get(k) or num(mc)/num(sh)
    ADV[k] = round(num(vol)*px)
FXP = {c: FX['PHP']/v for c, v in FX.items()}

cand = []
for key, t, ctry, gics, name, yh in L:
    r = rows[key]; ccy = raw[key][0]
    tg, src = THEME.get(key, ('', ''))
    cand.append((key, name, ctry, ccy, ROLE[t], gics, MS_OVERRIDE.get(key, MILESTONE[t]), r['nd'], r['cov'], r['ev'],
                 tg if key in held else '', src if key in held else '', result[key], TYPES[t], region(ctry), r['usd_bn']))
GROUP = {'ICT': 'Razon group', 'MWC': 'Razon group', 'ADPORTS': 'Adani group', 'ADANIPOWER': 'Adani group',
         'NTPC': 'Government of India'}

hdr = '''"""Static inputs for The Firsts Fund, Map v2 (region-balanced), pulled 7 Oct 2026. See AGENTS.md for provenance.

Map v2: seven capacity types x three regions (Asia-Pacific incl. the Philippines; Europe; Americas).
In each cell, candidates are ranked by US-dollar market value; the two largest that pass every Verify test are held.
"""
'''
with open('../inputs.py', 'w') as f:
    f.write(hdr)
    f.write('PH_POLICY = ' + pprint.pformat(V1.PH_POLICY, width=120, compact=True) + '\n\n')
    f.write('# Cash dividends per share (PHP) by ex-date, PSE names held\n')
    f.write('PH_DIVS = ' + pprint.pformat({k: V1.PH_DIVS[k] for k in ['ICT', 'MWC']}, width=120) + '\n\n')
    f.write('# Average daily traded value in local currency: 20-day average volume x last price (stockanalysis.com, 7 Oct 2026)\n')
    f.write('ADV_LOCAL = ' + pprint.pformat(dict(sorted(ADV.items())), width=120, compact=True) + '\n\n')
    f.write('# Pesos per unit of local currency, Yahoo, 7 Oct 2026 (USDPHP 62.763)\n')
    f.write('FX_TO_PHP = ' + pprint.pformat({k: round(v, 6) for k, v in FXP.items()}, width=120, compact=True) + '\n\n')
    f.write('# key, name, country, ccy, role, gics, milestone(s), nd, cov, ev, capacity target, source, result, capacity type, region, USD bn\n')
    f.write('# nd = net debt/EBITDA, cov = EBIT/interest, ev = EV/EBITDA (stockanalysis.com, S&P Global data, 7 Oct 2026)\n')
    f.write('CANDIDATES = [\n' + ''.join(' ' + repr(c) + ',\n' for c in cand) + ']\n\n')
    f.write('GROUP = ' + pprint.pformat(GROUP, width=120) + '\n')
print(len(held), sorted(held))

# returns
y = json.load(open('../v1 (15 holdings, superseded)/yret.json'))
keep = ['NTPC', 'ADPORTS', 'IBE', 'SU', 'DG', 'SIE', 'HITACHI', 'TSMC', 'ACWI', 'USDPHP']
out = {k: y[k] for k in keep}
for i in range(3):
    for line in open(f'c{i}.txt').read().strip().split('\n'):
        k, v = line.split(':'); out[k] = [None if x == 'x' else int(x) for x in v.split(',')]
missing = [k for k in held if k not in out and k not in ('ICT', 'MWC')]
print('missing returns', missing)
json.dump(out, open('../yret.json', 'w'))
ph = [l for l in open('../v1 (15 holdings, superseded)/ph.txt').read().strip().split('\n') if l.split(':')[0] in ('ICT', 'MWC')]
open('../ph.txt', 'w').write('\n'.join(ph) + '\n')
