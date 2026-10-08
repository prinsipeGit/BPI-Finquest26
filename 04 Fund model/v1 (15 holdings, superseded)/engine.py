"""The Firsts Fund: Position step + 5-year simulation, no look-ahead.

Rules (fact sheet, revised 7 Oct 2026):
  equal risk contribution on trailing 156 weeks (min 104 weeks of history to enter)
  issuer <= 10%; control group <= 15%; country <= 1/3 of fund; Owners >= 45%; Suppliers <= 25%; Platforms <= 20%
  liquid reserve 10% earning the BSP policy rate; liquidity cap = ADV x 20% x 5 days / P1bn launch size
  quarterly rebalance (first Friday of Jan/Apr/Jul/Oct), drift in between; 1.50% p.a. fee
All returns in pesos, weekly (Friday closes).
"""
import json, numpy as np, pandas as pd
from scipy.optimize import minimize
from inputs import PH_POLICY, PH_DIVS, ADV_LOCAL, FX_TO_PHP, CANDIDATES, GROUP

AUM = 1e9; LIQ_SHARE = 0.20; LIQ_DAYS = 5
RESERVE = 0.10; FEE = 0.015; ISSUER = 0.10; GROUP_CAP = 0.15; COUNTRY_CAP = 1/3
ROLE_LIMITS = {'Owner': ('min', 0.45), 'Supplier': ('max', 0.25), 'Platform': ('max', 0.20)}
LOOKBACK, MIN_HIST = 156, 104
START, END = '2021-10-01', '2026-10-02'

HOLD = [c for c in CANDIDATES if c[-1] == 'PASS']
NAMES = [c[0] for c in HOLD]
INFO = {c[0]: dict(name=c[1], country=c[2], ccy=c[3], role=c[4], gics=c[5], milestone=c[6],
                   nd=c[7], cov=c[8], ev=c[9], target=c[10], source=c[11]) for c in HOLD}

def fridays():
    return pd.date_range('2018-06-01', '2026-10-02', freq='7D')

def load_returns():
    F = fridays()
    R = pd.DataFrame(index=F[1:])
    y = json.load(open('yret.json'))
    for k, v in y.items(): R[k] = np.array(v) / 1e5
    for line in open('ph.txt').read().strip().split('\n'):
        k, v = line.split(':')
        p = pd.Series([np.nan if x == 'x' else float(x) for x in v.split(',')], index=F)
        div = pd.Series(0.0, index=F)
        for d, amt in PH_DIVS[k]:
            wk = F[F >= pd.Timestamp(d)][0]          # dividend lands in the week containing its ex-date
            div[wk] += amt
        R[k] = ((p + div) / p.shift(1) - 1).iloc[1:].values
    # reserve: BSP policy rate, weekly
    cash = []
    for t in R.index:
        key = t.strftime('%y%m'); rate = PH_POLICY.get(key, list(PH_POLICY.values())[-1])
        cash.append((1 + rate/100)**(1/52) - 1)
    R['CASH'] = cash
    return R

def liq_caps():
    caps = {}
    for k in NAMES:
        adv_php = ADV_LOCAL[k] * FX_TO_PHP[INFO[k]['ccy']]
        caps[k] = adv_php * LIQ_SHARE * LIQ_DAYS / AUM
    return caps

def solve(cov, names, caps):
    n = len(names)
    ub = [min(ISSUER, caps[k]) for k in names]
    def obj(w):
        pv = w @ cov @ w; rc = w * (cov @ w) / pv
        return np.sum((rc - rc.mean())**2) * 1e4
    cons = [{'type': 'eq', 'fun': lambda w: w.sum() - (1 - RESERVE)}]
    def grp(mask, lim, kind):
        m = np.array(mask, float)
        return {'type': 'ineq', 'fun': (lambda w, m=m: m @ w - lim) if kind == 'min' else (lambda w, m=m: lim - m @ w)}
    for role, (kind, lim) in ROLE_LIMITS.items():
        cons.append(grp([INFO[k]['role'] == role for k in names], lim, kind))
    for c in set(INFO[k]['country'] for k in names):
        cons.append(grp([INFO[k]['country'] == c for k in names], COUNTRY_CAP, 'max'))
    for g in set(GROUP.get(k) for k in names if GROUP.get(k)):
        cons.append(grp([GROUP.get(k) == g for k in names], GROUP_CAP, 'max'))
    def feasible(w):
        return (all(c['fun'](w) >= -1e-6 for c in cons if c['type'] == 'ineq')
                and abs(cons[0]['fun'](w)) < 1e-6 and all(-1e-9 <= w[i] <= ub[i] + 1e-6 for i in range(n)))
    best, bestf = None, np.inf
    for seed in range(8):                      # several starts; keep the best solution that meets every rule
        rng = np.random.default_rng(seed)
        x0 = np.array(ub) * rng.uniform(0.3, 1.0, n); x0 *= (1 - RESERVE) / x0.sum(); x0 = np.minimum(x0, ub)
        res = minimize(obj, x0, bounds=[(0, u) for u in ub], constraints=cons, method='SLSQP',
                       options={'maxiter': 2000, 'ftol': 1e-15})
        if feasible(res.x) and res.fun < bestf: best, bestf = res.x, res.fun
    if best is None: raise RuntimeError('no feasible solution')
    return pd.Series(np.clip(best, 0, None), index=names)

def eligible(R, t):
    hist = R.loc[:t - pd.Timedelta(days=1)]
    return [k for k in NAMES if hist[k].dropna().shape[0] >= MIN_HIST]

def weights_at(R, t, caps):
    names = eligible(R, t)
    hist = R.loc[:t - pd.Timedelta(days=1), names].iloc[-LOOKBACK:]
    cov = hist.cov().values * 52
    return solve(cov, names, caps), cov, names

def simulate(R):
    caps = liq_caps()
    idx = R.loc[START:END].index[1:]          # first return week ends 8 Oct 2021
    out, log, w = [], {}, None
    last_q = None
    for t in idx:
        q = (t.year, (t.month - 1)//3)
        if w is None or (q != last_q):
            w, _, _ = weights_at(R, t, caps)
            w = w.copy(); w['CASH'] = RESERVE
            log[t] = w.copy(); last_q = q
        r = R.loc[t, w.index].fillna(0)
        g = float((w * r).sum() / w.sum())
        out.append((t, g))
        w = w * (1 + r)
    gross = pd.Series(dict(out))
    net = (1 + gross) * (1 - FEE)**(1/52) - 1
    return net, pd.DataFrame(log).T.fillna(0), caps

if __name__ == '__main__':
    R = load_returns()
    net, wl, caps = simulate(R)
    pd.to_pickle(dict(R=R, net=net, wlog=wl, caps=caps), 'sim.pkl')
    print('weeks', len(net), net.index[0].date(), net.index[-1].date())
    print('cum', (1+net).prod(), 'ACWI', (1+R.loc[net.index,'ACWI']).prod())
    print('rebalances', len(wl))
