"""Everything the fact sheet prints, recomputed from engine.py output. Writes results.json."""
import json, numpy as np, pandas as pd
import engine as E

S = pd.read_pickle('sim.pkl'); R, net = S['R'], S['net']; caps = S['caps']
acwi = R.loc[net.index, 'ACWI']; cash = R.loc[net.index, 'CASH']
P = 52

def stats(r, rf):
    w = (1 + r).cumprod(); yrs = len(r) / P
    cagr = w.iloc[-1]**(1/yrs) - 1; vol = r.std()*np.sqrt(P)
    ex = r - rf; down = np.sqrt((np.minimum(ex, 0)**2).mean())*np.sqrt(P)
    dd = w/w.cummax() - 1
    r52 = (1 + r).rolling(P).apply(np.prod, raw=True) - 1
    rf_pa = (1 + rf).prod()**(1/yrs) - 1
    return dict(cagr=cagr, vol=vol, sharpe=(cagr - rf_pa)/vol, sortino=(cagr - rf_pa)/down, downdev=down,
                maxdd=dd.min(), dd_trough=str(dd.idxmin().date()), dd_peak=str(w.loc[:dd.idxmin()].idxmax().date()),
                worst12=r52.min(), best12=r52.max(), pos12=(r52.dropna() > 0).mean(), growth=100*w.iloc[-1], rf_pa=rf_pa)

fs, bs = stats(net, cash), stats(acwi, cash)
c = np.cov(net, acwi); beta = c[0, 1]/c[1, 1]; corr = np.corrcoef(net, acwi)[0, 1]

def period(r, a, b): x = r.loc[a:b]; return (1 + x).prod() - 1
cal = {}
for y in range(2021, 2027):
    a, b = (f'{y}-01-01' if y > 2021 else '2021-10-01'), f'{y}-12-31'
    cal[str(y)] = (period(net, a, b), period(acwi, a, b))
def trailing(r, yrs):
    x = r.iloc[-int(round(yrs*P)):]; return (1 + x).prod()**(1/yrs) - 1
trail = {k: (trailing(net, y), trailing(acwi, y)) for k, y in [('1y', 1), ('3y', 3), ('5y', 5)]}

# ---- current portfolio: solved on data through 2 Oct 2026 --------------------------------------------
t_now = pd.Timestamp('2026-10-03')
w_now, cov, names = E.weights_at(R, t_now, caps)
w = w_now.values; pv = w @ cov @ w; rc = w*(cov @ w)/pv
vol_i = np.sqrt(np.diag(cov))
corr_m = cov/np.outer(vol_i, vol_i)
avg_corr = [(corr_m[i].sum() - 1)/(len(names) - 1) for i in range(len(names))]
port = []
for i, k in enumerate(names):
    inf = E.INFO[k]; binding = []
    if w[i] >= E.ISSUER - 1e-4: binding.append('issuer cap 10%')
    if w[i] >= caps[k] - 1e-4: binding.append(f'liquidity cap {caps[k]*100:.1f}%')
    g = E.GROUP.get(k)
    if g and sum(w[j] for j, n in enumerate(names) if E.GROUP.get(n) == g) >= E.GROUP_CAP - 1e-4: binding.append(f'group cap 15% ({g})')
    if sum(w[j] for j, n in enumerate(names) if E.INFO[n]['ctype'] == inf['ctype']) >= E.TYPE_CAP - 1e-4:
        binding.append('capacity-type cap 25%')
    port.append(dict(key=k, name=inf['name'], country=inf['country'], role=inf['role'], gics=inf['gics'],
                     milestone=inf['milestone'], ctype=inf['ctype'], weight=w[i], risk_share=rc[i], vol=vol_i[i], avg_corr=avg_corr[i],
                     binding=binding, liq_cap=caps[k], nd=inf['nd'], cov=inf['cov'], ev=inf['ev'],
                     target=inf['target'], source=inf['source']))
port.sort(key=lambda d: -d['weight'])

def agg(field):
    d = {}
    for p in port: d[p[field]] = d.get(p[field], 0) + p['weight']
    return dict(sorted(d.items(), key=lambda x: -x[1]))
groups = {}
for p in port:
    g = E.GROUP.get(p['key'], p['name']); groups[g] = groups.get(g, 0) + p['weight']

# effective number of bets (eigen-based) and share of risk in top two factors
ev_, evec = np.linalg.eigh(cov); ev_ = ev_[::-1]; evec = evec[:, ::-1]
fac_contrib = [(w @ evec[:, j])**2 * ev_[j] for j in range(len(names))]
fac_share = np.array(fac_contrib)/sum(fac_contrib)
enb = 1/np.sum(fac_share**2)

# ---- monthly series for contributor tests ----------------------------------------------------------
m = (1 + net).groupby(net.index.to_period('M')).prod() - 1
m = m.loc['2021-10':'2026-09']
rng = np.random.default_rng(7)
N = 20000
def contrib(rs, pay=1000):
    v = 0.0
    for r in rs: v = (v + pay)*(1 + r)
    return v
def withdraw(rs, start=60000, take=900):
    v = start
    for r in rs: v = v*(1 + r) - take
    return v
perms = [rng.permutation(m.values) for _ in range(N)]
first_half = np.array([np.prod(1 + p[:30]) - 1 for p in perms])
cfin = np.array([contrib(p) for p in perms]); wfin = np.array([withdraw(p) for p in perms])
mmf = sum(1000*(1.045**(1/12))**(60 - k) for k in range(60))   # paid at start of month, 4.5% MMF
shuffle = dict(corr_contrib=np.corrcoef(first_half, cfin)[0, 1], corr_withdraw=np.corrcoef(first_half, wfin)[0, 1],
               contrib_worst=cfin.min(), contrib_median=float(np.median(cfin)), contrib_best=cfin.max(), mmf=mmf,
               share_beat_mmf=(cfin > mmf).mean(), months=len(m))

