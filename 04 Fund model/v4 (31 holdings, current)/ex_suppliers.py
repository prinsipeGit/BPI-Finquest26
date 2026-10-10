"""Rerun the v4 simulation without the chip and grid-equipment holdings (same rules, costs and limits) -> ex_suppliers.json. Run from this folder."""
import pandas as pd, numpy as np, json
src = open('engine4.py').read().split("if __name__ == '__main__':")[0].replace("'../v3/inputs.py'", "'../v3 (21 holdings, superseded)/inputs.py'")
ns = {}; exec(src, ns)
S = pd.read_pickle('sim4.pkl'); R = S['R']; held = S['held']; UNI = ns['UNI']
def stats(s):
    g = (1+s).prod(); c = g**(52/len(s))-1; v = s.std()*np.sqrt(52); p=(1+s).cumprod(); dd=(p/p.cummax()-1).min()
    return dict(cagr=c, growth=100*g, vol=v, maxdd=dd)
dy = ns['wht_drag'](held)
net, wl, c = ns['simulate'](R, held, 'erc', ns['V4LIM'], ns['V4CASH'], dy)
print('repro full', stats(net), 'stored', stats(S['net4']))
sup = [k for k in held if UNI[k]['ctype'] in ('Semiconductors', 'Grid & power equipment')]
print('excluded', [(k, UNI[k]['ctype']) for k in sup])
rest = [k for k in held if k not in sup]
net2, wl2, c2 = ns['simulate'](R, rest, 'erc', ns['V4LIM'], ns['V4CASH'], {k: dy[k] for k in rest})
s2 = stats(net2); print('without suppliers', len(rest), s2)
# attribution: share of gross growth from supplier weights (weekly contribution sum)
json.dump(dict(n=len(rest), excluded=sup, **{k: float(v) for k, v in s2.items()}), open('ex_suppliers.json', 'w'), indent=1)
