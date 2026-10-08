"""Builds the revised 2-page Fund Fact Sheet PDF from results.json and engine outputs."""
import json, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Table, TableStyle, Image,
                                Spacer, PageBreak, KeepInFrame)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DJ', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DJB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
import re
def P(s):   # glyphs outside Helvetica's encoding (peso, minus, ≤ ≥ →) come from DejaVu; body stays Helvetica (Arial metrics)
    return re.sub('([₱−≤≥→])', r'<font name="DJ">\1</font>', s)

R = json.load(open('results.json'))
import engine as E, inputs as I
NH = len(R['portfolio'])
CN = {'PH': 'Philippines', 'IN': 'India', 'ES': 'Spain', 'FR': 'France', 'MY': 'Malaysia', 'TW': 'Taiwan', 'DE': 'Germany',
      'JP': 'Japan', 'US': 'United States', 'HK': 'Hong Kong / China', 'CH': 'Switzerland', 'MX': 'Mexico', 'BR': 'Brazil',
      'IT': 'Italy', 'KR': 'South Korea', 'GB': 'United Kingdom', 'NL': 'Netherlands'}
NC = len(R['by_country'])
WORDS = {14: 'fourteen', 33: 'thirty-three', 15: 'fifteen', 8: 'eight'}
S = pd.read_pickle('sim.pkl'); net = S['net']; acwi = S['R'].loc[net.index, 'ACWI']
F, B = R['fund'], R['bench']
GREEN = colors.HexColor('#0F7A45'); DARK = colors.HexColor('#1E2622'); RULE = colors.HexColor('#C9D3CD')
SOFT = colors.HexColor('#EEF5F0'); AMBER = colors.HexColor('#FFF4E0'); MUTED = colors.HexColor('#58635C')

def pct(x, d=2, sign=False):
    s = f'{x*100:+.{d}f}%' if sign else f'{x*100:.{d}f}%'
    return s.replace('-', '−')

# ---------- chart ----------
w = (1 + net).cumprod()*100; b = (1 + acwi).cumprod()*100
w = pd.concat([pd.Series([100.0], index=[pd.Timestamp('2021-10-01')]), w])
b = pd.concat([pd.Series([100.0], index=[pd.Timestamp('2021-10-01')]), b])
fig, ax = plt.subplots(figsize=(7.6, 1.75), dpi=220)
ax.plot(b.index, b.values, color='#8A928D', lw=1.0, label=f'MSCI ACWI in PHP — ends {b.iloc[-1]:.1f}')
ax.plot(w.index, w.values, color='#0F7A45', lw=1.5, label=f'The Firsts Growth Fund (net of fees) — ends {w.iloc[-1]:.1f}')
ax.set_ylabel('NAV per unit (base 100)', fontsize=6); ax.tick_params(labelsize=6)
ax.grid(axis='y', color='#E3E8E5', lw=0.6); [ax.spines[s].set_visible(False) for s in ['top', 'right']]
ax.legend(fontsize=6, frameon=False, loc='upper left'); ax.set_xlim(w.index[0], w.index[-1])
fig.tight_layout(pad=0.3); fig.savefig('growth.png'); plt.close(fig)

# ---------- styles ----------
base = ParagraphStyle('b', fontName='Helvetica', fontSize=7.1, leading=8.9, textColor=DARK)
small = ParagraphStyle('s', parent=base, fontSize=6.3, leading=7.8)
tiny = ParagraphStyle('t', parent=base, fontSize=5.8, leading=7.0, textColor=MUTED)
bold = ParagraphStyle('bb', parent=base, fontName='Helvetica-Bold')
cell = ParagraphStyle('c', parent=base, fontSize=6.5, leading=7.8)
cellb = ParagraphStyle('cb', parent=cell, fontName='Helvetica-Bold')
cellr = ParagraphStyle('cr', parent=cell, alignment=TA_RIGHT)
cellrb = ParagraphStyle('crb', parent=cellr, fontName='Helvetica-Bold')
band = ParagraphStyle('band', parent=base, fontName='Helvetica-Bold', fontSize=7.4, textColor=colors.white)
def p(t, st=base): return Paragraph(P(t), st)
def bandrow(text, width):
    t = Table([[p(text, band)]], colWidths=[width]); t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), DARK),
        ('LEFTPADDING', (0, 0), (-1, -1), 4), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
    return t
