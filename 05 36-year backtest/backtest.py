"""Long-history proxy backtests for The Firsts Fund (FinQuest 2026).

Data: Ken French 49-industry value-weighted monthly returns (CRSP, US-listed),
F-F market and T-bill, F-F Developed ex-US / Emerging market returns, BIS USD/PHP
end-of-month rates. Jan 1989 - Aug 2026. Backtests start Jan 1990 (1989 = warm-up).

Both funds use the same published process as the fact sheet:
  equal risk contribution on TRAILING covariance only (no look-ahead),
  role limits, 10% liquid reserve, quarterly rebalance with drift between,
  1.50% p.a. fee, everything measured in Philippine pesos.
"""
import numpy as np, pandas as pd
from scipy.optimize import minimize

COLS = ['Hlth','MedEq','Cnstr','BldMt','Mach','ElcEq','Util','Telcm','Trans',
        'Hardw','Softw','Chips','LabEq','BusSv','Banks','MktRF','RF','DevExUS','APxJ','EM']

def load():
    rows = (open('enc_part1.txt').read().strip()+' '+open('enc_part2.txt').read().strip()).split()
    idx = pd.period_range('1989-01', periods=len(rows), freq='M')
    data = [[np.nan if x == 'x' else int(x)/10000 for x in r.split(',')] for r in rows]
    df = pd.DataFrame(data, index=idx, columns=COLS)
    df['Mkt'] = df.MktRF + df.RF
    for c in ['DevExUS', 'APxJ', 'EM']:          # these files give excess returns
        df[c] = df[c] + df.RF
    fx = np.array([float(x) for x in open('usdphp_eop.txt').read().split()[1:]])
    df['USDPHP'] = fx
    df['fxret'] = df.USDPHP.pct_change()
    return df

def to_php(r_usd, fxret):
    return (1 + r_usd) * (1 + fxret) - 1

# ---- fund definitions -------------------------------------------------------
# role: O = Owner (paid for use of capacity), S = Supplier (paid during build), P = Platform
CAPACITY = {'Util': 'O', 'Telcm': 'O', 'Hlth': 'O', 'Trans': 'O',
            'ElcEq': 'S', 'Mach': 'S', 'Cnstr': 'S', 'BldMt': 'S', 'Chips': 'S',
            'Banks': 'P', 'BusSv': 'P'}
CAP_LIMITS = {'O': ('min', 0.45), 'S': ('max', 0.25), 'P': ('max', 0.20)}
TECH = {'Hardw': 'T', 'Softw': 'T', 'Chips': 'T', 'LabEq': 'T'}
TECH_LIMITS = {}

RESERVE, FEE, SLEEVE_CAP = 0.10, 0.015, 0.25

def erc_weights(cov, roles, limits, invested=1-RESERVE, cap=SLEEVE_CAP):
    n = len(roles); names = list(roles)
    def obj(w):
        w = np.asarray(w); pv = w @ cov @ w
        rc = w * (cov @ w) / pv
        return np.sum((rc - 1/n)**2) * 1e4
    cons = [{'type': 'eq', 'fun': lambda w: w.sum() - invested}]
    for role, (kind, lim) in limits.items():
        m = np.array([roles[k] == role for k in names], float)
        if kind == 'min': cons.append({'type': 'ineq', 'fun': lambda w, m=m, lim=lim: m @ w - lim})
        else:             cons.append({'type': 'ineq', 'fun': lambda w, m=m, lim=lim: lim - m @ w})
    x0 = np.full(n, invested/n)
    res = minimize(obj, x0, bounds=[(0.01, cap)]*n, constraints=cons, method='SLSQP',
                   options={'maxiter': 500, 'ftol': 1e-12})
    return pd.Series(res.x, index=names)

