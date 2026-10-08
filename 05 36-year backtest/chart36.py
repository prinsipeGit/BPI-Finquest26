"""36-year industry-level history (v4 rules), growth of ₱100 and falls from peak. Reads results_v4.pkl. Context only."""
import sys, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, FixedLocator
L = pd.read_pickle(sys.argv[1] if len(sys.argv) > 1 else 'results_v4.pkl')
S = [('cap4', 'Firsts Fund strategy', '#0F7A45', 2.4), ('mkt4', 'US stock market', '#B07A2E', 1.6), ('tech4', 'Tech industries', '#2E5AAC', 1.6)]
idx = L['cap4'].index.to_timestamp(how='end')
INK, MUT, GRID = '#1E2622', '#58635C', '#E3E8E5'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 13, 'text.color': INK, 'axes.labelcolor': MUT, 'xtick.color': MUT, 'ytick.color': MUT})
fig, (a1, a2) = plt.subplots(2, 1, figsize=(16, 9), dpi=150, sharex=True, gridspec_kw=dict(height_ratios=[2.3, 1], hspace=0.08))
stats = {}
for k, name, c, lw in S:
    r = L[k]; w = 100 * (1 + r).cumprod(); w.index = idx
    yrs = len(r) / 12; cagr = (w.iloc[-1] / 100) ** (1 / yrs) - 1; dd = w / w.cummax() - 1
    stats[k] = (w.iloc[-1], cagr, dd.min())
    a1.plot(w.index, w.values, color=c, lw=lw, zorder=3 if k == 'cap4' else 2, solid_capstyle='round')
    a2.plot(dd.index, 100 * dd.values, color=c, lw=lw * 0.8, zorder=3 if k == 'cap4' else 2)
# direct labels at the right end (placed to avoid collisions)
OFF = {'cap4': -0.17, 'mkt4': 0.17, 'tech4': 0.07}
ypos = {k: 10 ** (np.log10(stats[k][0]) + OFF[k]) for k in OFF}
for k, name, c, _ in S:
    v, cagr, mdd = stats[k]
    a1.annotate(f'{name}\n₱{v:,.0f} · {cagr*100:.1f}% a year\nworst fall {mdd*100:.0f}%'.replace('-', '−'), xy=(idx[-1], v), xytext=(idx[-1] + pd.Timedelta(days=200), ypos[k]),
                va='center', fontsize=12.5, color=INK, fontweight='bold' if k == 'cap4' else 'normal', annotation_clip=False,
                arrowprops=dict(arrowstyle='-', color=c, lw=1.2))
a1.set_yscale('log'); ticks = [100, 300, 1000, 3000, 10000, 30000]
a1.yaxis.set_major_locator(FixedLocator(ticks)); a1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'₱{x:,.0f}'))
a1.yaxis.set_minor_locator(FixedLocator([])); a1.set_ylim(70, max(s[0] for s in stats.values()) * 1.4)
a1.set_ylabel('Value of ₱100 (log scale)')
a2.set_ylabel('Fall from previous high'); a2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0f}%'.replace('-', '−')))
a2.set_ylim(-80, 12); a2.set_yticks([0, -20, -40, -60, -80])
for a in (a1, a2):
    a.grid(axis='y', color=GRID, lw=0.8); a.set_axisbelow(True)
    for s in ['top', 'right', 'left']: a.spines[s].set_visible(False)
    a.spines['bottom'].set_color('#C9D3CD'); a.tick_params(length=0)
a2.set_xlim(idx[0], idx[-1])
for (x, lab) in [('2002-09', 'Dot-com crash'), ('2009-02', '2008–09 crisis'), ('2020-03', 'COVID')]:
    a2.annotate(lab, xy=(pd.Timestamp(x), 4), xytext=(0, 0), textcoords='offset points', ha='center', va='bottom', fontsize=10.5, color=MUT)

fig.text(0.06, 0.965, '36 years: about the market\'s return, with shallower falls than tech', fontsize=20, fontweight='bold', color=INK)
fig.text(0.06, 0.93, 'Industry-level history, Jan 1990 – Aug 2026, in pesos, after a 1.50% fee and trading costs. Context only: it does not test our company choices.',
         fontsize=12.5, color=MUT)
fig.text(0.06, 0.015, 'Source: Kenneth French Data Library (US industry portfolios), BIS USD/PHP. Strategy = Util, Telcm, Trans, Hlth, ElcEq, Chips; tech = Hardw, Softw, Chips, LabEq;\n'
         'both weighted for equal risk on the past 36 months, quarterly, 3% cash. Market = US total market, 3% cash, same fee.', fontsize=9.5, color=MUT)
fig.subplots_adjust(left=0.08, right=0.80, top=0.89, bottom=0.09)
fig.savefig('backtest36_growth_drawdown.png'); print({k: (round(v[0]), round(v[1]*100, 2), round(v[2]*100, 1)) for k, v in stats.items()})
