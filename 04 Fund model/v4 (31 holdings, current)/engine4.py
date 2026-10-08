"""Firsts Fund v4: P step (inclusion + weights) and like-for-like simulations, per RULES_v4.md (fixed 8 Oct 2026).

Outputs sim4.pkl with: R (weekly peso returns), selection log, final weights, simulated net series for
  v4 ERC (the proposal), v4 equal weight, v4 inverse volatility, v3 (previous rules) under the same cost conventions.
"""
import json, numpy as np, pandas as pd
from scipy.optimize import minimize
import importlib.util as U

def load(name, path):
    s = U.spec_from_file_location(name, path); m = U.module_from_spec(s); s.loader.exec_module(m); return m
V3 = load('V3', '../v3/inputs.py')
UNI = {r['key']: r for r in json.load(open('map/universe4.json'))}

F = pd.date_range('2018-06-01', '2026-10-02', freq='7D')
START, END = '2021-10-01', '2026-10-02'
LOOKBACK, MIN_HIST = 156, 104
FEE, TC, AUM = 0.015, 0.003, 1e9
DECISION = pd.Timestamp('2026-10-03')          # solve on data through Fri 2 Oct 2026

# approximate dividend withholding for a Philippine fund, by listing country (treaty rate where known); to be confirmed by tax counsel
WHT = dict(US=.25, JP=.15, FR=.15, DE=.15, ES=.15, IT=.15, KR=.20, TW=.21, MY=0, SA=.05, MX=.10, BR=.10, TH=.10, IN=.20, GB=0,
           NL=.15, CH=.15, AU=.15, HK=.10, SG=0, ID=.20, CA=.15, ZA=.20, PH=.10, AE=0, DK=.15)
GROUP = {'ICT': 'Razon group', 'MWC': 'Razon group', 'ENEL': 'Enel group', 'ELE': 'Enel group'}

# ---------------- returns ----------------
def load_returns():
    R = pd.DataFrame(index=F[1:])
    for p in ['../yret.json', '../v2/yret.json', '../v3/yret.json', 'map/yret_new.json', 'map/psei.json']:
        for k, v in json.load(open(p)).items():
            R[k] = np.array([np.nan if x is None else x for x in v], float) / 1e5
    divs = {**load('V1', '../inputs.py').PH_DIVS, **V3.PH_DIVS}
    for path in ['../ph.txt', '../v3/ph.txt']:
        for line in open(path).read().strip().split('\n'):
            k, v = line.split(':')
            if k in R: continue
            p = pd.Series([np.nan if x == 'x' else float(x) for x in v.split(',')], index=F)
            div = pd.Series(0.0, index=F)
            for d, amt in divs.get(k, []):
                later = F[F >= pd.Timestamp(d)]
                if len(later): div[later[0]] += amt
            R[k] = ((p + div) / p.shift(1) - 1).iloc[1:].values
    ixn = [int(x) / 1e5 for x in open('../../compare/ixn.txt').read().strip().split(':')[1].split(',')]
    R['IXN'] = ixn
    pol = []
    for t in R.index:
        rate = V3.PH_POLICY.get(t.strftime('%y%m'), list(V3.PH_POLICY.values())[-1])
        pol.append(rate / 100)
    R['POLICY'] = [(1 + r)**(1/52) - 1 for r in pol]
    R['CASH'] = [(1 + max(r - 0.005, 0))**(1/52) - 1 for r in pol]       # BSP overnight deposit facility = policy - 0.50 pt
    return R

