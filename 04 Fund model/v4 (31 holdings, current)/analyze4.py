"""All v4 numbers for the deck, fact sheet and doc. Reads sim4.pkl, map/universe4.json, ../../results_v4.pkl. Writes results4.json."""
import json, numpy as np, pandas as pd, sys
sys.path.insert(0, '../..'); import backtest as BT
from engine4 import UNI, V4LIM, GROUP, WHT, window
P = 52
S = pd.read_pickle('sim4.pkl'); R = S['R']
if 'PSEI' not in R:   # PSEi tracker (FMETF price, PSE Edge), weekly Friday closes; added 8 Oct 2026
    R['PSEI'] = np.array(json.load(open('map/psei.json'))['PSEI'], float) / 1e5
net = S['net4']; idx = net.index
ser = {'v4': net, 'v4_ew': S['net_ew'], 'v4_iv': S['net_iv'], 'v3': S['net3'], 'acwi': R.loc[idx, 'ACWI'], 'ixn': R.loc[idx, 'IXN'], 'psei': R.loc[idx, 'PSEI']}
rf = R.loc[idx, 'CASH']

def stats(r):
    w = (1 + r).cumprod(); yrs = len(r)/P; cagr = w.iloc[-1]**(1/yrs) - 1; vol = r.std()*np.sqrt(P)
    dd = w/w.cummax() - 1; trough = dd.idxmin(); peak = w.loc[:trough].idxmax()
    rec = w.loc[trough:][w.loc[trough:] >= w.loc[peak]]
    r52 = (1 + r).rolling(P).apply(np.prod, raw=True) - 1
    rfp = (1 + rf).prod()**(1/yrs) - 1
    c = np.cov(r, ser['acwi']);
    return dict(cagr=cagr, vol=vol, sharpe=(cagr - rfp)/vol, maxdd=dd.min(), dd_peak=str(peak.date()), dd_trough=str(trough.date()),
                recovered=str(rec.index[0].date()) if len(rec) else None, worst12=r52.min(), best12=r52.max(), pos12=float((r52.dropna() > 0).mean()),
                growth=100*w.iloc[-1], beta=c[0, 1]/c[1, 1], corr=float(np.corrcoef(r, ser['acwi'])[0, 1]), rf=rfp)
def cal(r):
    o = {}
    for y in range(2021, 2027):
        a = f'{y}-01-01' if y > 2021 else '2021-10-01'; o[str(y)] = (1 + r.loc[a:f'{y}-12-31']).prod() - 1
    return o
def trailing(r, y): x = r.iloc[-int(round(y*P)):]; return (1 + x).prod()**(1/y) - 1
five = {k: dict(stats=stats(v), cal=cal(v), trail={f'{y}y': trailing(v, y) for y in (1, 3, 5)},
               dd2022=float(((1 + v.loc['2021-12-01':'2022-12-31']).cumprod()).pipe(lambda w: (w/w.cummax() - 1).min())))
        for k, v in ser.items()}
yrs = len(net)/P
costs = {k: dict(trading_pa=S[c]['trading_cost_total']/yrs, wht_pa=S[c]['wht_total']/yrs) for k, c in [('v4', 'c4'), ('v4_ew', 'c_ew'), ('v4_iv', 'c_iv'), ('v3', 'c3')]}
# growth path for charts (weekly cumulative, ₱100)
paths = {k: [round(100*x, 3) for x in (1 + v).cumprod().values] for k, v in ser.items()}
dates = [str(d.date()) for d in idx]

# ---- current portfolio ----
held = S['held']; w = S['w_now'].reindex(held); cov = S['cov_now']
wv = w.values; pv = wv @ cov @ wv; rc = wv*(cov @ wv)/pv; vol_i = np.sqrt(np.diag(cov)); cm = cov/np.outer(vol_i, vol_i)
avgc = [(cm[i].sum() - 1)/(len(held) - 1) for i in range(len(held))]
tw = {};
for k in held: tw[UNI[k]['ctype']] = tw.get(UNI[k]['ctype'], 0) + w[k]
port = []
for i, k in enumerate(held):
    u = UNI[k]; b = []
    if w[k] >= V4LIM['liq'][k] - 1e-4: b.append(f"liquidity limit {V4LIM['liq'][k]*100:.1f}%")
    if tw[u['ctype']] >= 0.25 - 1e-4: b.append('capacity-type limit 25%')
    if w[k] >= 0.20 - 1e-4: b.append('issuer ceiling 20%')
    port.append(dict(key=k, name=u['name'], country=u['country'], ctype=u['ctype'], role=u['role'], weight=float(w[k]), risk_share=float(rc[i]),
                     vol=float(vol_i[i]), avg_corr=float(avgc[i]), binding=b, merit=u['merit'], merit_rank=u['merit_rank'], peers=u['peers'],
                     ev=u['ev'], peer_med_ev=u['peer_med_ev'], cash_yield=u['cash_yield'], peer_med_cy=u['peer_med_cy'], spread=u['spread'],
                     peer_med_spread=u['peer_med_spread'], nd=u['nd'], cov=u['cov'], cov_stress=u['cov_stress'], shock=u['shock'],
                     ocf_ebitda=u['ocf_ebitda'], dy=u['dy'], liq_cap=u['liq_cap'], usd_bn=u['usd_bn'], gics=u['gics'], roic=u['roic'], wacc=u['wacc']))
