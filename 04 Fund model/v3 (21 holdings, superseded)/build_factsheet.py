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
      'IT': 'Italy', 'KR': 'South Korea', 'GB': 'United Kingdom', 'NL': 'Netherlands', 'SA': 'Saudi Arabia', 'MY': 'Malaysia'}
NC = len(R['by_country'])
WORDS = {14: 'fourteen', 33: 'thirty-three', 15: 'fifteen', 8: 'eight', 21: 'twenty-one', 13: 'thirteen'}
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
ax.set_ylabel('NAV per unit (base 100, axis from 0)', fontsize=6); ax.tick_params(labelsize=6)
ax.grid(axis='y', color='#E3E8E5', lw=0.6); [ax.spines[s].set_visible(False) for s in ['top', 'right']]
ax.legend(fontsize=6, frameon=False, loc='upper left'); ax.set_xlim(w.index[0], w.index[-1]); ax.set_ylim(0, 50*int(max(w.max(), b.max())/50 + 1)); ax.set_yticks(range(0, 50*int(max(w.max(), b.max())/50 + 1) + 1, 50))
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
 p(f'<b>No country rule at all.</b> An earlier draft fixed 30% in the Philippines, then sourced candidates mostly from home. '
   f'Both put the answer in by assumption. Now one global list is ranked on merit, and countries are an output: the Philippines '
   f'holds <b>{pct(R["by_country"]["PH"])}</b> (ICTSI on quality of returns, Manila Water on price). Essential is not enough: '
   f'every holding must also be cheaper than its global peers or earn more on its capital.'), Spacer(1, 2),
 p(f'<b>Why the risk level is what it is.</b> A young investor puts money in every month. We shuffled the Fund\'s 60 monthly '
   f'returns 20,000 times, which changes the path but never the total. A weak first half made the monthly contributor '
   f'<b>richer</b> and the person drawing down <b>poorer</b> (correlations of {st["corr_contrib"]:.2f} and +{st["corr_withdraw"]:.2f}'
   f'), because someone paying in buys more units while prices are low. In all 20,000 orderings, ₱1,000 a month in the Fund '
   f'beat the same money in a 4.5% money market fund (₱{st["mmf"]:,.0f}).'.replace('-0.', '−0.')),
]
callout = Table([[p(f'<b>How a dated goal gets funded.</b> The Fund is half the journey. The other half is an <b>account-level '
   f'glidepath</b>: from 24 months out, monthly transfers move the balance into a money market fund, leaving 15% here on the date. '
   f'We put the worst 12 months in 36 years (Aug 2001 to Jul 2002, {pct(gl["crash_total"],1)}) into the final year of every shuffled '
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
         ('Concentration caps', 'Issuer 10% · type 25%'), ('Weighting method', 'Equal risk contribution'),
         ('Benchmark', 'MSCI ACWI, in PHP'), ('Valuation', 'Daily, NAVPS')]
right = [bandrow('KEY FACTS', RW), kv(facts, [RW*0.45, RW*0.55]), Spacer(1, 3),
         p(f'<b>How holdings are sized.</b> Each holding is set to add the same share of portfolio risk, judged by how the {WORDS[NH]} '
           f'moved together over the previous three years. Nothing is sized on opinion. Today each contributes between '
           f'{rs[0]*100:.1f}% and {rs[-1]*100:.1f}% of total risk against a {100/NH:.1f}% target. The two below target are held back '
           f'by a rule: Saudi Telecom by the 10% issuer cap, Manila Water by its liquidity cap.', small)]
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
            'same method fell 41% and moved 0.85 as much as the market; see the long-history panel below.', tiny), Spacer(1, 2)]

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
story.append(Table([[[calt, Spacer(1, 2), p(f'The Fund led the index in {", ".join(lead)} and trailed it in {", ".join(lag)} and in late 2021. Over the last twelve '
                     f'months it {"led" if tr["1y"][0] > tr["1y"][1] else "trailed"} by {abs(gap1y):.2f} points. In 2022 it returned '
                     f'{pct(cal["2022"][0], sign=True)} against {pct(cal["2022"][1], sign=True)}: owners of earning assets held up as rates rose.', tiny)], '',
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
lh = [('Return a year', '11.7%', '11.7%'), ('Largest fall', '−41.2% (2007–09)', '−43.9%'), ('Months to recover', '67', '71'),
      ('Beta to US market', '0.85', '0.92'), ('Dot-com crash, 2000–02', '−8.5%', '−16.0%')]
lht = kv(lh, [CW*0.17, CW*0.14, CW*0.12], head=['1990–2026, in PHP', 'This method', 'Market fund'], right_cols=(1, 2))
story.append(Spacer(1, 3))
story.append(bandrow('THE SAME METHOD OVER 36 YEARS · US INDUSTRY PROXIES, SAME RULES AND FEE · JAN 1990 TO AUG 2026', CW))
story.append(Table([[lht, '', p('The five years above were calm for this Fund. Rebuilt from industry returns with the same rules, '
    'reserve and fee, the method matched a market fund with the same costs over 36 years and fell a little less in 2008. '
    'Its edge was the dot-com crash; its worst relative year was COVID. <b>Plan for a fall of up to 41%.</b> In the 1997–98 crisis, when the peso went from ₱26.4 '
    'to ₱39.1 per dollar, the same global holdings gained 111% in pesos: the reason the Fund is left unhedged. Proxies are '
    f'US-listed utility, telecom, transport, electrical-equipment and chip industries, so they move together more than {WORDS[NH]} companies in {WORDS[NC]} countries would.', small)]],
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
SHORT = {'Grupo Aeroportuario del Sureste': 'ASUR', 'OMA (Centro Norte airports)': 'OMA', 'Japan Airport Terminal': 'Japan Airport Term.',
         'Schneider Electric': 'Schneider', 'HD Hyundai Electric': 'HD Hyundai Elec.', 'America Movil': 'América Móvil'}
TYPES = ['Power generation & grids', 'Water', 'Digital networks', 'Ports', 'Airports & toll roads', 'Grid & power equipment', 'Semiconductors']
cellname = ParagraphStyle('cn', parent=cell, fontSize=5.9, leading=6.9)
cellnr = ParagraphStyle('cnr', parent=cellname, alignment=TA_RIGHT)
cellnb = ParagraphStyle('cnb', parent=cellname, fontName='Helvetica-Bold')
WQ = {q['key']: q for q in pr}
SHORTT = {'ENEL': '68 → 80+ GW installed by 2028', 'ELE': '+1.9 GW renewables, to 13.2 GW by 2028', 'ENGI': '95 GW renewables and storage by 2030',
  'SBS': 'R$70bn of works to universal service by 2029', 'MWC': '3,225 MLD of new supply by 2037', 'VIE': 'Double desalination (1.4M m³/day) by 2030',
  'AMX': '5,400 km of new fibre in Peru in 2026', 'STC': '1 GW of data centres by 2030', 'DTE': 'Fibre to every German home by 2030',
  'WPRTS': '14M → 27M TEU a year (Westports 2)', 'KAMIGUMI': 'Automated Kobe Port cold store, Aug 2029', 'ICT': 'US$300M, three terminals expanded by 2028',
  'ASR': 'Cancún T4 expansion by end-2028', 'OMAB': 'Monterrey to 18M+ passengers, 2026–30 plan', 'JAT': '6 Haneda gates 2026; T2 extension 2027',
  'HDHE': 'KRW397bn transformer capacity by 2028', 'NEX': '525 kV HVDC cable plants by 2026', 'SU': 'US$700M of US plant capacity by 2027',
  'MU': 'Idaho DRAM fab producing from 2027', 'SKHYNIX': 'Cheongju HBM packaging fab by end-2027', 'TSMC': 'US$60–64bn capital spending in 2026'}
TL = {'Power generation & grids': 'Power', 'Water': 'Water', 'Digital networks': 'Networks', 'Ports': 'Ports', 'Airports & toll roads': 'Airports, roads',
      'Grid & power equipment': 'Grid equipment', 'Semiconductors': 'Chips'}
rows = [[p(h, cellnb) for h in ['Capacity', 'Holding', 'Theme fit: dated capacity target', 'Merit: rank · EV/EBITDA (peer median) · return gap (median)',
                                'Role: swings · correlation · overlap', 'Weight', 'Risk']]]
grp_rows = []
for t in TYPES:
    ks = sorted([c for c in I.CANDIDATES if c[12] == 'PASS' and c[13] == t], key=lambda c: I.MERIT[c[0]]['rank'])
    for j, c in enumerate(ks):
        k = c[0]; m = I.MERIT[k]; q = WQ[k]
        merit = f'#{m["rank"]}/{m["peers"]} · {c[9]:.1f}× ({m["peer_med_ev"]:.1f}×) · {m["spread"]:+.1f} pts ({m["peer_med_spread"]:+.1f})'
        role = f'{q["vol"]*100:.0f}% · {q["avg_corr"]:.2f}'
        if q['binding']: role += ' · ' + q['binding'][0].replace('liquidity cap', 'liq. cap')
        if E.GROUP.get(k): role += ' · ' + E.GROUP[k]
        if j == 0: grp_rows.append(len(rows))
        rows.append([p(f'<b>{TL[t]}</b>' if j == 0 else '', cellname),
                     p(f'{SHORT.get(c[1], c[1]).replace("&", "&amp;")} <font color="#58635C">{c[2]}</font>', cellname),
                     p(SHORTT[k], cellname), p(merit, cellname), p(role, cellname),
                     p(f'<b>{pct(q["weight"])}</b>', cellnr), p(pct(q['risk_share'], 1), cellnr)])
hw = [CW*0.085, CW*0.13, CW*0.245, CW*0.245, CW*0.185, CW*0.06, CW*0.05]
holdt = Table(rows, colWidths=hw, repeatRows=1)
hst = [('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 2), ('RIGHTPADDING', (0, 0), (-1, -1), 2),
       ('TOPPADDING', (0, 0), (-1, -1), 0.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 0.5), ('BACKGROUND', (0, 0), (-1, 0), SOFT),
       ('LINEBELOW', (0, 0), (-1, 0), 0.3, RULE)]
for i in grp_rows[1:]: hst.append(('LINEABOVE', (0, i), (-1, i), 0.4, RULE))
holdt.setStyle(TableStyle(hst))
bt = R['by_type']
alloc = ' · '.join(f'{k} {pct(v)}' for k, v in bt.items())
ctry = ' · '.join(f'{CN.get(k, k)} {pct(v)}' for k, v in list(R['by_country'].items())[:6])
hold_note = p(f'<b>How to read it.</b> Theme fit makes a company eligible; merit decides who is held (the top three per kind of capacity '
    f'among companies that pass the debt, price and liquidity gates); the risk model sets the weight. Return gap = return on invested '
    f'capital minus cost of capital. The milestone each serves is the story, not the reason to buy. <b>By capacity:</b> {alloc}. '
    f'<b>Largest countries (reported, not limited):</b> {ctry}.', tiny)
story.append(bandrow(f'HOLDINGS · THEME FIT, INVESTMENT MERIT AND PORTFOLIO ROLE · {NH} COMPANIES', CW))
story += [holdt, Spacer(1, 2), hold_note, Spacer(1, 4)]

bw = CW*0.47
role = R['by_role']; grp = R['by_group']
topw = pr[0]; topc = max(R['by_country'].items(), key=lambda x: x[1])
gnames = {g: v for g, v in grp.items() if g in set(E.GROUP.values())}; topg = max(gnames.items(), key=lambda x: x[1])
mwc = [q for q in pr if q['key'] == 'MWC'][0]
rules = [('Owners', '≥ 45%', pct(role.get('Owner', 0))), ('Suppliers', '≤ 25%', pct(role.get('Supplier', 0))),
         ('Capacity type', '≤ 25%', f'{pct(max(R["by_type"].values()))} digital networks'), ('Liquid reserve', '10%', '10.00%'),
         ('Single issuer', '≤ 10%', f'{pct(topw["weight"])} {topw["name"]}'), ('Single group', '≤ 15%', f'{pct(topg[1])} {topg[0]}'),
         ('Country', 'no limit', f'{pct(topc[1])} {CN[topc[0]]}'),
         ('Liquidity', '5 days at 20% of volume', f'{pct(mwc["weight"])} Manila Water')]
rulest = kv(rules, [bw*0.3, bw*0.33, bw*0.37], head=['Limit', 'Rule', 'Actual (largest)'], right_cols=(1, 2))
rules_block = [bandrow('THE RULES THE PORTFOLIO MUST OBEY · ALL MET AT ONCE', bw), rulest, Spacer(1, 2),
    p('Two holdings sit at a limit: Saudi Telecom at the issuer cap and Manila Water at its liquidity cap (₱1 billion launch size). '
      'Every other weight came out of the risk model, and every rule held at all 21 quarterly rebalances. Groups by controlling '
      'shareholder: ICTSI and Manila Water (Razon), Enel and Endesa (Enel).', tiny), Spacer(1, 3),
    p(f'<b>Where the fund is still concentrated.</b> The {WORDS[NH]} behave like about {R["div_ratio_sq"]:.1f} independent bets; two '
      f'shared forces carry {pct(R["top2_factor_share"],1)} of the risk. Overlaps we report: AI and data-centre build-out (chips, '
      f'Schneider, HD Hyundai) about 12%, Mexico about 10% across three holdings.', small)]

mvp = [bandrow(f'HOW WE PICKED THE {NH} · THREE STEPS, IN ORDER', CW - bw - 8),
  p(f'<b><font color="#0F7A45">M</font> Map the capacity (theme fit).</b> One global list, no regions or country slots: up to the 20 '
    f'largest listed companies in each of seven kinds of capacity, 121 in all. Theme fit: the main business is on our list, and a '
    f'conglomerate needs half its revenue there (Siemens 29%, Hitachi 30%, Samsung 39% fail). Every holding cites a dated capacity target.', small), Spacer(1, 2),
  p('<b><font color="#0F7A45">V</font> Verify the merit (investment merit).</b> Gates: net debt ≤ 4.0× EBITDA (6.0× utilities) and '
    'interest cover ≥ 2.5×; EV/EBITDA ≤ 22.2×, the money-market yield; a position sellable in five days at 20% of volume. Then a rank '
    'against the same kind of company worldwide: half valuation, half return on capital minus cost of capital. Top three held. Out: '
    'NVIDIA, ASML, GE Vernova (price); NextEra, American Tower (debt).', small), Spacer(1, 2),
  p('<b><font color="#0F7A45">P</font> Position the risk (portfolio role).</b> Produces the weight as a number; judgment sets only the rules and exits. Equal risk contribution on the previous three years '
    'of weekly peso returns, re-solved every quarter with only the data available then, inside the rules on the left.', small),
  Spacer(1, 2),
  p(f'<b>How to read the simulation.</b> We chose the {WORDS[NH]} in October 2026, using today\'s ratios, and applied '
    'the rules to their past prices. That tests the method, not stock-picking in 2021, and it flatters the result: ranking by '
    'today\'s profits favour companies at a cyclical peak, such as the memory-chip makers. Plan on the 36-year figures.', tiny)]
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
      '41%, as in 2008. Not for money needed within five years, an emergency fund, or someone who would stop after a bad year. For '
      'all three a money market fund is right, and our sign-up screen sends them there.', small),
    Spacer(1, 2), p('<b>Team Los Angeles 76ers</b>, Ateneo de Manila University: Prince Angelo C. Rivera · Luis Tengonciang · Karol Josef Fuñe · Eric Fabian Thirdy Mendez.', tiny)]
risks = [('Market and equity', f'90% equities, Aggressive. 10% reserve; sizing keeps each holding near a {100/NH:.1f}% share of risk. '
          f'Reduced, not removed: the same method fell 41% in 2008–09.'),
         ('Concentration and factor', f'Issuer ≤ 10%, group ≤ 15%, capacity type ≤ 25%, role limits. Two shared forces still carry '
          f'{pct(R["top2_factor_share"],1)} of risk, so a chip downturn or a sell-off in Mexico or Saudi Arabia hits several holdings together.'),
         ('Currency, country and liquidity', f'About {100 - R["by_country"]["PH"]*100 - 10:.0f}% non-peso, unhedged on purpose: '
          f'salary and goals are already in pesos. {WORDS[NC].capitalize()} listing markets. Every position passes the five-day liquidity test. '
          f'Saudi Arabia (10%) and Mexico (10%) are the largest emerging-market exposures; the riyal is pegged to the US dollar.'),
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
