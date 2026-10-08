"""Writes annex.md: the Map grid long-list, every Verify result, and the held 33 with targets and sources."""
import json, inputs as I
R = json.load(open('results.json')); W = {q['key']: q for q in R['portfolio']}
TYPES = ['Power generation & grid', 'Water', 'Telecom & digital infrastructure', 'Ports', 'Airports & toll roads',
         'Power & grid equipment', 'Semiconductors']
REG = ['Asia-Pacific', 'Europe', 'Americas']
f = lambda x: '—' if x is None else f'{x:.2f}'
out = ['# Holdings annex — Map v2 (region-balanced), 7 Oct 2026', '',
       'Each cell: candidates ranked by US-dollar market value. The two largest that pass all four Verify tests are held. '
       'Ratios: stockanalysis.com (S&P Global data), 7 Oct 2026. Weights and risk shares: solved on data to 2 Oct 2026.', '']
for t in TYPES:
    out += [f'## {t}', '']
    for r in REG:
        cs = sorted([c for c in I.CANDIDATES if c[13] == t and c[14] == r], key=lambda c: -c[15])
        if not cs: out += [f'**{r}:** no listed candidate of size.', '']; continue
        out += [f'**{r}**', '', '| Company | Mkt | US$ bn | ND/EBITDA | Cover | EV/EBITDA | Result | Weight | Capacity target (source) |',
                '|---|---|---:|---:|---:|---:|---|---:|---|']
        for c in cs:
            held = c[12] == 'PASS'
            res = 'HELD' if held else ('Bench' if c[12].startswith('BENCH') else c[12].replace('FAIL ', 'Fail: '))
            wt = f"{W[c[0]]['weight']*100:.2f}%" if held else ''
            tgt = f'{c[10]} ([source]({c[11]}))' if held else ''
            out.append(f'| {c[1]} | {c[2]} | {c[15]:,.1f} | {f(c[7])} | {f(c[8])} | {f(c[9])} | {res} | {wt} | {tgt} |')
        out.append('')
out += ['Bench = passed Debt, Price and Liquidity but was not among the two largest passers in its cell (Theme not checked).',
        'Auckland Airport was on the long-list but its data could not be retrieved; it is excluded.']
open('annex.md', 'w').write('\n'.join(out) + '\n'); print(len(out))
