"""Extra v4 figures for the 6-page fact sheet (10 Oct 2026): sequence-risk shuffle on the fund's own monthly returns,
risk shares, Sortino, 1y/3y, risk in pesos -> extra4.json. Run from this folder after engine4.py / analyze4.py."""
import json, numpy as np, pandas as pd
R = json.load(open('results4.json')); S = pd.read_pickle('sim4.pkl'); net = S['net4']
st = R['five']['v4']['stats']
# monthly returns from weekly net series (month-end compounding)
m = (1 + net).groupby(net.index.to_period('M')).prod() - 1
m = m.iloc[-60:] if len(m) >= 60 else m
rng = np.random.default_rng(2026); N = 20000; n = len(m); r = m.values
def wealth_contrib(seq, pay=1000):   # pay at start of each month
    w = 0.0
    for x in seq: w = (w + pay) * (1 + x)
    return w
def wealth_withdraw(seq, start, take=900):
    w = start
    for x in seq: w = w * (1 + x) - take
    return w
start = 900 * n * 0.8
fh, wc, ww = [], [], []
for _ in range(N):
    s = rng.permutation(r); fh.append(np.prod(1 + s[:n//2]) - 1); wc.append(wealth_contrib(s)); ww.append(wealth_withdraw(s, start))
fh, wc, ww = map(np.array, (fh, wc, ww))
mm = (1 + 0.045)**(1/12) - 1          # money-market comparison, 4.5% a year
mmw = wealth_contrib(np.full(n, mm))
# downside / Sortino on weekly
dn = net[net < 0]; dd_vol = np.sqrt((np.minimum(net, 0)**2).mean() * 52)
sortino = (st['cagr'] - st['rf']) / dd_vol
g = (1 + net).cumprod(); y1 = g.iloc[-1] / g.iloc[-53] - 1; y3 = (g.iloc[-1] / g.iloc[-157])**(1/3) - 1
rs = [x['risk_share'] for x in R['portfolio']]
out = dict(months=n, n_shuffles=N, corr_contrib=float(np.corrcoef(fh, wc)[0, 1]), corr_withdraw=float(np.corrcoef(fh, ww)[0, 1]),
           contrib_min=float(wc.min()), contrib_median=float(np.median(wc)), paid_in=1000 * n, mm_wealth=float(mmw),
           beat_mm=float((wc > mmw).mean()), downside_dev=float(dd_vol), sortino=float(sortino), ret_1y=float(y1), ret_3y=float(y3),
           risk_share_min=min(rs), risk_share_max=max(rs), risk_share_sum=sum(rs),
           dd_on_5000=float(-st['maxdd'] * 5000), worst12=st['worst12'], best12=st['best12'], pos12=st['pos12'])
json.dump(out, open('extra4.json', 'w'), indent=1); print(json.dumps(out, indent=1))
print('eff bets', R['eff_bets'], 'div ratio', R['div_ratio'], 'top2', R['top2_factor'], 'violations', R['violations'], 'rebal', R['rebalances'])
print('by_role', R['by_role'], 'ph_range', R['ph_range'])
