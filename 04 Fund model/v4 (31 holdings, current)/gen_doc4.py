"""Markdown sections for the supporting-proposal doc, from results4.json + notes4.py. Writes doc_s1.md ... doc_s6.md, doc_decisions.md."""
import json
from notes4 import N, STORY
R = json.load(open('results4.json')); F5 = R['five']; PX = R['proxy']; PF = R['portfolio']; fun = R['funnel']
ps = PX['stats']; n = R['n_held']; bt = R['by_type']; cnt = R['by_country']; cost = R['costs']['v4']
v4, ew, iv, v3, aw, ix = (F5[k]['stats'] for k in ['v4', 'v4_ew', 'v4_iv', 'v3', 'acwi', 'ixn'])
pc = lambda x, d=1: f"{x*100:.{d}f}%".replace('-', '−')
sg = lambda x, d=1: (f"{x:+.{d}f}").replace('-', '−')
sens = json.load(open('sens4.json')) if __import__('os').path.exists('sens4.json') else []
out = {}
out['s1'] = f"""## Summary

The revised rules hold **{n} companies** in eight kinds of capacity, chosen and weighted by a process fixed on 8 October 2026 before any results were run. The holdings count, country mix and every weight are outputs; nothing was set by hand.

- **What changed:** healthcare facilities added to the theme; no dated-target requirement; debt tested under a stress set per capacity type; valuation judged against same-type peers with a cash-flow measure; eligible, watchlist or reject for every company; holdings count from inclusion tests; BSP's 20% single-issuer ceiling instead of our 10% cap; operating cash instead of a fixed 10% reserve; no owner/supplier or country quotas.
- **Funnel:** {fun['universe']} companies → {fun['m_pass']} pass Map → {fun['eligible']} eligible after Verify ({fun['v_reject']} rejected, {fun['watch_v']} watchlisted) → {n} held ({fun['eligible'] - n} watchlisted at Position).
- **Philippines:** {pc(R['ph_now'])} (ICTSI). Manila Water moved to the watchlist on cash conversion.
- **Evidence, labelled:** the five-year figures are the *historical performance of the currently selected portfolio* ({pc(v4['cagr'])} a year after all modelled costs, against {pc(aw['cagr'])} for the MSCI ACWI ETF). They include selection hindsight and are not a backtest of the process. The 36-year industry proxy ({pc(ps['cap']['cagr'])} a year against {pc(ps['mkt']['cagr'])} for a same-cost market fund) is context for the theme only.
- **Benchmark:** to be selected by the team; the ETFs here are references, not the benchmark."""

out['s2'] = f"""## The rules as applied

Full text and thresholds: `RULES_v4.md` in the fund model folder. Each threshold below was set per capacity type before testing; no exception was made for any stock.

| Step | Test | Outcome if failed |
| --- | --- | --- |
| M1 Material exposure | GICS sub-industry on the qualifying list, or at least 50% of revenue from a qualifying segment | Reject |
| M2 Earns from the capacity | Operating cash flow and ROIC both above zero | Reject |
| V1 Debt under stress | Interest cover after an EBITDA shock (water 10%, power 15%, networks 15%, hospitals 25%, ports 30%, grid equipment 35%, chips 50%, airports & roads 60%) at least 1.5× | Reject |
| V2 Leverage outlier | Net debt/EBITDA no more than 2.0 turns above the type median | Reject |
| V3 Investability | Position of 1% of a ₱1bn fund sellable in 5 days at 20% of volume; price history available | Reject |
| V4 Governance | No material concern on public record (Adani group: US DOJ/SEC charges, Nov 2024) | Reject |
| V5 Cash conversion | Operating cash flow at least 50% of EBITDA | Watchlist |
| V6 Price | EV/EBITDA no more than 2× the type median | Watchlist |
| V7 Merit | Merit at least 0.50 within its type: half valuation (EV/EBITDA; cash yield = (OCF − D&A)/EV), half quality (ROIC − WACC) | Watchlist |
| P1 Duplicate | Weekly correlation with a same-type holding at most 0.80 | Watchlist |
| P3 Sensible size | Risk-based weight at least 1.0% of NAV | Watchlist |
| P4 Diversification | Adding it raises the diversification ratio by at least 0.5% | Watchlist |

**Weighting:** equal risk contribution on the previous 156 weekly peso returns (104 minimum), re-solved quarterly. While the candidate set is too small for the limits to be feasible, the inclusion test uses unconstrained ERC; the final weights apply every limit. This clarification was written during coding, before any results were seen.

**Limits:** single issuer 20% of NAV (regulatory, BSP Circular No. 1234, a ceiling, not a target); company group 20% (internal); capacity type 25% (internal: one shock can hit a whole type); liquidity as V3 (internal). Operating cash modelled at 3%. All limits held at all {R['rebalances']} quarterly rebalances.

**Testing conventions:** weekly Friday closes, 1 Oct 2021 – 2 Oct 2026, total return in pesos; 1.50% fee; 0.30% trading cost on traded value (about {pc(cost['trading_pa'], 2)} a year); estimated dividend withholding by listing country (about {pc(cost['wht_pa'], 2)} a year, rates to be confirmed by tax counsel); cash at the BSP policy rate minus 0.50 pt. Previous (v3) and revised (v4) rules use identical conventions."""