def run(df, roles, limits, start='1990-01', lookback=36, min_obs=12):
    names = list(roles)
    php = df[names].apply(lambda s: to_php(s, df.fxret))
    cash = to_php(df.RF, df.fxret)            # reserve held as USD T-bills, valued in pesos
    out, wlog = [], {}
    w = None
    for t in pd.period_range(start, df.index[-1], freq='M'):
        if w is None or t.month in (1, 4, 7, 10):                 # quarterly rebalance
            hist = php.loc[:t-1].iloc[-lookback:]
            if len(hist) < min_obs: raise ValueError('not enough history')
            w = erc_weights(hist.cov().values*12, roles, limits)
            w['cash'] = RESERVE
            wlog[t] = w.copy()
        r_assets = pd.concat([php.loc[t, names], pd.Series({'cash': cash.loc[t]})])
        gross = float((w * r_assets).sum()) / float(w.sum())
        out.append((t, gross))
        w = w * (1 + r_assets)                                    # drift until next rebalance
    g = pd.Series(dict(out))
    net = (1 + g) * (1 - FEE)**(1/12) - 1
    return net, pd.DataFrame(wlog).T

def stats(r, rf_php=None):
    r = r.dropna(); n = len(r)
    wealth = (1 + r).cumprod()
    cagr = wealth.iloc[-1]**(12/n) - 1
    vol = r.std() * np.sqrt(12)
    dd = wealth / wealth.cummax() - 1
    r12 = (1 + r).rolling(12).apply(np.prod, raw=True) - 1
    r60 = ((1 + r).rolling(60).apply(np.prod, raw=True))**(1/5) - 1
    down = r[r < 0].std() * np.sqrt(12)
    return {'start': str(r.index[0]), 'end': str(r.index[-1]), 'months': n,
            'CAGR': cagr, 'Vol': vol, 'CAGR/Vol': cagr/vol, 'DownDev': down,
            'MaxDD': dd.min(), 'MaxDD_trough': str(dd.idxmin()),
            'Worst12m': r12.min(), 'Best12m': r12.max(), 'Pos12m': (r12.dropna() > 0).mean(),
            'Worst5y_pa': r60.min(), 'Pos5y': (r60.dropna() > 0).mean(),
            'Growth_of_100': 100*wealth.iloc[-1]}

def usd_sharpe(r_php, df):
    """Sharpe in USD terms, against the US T-bill, to keep the risk-free rate clean."""
    r_usd = (1 + r_php) / (1 + df.fxret.loc[r_php.index]) - 1
    ex = r_usd - df.RF.loc[r_php.index]
    return ex.mean() / ex.std() * np.sqrt(12)

def beta(r, m):
    c = np.cov(r, m); return c[0, 1] / c[1, 1], np.corrcoef(r, m)[0, 1]

def dca(r, monthly=1000, years=5):
    """Rolling windows: someone paying in monthly for `years`. Final value / total paid."""
    n = 12*years; res = []
    vals = r.values
    for i in range(len(vals) - n + 1):
        v = 0.0
        for k in range(n): v = (v + monthly) * (1 + vals[i+k])
        res.append(v / (monthly*n))
    return pd.Series(res, index=r.index[n-1:])

if __name__ == '__main__':
    df = load()
    cap, wcap = run(df, CAPACITY, CAP_LIMITS)
    tech, wtech = run(df, TECH, TECH_LIMITS)
    idx = cap.index
    us = to_php(df.Mkt, df.fxret).loc[idx]
    world = to_php(0.55*df.Mkt + 0.35*df.DevExUS + 0.10*df.EM, df.fxret).loc['1990-07':]
    series = {'Capacity fund': cap, 'Tech fund': tech, 'US market (PHP)': us}
    pd.to_pickle(dict(df=df, cap=cap, tech=tech, wcap=wcap, wtech=wtech, us=us, world=world), 'results.pkl')
    for k, s in series.items():
        st = stats(s); st['USD Sharpe'] = usd_sharpe(s, df)
        b, c = beta(s.values, us.values); st['beta_vs_US'] = b; st['corr_vs_US'] = c
        print(k, {a: (round(v, 4) if isinstance(v, float) else v) for a, v in st.items()})
    print('world blend (from 1990-07):', {a: (round(v, 4) if isinstance(v, float) else v) for a, v in stats(world).items()})