port.sort(key=lambda d: -d['weight'])
def agg(f):
    d = {}
    for p in port: d[p[f]] = d.get(p[f], 0) + p['weight']
    return dict(sorted(d.items(), key=lambda x: -x[1]))
ev, evec = np.linalg.eigh(cm); ev = ev[::-1]
dr = float(wv @ vol_i/np.sqrt(pv))
# weights through time; PH share; rule checks at every rebalance
wl = S['wl4']; ph = [k for k in wl.columns if k in UNI and UNI[k]['country'] == 'PH']
ph_share = wl[ph].sum(axis=1)
viol = []
for t, row in wl.iterrows():
    row = row[row > 1e-9]; eq = row.drop('CASH')
    if eq.max() > 0.20 + 1e-4: viol.append((str(t.date()), 'issuer'))
    for c in set(UNI[k]['ctype'] for k in eq.index):
        if sum(eq[k] for k in eq.index if UNI[k]['ctype'] == c) > 0.25 + 1e-4: viol.append((str(t.date()), 'type ' + c))
    for g in set(GROUP.get(k) for k in eq.index if GROUP.get(k)):
        if sum(eq[k] for k in eq.index if GROUP.get(k) == g) > 0.20 + 1e-4: viol.append((str(t.date()), 'group'))
    for k in eq.index:
        if eq[k] > V4LIM['liq'][k] + 1e-4: viol.append((str(t.date()), 'liq ' + k))
# EW / IV current weights for the same holdings
iv = 1/vol_i; w_iv = iv/iv.sum()*0.97
alt_now = dict(ew={k: 0.97/len(held) for k in held}, iv={k: float(w_iv[i]) for i, k in enumerate(held)})
alt_types = {s: {} for s in alt_now}
for s, d in alt_now.items():
    for k, x in d.items(): alt_types[s][UNI[k]['ctype']] = alt_types[s].get(UNI[k]['ctype'], 0) + x

# ---- funnel ----
U = [r for r in UNI.values() if r['in_universe']]
stage_after = {k: s for k, s, _ in S['log']}
funnel = dict(universe=len(U), by_type={t: sum(1 for r in U if r['ctype'] == t) for t in sorted(set(r['ctype'] for r in U))},
              m_pass=sum(1 for r in U if not r['stage'].startswith('Reject (M')),
              v_reject=sum(1 for r in U if r['stage'].startswith('Reject (V')),
              watch_v=sum(1 for r in U if r['stage'].startswith('Watchlist')),
              eligible=sum(1 for r in U if r['stage'] == 'Eligible'), held=len(held),
              watch_p=sum(1 for k, s, _ in S['log'] if s.startswith('Watchlist')),
              reasons={s: sum(1 for r in U if r['stage'] == s) for s in sorted(set(r['stage'] for r in U))},
              p_reasons={s: sum(1 for k, s2, _ in S['log'] if s2 == s and k not in held) for s in sorted(set(s for _, s, _ in S['log']))})
decisions = [dict(key=r['key'], name=r['name'], country=r['country'], ctype=r['ctype'], usd_bn=r['usd_bn'], stage=r['stage'], why=r['why'],
                  merit=r.get('merit'), merit_rank=r.get('merit_rank'), peers=r.get('peers'), ev=r['ev'], cash_yield=r['cash_yield'], spread=r['spread'],
                  nd=r['nd'], cov_stress=r['cov_stress'], p=next(((s, why) for k, s, why in S['log'] if k == r['key']), None)) for r in U]

# ---- 36-year industry proxy ----
L = pd.read_pickle('../../results_v4.pkl'); cap, mkt, tech, us = L['cap4'], L['mkt4'], L['tech4'], L['us']
import os; _cwd = os.getcwd(); os.chdir('../..'); df = BT.load(); os.chdir(_cwd)
def s36(r):
    s = BT.stats(r); w_ = (1 + r).cumprod(); dd = w_/w_.cummax() - 1; t0 = dd.idxmin(); pk = w_.loc[:t0].idxmax()
    rec = w_.loc[t0:][w_.loc[t0:] >= w_.loc[pk]]
    months = (rec.index[0] - pk).n if len(rec) else None
    b, c = BT.beta(r.values, mkt.values)
    return dict(cagr=s['CAGR'], vol=s['Vol'], maxdd=s['MaxDD'], worst12=s['Worst12m'], growth=s['Growth_of_100'], usd_sharpe=BT.usd_sharpe(r, df),
                beta_vs_mkt=b, corr_vs_mkt=c, months_peak_to_recovery=months, worst5y_pa=s['Worst5y_pa'], pos5y=s['Pos5y'])
