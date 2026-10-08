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
 p('<b>Objective.</b> Long-term capital growth from fifteen companies, held directly, that own or supply long-lived physical '
   'and network capacity. One pooled fund with a single share price, making no promise about any individual investor\'s goal date.'), Spacer(1, 2),
 p('<b>The need.</b> A Filipino aged 18 to 25 has a peso salary and peso goals, both tied to one economy. BPI\'s own Philippine '
   'Equity Index Fund returned <b>0.52% a year</b> after fees, and the closest global product on the shelf buys other funds, '
   'charges a second fee layer and finished <b>4.19 points a year behind</b> the index it targets. What is missing is a '
   '<b>peso-priced global growth fund, holding shares directly, that someone with ₱100 can buy.</b>'), Spacer(1, 2),
 p(f'<b>No country quota.</b> An earlier draft fixed 30% in the Philippines. We removed it: nothing required it, and our own '
   f'thesis argues against concentrating in one economy. The only country rule left is that no country may exceed a third of '
   f'the fund. The risk model chose <b>{pct(R["by_country"]["PH"])} in Philippine companies on its own</b>, because PSE-listed '
   f'infrastructure moved differently from the rest of the portfolio.'), Spacer(1, 2),
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
         ('Recommended horizon', '5 years and above'), ('Currency', 'Philippine peso'), ('Holdings', '15 direct securities'),
         ('Management fee', '1.50% p.a.'), ('Liquid reserve', '10% (Rule 6.10)'), ('Single-issuer cap', '10% (Rule 6)'),
         ('Country cap', 'One third (33.3%)'), ('Weighting method', 'Equal risk contribution'),
         ('Benchmark', 'MSCI ACWI, in PHP'), ('Valuation', 'Daily, NAVPS')]