def kv(rows, widths, head=None, right_cols=(1,), zebra=False, boldrows=()):
    data = []
    if head: data.append([p(h, cellrb if i in right_cols else cellb) for i, h in enumerate(head)])
    for r_ in rows:
        bold_ = r_ in boldrows
        data.append([p(str(c), (cellrb if bold_ else cellr) if i in right_cols else (cellb if bold_ or i == 0 else cell))
                     for i, c in enumerate(r_)])
    t = Table(data, colWidths=widths)
    st = [('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 2), ('RIGHTPADDING', (0, 0), (-1, -1), 2),
          ('TOPPADDING', (0, 0), (-1, -1), 0.8), ('BOTTOMPADDING', (0, 0), (-1, -1), 0.8),
          ('LINEBELOW', (0, 0), (-1, -1), 0.3, RULE)]
    if head: st.append(('BACKGROUND', (0, 0), (-1, 0), SOFT))
    t.setStyle(TableStyle(st)); return t

W, H = A4; M = 9*mm; CW = W - 2*M

def header(c, doc):
    c.saveState()
    c.setFillColor(GREEN); c.rect(M, H - M - 18, 14, 18, fill=1, stroke=0)
    c.setFillColor(DARK); c.setFont('Helvetica-Bold', 15); c.drawString(M + 20, H - M - 13, 'THE FIRSTS FUND')
    c.setFont('Helvetica-Bold', 7.3)
    sub = ('THE FIRSTS GROWTH FUND · FUND FACT SHEET · PESO-DENOMINATED GLOBAL CAPACITY FUND' if doc.page == 1
           else 'PORTFOLIO, PROCESS AND DISCLOSURES')
    c.drawString(M + 20, H - M - 23, sub)
    c.setFont('Helvetica', 6.5); c.setFillColor(MUTED)
    c.drawString(M + 20, H - M - 31, f'Hypothetical fund proposal · FinQuest 2026 · Data as of 2 October 2026 · Page {doc.page} of 2')
    c.setFillColor(GREEN); c.setFont('Helvetica-BoldOblique', 8)
    c.drawRightString(W - M, H - M - 10, '“There will always be'); c.drawRightString(W - M, H - M - 19, 'a new first.”')
    c.setStrokeColor(GREEN); c.setLineWidth(1.2); c.line(M, H - M - 36, W - M, H - M - 36)
    c.restoreState()

doc = BaseDocTemplate('LosAngeles76ers_TheFirstsFund_FactSheet_v2.pdf', pagesize=A4, leftMargin=M, rightMargin=M,
                      topMargin=M + 40, bottomMargin=M, title='The Firsts Fund — Fund Fact Sheet',
                      author='Team Los Angeles 76ers, Ateneo de Manila University')
frame = Frame(M, M, CW, H - 2*M - 40, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id='p', frames=[frame], onPage=header)])