crises = {'Asian crisis, Jul 1997 – Dec 1998': ('1997-07', '1998-12'), 'Dot-com, Mar 2000 – Sep 2002': ('2000-03', '2002-09'),
          'Global financial crisis, Nov 2007 – Feb 2009': ('2007-11', '2009-02'), 'COVID, Jan – Jun 2020': ('2020-01', '2020-06'), '2022 rate shock': ('2022-01', '2022-12')}
dec = {'1990s': ('1990-01', '1999-12'), '2000s': ('2000-01', '2009-12'), '2010s': ('2010-01', '2019-12'), '2020 – Aug 2026': ('2020-01', '2026-08')}
def ann(r, a, b): x = r.loc[a:b]; return (1 + x).prod()**(12/len(x)) - 1
yrs36 = sorted(set(p.year for p in cap.index))
calp = {y: {k: (1 + s[[p.year == y for p in s.index]]).prod() - 1 for k, s in [('cap', cap), ('mkt', mkt), ('tech', tech)]} for y in yrs36}
def dsum(d): return dict(worst=float(d.min()), p5=float(d.quantile(.05)), median=float(d.median()), below1=float((d < 1).mean()), n=len(d),
                         worst_end=str(d.idxmin()))
proxy = dict(stats={k: s36(v) for k, v in [('cap', cap), ('mkt', mkt), ('tech', tech)]},
             crises={n: {k: float((1 + s.loc[a:b]).prod() - 1) for k, s in [('cap', cap), ('mkt', mkt), ('tech', tech)]} for n, (a, b) in crises.items()},
             decades={n: {k: ann(s, a, b) for k, s in [('cap', cap), ('mkt', mkt), ('tech', tech)]} for n, (a, b) in dec.items()},
             years_ahead={'mkt': sum(calp[y]['cap'] > calp[y]['mkt'] for y in yrs36), 'tech': sum(calp[y]['cap'] > calp[y]['tech'] for y in yrs36), 'n': len(yrs36)},
             contrib={k: dsum(L[k]) for k in ['dca', 'dca_glide', 'dca_mkt', 'dca_tech']},
             growth={k: [round(100*x, 2) for x in (1 + s).cumprod().values] for k, s in [('cap', cap), ('mkt', mkt), ('tech', tech)]},
             months=[str(p) for p in cap.index], w_last=L['w4'].iloc[-1].to_dict())

out = dict(five=five, costs=costs, paths=paths, dates=dates, portfolio=port, by_type=agg('ctype'), by_country=agg('country'), by_role=agg('role'),
           n_held=len(held), div_ratio=dr, eff_bets=dr**2, top2_factor=float(ev[:2].sum()/ev.sum()), ph_now=float(sum(p['weight'] for p in port if p['country'] == 'PH')),
           ph_range=[float(ph_share.min()), float(ph_share.max())], rebalances=len(wl), violations=viol, alt_now=alt_now, alt_types=alt_types,
           funnel=funnel, decisions=decisions, plog=S['log'], proxy=proxy, cash=0.03)
json.dump(out, open('results4.json', 'w'), indent=1, default=float)
f = lambda x: f'{x*100:.2f}%'
for k in ser: s = five[k]['stats']; print(f"{k:6s} cagr {f(s['cagr'])} vol {f(s['vol'])} sharpe {s['sharpe']:.2f} maxdd {f(s['maxdd'])} worst12 {f(s['worst12'])} g {s['growth']:.1f} beta {s['beta']:.2f} dd2022 {f(five[k]['dd2022'])} cal {[round(v*100,1) for v in five[k]['cal'].values()]} trail {[round(v*100,1) for v in five[k]['trail'].values()]}")
print('costs', costs); print('n', len(held), 'DR^2', round(dr**2, 2), 'top2', round(out['top2_factor'], 3), 'PH', out['ph_now'], out['ph_range'], 'viol', viol, 'rebal', len(wl))
print('types', {k: round(v*100, 2) for k, v in out['by_type'].items()}); print('alt types', {s: {k: round(v*100, 1) for k, v in d.items()} for s, d in alt_types.items()})
print('funnel', funnel)
for k, v in proxy['stats'].items(): print(k, {a: round(b, 4) if isinstance(b, float) else b for a, b in v.items()})
print(proxy['crises']); print(proxy['decades']); print(proxy['years_ahead']); print(proxy['contrib'])