rows = []
for x in PF:
    nt = N[x['key']]
    ev = f" Evidence: [{nt['ev'][0]}]({nt['ev'][1]})." if nt.get('ev') else ''
    fund = (f"EV/EBITDA {x['ev']:.1f}× (median {x['peer_med_ev']:.1f}×); cash yield {x['cash_yield']*100:.1f}% (median {x['peer_med_cy']*100:.1f}%); "
            f"ROIC − WACC {sg(x['spread'])} pts (median {sg(x['peer_med_spread'])}); merit #{x['merit_rank']} of {x['peers']}; "
            + ("net cash" if x['nd'] is not None and x['nd'] < 0 else f"net debt {x['nd']:.1f}× EBITDA, stressed cover {x['cov_stress']:.1f}×"))
    role = f"Vol. {x['vol']*100:.0f}%; avg. correlation {x['avg_corr']:.2f}"
    wr = f"**{pc(x['weight'], 2)}**; {pc(x['risk_share'])} of risk" + (f"; {', '.join(x['binding'])}" if x['binding'] else '')
    nm = x['name'].replace('|', '/')
    rows.append(f"| {nm} ({x['country']}) | {x['ctype']} | {nt['cap']}. Hard to replace: {nt['moat']}. Earns: {nt['earn']}.{ev} *{STORY[x['ctype']]}* | {fund} | {nt['risk']} | {role} | {wr} |")
out['s3'] = f"""## Holdings assessment

Theme fit makes a company eligible, Verify decides whether it is worth owning, and Position sets the weight; the milestone line is the investor story, never the reason to buy. Ratios: stockanalysis.com, 8 Oct 2026; medians are among same-type companies that passed V1–V4; weights solved on data to 2 Oct 2026.

| Holding | Capacity | Theme and milestone | Fundamentals and valuation | Key risks | Portfolio role | Weight and rationale |
| --- | --- | --- | --- | --- | --- | --- |
""" + '\n'.join(rows) + f"""

Weights are equal-risk-contribution outputs: each holding contributes an equal share of risk (about {sum(x['risk_share'] for x in PF if not x['binding'])/len([x for x in PF if not x['binding']])*100:.1f}% each) unless a limit binds (digital networks at the 25% type limit, so each telecom carries less). Overlaps: data-centre build-out (chips and grid equipment) {pc(bt['Semiconductors'] + bt['Grid & power equipment'])}; US health policy (HCA, Encompass) {pc(sum(x['weight'] for x in PF if x['key'] in ('HCA', 'EHC')))}; Chinese state telecoms {pc(sum(x['weight'] for x in PF if x['key'] in ('CHMOB', 'CHTEL')))}. The portfolio behaves like about {R['eff_bets']:.1f} independent exposures. Every company not held, with its reason, is in the Decision record tab."""

alt = R['alt_types']
out['s4'] = f"""## Weighting: does the risk model earn its complexity?

Equal weight returned more over these five years, inverse volatility nearly matched the risk model but would breach the 25% type limit (telecoms 34%), and we keep equal risk contribution because it was chosen before testing and applies the limits inside the solve.

| Same {n} holdings, same costs (alternatives without the 25% type limit) | Risk model (ERC) | Inverse volatility | Equal weight |
| --- | --- | --- | --- |
| Return a year | {pc(v4['cagr'])} | {pc(iv['cagr'])} | {pc(ew['cagr'])} |
| Volatility | {pc(v4['vol'])} | {pc(iv['vol'])} | {pc(ew['vol'])} |
| Worst fall | {pc(v4['maxdd'])} | {pc(iv['maxdd'])} | {pc(ew['maxdd'])} |
| ₱100 became | {v4['growth']:.0f} | {iv['growth']:.0f} | {ew['growth']:.0f} |
| Semiconductors today | {pc(bt['Semiconductors'])} | {pc(alt['iv']['Semiconductors'])} | {pc(alt['ew']['Semiconductors'])} |

Equal weight's extra return came mainly from holding about twice as much in chipmakers through the AI rally; it also had higher volatility and a deeper fall."""