right = [bandrow('KEY FACTS', RW), kv(facts, [RW*0.45, RW*0.55]), Spacer(1, 3),
         p(f'<b>How holdings are sized.</b> Each holding is set to add the same share of portfolio risk, judged by how the fifteen '
           f'moved together over the previous three years. Nothing is sized on opinion. Today each contributes between '
           f'{rs[0]*100:.1f}% and {rs[-1]*100:.1f}% of total risk against a 6.7% target. The two below target are held back by a '
           f'rule: Iberdrola by the 10% issuer cap, Manila Water by its liquidity cap.', small)]
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
story.append(Table([[[calt, Spacer(1, 2), p(f'The Fund trailed the index by {gap1y:.2f} points over the last twelve months and in '
                     f'both partial years shown, and led in all four full years, 2022 to 2025. A portfolio that moves less than the '
                     f'market lags a rising one; the same property gave the shallower fall in 2022.', tiny)], '',
                     [riskt, Spacer(1, 2), p(f'Risk-free rate: BSP policy rate, averaging {pct(F["rf_pa"])} a year over the period. '
                     f'<b>In pesos, for someone paying ₱1,000 a month:</b> the {pct(-F["maxdd"])} worst fall on a ₱5,000 balance is '
                     f'₱{R["peso"]["maxdd_on_5000"]:,.0f}, about three weeks of contributions; the worst twelve months, '
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
    'US-listed industries, so they move together more than fifteen companies in eight countries would.', small)]],
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
hold_rows = []
for q in pr:
    why = f'{q["vol"]*100:.0f}% vol, corr {q["avg_corr"]:.2f}'
    if any('issuer' in x for x in q['binding']): why += '; at 10% issuer cap'
    if any('liquidity' in x for x in q['binding']): why += f'; at liquidity cap'
    hold_rows.append((q['name'].replace('&', '&amp;'), q['role'], q['country'], q['milestone'].split(',')[0].split(' (')[0],
                      pct(q['weight']), pct(q['risk_share']), why))
tot_w = sum(q['weight'] for q in pr); tot_r = sum(q['risk_share'] for q in pr)
hold_rows.append(('Fifteen holdings', '', '', '', pct(tot_w), pct(tot_r), 'Liquid reserve 10.00%'))
hw = [CW*0.17, CW*0.07, CW*0.05, CW*0.11, CW*0.075, CW*0.075, CW*0.18]
holdt = kv(hold_rows, hw, head=['Holding', 'Role', 'Mkt', 'First served', 'Weight', '% of risk', 'Why this weight'],
           right_cols=(4, 5), boldrows=(hold_rows[-1],))
hold_note = p('<b>Reading the table.</b> Weight comes from the risk model, not from conviction. A holding that swings less, or moves '
    'less with the others, gets more money. Iberdrola swings 16% a year and barely tracks the rest, so it reached the 10% cap; '
    'Converge swings 42%, so it gets 4.2%. Every holding ends up adding about the same share of risk.', tiny)

rest_w = CW - sum(hw) - 8
geo = [(k, pct(v)) for k, v in R['by_country'].items()] + [('Liquid reserve', '10.00%')]
names_c = {'PH': 'Philippines', 'IN': 'India', 'ES': 'Spain', 'FR': 'France', 'MY': 'Malaysia', 'TW': 'Taiwan', 'DE': 'Germany', 'JP': 'Japan'}
geo = [(names_c.get(a, a), b_) for a, b_ in geo]
sec = [(k.replace('Communication Services', 'Comm. Services').replace('Information Technology', 'Info. Technology'), pct(v))
       for k, v in R['by_sector'].items()] + [('Liquid reserve', '10.00%')]
geot = kv(geo, [rest_w*0.62, rest_w*0.38], head=['Geographic, by listing', ''])
sect = kv(sec, [rest_w*0.62, rest_w*0.38], head=['Sector · GICS', ''])
story.append(Table([[[bandrow('HOLDINGS · WEIGHT, SHARE OF RISK AND WHY', sum(hw)), holdt, Spacer(1, 2), hold_note], '',
                     [bandrow('ALLOCATION', rest_w), geot, Spacer(1, 3), sect]]],
                   colWidths=[sum(hw), 8, rest_w], style=[('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                                         ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
story.append(Spacer(1, 4))

bw = CW*0.47
role = R['by_role']; grp = R['by_group']
rules = [('Owners', '≥ 45%', pct(role.get('Owner', 0))), ('Suppliers', '≤ 25%', pct(role.get('Supplier', 0))),
         ('Platforms', '≤ 20%', pct(role.get('Platform', 0))), ('Liquid reserve', '10%', '10.00%'),
         ('Single issuer', '≤ 10%', '10.00% Iberdrola'), ('Single group', '≤ 15%', f'{pct(grp["First Pacific / MPIC"])} First Pacific'),
         ('Single country', '≤ 33.3%', f'{pct(R["by_country"]["PH"])} Philippines'),
         ('Liquidity', '5 days at 20% of volume', '5.97% Manila Water')]
rulest = kv(rules, [bw*0.3, bw*0.33, bw*0.37], head=['Limit', 'Rule', 'Actual (largest)'], right_cols=(1, 2))
rules_block = [bandrow('THE RULES THE PORTFOLIO MUST OBEY · ALL MET AT ONCE', bw), rulest, Spacer(1, 2),
    p('Two holdings sit at a limit: Iberdrola at the issuer cap and Manila Water at its liquidity cap, which assumes a ₱1 billion '
      'launch size. Every other weight came out of the risk model. Groups are counted by controlling shareholder: Meralco and PLDT '
      '(First Pacific), ICTSI and Manila Water (Razon), NTPC and Power Grid (Government of India).', tiny), Spacer(1, 3),
    p(f'<b>Where the fund is still concentrated.</b> The fifteen behave like about {R["div_ratio_sq"]:.1f} independent bets. Two '
      f'shared forces carry {pct(R["top2_factor_share"],1)} of the risk: a global power-equipment and chip-building cycle '
      f'(Hitachi, Schneider, Siemens, TSMC) and the Philippine market. This is the largest risk we have not removed.', small)]

mvp = [bandrow('HOW WE PICKED THE FIFTEEN · THREE STEPS, IN ORDER', CW - bw - 8),
  p('<b><font color="#0F7A45">M</font> Map the milestone.</b> Each of five firsts maps to the capacity its cost depends on: '
    'housing to power, water and grid; transport to ports and roads; education to fibre, data centres and chips; travel to '
    'airports; a first business to all of these. The map produced 37 listed candidates.', small), Spacer(1, 2),
  p('<b><font color="#0F7A45">V</font> Verify the investment.</b> Four pass/fail tests, no scores. <b>Theme:</b> a published '
    'capacity target with a number and a date, cited for every holding. <b>Debt:</b> net debt at most 4.0× EBITDA (6.0× for '
    'GICS Utilities) and interest covered at least 2.5×. <b>Price:</b> EBITDA at least 4.5% of enterprise value (EV/EBITDA ≤ '
    '22.2×), the yield of the money market fund our sign-up screen offers instead. <b>Liquidity:</b> a full position must be '
    'sellable in five days at 20% of daily volume. 15 of 37 passed. Out: IHH and Apollo (serve no first), Century Pacific and DBS '
    '(no capacity role), Sea, Indus Towers and Airtel (no dated target), Sembcorp, ACEN, Aboitiz Power and Globe (debt), '
    'Vertiv and Grab (price). Full list of 37 in the holdings annex.', small), Spacer(1, 2),
  p('<b><font color="#0F7A45">P</font> Position the risk.</b> Only after V. Equal risk contribution on the previous three years '
    'of weekly peso returns, re-solved every quarter with only the data available then, inside the rules on the left.', small),
  Spacer(1, 2),
  p('<b>How to read the simulation.</b> We chose the fifteen in October 2026 and applied the rules to their past prices, so it '
    'tests the method, not our stock-picking in 2021. The earlier draft\'s look-ahead in the weights is gone and PSE dividends are '
    'now included. Hindsight in the selection and survivorship remain, and both flatter the result.', tiny)]
story.append(Table([[rules_block, '', mvp]], colWidths=[bw, 8, CW - bw - 8],
                   style=[('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
story.append(Spacer(1, 4))

comp = [('BPI Global Equity Fund-of-Funds', 'Buys 11 funds; 1.50% plus their fees', '₱1,000', '7.15%'),
        ('BPI Philippine Equity Index Fund', 'Passive, 32 PSEi names, 1.50%', '₱1,000', '0.52%'),
        ('Pag-IBIG MP2', 'Government savings, tax-free', '₱500', '7.1%'),
        ('The Firsts Fund', '15 direct holdings, 1.50% single layer, no country quota', '₱100', f'{pct(F["cagr"])} simulated')]
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
risks = [('Market and equity', f'90% equities, Aggressive. 10% reserve; sizing keeps each holding near a 6.7% share of risk. Reduced, '
          f'not removed: the same method fell 48% in 2008–09.'),
         ('Concentration and factor', f'Issuer ≤ 10%, group ≤ 15%, country ≤ 33.3%, role limits. Two shared forces still carry '
          f'{pct(R["top2_factor_share"],1)} of risk, so a slowdown in power-equipment spending or a Philippine sell-off hits several '
          f'holdings together.'),
         ('Currency, country and liquidity', f'About {100 - R["by_country"]["PH"]*100 - 10:.0f}% non-peso, unhedged on purpose: '
          f'salary and goals are already in pesos. Eight listing countries. Every position passes the five-day liquidity test.'),
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
    'authors\' reading, unreviewed by counsel or any regulator. Debt and price tests use S&amp;P Global Market Intelligence data via '
    'stockanalysis.com as of 7 October 2026; capacity targets are cited in the holdings annex. Prices: PSE Edge (PSE names, with cash '
    'dividends) and Yahoo Finance (total return), converted to pesos weekly. Reserve yield: BIS policy-rate series for the BSP. Long '
    'history: Kenneth French Data Library and BIS exchange rates. Benchmark: iShares MSCI ACWI ETF in pesos. Comparison funds: BPI '
    'and Pag-IBIG disclosure statements. GICS sectors assigned by the team.', tiny)]], colWidths=[CW])
disc2.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.5, DARK), ('LEFTPADDING', (0, 0), (-1, -1), 4), ('TOPPADDING', (0, 0), (-1, -1), 2)]))
story.append(disc2)
doc.build(story)
print('built')