# ---------------- solver ----------------
def erc(cov, names, lim, budget):
    """Equal risk contribution under limits. lim: dict(issuer, group, type, liq caps, role limits)."""
    n = len(names)
    ub = np.array([min(lim['issuer'], lim['liq'].get(k, 1.0)) for k in names])
    def obj(w):
        pv = w @ cov @ w; rc = w * (cov @ w) / pv
        return np.sum((rc - rc.mean())**2) * 1e4
    cons = [{'type': 'eq', 'fun': lambda w: w.sum() - budget}]
    def grp(mask, cap, kind='max'):
        m = np.array(mask, float)
        return {'type': 'ineq', 'fun': (lambda w, m=m: cap - m @ w) if kind == 'max' else (lambda w, m=m: m @ w - cap)}
    if lim.get('type'):
        for c in set(UNI[k]['ctype'] for k in names): cons.append(grp([UNI[k]['ctype'] == c for k in names], lim['type']))
    if lim.get('group'):
        for g in set(GROUP.get(k) for k in names if GROUP.get(k)): cons.append(grp([GROUP.get(k) == g for k in names], lim['group']))
    for role, (kind, cap) in lim.get('roles', {}).items():
        cons.append(grp([UNI[k]['role'] == role for k in names], cap, kind))
    def ok(w):
        return abs(w.sum() - budget) < 1e-6 and all(c['fun'](w) >= -1e-6 for c in cons[1:]) and np.all(w <= ub + 1e-6) and np.all(w >= -1e-9)
    best, bf = None, np.inf
    iv = 1 / np.sqrt(np.diag(cov))
    for seed in range(8):
        rng = np.random.default_rng(seed)
        x0 = iv * (rng.uniform(0.5, 1.5, n) if seed else 1); x0 = np.minimum(x0 / x0.sum() * budget, ub)
        res = minimize(obj, x0, bounds=[(0, u) for u in ub], constraints=cons, method='SLSQP', options={'maxiter': 3000, 'ftol': 1e-15})
        if ok(res.x) and res.fun < bf: best, bf = res.x, res.fun
    if best is None: raise RuntimeError(f'no feasible solution for {names}')
    return pd.Series(np.clip(best, 0, None), index=names)

def erc_free(cov, names, budget):
    """Unconstrained ERC (used only while the candidate set is too small for the limits to be feasible)."""
    n = len(names); w = 1 / np.sqrt(np.diag(cov))
    for _ in range(500):
        m = cov @ w; w = w * ((w @ m) / n / (w * m))**0.5
    return pd.Series(w / w.sum() * budget, index=names)

def div_ratio(w, cov):
    w = np.asarray(w); return float(w @ np.sqrt(np.diag(cov)) / np.sqrt(w @ cov @ w))

V4LIM = dict(issuer=0.20, group=0.20, type=0.25, liq={k: (UNI[k]['liq_cap'] if UNI[k]['liq_cap'] is not None else 1.0) for k in UNI})
V4CASH = 0.03

def window(R, t, names):
    h = R.loc[:t - pd.Timedelta(days=1), names].iloc[-LOOKBACK:]
    return h

# ---------------- P: inclusion ----------------
def select(R):
    el = sorted([r for r in UNI.values() if r['stage'] == 'Eligible'], key=lambda r: (-r['merit'], -r['spread']))
    held, log = [], []
    budget = 1 - V4CASH
    def solve(names):
        h = window(R, DECISION, names); cov = h.cov().values * 52
        try: return erc(cov, names, V4LIM, budget), cov
        except RuntimeError: return erc_free(cov, names, budget), cov
    for r in el:
        k = r['key']
        if k not in R or R.loc[:DECISION, k].iloc[-LOOKBACK:].notna().sum() < MIN_HIST:
            log.append((k, 'Watchlist (P)', 'not enough price history')); continue
        h = window(R, DECISION, held + [k]).dropna()
        same = [j for j in held if UNI[j]['type'] == r['type']]
        if same:
            c = h.corr()[k].drop(k); cs = c[same]
            if cs.max() > 0.80:
                log.append((k, 'Watchlist (P1 duplicate)', f"weekly correlation {cs.max():.2f} with {UNI[cs.idxmax()]['name']} (> 0.80)")); continue
        if len(held) >= 2:
            w0, c0 = solve(held); dr_old = div_ratio(w0.values, c0)
        else: dr_old = 1.0
        w, cov = solve(held + [k])
        if w[k] < 0.01:
            log.append((k, 'Watchlist (P3 negligible)', f"risk-based weight {w[k]*100:.2f}% < 1.0%")); continue
        dr_new = div_ratio(w.values, cov)
        if len(held) >= 2 and dr_new < dr_old * 1.005:
            log.append((k, 'Watchlist (P4 diversification)', f"diversification ratio {dr_old:.3f} -> {dr_new:.3f} (< +0.5%)")); continue
        held.append(k); log.append((k, 'Held', f"weight {w[k]*100:.2f}%, diversification ratio {dr_old:.3f} -> {dr_new:.3f}"))
        while True:                                   # earlier holdings pushed below 1%: drop the lowest-merit one, re-solve
            w, cov = solve(held)
            low = [j for j in held if w[j] < 0.01]
            if not low: break
            j = min(low, key=lambda x: UNI[x]['merit']); held.remove(j)
            log.append((j, 'Watchlist (P3 negligible)', f"pushed to {w[j]*100:.2f}% after later additions"))
    w, cov = solve(held)
    return held, log, w, cov

