"""Run: python3 bench_nfra.py  ->  bench.json. Benchmark series (NFRA, IGF) in pesos on the model's weekly grid; stats with the same definitions as analyze4.py."""
import json, numpy as np, pandas as pd, sys
S = pd.read_pickle(sys.argv[1] if len(sys.argv) > 1 else 'sim4.pkl'); R = S['R']; P = 52
d = json.load(open('map/bench_usd.json')); F = pd.date_range('2018-06-01', '2026-10-02', freq='7D')
def php(s):
    usd = pd.Series([float(x) for x in d[s].split(',')], index=F).pct_change().iloc[1:]
    return (1 + usd.values) * (1 + R['USDPHP'].values) - 1
for s in ['NFRA', 'IGF']: R[s] = php(s)
net = S['net4']; idx = net.index
ser = {'v4': net, 'nfra': R.loc[idx, 'NFRA'], 'igf': R.loc[idx, 'IGF'], 'acwi': R.loc[idx, 'ACWI']}
rf = R.loc[idx, 'CASH']
def stats(r, bench):
    w = (1 + r).cumprod(); yrs = len(r)/P; cagr = w.iloc[-1]**(1/yrs) - 1; vol = r.std()*np.sqrt(P)
    dd = w/w.cummax() - 1
    r52 = (1 + r).rolling(P).apply(np.prod, raw=True) - 1
    rfp = (1 + rf).prod()**(1/yrs) - 1; c = np.cov(r, bench)
    return dict(cagr=cagr, vol=vol, sharpe=(cagr - rfp)/vol, maxdd=dd.min(), worst12=r52.min(), growth=100*w.iloc[-1], beta=c[0, 1]/c[1, 1])
def cal(r):
    o = {}
    for y in range(2021, 2027):
        a = f'{y}-01-01' if y > 2021 else '2021-10-01'; o[str(y)] = (1 + r.loc[a:f'{y}-12-31']).prod() - 1
    return o
out = {}
for k in ['nfra', 'igf']:
    out[k] = dict(stats=stats(ser[k], ser['acwi']), cal=cal(ser[k]), path=[round(100*x, 3) for x in (1 + ser[k]).cumprod().values])
out['v4_vs_nfra'] = dict(beta=stats(net, ser['nfra'])['beta'], corr=float(np.corrcoef(net, ser['nfra'])[0, 1]),
                         excess_pa=stats(net, ser['nfra'])['cagr'] - out['nfra']['stats']['cagr'])
json.dump(out, open('bench.json', 'w'), indent=1, default=float)
for k in ['nfra', 'igf']:
    s = out[k]['stats']; print(k, {a: round(b*100, 2) if a not in ('growth', 'beta', 'sharpe') else round(b, 2) for a, b in s.items()}, {a: round(b*100, 1) for a, b in out[k]['cal'].items()})
print('v4 vs NFRA', {a: round(b, 3) for a, b in out['v4_vs_nfra'].items()})