story = []
# ================= PAGE 1 =================
LW, RW = CW*0.60, CW*0.38; GAP = CW - LW - RW
pr = R['portfolio']; rs = sorted(p_['risk_share'] for p_ in pr)
st, gl = R['shuffle'], R['stress']
left = [
 bandrow('INVESTMENT OBJECTIVE AND THE NEED IT ADDRESSES', LW), Spacer(1, 2),
 p('<b>Theme: global real capacity.</b> The power, water, grids, ports, airports, fibre and data centres that the cost of '
   'a young Filipino\'s firsts runs on, and the equipment makers that build them. A global theme rather than a bet on one '
   'country, and deliberately not a technology fund.'), Spacer(1, 2),
 p(f'<b>Objective.</b> Long-term capital growth from {WORDS[NH]} companies, held directly, that own or supply long-lived physical '
   'and network capacity. One pooled fund with a single share price, making no promise about any individual investor\'s goal date.'), Spacer(1, 2),
 p('<b>The need.</b> A Filipino aged 18 to 25 has a peso salary and peso goals, both tied to one economy. BPI\'s own Philippine '
   'Equity Index Fund returned <b>0.52% a year</b> after fees, and the closest global product on the shelf buys other funds, '
   'charges a second fee layer and finished <b>4.19 points a year behind</b> the index it targets. What is missing is a '
   '<b>peso-priced global growth fund, holding shares directly, that someone with ₱100 can buy.</b>'), Spacer(1, 2),
 p(f'<b>No home quota, in the rules or the sourcing.</b> An earlier draft fixed 30% in the Philippines. Removing the quota was '
   f'not enough: we had also sourced candidates mostly from home, so 31% still landed there. Map now gives every region the same '
   f'slots: the two largest verified companies per capacity type in Asia-Pacific (Philippines included), Europe and the '
   f'Americas. The Philippines holds <b>{pct(R["by_country"]["PH"])}</b> (ICTSI, Manila Water), above its {2/NH*100:.0f}% share of '
   f'slots because PSE stocks barely move with the rest. A one-third country cap remains as a backstop.'), Spacer(1, 2),
 p(f'<b>Why the risk level is what it is.</b> A young investor puts money in every month. We shuffled the Fund\'s 60 monthly '
   f'returns 20,000 times, which changes the path but never the total. A weak first half made the monthly contributor '
   f'<b>richer</b> and the person drawing down <b>poorer</b> (correlations of {st["corr_contrib"]:.2f} and +{st["corr_withdraw"]:.2f}'
   f'), because someone paying in buys more units while prices are low. In all 20,000 orderings, ₱1,000 a month in the Fund '
   f'beat the same money in a 4.5% money market fund (₱{st["mmf"]:,.0f}).'.replace('-0.', '−0.')),
]
callout = Table([[p(f'<b>How a dated goal gets funded.</b> The Fund is half the journey. The other half is an <b>account-level '
   f'glidepath</b>: from 24 months out, monthly transfers move the balance into a money market fund, leaving 15% here on the date. '
   f'We put the worst 12 months in 36 years (Mar 2008 to Feb 2009, {pct(gl["crash_total"],1)}) into the final year of every shuffled '
   f'path. The glidepath won in {gl["glide_wins"]*100:.0f}% of them and lifted the worst outcome from ₱{gl["worst_no"]:,.0f} to '
   f'₱{gl["worst_glide"]:,.0f}. In normal markets it costs about ₱{R["glide"]["median_cost"]:,.0f} at the median. '
   f'Goals under five years are declined at sign-up, with a reason.', small)]], colWidths=[LW])
callout.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), AMBER), ('LINEBEFORE', (0, 0), (0, -1), 2, colors.HexColor('#E3A33B')),
                             ('LEFTPADDING', (0, 0), (-1, -1), 5), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
left += [Spacer(1, 3), callout]

facts = [('Theme', 'Global real capacity'), ('Fund structure', 'Single pooled fund, unitized'), ('Classification', 'Aggressive'),
         ('Minimum initial', '₱100'), ('Contribution rails', 'Payday · Sukli · top-up'), ('Minimum recurring', '₱100 / month'),
         ('Recommended horizon', '5 years and above'), ('Currency', 'Philippine peso'), ('Holdings', f'{NH} direct securities'),
         ('Management fee', '1.50% p.a.'), ('Liquid reserve', '10% (Rule 6.10)'), ('Single-issuer cap', '10% (Rule 6)'),
         ('Country cap', 'One third (33.3%)'), ('Weighting method', 'Equal risk contribution'),
         ('Benchmark', 'MSCI ACWI, in PHP'), ('Valuation', 'Daily, NAVPS')]
right = [bandrow('KEY FACTS', RW), kv(facts, [RW*0.45, RW*0.55]), Spacer(1, 3),
         p(f'<b>How holdings are sized.</b> Each holding is set to add the same share of portfolio risk, judged by how the {WORDS[NH]} '
           f'moved together over the previous three years. Nothing is sized on opinion. Today each contributes between '
           f'{rs[0]*100:.1f}% and {rs[-1]*100:.1f}% of total risk against a {100/NH:.1f}% target. The one below target is held back '
           f'by a rule: Manila Water, by its liquidity cap.', small)]
