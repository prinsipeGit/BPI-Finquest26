"""Builds every slide of the competition pitch deck (v4) from results4.json, so the numbers on the slides are the numbers
the model produced. Writes into the Slides artifact project folder."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from notes4 import N, STORY
R = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results4.json')))
OUT = '/tmp/claude-0/-home-claude/719c76e7-6b1c-5bc2-bc35-4af87b679529/scratchpad/pitch/project'
SL = OUT + '/slides'
F5, PX, PF = R['five'], R['proxy'], R['portfolio']
W = {p['key']: p for p in PF}
pc = lambda x, d=1: f"{x*100:.{d}f}%".replace('-', '−')
pp = lambda x, d=1: (('+' if x >= 0 else '−') + f"{abs(x)*100:.{d}f}%")
num = lambda x: f"{x:,.0f}"

INK, BODY, MUTED, GREEN, BLUE, GRAY, BG, PANEL, LINE, MINT, AMBER, AMBERB, DARK = ('#142019', '#3D4943', '#6B7570', '#0F7A45', '#3557A8',
    '#8C938E', '#F5F4EE', '#FBFBF7', '#DCE0D9', '#E7EFE9', '#FFF4E0', '#C9761F', '#142019')
SANS = "font-family:'IBM Plex Sans', Arial, sans-serif"; SERIF = "font-family:'Source Serif 4', Georgia, serif"; MONO = "font-family:'IBM Plex Mono', 'Courier New', monospace"

def sec(sid, inner, notes, pad='112px 128px 140px', gap=28, bg=BG, color=BODY):
    return (f'<section id="{sid}" data-transition="fade" style="background:{bg};color:{color};{SANS};padding:{pad};display:flex;flex-direction:column;gap:{gap}px">\n'
            f'{inner}\n<aside>{notes}</aside>\n</section>\n')
def head(kick, title, size=56):
    return (f'<div style="display:flex;flex-direction:column;gap:12px">\n<p style="{MONO};font-size:24px;letter-spacing:3px;text-transform:uppercase;color:{GREEN}">{kick}</p>\n'
            f'<h2 style="{SERIF};font-size:{size}px;font-weight:600;line-height:1.1;color:{INK}">{title}</h2>\n</div>')
def foot(text): return f'<p style="position:absolute;left:128px;bottom:52px;width:1664px;font-size:24px;color:{MUTED}">{text}</p>'
def card(inner, bg=PANEL, border=True, pad='20px 28px', extra=''):
    b = f'border:1px solid {LINE};' if border else ''
    return f'<div style="background:{bg};{b}border-radius:12px;padding:{pad};display:flex;flex-direction:column;gap:8px;{extra}">{inner}</div>'
def h3(t, color=INK, size=28): return f'<h3 style="font-size:{size}px;font-weight:600;color:{color}">{t}</h3>'
def p(t, size=24, color=BODY, extra=''): return f'<p style="font-size:{size}px;line-height:1.4;color:{color};{extra}">{t}</p>'
def callout(t): return f'<div style="background:{AMBER};border-left:6px solid {AMBERB};border-radius:12px;padding:16px 28px"><p style="font-size:26px;line-height:1.4;color:{INK}">{t}</p></div>'
def table(rows, widths, head_row=None, size=24, align=None, colors=None):
    align = align or ['left'] + ['right'] * (len(widths) - 1)
    h = ''
    if head_row:
        h = '<tr>' + ''.join(f'<th style="width:{w}%;text-align:{a}{";color:" + colors[i] if colors and colors[i] else ""}">{c}</th>' for i, (c, w, a) in enumerate(zip(head_row, widths, align))) + '</tr>'
    b = ''.join('<tr>' + ''.join(f'<td style="text-align:{a}">{c}</td>' for c, a in zip(r, align)) + '</tr>' for r in rows)
    return f'<table style="font-size:{size}px;line-height:1.3;color:{INK};border:1px solid {LINE};background:{PANEL};font-variant-numeric:tabular-nums">{h}{b}</table>'
S = {}

v4, ew, iv, v3, aw, ix = (F5[k]['stats'] for k in ['v4', 'v4_ew', 'v4_iv', 'v3', 'acwi', 'ixn'])
n = R['n_held']; ph = R['ph_now']; bt = R['by_type']; cnt = R['by_country']; fun = R['funnel']
cost = R['costs']['v4']; ps = PX['stats']; cr = PX['crises']; ct = PX['contrib']

# ---------------- 1 cover ----------------
S['cover'] = sec('cover', f'''<div style="position:absolute;left:0;top:0;width:24px;height:1080px;background:{GREEN}"></div>
<p style="{MONO};font-size:24px;letter-spacing:3px;text-transform:uppercase;color:#5FC48C">BPI Wealth FinQuest 2026 · Final showdown · Team Los Angeles 76ers</p>
<div style="display:flex;flex-direction:column;gap:28px">
<h1 style="{SERIF};font-size:120px;font-weight:600;line-height:1;color:#F5F4EE">Firsts Fund</h1>
<p style="font-size:40px;line-height:1.35;color:#F5F4EE;max-width:1500px">A proposed, actively managed global equity UITF for young Filipinos whose first is five years or more away. It would own the businesses behind everyday life: power, water, networks, ports, airports, hospitals and the equipment they run on.</p>
<p style="{SERIF};font-size:52px;font-style:italic;color:#5FC48C">“Fund your firsts.”</p>
</div>
<div style="display:flex;justify-content:space-between;align-items:end">
<p style="font-size:26px;line-height:1.5;color:#C9D6CE">Prince Angelo C. Rivera · Luis Tengonciang · Karol Josef Fuñe · Eric Fabian Thirdy Mendez<br>Ateneo de Manila University</p>
<p style="{MONO};font-size:24px;color:#C9D6CE;text-align:right">Proposed: ₱100 minimum · 1.50% a year<br>Recommended horizon: 5 years or longer</p>
</div>''', "Open with the person, not the product. Good morning. Firsts Fund is a proposed, actively managed global equity UITF for an early-career Filipino saving for a first that is five or more years away: a first home, a first business, a first trip. It is one fund with one mandate, holding company shares directly. In the next ten minutes we will show you what it owns, how each company got in, why each weight is what it is, and how it compares with a world index and a tech fund, including where it does worse. Everything here is a proposal; nothing is an existing BPI product.",
pad='128px', bg=DARK, color='#C9D6CE').replace('gap:28px">', 'justify-content:space-between">', 1)

# ---------------- 2 saver ----------------
S['saver'] = sec('saver', head('Who it is for', 'An early-career Filipino saving for a first five or more years away') + f'''
<div style="display:grid;grid-template-columns:1.2fr 1fr;gap:28px">
{card(h3('The suitable investor') + p('Regular income from a first job, an affordable monthly contribution, one primary first at least <b>five years</b> away, and the risk tolerance for an equity fund that can fall in a bad year.', 28) + p('Not everyone aged 18 to 25 is suitable: a goal two years away belongs in a lower-risk fund, and the suitability check says so.', 24, MUTED))}
{card(h3('Illustrative monthly budget, first job') + table([['Take-home pay', '₱25,000'], ['Rent, food, transport', '₱19,500'], ['Emergency savings', '₱2,500'], ['Regular subscription to Firsts Fund', '<b>₱1,000</b>'], ['Left over', '₱2,000']], [70, 30]) + p('Illustrative only', 24, MUTED))}
</div>
<div style="display:flex;gap:24px">
{card(p('<b style="font-size:40px;color:' + INK + '">0.52%</b><br>a year over five years from BPI\'s Philippine Equity Index Fund, after fees: one economy', 24), extra='flex:1')}
{card(p('<b style="font-size:40px;color:' + INK + '">4.19 pts</b><br>a year the closest global product trailed its own index: it buys other funds and adds a second fee layer', 24), extra='flex:1')}
{card(p('<b style="font-size:40px;color:' + GREEN + '">The gap</b><br>a peso-priced global fund that holds shares directly, with one fee layer', 24), bg=MINT, border=False, extra='flex:1')}
</div>''' + foot('Comparison funds: BPI Wealth and Pag-IBIG disclosure statements, as cited in our Phase 1 fact sheet · budget figures are illustrative'),
"Start with who this is for, and who it is not for. Our investor has a first job and a regular income, can set aside about a thousand pesos a month after an emergency fund, and has one primary first at least five years away. The fund is not for every young person: someone saving for something two years away should be in a lower-risk fund, and our suitability step says so. Today that investor can buy a local index fund that made half a percent a year over five years, or a global fund of funds that trailed its own index by four points a year because of a second fee layer. We fill that gap with one global fund, priced in pesos, holding companies directly.")

# ---------------- 3 theme ----------------
S['theme'] = sec('theme', head('The theme · essential capacity with a defensible investment case', 'Essential is where we look. It is not the reason we buy.') + f'''
{p('Listed businesses that own, operate or supply capacity everyday life depends on, where replacing it is hard and the business earns from providing it.', 30, INK)}
<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">
{card(h3('Where we look: eight kinds of capacity', GREEN) + p('<b>Own or operate:</b> power generation &amp; grids · water · digital networks (telecom, towers, data centres) · ports · airports &amp; toll roads · <b>healthcare facilities (new)</b>', 26) + p('<b>Supply:</b> grid &amp; power equipment · semiconductors', 26) + p('These define a research universe, not allocations.', 24, MUTED), bg=MINT, border=False)}
{card(h3('What changed from our first draft') + p('<b>No blanket “non-tech” claim.</b> Chipmakers are assessed like everyone else; NVIDIA is held, small.', 24) + p('<b>No dated capacity target required.</b> A target is evidence, not a ticket in.', 24) + p('<b>Essential ≠ attractive.</b> Every company must still pass the investment test at today\'s price.', 24) + p('<b>Conglomerates</b> need half their revenue in the theme: Siemens 29%, Hitachi 30%, Samsung 39%, Vinci 16% are out.', 24))}
</div>''' + foot('Conglomerate shares: latest annual reports · sub-industries follow GICS, assigned by the team · the five firsts explain the theme to investors; they are not industry categories'),
"A judge will ask: isn't every business essential? Yes, and that is why essential is only where we look, not why we buy. Our theme is capacity that is hard to replace and that the company actually earns from. That gives eight kinds, and we added one since the semifinal: hospitals, because a healthcare facility is exactly that kind of capacity. We also dropped two things. We no longer call the fund non-tech; chipmakers go through the same tests as everyone, and NVIDIA is held at a small weight. And we no longer require a dated expansion target: a target is good evidence, but a company should not be rejected for lacking a press release. Conglomerates still need half their revenue inside the theme.")

# ---------------- 4 mvp ----------------
def mcol(letter, name, q, out, decides):
    return card(f'<p style="{SERIF};font-size:96px;font-weight:600;line-height:1;color:{GREEN}">{letter}</p>' + h3(name, INK, 32) + p(q, 26) +
                p(f'<b>Output:</b> {out}', 24) + p(decides, 24, GREEN, 'font-weight:600'), extra='flex:1;padding:28px 32px')
S['mvp'] = sec('mvp', head('How we choose · M.V.P.', 'Three questions, asked in order, each with its own record') + f'''
<div style="display:flex;gap:24px">
{mcol('M', 'Map the milestone', 'What essential capacity does it provide, why is it hard to replace, and how does it earn from it?', 'a thematic eligibility note', 'Pass or reject')}
{mcol('V', 'Verify the investment', 'Is it an investable business at today\'s price, given its cash, debt and risks?', 'a dated decision record', 'Eligible, watchlist or reject')}
{mcol('P', 'Position the risk', 'What does it add to the portfolio, and what weight is justified?', 'weights, overlap report, holdings-count rationale', 'Held at a number, or watchlist')}
</div>
{callout('The milestone is the story, not the reason to buy. Passing M does not guarantee V; passing V does not guarantee a position.')}''',
"M.V.P. is three questions in order, and each leaves a written record. Map the milestone asks what capacity a company provides, why it is hard to replace and how it earns from it; the output is an eligibility note, and the answer is pass or reject. Verify the investment asks whether it is worth owning at today's price, given its cash generation and its debt; every company gets a decision: eligible, watchlist or reject. Position the risk asks what the company adds to the portfolio and how much to hold; it produces the weight as a number. The milestone, a first home or a first trip, is how we explain a holding to an investor after it has passed. It is never why we buy.")

# ---------------- 5 map ----------------
S['map'] = sec('map', head('M · Map the milestone · thematic eligibility', 'One global list. Material exposure, and a business that earns from it.') + f'''
<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:28px">
<div style="display:flex;flex-direction:column;gap:18px">
{card(p(f'<b style="color:{GREEN}">1 · Universe</b> Up to the 20 largest listed companies by US-dollar value in each of the eight kinds of capacity, anywhere in the world: <b>{fun["universe"]}</b>', 26))}
{card(p(f'<b style="color:{GREEN}">2 · Material exposure</b> The main business is on our sub-industry list, or at least half of revenue comes from it. <b>7 out</b> (Siemens, Hitachi, Samsung, Vinci, Ferrovial, Mitsubishi Electric, Quanta)', 26))}
{card(p(f'<b style="color:{GREEN}">3 · Earns from the capacity</b> Positive operating cash flow and positive return on capital. <b>4 out</b> (LS Electric, Rede D\'Or, Zhejiang Expressway, Atlas Arteria)', 26))}
</div>
<div style="display:flex;flex-direction:column;gap:18px">
{card(h3('No country slots') + p('No regions, no quota, no cap. Where the fund lands is an output of the tests.', 26), bg=MINT, border=False)}
{card(h3('Every holding gets an eligibility note') + p('The capacity · why it is hard to replace (licence, network scale, permits, specialist skill, time to rebuild) · how it earns · the main competitive or regulatory risk', 24))}
</div>
</div>''' + foot('Market values: stockanalysis.com (S&amp;P Global Market Intelligence data), 8 Oct 2026 · only 12 water, 9 port and 19 airport &amp; toll-road companies of size are listed, so those lists are shorter · mainland China A-shares not in the universe'),
f"Map builds one global list: the twenty largest listed companies in each of the eight kinds of capacity, anywhere, {fun['universe']} companies. There are no country slots. Two tests decide eligibility. First, material exposure: the main business must be on our list, or at least half of revenue must come from it, which removes seven conglomerates and contractors. Second, the company must actually earn from its capacity: positive operating cash flow and a positive return on capital, which removes four. For every company we hold, the team writes a short eligibility note: what the capacity is, why it is hard to replace, how the company earns from it, and the main risk.")

# ---------------- 6 verify ----------------
pr = [d for d in R['decisions'] if d['ctype'] == 'Ports']
def prow(k, nm, res):
    d = next(x for x in pr if x['key'] == k)
    return [nm, f"{d['ev']:.1f}×" if d['ev'] else '—', (f"{d['cash_yield']*100:.1f}%" if d['cash_yield'] is not None else '—'), (f"{d['spread']:+.1f}" if d['spread'] is not None else '—').replace('-', '−'), res]
port_rows = [prow('WPRTS', 'Westports', '<b style="color:#0F7A45">Eligible · held</b>'), prow('ICT', 'ICTSI', '<b style="color:#0F7A45">Eligible · held</b>'),
             prow('KAMIGUMI', 'Kamigumi', 'Eligible · watchlist (P)'), prow('CMPORT', 'China Merchants Port', 'Eligible · watchlist (P)'),
             prow('JSWINFRA', 'JSW Infrastructure', 'Watchlist: price'), prow('QUB', 'Qube', 'Reject: debt stress'), prow('ADPORTS', 'Adani Ports', 'Reject: governance')]
S['verify'] = sec('verify', head('V · Verify the investment', 'Can it carry its debt in a bad year, and is the price justified against its peers?') + f'''
<div style="display:grid;grid-template-columns:1fr 1.15fr;gap:28px">
<div style="display:flex;flex-direction:column;gap:14px">
{card(h3('Reject') + p('<b>Debt under stress:</b> interest cover after a shock set per type, at least 1.5×. Shock: water 10%, power and networks 15%, hospitals 25%, ports 30%, grid equipment 35%, chips 50%, airports 60%.', 24) + p('<b>Leverage outlier:</b> more than 2 turns above its type\'s median. <b>Investability:</b> a position can\'t be built. <b>Governance:</b> on public record.', 24))}
{card(h3('Watchlist') + p('Cash conversion under 50% of EBITDA · price above 2× its type\'s median · merit in the bottom half of its type', 24))}
{card(h3('Merit, among same-type peers') + p('Half valuation (EV/EBITDA, and cash yield after maintenance spending), half quality (return on capital minus its cost)', 24), bg=MINT, border=False)}
</div>
<div style="display:flex;flex-direction:column;gap:12px">
{p('<b>Worked example · port operators</b> (COSCO Ports and HHLA also fail the debt stress)', 26, INK)}
{table(port_rows, [30, 13, 13, 12, 32], ['Operator', 'EV/EBITDA', 'Cash yield', 'Gap', 'Decision'], size=24, align=['left', 'right', 'right', 'right', 'left'])}
{p('Gap = ROIC − WACC, percentage points · Kamigumi and China Merchants passed V and lost at P (they added too little diversification)', 24, MUTED)}
</div>
</div>''' + foot('Ratios: stockanalysis.com, trailing twelve months, read 8 Oct 2026 · stress shocks set per type from each type\'s worst observed episode, before any results were run'),
"Verify asks: is this worth owning at today's price? We dropped the old universal cut-offs, the 22-times price ceiling and the fixed debt limits, because one number cannot fit a water utility and a chipmaker. Instead, debt is tested under stress, with a shock that fits each kind of business: sixty percent for airports, roughly what 2020 did to them, and ten percent for water, where tariffs are regulated and demand barely moves. A company must still cover its interest one and a half times after the shock. Price is judged against the same kind of company worldwide, on EV to EBITDA and on cash yield, and quality on return on capital above its cost. Ports show every outcome: Westports and ICTSI are eligible and held; Kamigumi and China Merchants are eligible but lost at the portfolio step; JSW is too expensive; Qube fails the debt stress; Adani Ports fails governance.")

# ---------------- 7 funnel ----------------
v_pass = fun['universe'] - (fun['universe'] - fun['m_pass']) - fun['v_reject']
bars = [('Global universe', fun['universe']), ('Pass M (theme)', fun['m_pass']), ('Not rejected at V', v_pass), ('Eligible after V', fun['eligible']), ('Held after P', n)]
bh = ''.join(f'<div style="display:flex;align-items:center;gap:24px"><p style="width:360px;font-size:26px;color:{INK}">{lab}</p><div style="width:{int(1100*v/fun["universe"])}px;height:52px;background:{GREEN if i == 4 else "#9FC8B0"};border-radius:6px"></div><p style="{MONO};font-size:28px;color:{INK};font-weight:600">{v}</p></div>' for i, (lab, v) in enumerate(bars))
S['funnel'] = sec('funnel', head('M, V and P together', f'{fun["universe"]} companies in, {n} held, every exit recorded') + f'''
<div style="display:flex;flex-direction:column;gap:18px">{bh}</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">
{card(p(f'<b>Debt took 32:</b> stress tests (Transurban, Fraport, Intel, Vodafone) and leverage far above peers (NextEra, American Tower)', 24))}
{card(p(f'<b>Watchlist on price, 12:</b> GE Vernova, Equinix, AMD, Arm, Apollo Hospitals; <b>on merit, 29</b>', 24))}
{card(p(f'<b>Watchlist at P, 18:</b> eligible but added too little diversification, e.g. Endesa, TSMC, Veolia, Verizon', 24))}
</div>''' + foot('Bar lengths are to scale · full decision record for all ' + str(fun['universe']) + ' companies in the supporting proposal'),
f"Here is the whole funnel, drawn to scale. {fun['universe']} companies in; {fun['m_pass']} pass Map. Verify rejects {fun['v_reject']}, mostly on debt under stress, and puts {fun['watch_v']} on a watchlist, mostly because they are expensive against their peers or rank in the bottom half. That leaves {fun['eligible']} eligible. Position then holds {n}. The other {fun['eligible'] - n} are good, fairly priced businesses that would have added too little diversification, such as Endesa next to Enel, or TSMC next to the chips we already hold. Every one of those exits is written down, with its reason.")

# ---------------- 8 position ----------------
S['position'] = sec('position', head('P · Position the risk', 'The holdings count and every weight come out of the process') + f'''
<div style="display:grid;grid-template-columns:1fr 1fr;gap:28px">
<div style="display:flex;flex-direction:column;gap:14px">
{h3('Who gets in, in merit order')}
{card(p('<b>1 · Not a duplicate:</b> weekly correlation with a same-type holding at most 0.80', 24))}
{card(p('<b>2 · A sensible size:</b> its risk-based weight is at least 1.0% of the fund', 24))}
{card(p('<b>3 · Adds diversification:</b> raises the diversification ratio by at least 0.5%', 24))}
{p(f'Result: <b>{n} holdings</b>. No target count was set.', 26, INK)}
</div>
<div style="display:flex;flex-direction:column;gap:14px">
{h3('How much: equal risk contribution')}
{p('Each holding is sized to add an equal share of the fund\'s risk, except where a limit binds (the eight telecoms share the 25% type limit), using only the previous three years of weekly peso returns, re-solved each quarter. Calm businesses get more money; volatile ones less.', 24)}
{table([['Single issuer', '20% (BSP, regulatory)', pc(max(x["weight"] for x in PF), 2)], ['Company group', '20% (internal)', 'Razon ' + pc(W['ICT']['weight'], 2)], ['Kind of capacity', '25% (internal)', 'Networks 25.00%'], ['Liquidity', '5 days at 20% of volume', 'None binding'], ['Cash', 'Operating, ~3% (illustrative)', '3.00%']], [32, 40, 28], ['Limit', 'Rule', 'Largest now'], size=24, align=['left', 'left', 'right'])}
{p('No country quotas, no owner/supplier quotas, no fixed reserve. All limits met at all ' + str(R['rebalances']) + ' quarterly rebalances.', 24, MUTED)}
</div>
</div>''' + foot('BSP Circular 1234 (2026), as reproduced by RCBC Trust: 20% single-issuer ceiling for UITFs in exchange-traded equities; above 15% must be that issuer\'s listed shares · the 20% is a ceiling, not a target'),
f"Position answers two questions. Who gets in: we take the eligible companies in merit order, and each must pass three tests. It must not duplicate a holding we already have, it must earn a sensible weight of at least one percent, and it must actually improve the fund's diversification. That process stopped at {n}; we never set a number. How much: each holding is sized to add the same share of risk, using only past data, re-solved each quarter. The only regulatory limit is the BSP's twenty percent single-issuer ceiling, and it is a ceiling, not a target; our largest position is under six percent. We keep two internal limits with stated reasons, twenty-five percent per kind of capacity, because one shock can hit a whole industry, and a liquidity limit. There is no country quota and no fixed cash reserve; the manager holds operating cash for redemptions.")

# ---------------- 9 grid ----------------
order = ['Digital networks', 'Healthcare facilities', 'Power generation & grids', 'Ports', 'Semiconductors', 'Water', 'Grid & power equipment', 'Airports & toll roads']
short = {'EXC': 'Exelon', 'WPRTS': 'Westports', 'ICT': 'ICTSI', 'ENGI': 'Engie', 'BDMS': 'Bangkok Dusit', 'EOAN': 'E.ON', 'SULAIMAN': 'Sulaiman Al Habib', 'GDI': 'Guangdong Inv.',
         'KDDI': 'KDDI', 'EHC': 'Encompass', 'T': 'AT&amp;T', 'MOUWASAT': 'Mouwasat', 'CHTEL': 'China Telecom', 'SBS': 'Sabesp', 'CHMOB': 'China Mobile', 'HCA': 'HCA',
         'ENEL': 'Enel', 'STC': 'Saudi Telecom', 'AIRTEL': 'Bharti Airtel', 'DTE': 'Deutsche Telekom', 'BH': 'Bumrungrad', 'QCOM': 'Qualcomm', 'AMX': 'América Móvil',
         'OMAB': 'OMA', 'ADVANTEST': 'Advantest', 'HDHE': 'HD Hyundai Elec.', 'NVDA': 'NVIDIA', 'VST': 'Vistra', 'SKHYNIX': 'SK hynix', 'MU': 'Micron', 'ENR': 'Siemens Energy'}
def gcard(t):
    hs = sorted([x for x in PF if x['ctype'] == t], key=lambda x: -x['weight'])
    items = ' · '.join(f"{short[x['key']]} {x['country']} <b>{x['weight']*100:.2f}</b>" for x in hs)
    tt = t.replace('&', '&amp;').replace('Power generation & grids', 'Power &amp; grids')
    return card(f'<p style="font-size:24px;color:{GREEN};font-weight:600">{tt.replace("Power generation &amp; grids", "Power &amp; grids")} · {bt[t]*100:.2f}%</p>' + p(items, 24, INK), pad='14px 22px')
S['grid'] = sec('grid', head('The portfolio · solved on data to 2 October 2026', f'{n} holdings across eight kinds of capacity, plus 3% operating cash', 48) +
f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">{"".join(gcard(t) for t in order)}</div>' +
foot('Weights in % of the fund · who is held came from V and P\'s inclusion tests; how much came from the risk model, not from rank'),
f"Here is the whole portfolio on one page: {n} companies in eight kinds of capacity. Read the weights carefully. The biggest positions are calm, cash-generating owners: Exelon's wires, Westports, ICTSI, Engie, Bangkok Dusit. The chipmakers sit between about one and two percent, even though Micron has the best merit score of all {fun['eligible']} eligible companies, because their share prices swing 42 to 63 percent a year. Digital networks sit exactly at the twenty-five percent cap. Rank decides who gets in; the risk model decides how much.", pad='96px 128px 120px', gap=20)

# ---------------- 10-11 two stock examples ----------------
def example(sid, k, kicker, title, role, wr, notes):
    x = W[k]; nt = N[k]
    ev_line = f" Supporting evidence: {nt['ev'][0]}." if nt.get('ev') else ''
    rows = [('Theme &amp; milestone', f"{nt['cap']}. Hard to replace: {nt['moat']}. Earns: {nt['earn']}.{ev_line} <i>Story: {STORY[x['ctype']]}.</i>"),
            ('Fundamentals &amp; valuation', f"EV/EBITDA {x['ev']:.1f}× (peer median {x['peer_med_ev']:.1f}×) · cash yield {x['cash_yield']*100:.1f}% (median {x['peer_med_cy']*100:.1f}%) · ROIC − WACC {x['spread']:+.1f} pts (median {x['peer_med_spread']:+.1f}) · merit #{x['merit_rank']} of {x['peers']} · " + (f"net cash; stressed interest cover passes easily" if x['nd'] is not None and x['nd'] < 0 else f"net debt {x['nd']:.2f}× EBITDA; interest cover {x['cov_stress']:.1f}× after a {int(x['shock']*100)}% EBITDA shock")),
            ('Key risks', nt['risk']), ('Portfolio role', role), ('Weighting rationale', wr)]
    rr = ''.join(f'<div style="display:grid;grid-template-columns:330px 1fr;gap:24px;padding:14px 0;border-top:1px solid {LINE}"><p style="font-size:24px;font-weight:600;color:{GREEN}">{a}</p><p style="font-size:24px;line-height:1.4;color:{INK}">{b.replace("-", "−") if a == "Fundamentals &amp; valuation" else b}</p></div>' for a, b in rows)
    return sec(sid, head(kicker, title, 52) + f'<div style="display:flex;flex-direction:column">{rr}</div>' +
               foot('Ratios: stockanalysis.com, 8 Oct 2026 · weight and risk from the quarterly solve on data to 2 Oct 2026 · full table for all ' + str(n) + ' holdings in the supporting proposal'), notes, pad='100px 128px 120px', gap=16)
ict, nv = W['ICT'], W['NVDA']
S['ex1'] = example('ex1', 'ICT', f'Holding example 1 · ICTSI · Philippines · {pc(ict["weight"], 2)}', 'A Filipino company that earned its place against every port operator in the world',
    f"Ports {bt['Ports']*100:.1f}% of the fund with Westports. ICTSI's average correlation with the other holdings is {ict['avg_corr']:.2f}, among the lowest: it moves on its own. It is our only Philippine holding.",
    f"{pc(ict['weight'], 2)} = an equal {pc(ict['risk_share'])} share of fund risk at {pc(ict['vol'])} volatility. No limit binds. Not a home bias: the same rules applied to Kamigumi and China Merchants put them on the watchlist.",
    f"Our first example is ICTSI, and the point is that it competed against the world. Theme: it runs container terminals under long concessions, including Manila's, renewed this year for another 25 years. Valuation: it is not the cheapest port, at about fifteen times EBITDA, but it earns almost fourteen points more than its cost of capital, and its debt passes a thirty percent shock with cover to spare. Risk: emerging-market concessions and currencies. Role: it barely moves with the rest of the fund. Weight: {pc(ict['weight'], 2)}, which is simply what an equal share of risk works out to.")
S['ex2'] = example('ex2', 'NVDA', f'Holding example 2 · NVIDIA · United States · {pc(nv["weight"], 2)}', 'The AI chip leader is in the fund, and the risk model keeps it small',
    f"Semiconductors {bt['Semiconductors']*100:.1f}% of the fund across five names; with grid equipment, about {(bt['Semiconductors'] + bt['Grid & power equipment'])*100:.0f}% rides on the data-centre build-out. That overlap is reported, not hidden.",
    f"{pc(nv['weight'], 2)}: its price swings {pc(nv['vol'], 0)} a year, so an equal {pc(nv['risk_share'])} share of risk buys little. Equal weighting would hold {pc(0.97/n, 2)}; that is the concentration we choose not to take.",
    f"Our second example shows that the theme is not anti-tech. NVIDIA makes the chips and networking that AI data centres are built on, and its software ecosystem is very hard to replace. On valuation it is expensive in absolute terms, about 28 times EBITDA, but cheaper than the semiconductor median of 36, and it earns seventy-five points above its cost of capital, so it ranks second of seventeen. Risks: a few huge customers, export controls, and an AI spending cycle that could turn. Its weight is {pc(nv['weight'], 2)}, because its price swings about {pc(nv['vol'], 0)} a year. That is the risk model doing its job.")

# ---------------- 12 role ----------------
mx = max(bt.values())
tb = ''.join(f'<div style="display:flex;align-items:center;gap:16px"><p style="width:300px;font-size:24px;color:{INK}">{t.replace("&", "&amp;").replace("Power generation &amp; grids", "Power &amp; grids")}</p><div style="width:{int(560*v/0.25)}px;height:30px;background:{GREEN if W and next(x for x in PF if x["ctype"] == t)["role"] == "Owner" else BLUE};border-radius:4px"></div><p style="{MONO};font-size:24px;color:{INK}">{v*100:.1f}</p></div>' for t, v in bt.items())
top_c = ' · '.join(f"{k} {v*100:.1f}" for k, v in list(cnt.items())[:6])
S['role'] = sec('role', head('Portfolio role · exposure and overlap', 'Spread by what drives earnings, with every overlap reported') + f'''
<div style="display:grid;grid-template-columns:1.05fr 1fr;gap:36px">
<div style="display:flex;flex-direction:column;gap:12px">{p('Weight by kind of capacity · bars scaled 0 to 25%, the limit', 24, MUTED)}{tb}{p('Green = owners/operators · blue = suppliers', 24, MUTED)}</div>
<div style="display:flex;flex-direction:column;gap:16px">
{card(p(f'<b>Overlaps we report</b><br>Data-centre build-out (chips + grid equipment) {(bt["Semiconductors"] + bt["Grid & power equipment"])*100:.1f}% · US health policy (HCA, Encompass) {(W["HCA"]["weight"] + W["EHC"]["weight"])*100:.1f}% · Chinese state telecoms {(W["CHMOB"]["weight"] + W["CHTEL"]["weight"])*100:.1f}% · Saudi Arabia {cnt.get("SA", 0)*100:.1f}%', 24))}
{card(p(f'<b>Countries are an output</b><br>{top_c} · {len(cnt) - 6} others · listing country, not where revenue is earned', 24))}
{card(p(f'<b>About {R["eff_bets"]:.1f} independent exposures</b>; the two largest shared forces explain {R["top2_factor"]*100:.0f}% of risk', 24), bg=MINT, border=False)}
</div>
</div>''' + foot('Weights solved on data to 2 Oct 2026 · independent exposures = diversification ratio squared · countries by listing; ICTSI, América Móvil and others earn across many countries'),
f"Portfolio role means what each holding adds and what it duplicates. The fund is spread across eight kinds of capacity; digital networks sit at the twenty-five percent limit, healthcare and power follow. We publish the overlaps instead of hiding them: about eleven percent rides on data-centre spending, about seven percent on US health policy, and almost eleven on Saudi Arabia. Countries are an output, and they are listing countries; a company like ICTSI earns in twenty. Statistically the {n} behave like about {R['eff_bets']:.0f} independent exposures, a real improvement on the six of our earlier draft.")

# ---------------- 13 ph ----------------
S['ph'] = sec('ph', head('The question every judge will ask', f'Why only {pc(ph)} in Philippine companies?') + f'''
<div style="display:flex;gap:24px">
{card(f'<p style="{SERIF};font-size:72px;font-weight:600;color:{GREEN};line-height:1">{pc(ict["weight"], 2)}</p>' + h3('ICTSI, held') + p('Second on merit of the five port operators that passed Verify\'s reject tests; earns 13.9 points above its cost of capital', 24), extra='flex:1')}
{card(f'<p style="{SERIF};font-size:72px;font-weight:600;color:{INK};line-height:1">Watchlist</p>' + h3('Manila Water') + p('Cheap at 8.2× EBITDA, but operating cash flow is only 28% of EBITDA, under our 50% test. It returns when cash catches up.', 24), extra='flex:1')}
{card(f'<p style="{SERIF};font-size:72px;font-weight:600;color:{INK};line-height:1">Outside</p>' + h3('Meralco, PLDT, Globe, Aboitiz Power') + p('Good companies below the 20 largest worldwide in their field: the same size floor every country faces', 24), extra='flex:1')}
</div>
{callout(f'Our answer: we never set it. A quota would put the number in by assumption. The investor still saves, invests and redeems in pesos.')}''' +
foot(f'Philippine weight ranged {pc(R["ph_range"][0])}–{pc(R["ph_range"][1])} across the {R["rebalances"]} quarterly rebalances · Meralco US$7.4bn and PLDT US$3.9bn against a 20th-largest power or telecom company near US$39bn'),
f"Expect this question. Our first draft held thirty percent here by rule. The theme is global, so the rule went, and the number now comes out of the tests. One Philippine company earned its place against the world: ICTSI. Manila Water was in our previous portfolio, and it is now on the watchlist, for a specific reason: its operating cash flow is only twenty-eight percent of its EBITDA, under our fifty percent test. When cash catches up, it comes back. Meralco and PLDT are good businesses but smaller than the twenty largest in their fields worldwide, the same floor every country faces. The investor is still Filipino: they save, invest and redeem in pesos.")

# ---------------- 14 weighting ----------------
alt = R['alt_types']
S['weighting'] = sec('weighting', head('Does the risk model earn its complexity?', 'Same 31 holdings, three ways to weight them, same costs') + f'''
<div style="display:grid;grid-template-columns:1.3fr 1fr;gap:32px">
{table([['₱100 became', f"<b>{num(v4['growth'])}</b>", num(iv['growth']), num(ew['growth'])], ['Return a year', f"<b>{pc(v4['cagr'])}</b>", pc(iv['cagr']), pc(ew['cagr'])],
        ['Volatility', f"<b>{pc(v4['vol'])}</b>", pc(iv['vol']), pc(ew['vol'])], ['Worst fall', f"<b>{pc(v4['maxdd'])}</b>", pc(iv['maxdd']), pc(ew['maxdd'])],
        ['Semiconductors today', f"<b>{pc(bt['Semiconductors'])}</b>", pc(alt['iv']['Semiconductors']), pc(alt['ew']['Semiconductors'])],
        ['Digital networks today', f"<b>{pc(bt['Digital networks'])}</b>", pc(alt['iv']['Digital networks']), pc(alt['ew']['Digital networks'])]],
       [40, 20, 20, 20], ['', 'Risk model (ERC)', 'Inverse vol.', 'Equal weight'], size=26, colors=[None, GREEN, None, None])}
<div style="display:flex;flex-direction:column;gap:16px">
{card(p(f'<b>Equal weight made more:</b> {pc(ew["cagr"])} a year, because it held about twice as much in chips through the AI boom. It also swung more and fell further.', 24))}
{card(p(f'<b>Inverse volatility came within {abs(v4["cagr"] - iv["cagr"])*100:.1f} pts</b> of the risk model, but without our limits: it would put {pc(alt["iv"]["Digital networks"])} in telecoms, over the 25% limit. ERC applies the limits inside the solve and accounts for correlation.', 24))}
{card(p('<b>We chose the method before testing</b> and do not switch to the winner after the fact.', 24), bg=MINT, border=False)}
</div>
</div>''' + foot('Weekly, 1 Oct 2021 – 2 Oct 2026, in pesos, after the 1.50% fee, 0.30% trading costs and estimated dividend withholding · historical performance of the currently selected portfolio, not a backtest of the process · inverse volatility and equal weight shown without the 25% type limit'),
f"The team's revised rules ask us to prove the optimizer is worth it, so here is the honest comparison, same holdings, same costs. Equal weighting made the most, {pc(ew['cagr'])} a year, and we should say why: it held twice as much in chipmakers through the AI boom, and it swung more and fell further. Simple inverse-volatility weighting landed within a fraction of a point of our risk model. So the complexity buys little extra return. We keep equal risk contribution because the limits are applied inside the solve and it accounts for how holdings move together. We chose it before testing, and we are not switching to whichever method won the last five years.")

# ---------------- 15 sim5 chart ----------------
paths = R['paths']; nweek = len(paths['v4'])
ymax = 450
def path_d(vals, x0=0, w=980, h=440, top=0):
    pts = [f"{x0 + i*w/(len(vals) - 1):.1f},{top + h - v/ymax*h:.1f}" for i, v in enumerate(vals)]
    return 'M' + ' L'.join(pts)
gl = ''.join(f'<line x1="0" y1="{440 - v/ymax*440:.0f}" x2="980" y2="{440 - v/ymax*440:.0f}" stroke="{"#9AA39D" if v == 0 else LINE}" stroke-width="{2 if v == 0 else 1.5}"/>' for v in range(0, ymax + 1, 50))
yl = ''.join(f'<p style="position:absolute;left:128px;top:{300 + 440 - v/ymax*440 - 17:.0f}px;width:80px;text-align:right;{MONO};font-size:24px;color:{MUTED}">{v}</p>' for v in range(0, ymax + 1, 100))
xt = {}
for i, d in enumerate(R['dates']):
    y = d[:4]
    if d[5:7] == '01' and y not in xt: xt[y] = i
xl = ''.join(f'<p style="position:absolute;left:{228 + i*980/(nweek - 1) - 40:.0f}px;top:752px;width:80px;text-align:center;{MONO};font-size:24px;color:{MUTED}">{y}</p>' for y, i in xt.items())
pe = F5['psei']['stats']
c22 = lambda k: pc(F5[k]['cal']['2022'])
S['sim5'] = sec('sim5', head('Historical performance of the currently selected portfolio · after all costs, in pesos', 'Five years: ahead of the world and the PSEi, behind tech', 48) + f'''
<p style="position:absolute;left:228px;top:262px;width:700px;font-size:24px;color:{MUTED}">Growth of ₱100 · linear scale from zero</p>
<svg aria-label="Growth of 100 pesos, Oct 2021 to Oct 2026: Firsts Fund {v4['growth']:.0f}, global tech ETF {ix['growth']:.0f}, MSCI ACWI {aw['growth']:.0f}" style="position:absolute;left:228px;top:300px;width:980px;height:440px" width="980" height="440" viewBox="0 0 980 440">
{gl}
<path d="{path_d(paths['acwi'])}" fill="none" stroke="{GRAY}" stroke-width="3" stroke-linejoin="round"/>
<path d="{path_d(paths['psei'])}" fill="none" stroke="{AMBERB}" stroke-width="3" stroke-linejoin="round"/>
<path d="{path_d(paths['ixn'])}" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linejoin="round"/>
<path d="{path_d(paths['v4'])}" fill="none" stroke="{GREEN}" stroke-width="5" stroke-linejoin="round"/>
</svg>
{yl}{xl}
<div style="position:absolute;left:1260px;top:262px;width:532px;display:flex;flex-direction:column;gap:16px">
{table([['₱100 →', f"<b>{v4['growth']:.0f}</b>", f"{aw['growth']:.0f}", f"{pe['growth']:.0f}", f"{ix['growth']:.0f}"], ['A year', f"<b>{pc(v4['cagr'])}</b>", pc(aw['cagr']), pc(pe['cagr']), pc(ix['cagr'])],
        ['Swings', f"<b>{pc(v4['vol'])}</b>", pc(aw['vol']), pc(pe['vol']), pc(ix['vol'])], ['Worst fall', f"<b>{pc(v4['maxdd'])}</b>", pc(aw['maxdd']), pc(pe['maxdd']), pc(ix['maxdd'])], ['2022', f"<b>{c22('v4')}</b>", c22('acwi'), c22('psei'), c22('ixn')]],
       [28, 18, 18, 18, 18], ['', 'Firsts', 'World', 'PSEi', 'Tech'], colors=[None, GREEN, None, AMBERB, BLUE])}
{p(f'<b style="color:{GREEN}">━ Firsts Fund</b><br><b style="color:{MUTED}">━ MSCI ACWI ETF (reference)</b><br><b style="color:{AMBERB}">━ PSEi, via the FMETF tracker (local reference)</b><br><b style="color:{BLUE}">━ Global tech ETF (context)</b>', 24)}
</div>
<div style="position:absolute;left:128px;top:806px;width:1664px">{callout(f'<b>How we defend it:</b> these {n} were picked in October 2026 with today\'s numbers, so {pc(v4["cagr"])} is hindsight, not a forecast or a backtest of our process. The shallow falls (about {abs(v4["maxdd"]/aw["maxdd"])*100:.0f}% of the world index\'s worst) carry the same caveat; over 36 years the industry proxy\'s worst fall was {pc(-ps["cap"]["maxdd"], 0)}.')}</div>
''' + foot(f'Weekly, 1 Oct 2021 – 2 Oct 2026 · net of fee, trading costs and withholding · ETFs after their own costs · PSEi = FMETF price, no dividends · none is the fund\'s benchmark'),
f"Five years, in pesos, after every cost we can model: our fee, trading costs and dividend taxes. One hundred pesos became {v4['growth']:.0f} in Firsts Fund, {aw['growth']:.0f} in the world index, {pe['growth']:.0f} in the PSEi tracker and {ix['growth']:.0f} in a global tech fund. That PSEi line is the home-market alternative our saver already has: it went backwards. The axis starts at zero, so the gaps are drawn true to size. Tech made more, and we say so. Now the caveat, in our own words before a judge says it: we picked these companies in October 2026 using today's data, so this is the history of today's portfolio, not proof that our process works. What we lead on is the path: our worst fall was about seven percent, against eighteen for the world and twenty-seven for tech.", pad='112px 128px 140px', gap=14)

# ---------------- 16 old vs new rules ----------------
c3 = F5['v3']['cal']; c4 = F5['v4']['cal']
S['oldnew'] = sec('oldnew', head('Previous rules vs revised rules', 'Same five years, same costs: the new rules are more defensible, not proven better') + f'''
<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:32px">
{table([['Holdings', '21 (top 3 per type)', f'<b>{n}</b> (process decides)'], ['Philippines', '9.6%', f'<b>{pc(ph)}</b>'], ['Return a year', pc(v3['cagr']), f"<b>{pc(v4['cagr'])}</b>"],
        ['Volatility', pc(v3['vol']), f"<b>{pc(v4['vol'])}</b>"], ['Worst fall', pc(v3['maxdd']), f"<b>{pc(v4['maxdd'])}</b>"], ['Worst 12 months', pc(v3['worst12']), f"<b>{pp(v4['worst12'])}</b>"],
        ['2022', pc(c3['2022']), f"<b>{pp(c4['2022'])}</b>"], ['Independent exposures', 'about 5.9', f"<b>about {R['eff_bets']:.1f}</b>"]],
       [38, 31, 31], ['', 'Previous (v3)', 'Revised (v4)'], size=26, align=['left', 'right', 'right'], colors=[None, None, GREEN])}
<div style="display:flex;flex-direction:column;gap:16px">
{card(p('<b>What changed:</b> no dated-target test, debt judged under a stress that fits each type, valuation against peers including cash yield, hospitals added, holdings count from the process, 20% regulatory ceiling instead of our 10% cap, operating cash instead of a 10% reserve.', 24))}
{card(p('<b>Why the better numbers prove little:</b> both lists were chosen with October 2026 data. The gain may mostly reflect hospitals and broader diversification in this period; we have not attributed it.', 24))}
{card(p('<b>What we can claim:</b> rules set before testing, each exit recorded, and less concentration.', 24), bg=MINT, border=False)}
</div>
</div>''' + foot('Both: weekly, 1 Oct 2021 – 2 Oct 2026, in pesos, net of 1.50% fee, 0.30% trading costs, est. withholding, cash at BSP policy rate − 0.50 pt · v3 keeps its own 10% reserve and limits'),
f"The team asked us to compare old and new rules over the same period, with the same costs. Here it is. The revised rules hold {n} companies instead of twenty-one, about half the Philippine weight, and the five-year history looks better on every line. We do not claim that proves the new rules are better: both lists were chosen with today's data, and the improvement may mostly come from adding hospitals and spreading wider over a period when that worked; we have not tested that. What we do claim is that the new rules were fixed before testing, every exit is recorded, and the portfolio is less concentrated: about {R['eff_bets']:.0f} independent exposures instead of six.")

# ---------------- 17 vstech, 18 vsmkt ----------------
def side(sid, other, okey, title, kicker, defense, notes):
    o5 = F5[okey]['stats']; o36 = ps[other]
    rows36 = [['Return a year', pc(ps['cap']['cagr']), pc(o36['cagr'])], ['₱100 grew to', '₱' + num(ps['cap']['growth']), '₱' + num(o36['growth'])],
              ['Volatility', pc(ps['cap']['vol']), pc(o36['vol'])], ['Largest fall', pc(ps['cap']['maxdd']), pc(o36['maxdd'])],
              ['Months to recover', str(ps['cap']['months_peak_to_recovery']), str(o36['months_peak_to_recovery'])], ['Worst 12 months', pc(ps['cap']['worst12']), pc(o36['worst12'])],
              ['Calendar years ahead', f"{PX['years_ahead'][other]} of 37", f"{37 - PX['years_ahead'][other]} of 37"]]
    rows_c = [[n_, pc(v['cap']), pc(v[other])] for n_, v in cr.items() if n_.split(',')[0] in ('Dot-com', 'Global financial crisis', 'COVID', '2022 rate shock')]
    rows_c = [[r[0].split(',')[0].replace('Global financial crisis', '2008 crisis').replace('2022 rate shock', 'Rate shock, 2022'), r[1], r[2]] for r in rows_c]
    lab = 'Tech' if other == 'tech' else 'Market'
    return sec(sid, head(kicker, title) + f'''
<div style="display:grid;grid-template-columns:1fr 1fr;gap:32px">
<div style="display:flex;flex-direction:column;gap:12px">{p('<b>36 years · Jan 1990 – Aug 2026 · industry proxy, context only</b>', 24, INK)}
{table(rows36, [46, 27, 27], ['In pesos', 'Firsts method', lab], size=24, colors=[None, GREEN, None])}</div>
<div style="display:flex;flex-direction:column;gap:12px">{p('<b>When it mattered · total over the episode</b>', 24, INK)}
{table(rows_c, [46, 27, 27], ['Episode', 'Firsts method', lab], size=24, colors=[None, GREEN, None])}
{p('<b>5 years · our ' + str(n) + ' vs the ' + ('global tech ETF' if other == 'tech' else 'world index ETF') + '</b>', 24, INK)}
{table([['Return · worst fall', pc(v4['cagr']) + ' · ' + pc(v4['maxdd']), pc(o5['cagr']) + ' · ' + pc(o5['maxdd'])]], [46, 27, 27], size=24)}</div>
</div>
{callout(defense)}''' + foot('36 years: industry proxy, context only: six US industries standing in for the eight types, same weighting (ERC, 25% type limit), 1.50% fee and trading costs, no company screens; ' + ('tech = hardware, software, chips, lab equipment' if other == 'tech' else 'market = 97% US market + 3% cash, same fee') + ' · 5 years: historical performance of the currently selected portfolio, with hindsight'),
               notes, gap=22)
S['vstech'] = side('vstech', 'tech', 'ixn', 'Tech pays more, and asks more of the saver', 'Side by side · our fund vs a tech fund',
    f'<b>Our defense:</b> tech earned more, and we say so. A saver with a first five years away cannot plan around a {pc(ps["tech"]["maxdd"], 0)} fall and {ps["tech"]["months_peak_to_recovery"] // 12} years under water.',
    f"Head to head with tech, be direct: tech wins on return, over 36 years and over the last five, and it even wins narrowly on return per unit of risk. It also did better in COVID. Then make the point that matters for our investor: after 2000, tech fell {pc(ps['tech']['maxdd'], 0)} and took {ps['tech']['months_peak_to_recovery']} months to get back. Our method lost about ten percent through the same crash. Someone saving for a first home five years away cannot wait sixteen years to break even. That is why we are not a tech fund, and why we hold chipmakers at small, risk-sized weights instead of excluding them.")
S['vsmkt'] = side('vsmkt', 'mkt', 'acwi', 'Over 36 years, about the market\'s return, with shallower falls', 'Side by side · our fund vs a market fund',
    f'<b>Our defense:</b> over the long run we do not beat the market on return ({pc(ps["cap"]["cagr"])} vs {pc(ps["mkt"]["cagr"])}). We offer about the same return with smaller worst falls, in a theme an investor can understand.',
    f"Against a plain market fund with the same fee, the honest result over 36 years is a draw on return, slightly in the market's favour: {pc(ps['cap']['cagr'])} against {pc(ps['mkt']['cagr'])} a year. Where the method helped was in the bad stretches: it lost about ten percent through the dot-com crash when the market lost twenty-seven, and a little less in 2008. It did worse in COVID, when hospitals and airports shut. So our claim is modest: about the market's return, with shallower worst falls, in businesses an investor can picture. Over the last five years, the current holdings did better than the world index, with the hindsight caveat from before.")

# ---------------- 19 long36 chart ----------------
g = PX['growth']; m = PX['months']; NM = len(m); top = 24000
def lpath(vals, h=380, scale=top): return 'M' + ' L'.join(f"{i*1105/(NM - 1):.1f},{h - v/scale*h:.1f}" for i, v in enumerate(vals))
def dd(vals):
    pk = 0; out = []
    for v in vals: pk = max(pk, v); out.append(v/pk - 1)
    return out
def dpath(vals): return 'M' + ' L'.join(f"{i*1105/(NM - 1):.1f},{6 + 180*(-d)/0.75:.1f}" for i, d in enumerate(dd(vals)))
g1 = ''.join(f'<line x1="0" y1="{380 - v/top*380:.0f}" x2="1105" y2="{380 - v/top*380:.0f}" stroke="{"#9AA39D" if v == 0 else LINE}" stroke-width="{2 if v == 0 else 1.5}"/>' for v in range(0, top + 1, 4000))
yl1 = ''.join(f'<p style="position:absolute;left:128px;top:{258 + 380 - v/top*380 - 15:.0f}px;width:110px;text-align:right;{MONO};font-size:24px;color:{MUTED}">{v:,}</p>' for v in range(0, top + 1, 8000))
g2 = ''.join(f'<line x1="0" y1="{6 + 180*d/75:.0f}" x2="1105" y2="{6 + 180*d/75:.0f}" stroke="{"#9AA39D" if d == 0 else LINE}" stroke-width="{2 if d == 0 else 1.5}"/>' for d in [0, 25, 50, 75])
yl2 = ''.join(f'<p style="position:absolute;left:128px;top:{690 + 6 + 180*d/75 - 15:.0f}px;width:110px;text-align:right;{MONO};font-size:24px;color:{MUTED}">{"0" if d == 0 else "−" + str(d) + "%"}</p>' for d in [0, 25, 50, 75])
xl36 = ''.join(f'<p style="position:absolute;left:{253 + i*1105/(NM - 1) - 40:.0f}px;top:892px;width:80px;text-align:center;{MONO};font-size:24px;color:{MUTED}">{mm[:4]}</p>' for i, mm in enumerate(m) if mm.endswith('-01') and int(mm[:4]) % 10 == 0)
S['long36'] = sec('long36', head('Industry proxy, 36 years · context only, not a test of our company screens', 'The method kept pace with the market and fell far less than tech', 48) + f'''
<p style="position:absolute;left:253px;top:222px;width:1000px;font-size:24px;color:{MUTED}">Growth of ₱100 · linear scale from zero</p>
<svg aria-label="Growth of 100 pesos, Jan 1990 to Aug 2026, linear: tech {num(ps['tech']['growth'])}, market {num(ps['mkt']['growth'])}, Firsts method {num(ps['cap']['growth'])}" style="position:absolute;left:253px;top:258px;width:1105px;height:380px" width="1105" height="380" viewBox="0 0 1105 380">
{g1}<path d="{lpath(g['mkt'])}" fill="none" stroke="{GRAY}" stroke-width="2.5"/><path d="{lpath(g['tech'])}" fill="none" stroke="{BLUE}" stroke-width="2.5"/><path d="{lpath(g['cap'])}" fill="none" stroke="{GREEN}" stroke-width="4"/>
</svg>{yl1}
<p style="position:absolute;left:253px;top:652px;width:1000px;font-size:24px;color:{MUTED}">Fall from the previous peak · 0 to −75%</p>
<svg aria-label="Drawdowns: tech fell {pc(-ps['tech']['maxdd'], 0)} after 2000; Firsts method's worst fall {pc(-ps['cap']['maxdd'], 0)} in 2008-09; market {pc(-ps['mkt']['maxdd'], 0)}" style="position:absolute;left:253px;top:690px;width:1105px;height:196px" width="1105" height="196" viewBox="0 0 1105 196">
{g2}<path d="{dpath(g['mkt'])}" fill="none" stroke="{GRAY}" stroke-width="2"/><path d="{dpath(g['tech'])}" fill="none" stroke="{BLUE}" stroke-width="2.5"/><path d="{dpath(g['cap'])}" fill="none" stroke="{GREEN}" stroke-width="3.5"/>
</svg>{yl2}{xl36}
<div style="position:absolute;left:1416px;top:258px;width:376px;display:flex;flex-direction:column;gap:20px">
{table([['₱100 →', f"<b>{num(ps['cap']['growth'])}</b>", num(ps['mkt']['growth']), num(ps['tech']['growth'])], ['A year', f"<b>{pc(ps['cap']['cagr'])}</b>", pc(ps['mkt']['cagr']), pc(ps['tech']['cagr'])],
        ['Worst fall', f"<b>{pc(ps['cap']['maxdd'], 0)}</b>", pc(ps['mkt']['maxdd'], 0), pc(ps['tech']['maxdd'], 0)], ['Months to recover', f"<b>{ps['cap']['months_peak_to_recovery']}</b>", str(ps['mkt']['months_peak_to_recovery']), str(ps['tech']['months_peak_to_recovery'])]],
       [34, 22, 22, 22], ['', 'Firsts', 'Mkt', 'Tech'], colors=[None, GREEN, None, BLUE])}
{p(f'<b style="color:{GREEN}">━ Firsts method</b><br><b style="color:{MUTED}">━ Market fund</b><br><b style="color:{BLUE}">━ Tech fund</b>', 24)}
</div>''' + foot('US industry returns (Kenneth French): utilities, telecom, transport, health services, electrical equipment, chips · same ERC, 25% type limit, 3% cash, 1.50% fee, 0.30% trading cost · BIS peso rates'),
f"Five years is too short to judge a fund, so we rebuilt the method over 36 years using US industry returns for the same kinds of capacity, now including health services, with the same weighting rules and costs but none of our company screens. Be clear about what this is: context for the theme, not a test of our company screens. Both panels use linear scales from zero. In the top panel, our method ends a little below a same-cost market fund, and tech ends far higher, which we say plainly. The bottom panel is why we are not a tech fund: after 2000 tech fell {pc(-ps['tech']['maxdd'], 0)} and took sixteen years to recover. Our worst fall was {pc(-ps['cap']['maxdd'], 0)}, in 2008, slightly less than the market.", pad='104px 128px 140px', gap=14)

# ---------------- 20 crises ----------------
crows = [[k, pc(v['cap']), pc(v['mkt']), pc(v['tech'])] for k, v in cr.items()]
drows = [[k, pc(v['cap']), pc(v['mkt']), pc(v['tech'])] for k, v in PX['decades'].items()]
S['crises'] = sec('crises', head('Industry proxy · good and bad stretches, as they happened', 'Better in some crises, worse in others: no protection is promised') + f'''
<div style="display:grid;grid-template-columns:1fr 1fr;gap:32px">
<div style="display:flex;flex-direction:column;gap:12px">{p('<b>Crises · total over the episode</b>', 24, INK)}
{table(crows, [46, 18, 18, 18], ['Episode', 'Firsts', 'Market', 'Tech'], size=24, colors=[None, GREEN, None, BLUE])}</div>
<div style="display:flex;flex-direction:column;gap:12px">{p('<b>Decades · a year</b>', 24, INK)}
{table(drows, [46, 18, 18, 18], ['Period', 'Firsts', 'Market', 'Tech'], size=24, colors=[None, GREEN, None, BLUE])}
{p(f"Calendar years ahead of the market: {PX['years_ahead']['mkt']} of 37 · ahead of tech: {PX['years_ahead']['tech']} of 37", 24)}</div>
</div>
{callout('<b>What we say:</b> the method fell less than the market in the dot-com crash and in 2008, and did <b>worse</b> in COVID and gained less in 1997–98. It is an equity fund: it can lose a quarter of its value in a year.')}''' +
foot('US industry proxy, in pesos, after 1.50% fee and trading costs · the 1997–98 figures are positive because the peso fell sharply, raising the peso value of dollar assets'),
"This slide is here so nobody thinks we only show good years. Over 36 years the method was better than the market in the dot-com crash and in 2008, and worse in COVID, when hospitals and airports shut, and worse than both in the Asian-crisis period, which in pesos was a gain for everyone because the peso fell. By decade it trails the market in three of four. So we make no promise of protection. This is an equity fund, and in its worst twelve months it lost twenty-seven percent. What the account-level glidepath does about that is the next slide.")

# ---------------- 21 investor ----------------
d0, dg = ct['dca'], ct['dca_glide']
bar = lambda v, c: f'<div style="width:{int(700*v/1.5)}px;height:40px;background:{c};border-radius:4px"></div>'
S['investor'] = sec('investor', head('Fund versus investor · regular contributions and the glidepath', 'What a five-year saver actually experienced, every start month since 1990') + f'''
<div style="display:grid;grid-template-columns:1.1fr 1fr;gap:32px">
<div style="display:flex;flex-direction:column;gap:14px">
{p('<b>₱1,000 a month for 60 months · ending value ÷ total paid in</b> · industry proxy, ' + str(d0['n']) + ' windows', 24, INK)}
{table([['Median', f"{d0['median']:.2f}×", f"{dg['median']:.2f}×"], ['Worst 5% of windows', f"{d0['p5']:.2f}×", f"{dg['p5']:.2f}×"], ['Worst window', f"{d0['worst']:.2f}×", f"{dg['worst']:.2f}×"],
        ['Ended below what was paid in', pc(d0['below1'], 0), pc(dg['below1'], 0)]], [46, 27, 27], ['', 'Fund only', 'With glidepath'], size=26, colors=[None, None, GREEN])}
{p(f'Worst window, ₱60,000 paid in: <b>₱{num(60000*d0["worst"])}</b> fund only, <b>₱{num(60000*dg["worst"])}</b> with the glidepath. The glidepath gives up some upside: median {d0["median"]:.2f}× → {dg["median"]:.2f}×.', 24)}
</div>
<div style="display:flex;flex-direction:column;gap:14px">
{table([['One shared global equity mandate', 'A personal goal date and allocation'], ['Manager selects and re-weights stocks', 'Platform redeems some Firsts Fund units and reinvests the proceeds in a lower-risk fund'], ['Active management continues', 'Exposure falls as the goal approaches']],
       [50, 50], ['Fund level', 'Investor level (proposed)'], size=24, align=['left', 'left'])}
{p('Illustrative schedule only: from 24 months before the goal, the target equity share falls in a straight line to 20%. Transfers use redemption proceeds, at a gain or a loss. Lower risk is not a guarantee.', 24, MUTED)}
</div>
</div>''' + foot('Proxy: US industry returns, in pesos, after fee and costs; lower-risk fund modelled as US T-bills in pesos · investor outcomes are reported separately from fund performance · the glidepath is a proposed platform feature, not an existing BPI App function'),
f"Fund performance and investor outcomes are different things, so we measure them separately. Take someone paying a thousand pesos a month for five years, starting in every month since 1990. In the median case they ended with about {d0['median']:.2f} times what they paid in. But {pc(d0['below1'], 0)} of those five-year savers ended below what they paid, and the worst ended at {d0['worst']:.2f} times. That is why we propose the account-level glidepath. It does not change the fund; it moves part of one investor's units into a lower-risk fund as their date approaches. In the same history it lifts the worst outcome from {d0['worst']:.2f} to {dg['worst']:.2f} times, at the cost of some upside. The schedule shown is illustrative, and lower risk is not a guarantee.")

# ---------------- 22 shelf ----------------
S['shelf'] = sec('shelf', head('Against what a young Filipino can buy today', 'Compare the structure, not a simulated return') + f'''
{table([['BPI Global Equity Fund-of-Funds', 'Buys 11 other funds; 1.50% plus their fees', '₱1,000', '7.15% (live)'], ['BPI Philippine Equity Index Fund', 'Passive, 32 PSEi names, 1.50%', '₱1,000', '0.52% (live)'],
        ['Pag-IBIG MP2', 'Government savings, tax-free', '₱500', '7.1% (live)'], ['<b>Firsts Fund (proposed)</b>', f'<b>{n} direct holdings, 14 markets, one 1.50% fee layer</b>', '<b>₱100</b>', 'Not yet live']],
       [30, 38, 12, 20], ['Product', 'Structure', 'Minimum', '5 years, a year'], size=26, align=['left', 'left', 'right', 'right'])}
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">
{card(p('<b>Where we win:</b> one fee layer instead of two, holdings you can name, a minimum a first-jobber can meet.', 24))}
{card(p('<b>Where MP2 wins:</b> goals under five years away. Our suitability step sends those savers to a lower-risk product.', 24))}
{card(p(f'<b>What we don\'t claim:</b> a live return. Ours is history with hindsight ({pc(v4["cagr"])}); the 36-year industry proxy (context only) made {pc(ps["cap"]["cagr"])}.', 24))}
</div>''' + foot('Comparison funds: BPI Wealth and Pag-IBIG disclosure statements, as in our Phase 1 fact sheet · Firsts Fund is a proposal; benchmark and live performance to follow'),
"Against what a young Filipino can actually buy, do not lead with our return: ours is history with hindsight, theirs are live. Lead with structure. BPI's global product buys other funds and charges two fee layers. The local index fund holds one economy. We would hold named companies directly for one fee, from a hundred pesos. Then say where we lose: for a goal under five years away, MP2 or a money-market fund is the better product, and our suitability step says so.")

# ---------------- 23 risks ----------------
S['risks'] = sec('risks', head('Key risks we state first', 'What can go wrong, and what we do about it') + f'''
{table([['Equity losses', f'In the 36-year proxy, the worst 12 months lost {pc(-ps["cap"]["worst12"], 0)} and the worst fall was {pc(-ps["cap"]["maxdd"], 0)}. No protection is promised; plan on losses in bad years.'],
        ['Hindsight', f'The five-year {pc(v4["cagr"])} uses today\'s selections. The calculator uses balanced assumptions, not this number.'],
        ['Concentration', f'Networks at the 25% limit; data-centre build-out {pc(bt["Semiconductors"] + bt["Grid & power equipment"])}; Saudi Arabia {pc(cnt.get("SA", 0))}; Chinese state telecoms {pc(W["CHMOB"]["weight"] + W["CHTEL"]["weight"])}. All reported.'],
        ['Currency', f'About {pc(1 - ph - 0.03, 0)} is in non-peso assets, unhedged. Peso strength lowers peso returns.'],
        ['Liquidity &amp; costs', f'{len(cnt)} markets: trading costs modelled at {pc(cost["trading_pa"], 2)} a year, withholding about {pc(cost["wht_pa"], 2)}; small listings capped by volume.'],
        ['Data &amp; judgment', 'One ratio vendor; sub-industries assigned by the team; stress shocks are our estimates. All rules published and re-run quarterly.']],
       [22, 78], ['Risk', 'What we do, and what remains'], size=25, align=['left', 'left'])}
''' + foot('Risk figures: industry proxy 1990–2026 and current portfolio · withholding rates approximate, to be confirmed by tax counsel'),
"Say the risks before the judges ask. This is an equity fund and it will have bad years: in our long proxy the worst twelve months lost twenty-seven percent. The five-year record has hindsight in it, so our calculator does not use it. We report our concentrations: networks at their limit, about eleven percent on data-centre spending, Saudi Arabia, and two Chinese state telecoms. Most of the fund is in foreign currencies, unhedged, so a stronger peso lowers returns. Fourteen markets cost money to trade, and we now model that. And our data has limits: one ratio vendor, our own sub-industry calls, and stress shocks we chose. The defence is that every rule is written down and re-run each quarter.")

# ---------------- 24 qa ----------------
qa = [('Why so many telecoms?', 'Eight passed merit and diversification tests; the 25% type limit caps the group, so each gets less than its risk share.'),
      ('Why only 1–2% in chips?', f'They swing 42–63% a year. Equal weighting would have earned more since 2021 and fallen further; we chose the method before testing.'),
      (f'Isn\'t {pc(v4["cagr"])} too good to be true?', f'Yes, as a forecast. It is today\'s portfolio looking back. The 36-year proxy made {pc(ps["cap"]["cagr"])}, about the market.'),
      ('What if a company\'s debt or cash flow turns?', 'Quarterly review re-runs M and V on current data; a failure moves it to the watchlist or out. Every exit is logged.'),
      ('Why hospitals now?', 'Healthcare infrastructure is hard-to-replace capacity; leaving it out was a gap in our theme. They passed the same tests.'),
      ('Why should a Filipino own Saudi or Mexican stocks?', 'Their salary and savings already ride on one economy. A global fund spreads that, and they still invest in pesos.')]
S['qa'] = sec('qa', head('Q&amp;A preparation', 'Six questions we expect, with our answers') + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">' +
    ''.join(card(h3(q) + p(a, 24), pad='18px 26px') for q, a in qa) + '</div>' + foot('Every company, ratio and decision: supporting proposal · rules re-checked at all ' + str(R['rebalances']) + ' quarterly rebalances'),
    "Six questions we should all answer the same way. Assign each to a teammate. The rule for Q&amp;A: give the number, then the reason, then stop. If we do not know, say what we would check and how.", gap=22)

# ---------------- 25 close ----------------
S['close'] = sec('close', f'''<div style="position:absolute;left:0;top:0;width:24px;height:1080px;background:{GREEN}"></div>
<p style="{MONO};font-size:24px;letter-spacing:3px;text-transform:uppercase;color:#5FC48C">Firsts Fund · in three sentences</p>
<div style="display:flex;flex-direction:column;gap:28px">
<p style="font-size:40px;line-height:1.35;color:#F5F4EE"><b>What it owns:</b> essential, hard-to-replace capacity anywhere in the world, but only where the price and the balance sheet hold up.</p>
<p style="font-size:40px;line-height:1.35;color:#F5F4EE"><b>How it chooses:</b> M for eligibility, V for the investment case, P for a weight and a holdings count that come out of the process.</p>
<p style="font-size:40px;line-height:1.35;color:#F5F4EE"><b>What it offers:</b> not the highest return, but a path a young Filipino can stay on, five years and longer.</p>
</div>
<div style="display:flex;justify-content:space-between;align-items:end">
<h2 style="{SERIF};font-size:72px;font-weight:600;font-style:italic;line-height:1.1;color:#5FC48C">“Fund your firsts.”</h2>
<p style="{MONO};font-size:24px;color:#C9D6CE;text-align:right">A proposal by Team Los Angeles 76ers<br>Not an existing BPI product</p>
</div>''', "Close in three sentences, then stop. What it owns: essential capacity, anywhere, but only where the price and the balance sheet hold up. How it chooses: three tests in order, ending in a weight and a holdings count that nobody set by hand. What it offers: not the highest return, a path a young Filipino can stay on, five years and longer, until the first home, the first business or the first trip. Fund your firsts. Thank you.",
pad='128px', bg=DARK, color='#C9D6CE').replace('gap:28px">', 'justify-content:space-between">', 1)

ORDER = ['cover', 'saver', 'theme', 'mvp', 'map', 'verify', 'funnel', 'position', 'grid', 'ex1', 'ex2', 'role', 'ph', 'weighting', 'sim5', 'oldnew', 'vstech', 'vsmkt',
         'long36', 'crises', 'investor', 'shelf', 'risks', 'qa', 'close']
for k in ORDER: open(f'{SL}/{k}.html', 'w').write(S[k])
for old in ['why1', 'why2', 'why3']:
    if os.path.exists(f'{SL}/{old}.html'): os.remove(f'{SL}/{old}.html')
d = json.load(open(f'{OUT}/deck.json'))
d['order'] = ORDER; d['title'] = 'Firsts Fund — Competition Pitch'
d['sections'] = {'s1': {'description': 'Who the fund is for and what it owns', 'start': 'cover'}, 's2': {'description': 'M.V.P.: how holdings are chosen', 'start': 'mvp'},
                 's3': {'description': 'The portfolio, two examples, and why each weight', 'start': 'grid'},
                 's4': {'description': 'Performance, labelled honestly, and how we defend each result', 'start': 'sim5'},
                 's5': {'description': 'Investor outcomes, risks, questions and close', 'start': 'investor'}}
json.dump(d, open(f'{OUT}/deck.json', 'w'))
print('wrote', len(ORDER), 'slides')