# ---------------- simulation ----------------
def simulate(R, names, scheme, lim=None, cash=V4CASH, dy=None):
    idx = R.loc[START:END].index[1:]
    out, wlog, w, last_q, cost_total, wht_total = [], {}, None, None, 0.0, 0.0
    for t in idx:
        q = (t.year, (t.month - 1) // 3)
        if w is None or q != last_q:
            avail = [k for k in names if R.loc[:t - pd.Timedelta(days=1), k].dropna().shape[0] >= MIN_HIST]
            h = window(R, t, avail); cov = h.cov().values * 52
            if scheme == 'erc': tw = erc(cov, avail, lim, 1 - cash)
            elif scheme == 'ew': tw = pd.Series((1 - cash) / len(avail), index=avail)
            elif scheme == 'iv':
                iv = 1 / np.sqrt(np.diag(cov)); tw = pd.Series(iv / iv.sum() * (1 - cash), index=avail)
            tw['CASH'] = cash
            cur = (w / w.sum()) if w is not None else pd.Series(0.0, index=tw.index)
            turnover = (tw.reindex(cur.index.union(tw.index), fill_value=0) - cur.reindex(cur.index.union(tw.index), fill_value=0)).abs()
            trade = turnover.drop('CASH', errors='ignore').sum()
            cost = TC * trade; cost_total += cost
            w = tw.copy(); wlog[t] = tw.copy(); last_q = q
            pend_cost = cost
        else:
            pend_cost = 0.0
        r = R.loc[t, w.index].fillna(0)
        g = float((w * r).sum() / w.sum())
        wht = float(sum(w.get(k, 0) / w.sum() * dy[k] for k in w.index if k != 'CASH')) / 52 if dy else 0.0
        wht_total += wht
        out.append((t, (1 + g) * (1 - pend_cost) * (1 - wht) - 1))
        w = w * (1 + r)
    gross = pd.Series(dict(out))
    net = (1 + gross) * (1 - FEE)**(1/52) - 1
    return net, pd.DataFrame(wlog).T.fillna(0), dict(trading_cost_total=cost_total, wht_total=wht_total)

def wht_drag(names):
    return {k: UNI[k]['dy'] * WHT[UNI[k]['country']] for k in names}

if __name__ == '__main__':
    R = load_returns()
    held, log, w_now, cov_now = select(R)
    print(len(held), 'held'); [print(' ', *x) for x in log]
    dy = wht_drag(held)
    net4, wl4, c4 = simulate(R, held, 'erc', V4LIM, V4CASH, dy)
    net_ew, wl_ew, c_ew = simulate(R, held, 'ew', None, V4CASH, dy)
    net_iv, wl_iv, c_iv = simulate(R, held, 'iv', None, V4CASH, dy)
    v3names = [c[0] for c in V3.CANDIDATES if c[12] == 'PASS']
    V3LIM = dict(issuer=0.10, group=0.15, type=0.25, roles={'Owner': ('min', 0.45), 'Supplier': ('max', 0.25)},
                 liq={k: V3.MERIT[k]['liq_cap'] for k in v3names})
    net3, wl3, c3 = simulate(R, v3names, 'erc', V3LIM, 0.10, wht_drag(v3names))
    pd.to_pickle(dict(R=R, held=held, log=log, w_now=w_now, cov_now=cov_now, net4=net4, wl4=wl4, c4=c4, net_ew=net_ew, net_iv=net_iv,
                      c_ew=c_ew, c_iv=c_iv, net3=net3, wl3=wl3, c3=c3, v3names=v3names), 'sim4.pkl')
    for nm, s in [('v4 ERC', net4), ('v4 EW', net_ew), ('v4 IV', net_iv), ('v3 same costs', net3), ('ACWI', R.loc[net4.index, 'ACWI']), ('IXN', R.loc[net4.index, 'IXN'])]:
        g = (1 + s).prod(); print(f'{nm:15s} growth {g:.3f} cagr {g**(52/len(s))-1:.4f} vol {s.std()*np.sqrt(52):.4f}')
    print(c4, c3)