story.append(Table([[left, '', right]], colWidths=[LW, GAP, RW],
                   style=[('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
story.append(Spacer(1, 4))

# KPI tiles
story.append(bandrow('PERFORMANCE · SIMULATED, AFTER THE 1.50% FEE · 1 OCT 2021 TO 2 OCT 2026 · WEIGHTS USE ONLY DATA AVAILABLE AT EACH QUARTER', CW))
big = ParagraphStyle('big', parent=base, fontName='Helvetica-Bold', fontSize=12, leading=14, textColor=GREEN, alignment=TA_CENTER)
lab = ParagraphStyle('lab', parent=tiny, alignment=TA_CENTER)
tiles = [(pct(F['vol']), f'Volatility p.a.<br/>vs {pct(B["vol"])} index'), (f'{R["beta"]:.2f}', 'Beta<br/>to MSCI ACWI'),
         (pct(F['maxdd']), f'Maximum drawdown<br/>₱{R["peso"]["maxdd_on_5000"]:,.0f} on ₱5,000'),
         (f'{F["sharpe"]:.2f}', f'Sharpe ratio<br/>vs {B["sharpe"]:.2f} index'),
         (pct(F['cagr']), f'Return p.a., net<br/>vs {pct(B["cagr"])} index')]
tw = CW/5
tt = Table([[[p(a, big), p(bb, lab)] for a, bb in tiles]], colWidths=[tw]*5)
tt.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.4, RULE), ('INNERGRID', (0, 0), (-1, -1), 0.4, RULE),
                        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
story += [Spacer(1, 2), tt, Spacer(1, 2),
          p('Risk comes before return on purpose: the return figure is the least reliable number on this page. Over 36 years the '
            'same method fell 48% and moved 0.88 as much as the market; see the long-history panel below.', tiny), Spacer(1, 2)]

cal = R['calendar']; tr = R['trailing']
calrows = [('2021 (from 1 Oct)', pct(cal['2021'][0], sign=True), pct(cal['2021'][1], sign=True))]
calrows += [(y, pct(cal[y][0], sign=True), pct(cal[y][1], sign=True)) for y in ['2022', '2023', '2024', '2025']]
calrows += [('2026 (to 2 Oct)', pct(cal['2026'][0], sign=True), pct(cal['2026'][1], sign=True)),
            ('Last 12 months', pct(tr['1y'][0], sign=True), pct(tr['1y'][1], sign=True)),
            ('3 years p.a.', pct(tr['3y'][0], sign=True), pct(tr['3y'][1], sign=True)),
            ('Since 1 Oct 2021 p.a.', pct(F['cagr'], sign=True), pct(B['cagr'], sign=True))]
gap1y = round(tr['1y'][1]*100, 2) - round(tr['1y'][0]*100, 2)
lead = [y for y in ['2022', '2023', '2024', '2025'] if cal[y][0] > cal[y][1]]
lag = [y for y in ['2022', '2023', '2024', '2025'] if cal[y][0] <= cal[y][1]]
cw1 = CW*0.43
calt = kv(calrows, [cw1*0.46, cw1*0.27, cw1*0.27], head=['Period', 'Fund', 'MSCI ACWI (PHP)'], right_cols=(1, 2),
          boldrows=tuple(calrows[-3:]))
risk = [('Volatility p.a.', pct(F['vol']), pct(B['vol'])), ('Downside deviation', pct(F['downdev']), pct(B['downdev'])),
        ('Sharpe ratio', f'{F["sharpe"]:.2f}', f'{B["sharpe"]:.2f}'), ('Sortino ratio', f'{F["sortino"]:.2f}', f'{B["sortino"]:.2f}'),
        ('Maximum drawdown', pct(F['maxdd']), pct(B['maxdd'])), ('Worst rolling 12 months', pct(F['worst12']), pct(B['worst12'])),
        ('Best rolling 12 months', pct(F['best12'], sign=True), pct(B['best12'], sign=True)),
        ('12-month periods positive', f'{F["pos12"]*100:.0f}%', f'{B["pos12"]*100:.0f}%'),
        ('Beta / correlation', f'{R["beta"]:.2f} / {R["corr"]:.2f}', '1.00 / 1.00'),
        ('Excess return over index, geometric', pct((1 + F['cagr'])/(1 + B['cagr']) - 1, sign=True), '—')]
cw2 = CW - cw1 - 8
riskt = kv(risk, [cw2*0.56, cw2*0.22, cw2*0.22], head=['Risk statistic', 'Fund', 'Index'], right_cols=(1, 2))
story.append(Table([[[calt, Spacer(1, 2), p(f'The Fund led the index in {", ".join(lead)} and trailed it in {", ".join(lag)}, and by {gap1y:.2f} points over the '
                     f'last twelve months, when chip and AI shares drove the index. A portfolio that moves less than the market lags a '
                     f'fast-rising one; the same property gave a {pct(cal["2022"][0], sign=True)} year in 2022 against {pct(cal["2022"][1], sign=True)}.', tiny)], '',
                     [riskt, Spacer(1, 2), p(f'Risk-free rate: BSP policy rate, averaging {pct(F["rf_pa"])} a year over the period. '
                     f'<b>In pesos, for someone paying ₱1,000 a month:</b> the {pct(-F["maxdd"])} worst fall on a ₱5,000 balance is '
                     f'₱{R["peso"]["maxdd_on_5000"]:,.0f}, about {R["peso"]["maxdd_on_5000"]/(12000/52):.0f} weeks of contributions; the worst twelve months, '
                     f'{pct(-F["worst12"])}, is ₱{R["peso"]["worst12_on_5000"]:,.0f}.', tiny)]]],
                   colWidths=[cw1, 8, cw2], style=[('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                                    ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
story.append(Spacer(1, 3))
story.append(bandrow('GROWTH OF ONE UNIT · SIMULATED, STARTING AT 100 ON 1 OCTOBER 2021', CW))
story.append(Image('growth.png', width=CW, height=CW*1.75/7.6))

# long-history panel
lh = [('Return a year', '11.2%', '11.7%'), ('Largest fall', '−48.1% (2007–09)', '−43.9%'), ('Months to recover', '72', '72'),
      ('Beta to US market', '0.88', '0.92'), ('Dot-com fall, 2000–02', '−26.2%', '−37.2%')]
lht = kv(lh, [CW*0.17, CW*0.14, CW*0.12], head=['1990–2026, in PHP', 'This method', 'Market fund'], right_cols=(1, 2))
story.append(Spacer(1, 3))
story.append(bandrow('THE SAME METHOD OVER 36 YEARS · US INDUSTRY PROXIES, SAME RULES AND FEE · JAN 1990 TO AUG 2026', CW))
story.append(Table([[lht, '', p('The five years above were calm for this Fund. Rebuilt from industry returns with the same rules, '
    'reserve and fee, the method matched a market fund with the same costs over 36 years and fell almost as far in 2008. '
    'Its edge was the dot-com crash. <b>Plan for a fall of up to half.</b> In the 1997–98 crisis, when the peso went from ₱26.4 '
    'to ₱39.1 per dollar, the same global holdings gained 87% in pesos: the reason the Fund is left unhedged. Proxies are '
    f'US-listed industries, so they move together more than {WORDS[NH]} companies in {WORDS[NC]} countries would.', small)]],
    colWidths=[CW*0.43, 8, CW*0.57 - 8], style=[('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                              ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 2)]))
story.append(Spacer(1, 3))
disc = Table([[p('<b>IMPORTANT.</b> All figures are simulated and prepared with hindsight; simulated performance does not represent '
    'actual trading and cannot account for real dealing costs, taxes, liquidity or a manager\'s decisions under live conditions. '
    'Past simulated performance is not a guarantee of future results. The value of an investment can fall as well as rise, and '
    'an investor may get back less than the amount invested. Not an offer, solicitation or investment advice, and not a BPI Wealth '
    'product; no fund described here exists.', tiny)]], colWidths=[CW])
disc.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.5, DARK), ('LEFTPADDING', (0, 0), (-1, -1), 4), ('TOPPADDING', (0, 0), (-1, -1), 2)]))
story += [disc, PageBreak()]

# ================= PAGE 2 =================
SHORT = {'Grupo Aeroportuario del Pacifico': 'GAP (Pacífico)', 'Grupo Aeroportuario del Sureste': 'ASUR (Sureste)',
         'Adani Ports & SEZ': 'Adani Ports', 'American Water Works': 'American Water', 'Samsung Electronics': 'Samsung',
         'Deutsche Telekom': 'Deutsche Telekom', 'Mitsubishi Electric': 'Mitsubishi Electric', 'Schneider Electric': 'Schneider'}
REG = ['Asia-Pacific', 'Europe', 'Americas']
TYPES = ['Power generation & grid', 'Water', 'Telecom & digital infrastructure', 'Ports', 'Airports & toll roads',
         'Power & grid equipment', 'Semiconductors']
FIRST = {'Power generation & grid': 'Housing, business', 'Water': 'Housing', 'Telecom & digital infrastructure': 'Education, business',
         'Ports': 'Transport, business', 'Airports & toll roads': 'Travel, transport', 'Power & grid equipment': 'Housing, business',
         'Semiconductors': 'Education, business'}
EMPTY = {('Ports', 'Europe'): 'None passed: HHLA fails debt and liquidity', ('Ports', 'Americas'): 'No listed operator of size',
         ('Power & grid equipment', 'Americas'): 'None passed: GE Vernova, Eaton, Quanta, Vertiv all priced above 22×',
         ('Water', 'Europe'): None, ('Water', 'Asia-Pacific'): None, ('Semiconductors', 'Americas'): None}
cellname = ParagraphStyle('cn', parent=cell, fontSize=6.3, leading=7.6)
cellmute = ParagraphStyle('cm', parent=cellname, textColor=MUTED, fontName='Helvetica-Oblique')
by = {}
for q in pr:
    inf = E.INFO[q['key']]; by.setdefault((inf['ctype'], inf['region']), []).append(q)
grid = [[p('Capacity type · first served', cellb)] + [p(f'{r_} · {pct(sum(q["weight"] for q in pr if E.INFO[q["key"]]["region"] == r_))}', cellb) for r_ in REG]
        + [p('Row', cellrb)]]
for t in TYPES:
    row = [p(f'<b>{t}</b><br/><font color="#58635C">{FIRST[t]} · {"Owner" if t not in ("Power & grid equipment", "Semiconductors") else "Supplier"}</font>', cellname)]
    for r_ in REG:
        qs = sorted(by.get((t, r_), []), key=lambda q: -q['weight'])
        lines = [f'{SHORT.get(q["name"], q["name"]).replace("&", "&amp;")} <font color="#58635C">{q["country"]}</font> <b>{pct(q["weight"])}</b>' for q in qs]
        if len(qs) < 2:
            note = EMPTY.get((t, r_))
            if note: lines.append(f'<font color="#58635C"><i>{note}</i></font>')
            elif len(qs) == 1: lines.append('<font color="#58635C"><i>Only one passed every test</i></font>')
        row.append(p('<br/>'.join(lines), cellname))
    row.append(p(pct(sum(q['weight'] for qs in [by.get((t, r_), []) for r_ in REG] for q in qs)), cellr))
    grid.append(row)
gw = [CW*0.155, CW*0.17, CW*0.17, CW*0.17, CW*0.06]
gridt = Table(grid, colWidths=gw)
gridt.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 2), ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ('TOPPADDING', (0, 0), (-1, -1), 1.2), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.2), ('LINEBELOW', (0, 0), (-1, -1), 0.3, RULE),
    ('BACKGROUND', (0, 0), (-1, 0), SOFT), ('LINEBEFORE', (1, 0), (3, -1), 0.3, RULE)]))
nbench = sum(1 for c in I.CANDIDATES if c[12].startswith('BENCH')); ncand = len(I.CANDIDATES)
grid_note = p(f'<b>Reading the grid.</b> Map decides <i>who</i> is held: in each cell, the two largest companies by US-dollar market '
    f'value that pass all four Verify tests. The risk model decides <i>how much</i>: a holding that swings less, or moves less with '
    f'the rest, gets more money, so each adds {rs[0]*100:.1f}–{rs[-1]*100:.1f}% of the risk. Swisscom swings {[q for q in pr if q["key"]=="SCMN"][0]["vol"]*100:.0f}% '
    f'a year and gets {pct([q for q in pr if q["key"]=="SCMN"][0]["weight"])}; Micron swings {[q for q in pr if q["key"]=="MU"][0]["vol"]*100:.0f}% and gets '
    f'{pct([q for q in pr if q["key"]=="MU"][0]["weight"])}. Another {nbench} companies passed the money tests but ranked third or lower in their cell.', tiny)
rest_w = CW - sum(gw) - 8
geo = [(CN.get(k, k), pct(v)) for k, v in R['by_country'].items()] + [('Liquid reserve', '10.00%')]
sec = [(k.replace('Communication Services', 'Comm. Services').replace('Information Technology', 'Info. Technology'), pct(v))
       for k, v in R['by_sector'].items()]
geot = kv(geo, [rest_w*0.66, rest_w*0.34], head=['By listing', ''])
sect = kv(sec, [rest_w*0.66, rest_w*0.34], head=['Sector · GICS', ''])
story.append(Table([[[bandrow(f'HOLDINGS · THE MAP GRID · {NH} COMPANIES, WEIGHT OF FUND', sum(gw)), gridt, Spacer(1, 2), grid_note], '',
                     [bandrow('ALLOCATION', rest_w), geot, Spacer(1, 3), sect]]],
                   colWidths=[sum(gw), 8, rest_w], style=[('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                                         ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
story.append(Spacer(1, 4))

bw = CW*0.47
role = R['by_role']; grp = R['by_group']
topw = pr[0]; topc = max(R['by_country'].items(), key=lambda x: x[1])
gnames = {g: v for g, v in grp.items() if g in set(E.GROUP.values())}; topg = max(gnames.items(), key=lambda x: x[1])
mwc = [q for q in pr if q['key'] == 'MWC'][0]
rules = [('Owners', '≥ 45%', pct(role.get('Owner', 0))), ('Suppliers', '≤ 25%', pct(role.get('Supplier', 0))),
         ('Platforms', '≤ 20%', pct(role.get('Platform', 0))), ('Liquid reserve', '10%', '10.00%'),
         ('Single issuer', '≤ 10%', f'{pct(topw["weight"])} {topw["name"]}'), ('Single group', '≤ 15%', f'{pct(topg[1])} {topg[0]}'),
         ('Single country', '≤ 33.3%', f'{pct(topc[1])} {CN[topc[0]]}'),
         ('Liquidity', '5 days at 20% of volume', f'{pct(mwc["weight"])} Manila Water')]
rulest = kv(rules, [bw*0.3, bw*0.33, bw*0.37], head=['Limit', 'Rule', 'Actual (largest)'], right_cols=(1, 2))
rules_block = [bandrow('THE RULES THE PORTFOLIO MUST OBEY · ALL MET AT ONCE', bw), rulest, Spacer(1, 2),
    p('One holding sits at a limit: Manila Water at its liquidity cap, which assumes a ₱1 billion launch size. Every other weight '
      'came out of the risk model, and every rule held at all 21 quarterly rebalances. Groups are counted by controlling shareholder: '
      'ICTSI and Manila Water (Razon), Adani Ports and Adani Power (Adani), NTPC (Government of India).', tiny), Spacer(1, 3),
    p(f'<b>Where the fund is still concentrated.</b> The {WORDS[NH]} behave like about {R["div_ratio_sq"]:.1f} independent bets. Two '
      f'shared forces carry {pct(R["top2_factor_share"],1)} of the risk: the global chip and AI-power cycle (Micron, Infineon, '
      f'STMicroelectronics, Samsung, Constellation Energy) and Indian infrastructure (Adani Power, Adani Ports, NTPC). This is the '
      f'largest risk we have not removed.', small)]

mvp = [bandrow(f'HOW WE PICKED THE {NH} · THREE STEPS, IN ORDER', CW - bw - 8),
  p(f'<b><font color="#0F7A45">M</font> Map the milestone.</b> Five firsts map to seven kinds of capacity: housing to power, water '
    f'and grid equipment; transport to ports and roads; education to fibre, data centres and chips; travel to airports; a first '
    f'business to all of these. Each type is sourced in three regions on equal terms (Asia-Pacific with the Philippines, Europe, '
    f'the Americas), ranked by market value: {ncand} listed candidates. Health is not a first, so hospitals are out.', small), Spacer(1, 2),
  p('<b><font color="#0F7A45">V</font> Verify the investment.</b> Four pass/fail tests, no scores. <b>Theme:</b> a published '
    'capacity target with a number and a date, cited for every holding. <b>Debt:</b> net debt at most 4.0× EBITDA (6.0× for '
    'GICS Utilities) and interest covered at least 2.5×. <b>Price:</b> EBITDA at least 4.5% of enterprise value (EV/EBITDA ≤ '
    '22.2×), the yield of the money market fund our sign-up screen offers instead. <b>Liquidity:</b> a full position must be '
    'sellable in five days at 20% of daily volume. Out, for example: NextEra, National Grid, Vodafone (debt); NVIDIA, ASML, '
    'GE Vernova, ABB (price); Guangdong Investment and Orange (no dated target). Every candidate and reason is in the annex.', small), Spacer(1, 2),
  p('<b><font color="#0F7A45">P</font> Position the risk.</b> Only after V. Equal risk contribution on the previous three years '
    'of weekly peso returns, re-solved every quarter with only the data available then, inside the rules on the left.', small),
  Spacer(1, 2),
  p(f'<b>How to read the simulation.</b> We chose the {WORDS[NH]} in October 2026, ranking by today\'s market values, and applied '
    'the rules to their past prices. That tests the method, not stock-picking in 2021, and it flatters the result: ranking by '
    'today\'s size favours companies that grew fastest, such as the memory-chip makers. Plan on the 36-year figures.', tiny)]
story.append(Table([[rules_block, '', mvp]], colWidths=[bw, 8, CW - bw - 8],
                   style=[('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
story.append(Spacer(1, 4))

comp = [('BPI Global Equity Fund-of-Funds', 'Buys 11 funds; 1.50% plus their fees', '₱1,000', '7.15%'),
        ('BPI Philippine Equity Index Fund', 'Passive, 32 PSEi names, 1.50%', '₱1,000', '0.52%'),
        ('Pag-IBIG MP2', 'Government savings, tax-free', '₱500', '7.1%'),
        ('The Firsts Fund', f'{NH} direct holdings in {NC} markets, 1.50% single layer, no country quota', '₱100', f'{pct(F["cagr"])} simulated')]
cmpw = CW*0.47
compt = kv(comp, [cmpw*0.33, cmpw*0.39, cmpw*0.12, cmpw*0.16], head=['Fund', 'Structure', 'Min.', '5-yr p.a.'], right_cols=(2, 3),
           boldrows=(comp[-1],))
cmp_block = [bandrow('HOW THIS FUND COMPARES', cmpw), compt, Spacer(1, 2),
    p('Compare the structures, not the returns: ours is simulated and theirs are live. What holds without our return: the closest '
      'product targets the same world index, finished 4.19 points a year behind it, and charges a second fee layer. Where MP2 beats '
      'us, we say so: for a goal three to five years away it is the better product, and our sign-up screen sends people there.', tiny),
    Spacer(1, 3), bandrow('CLIENT SUITABILITY', cmpw),
    p('For an investor with a goal five or more years away who can contribute regularly and keep going through a fall of up to '
      'half, as in 2008. Not for money needed within five years, an emergency fund, or someone who would stop after a bad year. For '
      'all three a money market fund is right, and our sign-up screen sends them there.', small),
    Spacer(1, 3), bandrow('THE TEAM', cmpw),
    p('Prince Angelo C. Rivera · Luis Tengonciang · Karol Josef Fuñe · Eric Fabian Thirdy Mendez. Team Los Angeles 76ers. All four '
      'study BS Applied Mathematics with a Master in Data Science at Ateneo de Manila University, and built the screens, weighting '
      'engine, constraint stack, shuffle test and simulations in Python.', small)]
risks = [('Market and equity', f'90% equities, Aggressive. 10% reserve; sizing keeps each holding near a {100/NH:.1f}% share of risk. '
          f'Reduced, not removed: the same method fell 48% in 2008–09.'),
         ('Concentration and factor', f'Issuer ≤ 10%, group ≤ 15%, country ≤ 33.3%, role limits. Two shared forces still carry '
          f'{pct(R["top2_factor_share"],1)} of risk, so a chip downturn or an Indian sell-off hits several holdings together.'),
         ('Currency, country and liquidity', f'About {100 - R["by_country"]["PH"]*100 - 10:.0f}% non-peso, unhedged on purpose: '
          f'salary and goals are already in pesos. {WORDS[NC].capitalize()} listing markets. Every position passes the five-day liquidity test. '
          f'China Mobile is on a US investment-restriction list; not binding on a Philippine fund, but to be cleared by compliance.'),
         ('Sequence risk near the goal date', f'Account glidepath from 24 months out. With a 2008-size crash in the final year, worst '
          f'outcome ₱{gl["worst_no"]:,.0f} → ₱{gl["worst_glide"]:,.0f}; typical cost ₱{R["glide"]["median_cost"]:,.0f}.')]
rkw = CW - cmpw - 8
riskt2 = kv(risks, [rkw*0.25, rkw*0.75], head=['Risk', 'How it is managed, and what remains'], right_cols=())
story.append(Table([[cmp_block, '', [bandrow('THE MAIN RISKS, AND WHAT WE DO ABOUT EACH', rkw), riskt2]]],
                   colWidths=[cmpw, 8, rkw], style=[('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                                   ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
story.append(Spacer(1, 4))
disc2 = Table([[p('<b>IMPORTANT.</b> All figures are simulated and prepared with hindsight. Not an offer or investment advice and not '
    'a BPI Wealth product. Full risk disclosures appear on page 1. References to Investment Company Act rules 6 and 6.10 are the '
    'authors\' reading, unreviewed by counsel or any regulator. Debt and price tests and market values use S&amp;P Global Market Intelligence data via '
    'stockanalysis.com as of 7 October 2026; capacity targets are cited in the holdings annex. Prices: PSE Edge (PSE names, with cash '
    'dividends) and Yahoo Finance (total return), converted to pesos weekly. Reserve yield: BIS policy-rate series for the BSP. Long '
    'history: Kenneth French Data Library and BIS exchange rates. Benchmark: iShares MSCI ACWI ETF in pesos. Comparison funds: BPI '
    'and Pag-IBIG disclosure statements. GICS sectors assigned by the team.', tiny)]], colWidths=[CW])
disc2.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.5, DARK), ('LEFTPADDING', (0, 0), (-1, -1), 4), ('TOPPADDING', (0, 0), (-1, -1), 2)]))
story.append(disc2)
doc.build(story)
print('built')