# ---- glidepath: from month 37 (24 months out) move equal slices to a 4.5% MMF, leaving 15% in the Fund ----
mm = (1.045)**(1/12) - 1
def path(rs, glide):
    fund, safe = 0.0, 0.0
    for i, r in enumerate(rs):
        fund += 1000
        if glide and i >= 36:
            months_left = 60 - i
            target_fund = 0.15*(fund + safe)
            move = max(fund - target_fund, 0)/months_left
            fund -= move; safe += move
        fund *= (1 + r); safe *= (1 + mm)
    return fund + safe
gp = np.array([path(p, True) for p in perms]); ng = np.array([path(p, False) for p in perms])
glide = dict(worst_no=ng.min(), worst_glide=gp.min(), p5_no=np.percentile(ng, 5), p5_glide=np.percentile(gp, 5),
             spread_no=np.percentile(ng, 95) - np.percentile(ng, 5), spread_glide=np.percentile(gp, 95) - np.percentile(gp, 5),
             median_cost=float(np.median(ng - gp)), share_glide_wins_bottom_decile=float(np.mean((gp > ng)[ng <= np.percentile(ng, 10)])),
             median_no=float(np.median(ng)), median_glide=float(np.median(gp)))

# ---- peso translations -------------------------------------------------------------------------------
peso = dict(maxdd_on_5000=-fs['maxdd']*5000, worst12_on_5000=-fs['worst12']*5000)
r8 = 1.08**(1/12) - 1
n_months = 32   # Oct 2026 -> Jun 2029
pmt = 26000*r8/((1 + r8)**n_months - 1)/(1 + r8)   # paid at start of each month
paid12 = 12*round(pmt)
peso.update(calc_pmt=pmt, calc_paid12=paid12, calc_bad_year=-fs['worst12']*paid12,
            fv_1300_8pct_5y=sum(1300*(1 + r8)**(60 - k) for k in range(60)))

res = dict(fund=fs, bench=bs, beta=beta, corr=corr, calendar=cal, trailing=trail, portfolio=port,
           by_country=agg('country'), by_type=agg('ctype'), by_role=agg('role'), by_sector=agg('gics'), by_group=groups,
           enb=enb, top2_factor_share=float(fac_share[:2].sum()), shuffle=shuffle, glide=glide, peso=peso,
           rebalances=len(S['wlog']), start=str(net.index[0].date()), end=str(net.index[-1].date()))
json.dump(res, open('results.json', 'w'), indent=1, default=float)

# console summary
pct = lambda x: f'{x*100:.2f}%'
print('FUND', {k: (pct(v) if isinstance(v, float) and abs(v) < 5 else v) for k, v in fs.items()})
print('ACWI', {k: (pct(v) if isinstance(v, float) and abs(v) < 5 else v) for k, v in bs.items()})
print('beta', round(beta, 2), 'corr', round(corr, 2))
print('calendar', {k: (pct(a), pct(b)) for k, (a, b) in cal.items()})
print('trailing', {k: (pct(a), pct(b)) for k, (a, b) in trail.items()})
for p in port: print(f"{p['name']:<26}{p['country']} {p['role']:<9}{p['weight']*100:6.2f}% risk {p['risk_share']*100:5.2f}% vol {p['vol']*100:5.1f}% avgcorr {p['avg_corr']:.2f} {p['binding']}")
print('country', {k: pct(v) for k, v in res['by_country'].items()})
print('role', {k: pct(v) for k, v in res['by_role'].items()})
print('sector', {k: pct(v) for k, v in res['by_sector'].items()})
print('groups', {k: pct(v) for k, v in groups.items() if v > 0.1})
print('ENB', round(enb, 2), 'top2 factors', pct(res['top2_factor_share']))
print('shuffle', {k: round(v, 3) for k, v in shuffle.items()})
print('glide', {k: round(v, 3) for k, v in glide.items()})
print('peso', {k: round(v, 1) for k, v in peso.items()})

# ---- added: stressed glidepath + diversification ratio ------------------------------------------------
L = pd.read_pickle('../05 36-year backtest/results_v3.pkl')   # 36-year proxy aligned to v3 types: run backtest_v3.py there first
lc = L['cap3']; r12 = (1 + lc).rolling(12).apply(np.prod, raw=True) - 1
end = r12.idxmin(); crash = lc.loc[:end].iloc[-12:].values          # worst 12-month sequence in 36 years
stress_paths = [np.concatenate([p[:48], crash]) for p in perms]
sg = np.array([path(p, True) for p in stress_paths]); sn = np.array([path(p, False) for p in stress_paths])
stress = dict(crash_window=f'{lc.loc[:end].index[-12]} to {end}', crash_total=float(np.prod(1 + crash) - 1),
              worst_no=sn.min(), worst_glide=sg.min(), median_no=float(np.median(sn)), median_glide=float(np.median(sg)),
              p5_no=np.percentile(sn, 5), p5_glide=np.percentile(sg, 5),
              spread_no=np.percentile(sn, 95) - np.percentile(sn, 5), spread_glide=np.percentile(sg, 95) - np.percentile(sg, 5),
              glide_wins=float(np.mean(sg > sn)))
dr = (w @ vol_i)/np.sqrt(pv)
res['stress'] = stress; res['div_ratio_sq'] = float(dr**2)
json.dump(res, open('results.json', 'w'), indent=1, default=float)
print('stress', {k: (round(v, 3) if not isinstance(v, str) else v) for k, v in stress.items()})
print('diversification ratio^2 (independent bets)', round(dr**2, 2))