c4, c3, ca, cx = (F5[k]['cal'] for k in ['v4', 'v3', 'acwi', 'ixn'])
calrow = lambda lab, c: f"| {lab} | " + ' | '.join(pc(c[y]) for y in ['2021', '2022', '2023', '2024', '2025', '2026']) + ' |'
cr = PX['crises']; d0, dg = PX['contrib']['dca'], PX['contrib']['dca_glide']
sens_md = ''
if sens:
    sens_md = "\n\n**Sensitivity of the Position thresholds (report only; rules unchanged):**\n\n| Diversification gain | Minimum weight | Holdings | Return a year | Volatility | Worst fall |\n| --- | --- | --- | --- | --- | --- |\n" + '\n'.join(
        f"| {s['dr_gain']*100:.2f}% | {s['min_weight']*100:.1f}% | {s['n']} | {pc(s['cagr'])} | {pc(s['vol'])} | {pc(s['maxdd'])} |" for s in sens) + "\n\nAcross these thresholds the holdings count moves between 24 and 33 and the five-year return between 20.2% and 25.0%. The pre-set rule sits at the top of that range, one more reason to read the five-year figure as hindsight, not a forecast."
out['s5'] = f"""## Performance evidence

The current holdings beat the world index over five years with less volatility, but that history includes selection hindsight. Over 36 years the industry proxy roughly matched a same-cost market fund, with shallower worst falls.

**1 · Historical performance of the currently selected portfolio** (weekly, in pesos, after all modelled costs; not actual fund performance and not a backtest of the selection process):

| | Firsts Fund holdings (v4) | Previous rules (v3), same costs | MSCI ACWI ETF (reference) | Global tech ETF (context) |
| --- | --- | --- | --- | --- |
| Return a year | {pc(v4['cagr'])} | {pc(v3['cagr'])} | {pc(aw['cagr'])} | {pc(ix['cagr'])} |
| Volatility | {pc(v4['vol'])} | {pc(v3['vol'])} | {pc(aw['vol'])} | {pc(ix['vol'])} |
| Sharpe (cash = BSP rate − 0.5 pt) | {v4['sharpe']:.2f} | {v3['sharpe']:.2f} | {aw['sharpe']:.2f} | {ix['sharpe']:.2f} |
| Worst fall | {pc(v4['maxdd'])} | {pc(v3['maxdd'])} | {pc(aw['maxdd'])} | {pc(ix['maxdd'])} |
| Worst 12 months | +{pc(v4['worst12'])} | {pc(v3['worst12'])} | {pc(aw['worst12'])} | {pc(ix['worst12'])} |
| ₱100 became | {v4['growth']:.0f} | {v3['growth']:.0f} | {aw['growth']:.0f} | {ix['growth']:.0f} |
| Beta to ACWI | {v4['beta']:.2f} | {v3['beta']:.2f} | 1.00 | {ix['beta']:.2f} |

| Calendar year | 2021 (from 1 Oct) | 2022 | 2023 | 2024 | 2025 | 2026 (to 2 Oct) |
| --- | --- | --- | --- | --- | --- | --- |
{calrow('Firsts Fund holdings (v4)', c4)}
{calrow('Previous rules (v3)', c3)}
{calrow('MSCI ACWI ETF', ca)}
{calrow('Global tech ETF', cx)}

Revised beat previous rules in this period, but both were selected with October 2026 data, so this does not show the new rules are better; the gain may mostly come from adding hospitals and spreading wider, which we have not attributed.

**2 · Industry proxy, 1990–Aug 2026** (US industries for the eight types, same ERC, 25% type limit, 3% cash, 1.50% fee, 0.30% trading cost; context only):

| | Firsts method | Same-cost market fund | Tech fund |
| --- | --- | --- | --- |
| Return a year | {pc(ps['cap']['cagr'])} | {pc(ps['mkt']['cagr'])} | {pc(ps['tech']['cagr'])} |
| Volatility | {pc(ps['cap']['vol'])} | {pc(ps['mkt']['vol'])} | {pc(ps['tech']['vol'])} |
| Worst fall | {pc(ps['cap']['maxdd'])} | {pc(ps['mkt']['maxdd'])} | {pc(ps['tech']['maxdd'])} |
| Months, peak to recovery | {ps['cap']['months_peak_to_recovery']} | {ps['mkt']['months_peak_to_recovery']} | {ps['tech']['months_peak_to_recovery']} |
| Worst 12 months | {pc(ps['cap']['worst12'])} | {pc(ps['mkt']['worst12'])} | {pc(ps['tech']['worst12'])} |
| USD Sharpe | {ps['cap']['usd_sharpe']:.2f} | {ps['mkt']['usd_sharpe']:.2f} | {ps['tech']['usd_sharpe']:.2f} |
""" + '\n'.join(f"| {k} | {pc(v['cap'])} | {pc(v['mkt'])} | {pc(v['tech'])} |" for k, v in cr.items()) + f"""

Ahead of the market in {int(PX['years_ahead']['mkt'])} of 37 calendar years and of tech in {int(PX['years_ahead']['tech'])}. No downside protection is claimed: the method did worse than the market in COVID and gained less in 1997–98.

**3 · Investor outcomes, reported separately from fund performance** (₱1,000 a month for 60 months, every start month on the proxy, {d0['n']} windows; illustrative glidepath: from 24 months before the goal, the target equity share falls in a straight line to 20%, the rest in T-bills as the lower-risk-fund proxy):

| Ending value ÷ total paid in | Fund only | With glidepath |
| --- | --- | --- |
| Median | {d0['median']:.2f}× | {dg['median']:.2f}× |
| Worst 5% of windows | {d0['p5']:.2f}× | {dg['p5']:.2f}× |
| Worst window | {d0['worst']:.2f}× | {dg['worst']:.2f}× |
| Windows ending below what was paid in | {pc(d0['below1'], 0)} | {pc(dg['below1'], 0)} |

The glidepath raised the worst outcome and gave up some median return; it does not guarantee capital or goal completion.""" + sens_md

