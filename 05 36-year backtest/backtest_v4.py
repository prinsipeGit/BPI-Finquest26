"""36-year INDUSTRY PROXY for the v4 rules (context only; it does not test the company screens).
Ken French US industries mapped to the eight v4 capacity types:
  Owners: Util (power, water), Telcm (digital networks), Trans (ports, airports, toll roads), Hlth (healthcare facilities)
  Suppliers: ElcEq (grid & power equipment), Chips (semiconductors)
v4 conventions: ERC on trailing 36 months, quarterly, type cap 25%, no role limits, 3% cash (US T-bill, in pesos),
1.50% fee, 0.30% trading cost on traded value. Market fund and tech fund use the same cash, fee and costs.
Also: rolling 60-month regular-contribution outcomes, with and without an ILLUSTRATIVE account-level glidepath.
Writes results_v4.pkl."""
import numpy as np, pandas as pd
from scipy.optimize import minimize
import backtest as BT

CASH, FEE, TC, CAP = 0.03, 0.015, 0.003, 0.25
df = BT.load()

def erc(cov, n):
    def obj(w):
        pv = w @ cov @ w; rc = w * (cov @ w) / pv
        return np.sum((rc - rc.mean())**2) * 1e4
    cons = [{'type': 'eq', 'fun': lambda w: w.sum() - (1 - CASH)}]
    iv = 1/np.sqrt(np.diag(cov)); x0 = np.minimum(iv/iv.sum()*(1 - CASH), CAP)
    res = minimize(obj, x0, bounds=[(0, CAP)]*n, constraints=cons, method='SLSQP', options={'maxiter': 1000, 'ftol': 1e-14})
    return res.x

def run(names, start='1990-01', lookback=36, cap=CAP):
    php = df[names].apply(lambda s: BT.to_php(s, df.fxret)); cash = BT.to_php(df.RF, df.fxret)
    out, w, wl = [], None, {}
    for t in pd.period_range(start, df.index[-1], freq='M'):
        cost = 0.0
        if w is None or t.month in (1, 4, 7, 10):
            hist = php.loc[:t-1].iloc[-lookback:]
            tw = pd.Series(erc(hist.cov().values*12, len(names)), index=names); tw['cash'] = CASH
            cur = w/w.sum() if w is not None else pd.Series(0.0, index=tw.index)
            cost = TC * (tw - cur).drop('cash').abs().sum(); w = tw; wl[t] = tw
        r = pd.concat([php.loc[t, names], pd.Series({'cash': cash.loc[t]})])
        g = float((w*r).sum()/w.sum()); out.append((t, (1 + g)*(1 - cost) - 1)); w = w*(1 + r)
    g = pd.Series(dict(out)); return (1 + g)*(1 - FEE)**(1/12) - 1, pd.DataFrame(wl).T

cap4, w4 = run(['Util', 'Telcm', 'Trans', 'Hlth', 'ElcEq', 'Chips'])
tech4, _ = run(['Hardw', 'Softw', 'Chips', 'LabEq'], cap=0.97)
idx = cap4.index
us = BT.to_php(df.Mkt, df.fxret).loc[idx]; cash = BT.to_php(df.RF, df.fxret).loc[idx]
mkt4 = (1 + (1 - CASH)*us + CASH*cash)*(1 - FEE)**(1/12) - 1

def contrib(r, months=60, monthly=1000, glide=False):
    """Final value / total paid for every 60-month window. Illustrative glidepath: from 24 months before the goal,
    the equity share falls in a straight line from 100% to 20% (moved to a money-market proxy = T-bill in pesos)."""
    res = []; rv = r.values; cv = cash.loc[r.index].values
    for i in range(len(rv) - months + 1):
        eq = mm = 0.0
        for k in range(months):
            left = months - k
            target = 1.0 if (not glide or left > 24) else 0.2 + 0.8*(left - 1)/24
            eq += monthly; tot = eq + mm; eq, mm = tot*target, tot*(1 - target)     # new money and transfers follow the target
            eq *= 1 + rv[i + k]; mm *= 1 + cv[i + k]
        res.append((eq + mm)/(monthly*months))
    return pd.Series(res, index=r.index[months - 1:])

out = dict(cap4=cap4, w4=w4, tech4=tech4, mkt4=mkt4, us=us, cash=cash,
           dca=contrib(cap4), dca_glide=contrib(cap4, glide=True), dca_mkt=contrib(mkt4), dca_tech=contrib(tech4))
pd.to_pickle(out, 'results_v4.pkl')
for k in ['cap4', 'mkt4', 'tech4']:
    s = BT.stats(out[k]); s['usd_sharpe'] = BT.usd_sharpe(out[k], df); print(k, {a: (round(v, 4) if isinstance(v, float) else v) for a, v in s.items()})
for k in ['dca', 'dca_glide', 'dca_mkt', 'dca_tech']:
    d = out[k]; print(k, 'worst', round(d.min(), 3), 'p5', round(d.quantile(.05), 3), 'median', round(d.median(), 3), 'below 1.0', round((d < 1).mean(), 3))
