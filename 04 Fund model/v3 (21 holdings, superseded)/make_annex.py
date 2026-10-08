"""Writes annex.md for Map v3: every candidate by capacity type with stage, ratios, merit and (for holdings) target and weight."""
import json, inputs as I
R = json.load(open('results.json')); W = {q['key']: q for q in R['portfolio']}
TYPES = ['Power generation & grids', 'Water', 'Digital networks', 'Ports', 'Airports & toll roads', 'Grid & power equipment', 'Semiconductors']
f = lambda x: '' if x is None else f'{x:.2f}'
out = ['# Holdings annex — Map v3 (global, merit-ranked), data to 7 Oct 2026', '',
       'Universe: up to the 20 largest listed companies by US$ value per capacity type. Theme fit: GICS sub-industry on the list, or >=50% '
       'of revenue for conglomerates. Gates: net debt/EBITDA <= 4.0x (6.0x utilities), interest cover >= 2.5x, EV/EBITDA <= 22.2x, '
       'liquidity cap >= 1%. Merit: average of valuation percentile (EV/EBITDA, cheaper = better) and quality percentile (ROIC - WACC) '
       'among gate-passers of the same type; ties go to the higher ROIC - WACC. Top 3 per type held, each with a dated capacity target.', '']
for t in TYPES:
    out += [f'## {t}', '', '| Company | Mkt | US$ bn | ND/EBITDA | Cover | EV/EBITDA | ROIC-WACC | Merit rank | Result | Weight | Capacity target |',
            '|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|']
    cs = [c for c in I.CANDIDATES if c[13] == t]
    cs.sort(key=lambda c: (I.MERIT[c[0]]['rank'] or 99, -c[15]))
    for c in cs:
        m = I.MERIT[c[0]]; held = c[12] == 'PASS'
        res = 'HELD' if held else c[12]
        tgt = f'[{c[10]}]({c[11]})' if held else ''
        out.append(f"| {c[1]} | {c[2]} | {c[15]:,.1f} | {f(c[7])} | {f(c[8])} | {f(c[9])} | {'' if m['spread'] is None else f'{m[chr(115)+chr(112)+chr(114)+chr(101)+chr(97)+chr(100)]:+.2f}'} | "
                   f"{m['rank'] or ''} | {res} | {pct if False else (f'{W[c[0]][chr(119)+chr(101)+chr(105)+chr(103)+chr(104)+chr(116)]*100:.2f}%' if held else '')} | {tgt} |")
    out.append('')
open('annex.md', 'w').write('\n'.join(out) + '\n'); print(len(out))