out['s6'] = """## Regulatory note and open items

RCBC Trust's official notice reproduces the amended exposure provision under BSP Circular No. 1234 (2026): UITFs invested in exchange-traded equities have a 20% single-issuer ceiling, and exposure above 15% must consist solely of that issuer's exchange-traded equity. The ceiling is regulatory context, not a target weight. [RCBC — Updated Exposure Limits for RCBC Trust UITFs](https://www.rcbc.com/updated-exposure-limits-for-rcbc-trust-uitfs)

- [ ] Team selects the benchmark (methodology, weights, currency treatment) before final performance comparisons
- [ ] Confirm dividend withholding rates by listing country with tax counsel
- [ ] Check team-assigned GICS sub-industries, especially the eight healthcare facilities and Kamigumi
- [ ] Spot-check debt, cash flow and ROIC for the 31 holdings against annual reports; memory makers are at a cyclical peak
- [ ] Confirm the stress shocks per capacity type with a source for each episode
- [ ] Decide whether the illustrative glidepath schedule appears in app mock-ups (label it illustrative)
- [ ] Calculator: contributions-only baseline plus balanced scenarios, not the five-year history"""

for k, v in out.items(): open(f'doc_{k}.md', 'w').write(v)
# decision record (second tab)
order = {'Eligible': 0}
dec = sorted([d for d in R['decisions'] if d['key'] not in [p['key'] for p in PF]], key=lambda d: (d['ctype'], d['stage'], -(d['usd_bn'] or 0)))
lines = ["| Company | Capacity | Decision | Reason |", "| --- | --- | --- | --- |"]
for d in dec:
    if d['stage'] == 'Eligible' and d['p']: st, why = d['p'][0], d['p'][1]
    else: st, why = d['stage'], d['why']
    lines.append(f"| {d['name'].replace('|', '/')} ({d['country']}) | {d['ctype']} | {st} | {why.replace('|', '/')} |")
open('doc_decisions.md', 'w').write('\n'.join(lines))
print({k: len(v) for k, v in out.items()}, len(lines))
