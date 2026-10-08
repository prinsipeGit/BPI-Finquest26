"""Sensitivity of the P step to its two pre-set thresholds (diversification gain, minimum weight). Report only; rules unchanged."""
import json, numpy as np, pandas as pd
import engine4 as E
R = pd.read_pickle('sim4.pkl')['R']
src = open('engine4.py').read()
res = []
for dr_gain, minw in [(0.0, 0.01), (0.0025, 0.01), (0.005, 0.01), (0.01, 0.01), (0.005, 0.005), (0.005, 0.02)]:
    def select(R, dr_gain=dr_gain, minw=minw):
        el = sorted([r for r in E.UNI.values() if r['stage'] == 'Eligible'], key=lambda r: (-r['merit'], -r['spread']))
        held = []
        def solve(names):
            h = E.window(R, E.DECISION, names); cov = h.cov().values * 52
            try: return E.erc(cov, names, E.V4LIM, 0.97), cov
            except RuntimeError: return E.erc_free(cov, names, 0.97), cov
        for r in el:
            k = r['key']
            h = E.window(R, E.DECISION, held + [k]).dropna()
            same = [j for j in held if E.UNI[j]['type'] == r['type']]
            if same and h.corr()[k].drop(k)[same].max() > 0.80: continue
            dr_old = E.div_ratio(*(lambda a: (a[0].values, a[1]))(solve(held))) if len(held) >= 2 else 1.0
            w, cov = solve(held + [k])
            if w[k] < minw: continue
            if len(held) >= 2 and E.div_ratio(w.values, cov) < dr_old * (1 + dr_gain): continue
            held.append(k)
            while True:
                w, cov = solve(held); low = [j for j in held if w[j] < minw]
                if not low: break
                held.remove(min(low, key=lambda x: E.UNI[x]['merit']))
        return held
    held = select(R)
    net, _, _ = E.simulate(R, held, 'erc', E.V4LIM, 0.03, E.wht_drag(held))
    g = (1 + net).prod(); w = (1 + net).cumprod(); dd = (w / w.cummax() - 1).min()
    res.append(dict(dr_gain=dr_gain, min_weight=minw, n=len(held), cagr=g**(52/len(net)) - 1, vol=net.std()*np.sqrt(52), maxdd=dd))
    print(res[-1], flush=True)
json.dump(res, open('sens4.json', 'w'), indent=1)
