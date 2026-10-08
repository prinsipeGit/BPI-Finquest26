"""Investor fact sheet (2 pages), simplified per the team's 7 Oct 2026 changes, Section 6. Detailed methodology lives in the
supporting proposal. All numbers from results4.json."""
import json, re, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Table, TableStyle, Image, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('DJ', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
def P(s): return re.sub('([₱−≤≥→×])', r'<font name="DJ">\1</font>', s)

R = json.load(open('results4.json')); F5 = R['five']; PX = R['proxy']; PF = R['portfolio']
v4, aw = F5['v4']['stats'], F5['acwi']['stats']; NH = R['n_held']; ps = PX['stats']
CN = {'PH': 'Philippines', 'IN': 'India', 'ES': 'Spain', 'FR': 'France', 'MY': 'Malaysia', 'TW': 'Taiwan', 'DE': 'Germany', 'JP': 'Japan',
      'US': 'United States', 'HK': 'Hong Kong / China', 'CH': 'Switzerland', 'MX': 'Mexico', 'BR': 'Brazil', 'IT': 'Italy', 'KR': 'South Korea',
      'GB': 'United Kingdom', 'NL': 'Netherlands', 'SA': 'Saudi Arabia', 'TH': 'Thailand'}
GREEN = colors.HexColor('#0F7A45'); DARK = colors.HexColor('#1E2622'); RULE = colors.HexColor('#C9D3CD')
SOFT = colors.HexColor('#EEF5F0'); AMBER = colors.HexColor('#FFF4E0'); MUTED = colors.HexColor('#58635C')
def pct(x, d=2, sign=False): return (f'{x*100:+.{d}f}%' if sign else f'{x*100:.{d}f}%').replace('-', '−')

# chart: growth of 100, axis from 0
dates = pd.to_datetime(['2021-10-01'] + R['dates'])
fund = [100] + R['paths']['v4']; ref = [100] + R['paths']['acwi']; pse = [100] + R['paths']['psei']
fig, ax = plt.subplots(figsize=(7.6, 1.7), dpi=220)
ax.plot(dates, ref, color='#8A928D', lw=1.0, label=f'MSCI ACWI ETF in pesos (reference, not the benchmark): ends {ref[-1]:.0f}')
ax.plot(dates, pse, color='#C9761F', lw=1.0, label=f'PSEi via FMETF tracker, price only (local reference): ends {pse[-1]:.0f}')
ax.plot(dates, fund, color='#0F7A45', lw=1.5, label=f'Currently selected Firsts Fund holdings, after all modelled costs: ends {fund[-1]:.0f}')
top = 50 * int(max(max(fund), max(ref)) / 50 + 1)
ax.set_ylim(0, top); ax.set_yticks(range(0, top + 1, 50)); ax.set_xlim(dates[0], dates[-1])
ax.set_ylabel('Base 100, axis from 0', fontsize=6); ax.tick_params(labelsize=6)
ax.grid(axis='y', color='#E3E8E5', lw=0.6); [ax.spines[s].set_visible(False) for s in ['top', 'right']]
ax.legend(fontsize=6, frameon=False, loc='upper left'); fig.tight_layout(pad=0.3); fig.savefig('growth4.png'); plt.close(fig)

base = ParagraphStyle('b', fontName='Helvetica', fontSize=7.3, leading=9.2, textColor=DARK)
small = ParagraphStyle('s', parent=base, fontSize=6.6, leading=8.2)
tiny = ParagraphStyle('t', parent=base, fontSize=5.9, leading=7.1, textColor=MUTED)
cell = ParagraphStyle('c', parent=base, fontSize=6.6, leading=8.0); cellb = ParagraphStyle('cb', parent=cell, fontName='Helvetica-Bold')
cellr = ParagraphStyle('cr', parent=cell, alignment=TA_RIGHT); cellrb = ParagraphStyle('crb', parent=cellr, fontName='Helvetica-Bold')
band = ParagraphStyle('band', parent=base, fontName='Helvetica-Bold', fontSize=7.4, textColor=colors.white)
def p(t, st=base): return Paragraph(P(t), st)
def bandrow(text, width):
    t = Table([[p(text, band)]], colWidths=[width])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), DARK), ('LEFTPADDING', (0, 0), (-1, -1), 4), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
    return t
def kv(rows, widths, head=None, right_cols=(1,), boldrows=()):
    data = []
    if head: data.append([p(h, cellrb if i in right_cols else cellb) for i, h in enumerate(head)])
    for r_ in rows:
        b_ = r_ in boldrows
        data.append([p(str(c), (cellrb if b_ else cellr) if i in right_cols else (cellb if b_ or i == 0 else cell)) for i, c in enumerate(r_)])
    t = Table(data, colWidths=widths)
    st = [('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 2), ('RIGHTPADDING', (0, 0), (-1, -1), 2),
          ('TOPPADDING', (0, 0), (-1, -1), 0.9), ('BOTTOMPADDING', (0, 0), (-1, -1), 0.9), ('LINEBELOW', (0, 0), (-1, -1), 0.3, RULE)]
    if head: st.append(('BACKGROUND', (0, 0), (-1, 0), SOFT))
    t.setStyle(TableStyle(st)); return t
def boxed(flow, width, bg=AMBER):
    t = Table([[flow]], colWidths=[width])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), bg), ('LEFTPADDING', (0, 0), (-1, -1), 5), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    return t
def two(a, b, wa, wb, gap=8):
    return Table([[a, '', b]], colWidths=[wa, gap, wb], style=[('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)])

W, H = A4; M = 9*mm; CW = W - 2*M
def header(c, doc):
    c.saveState()
    c.setFillColor(GREEN); c.rect(M, H - M - 18, 14, 18, fill=1, stroke=0)
    c.setFillColor(DARK); c.setFont('Helvetica-Bold', 15); c.drawString(M + 20, H - M - 13, 'FIRSTS FUND')
    c.setFont('Helvetica-Bold', 7.3)
    c.drawString(M + 20, H - M - 23, 'FUND FACT SHEET · PROPOSED ACTIVELY MANAGED GLOBAL EQUITY UITF' if doc.page == 1 else 'HOLDINGS, RISKS, FEES AND DISCLOSURES')
    c.setFont('Helvetica', 6.5); c.setFillColor(MUTED)
    c.drawString(M + 20, H - M - 31, f'A FinQuest 2026 proposal, not an existing BPI product · Portfolio as of 2 October 2026 · Page {doc.page} of 2')
    c.setFillColor(GREEN); c.setFont('Helvetica-BoldOblique', 9); c.drawRightString(W - M, H - M - 14, '“Fund your firsts.”')
    c.setStrokeColor(GREEN); c.setLineWidth(1.2); c.line(M, H - M - 36, W - M, H - M - 36)
    c.restoreState()
doc = BaseDocTemplate('LosAngeles76ers_FirstsFund_FactSheet.pdf', pagesize=A4, leftMargin=M, rightMargin=M, topMargin=M + 40, bottomMargin=M,
                      title='Firsts Fund — Fund Fact Sheet', author='Team Los Angeles 76ers, Ateneo de Manila University')
doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(M, M, CW, H - 2*M - 40, 0, 0, 0, 0)], onPage=header)])
story = []

# ---------- page 1 ----------
LW, RW = CW*0.60, CW*0.38; GAP = CW - LW - RW
bt = R['by_type']; cnt = R['by_country']
left = [bandrow('FUND OBJECTIVE AND THEME', LW), Spacer(1, 2),
  p('<b>Objective.</b> Long-term capital growth by investing directly in listed companies around the world that own, operate or supply '
    'essential, hard-to-replace capacity: power and water systems, digital networks, ports, airports, hospitals, and the equipment they run on.'), Spacer(1, 2),
  p('<b>How the fund invests, in one line.</b> We identify businesses providing essential capacity, check their financial strength and value, '
    'and build a portfolio that balances opportunities with risk. The number of investments follows that process. The fund is '
    '<b>actively managed with diversification and risk controls</b>; the manager may change holdings and weights within the mandate.'), Spacer(1, 2),
  p('<b>Why it exists.</b> An early-career Filipino earns and saves in pesos, tied to one economy. Today\'s options are a local index fund '
    '(0.52% a year over five years) or a global fund of funds with a second fee layer that trailed its index by 4.19 points a year. '
    'Firsts Fund would be a peso-priced global equity fund holding shares directly, with one fee layer.'), Spacer(1, 2),
  p('<b>Suitable investor.</b> Regular income, a goal at least <b>five years</b> away, and the risk tolerance for an equity fund that can '
    'fall sharply in a bad year. Not suitable for money needed within five years or for emergency savings.'), Spacer(1, 3),
  boxed(p('<b>Separate goal service (proposed platform feature).</b> An authorized account-level glidepath would gradually move part of an '
          'investor\'s Firsts Fund units into a lower-risk fund as their chosen goal approaches. It changes the investor\'s allocation, not '
          'this fund\'s mandate, uses redemption proceeds at a gain or a loss, and does not guarantee capital or goal completion.', small), LW)]
facts = [('Structure', 'Actively managed global equity UITF (proposed)'), ('Currency', 'Philippine peso; units and NAV per unit'),
         ('Recommended horizon', '5 years or longer'), ('Risk classification', 'Aggressive'), ('Minimum (proposed)', '₱100 initial · ₱100 regular'),
         ('Management fee (proposed)', '1.50% a year'), ('Dealing (proposed)', 'Daily subscription and redemption'),
         ('Redemption settlement', 'Per plan rules; no lock-in or penalty proposed'), ('Holdings', f'{NH} listed companies, {len(cnt)} markets'),
         ('Cash', 'Operating cash for redemptions and settlement (about 3% modelled)'), ('Single-issuer limit', '20% of NAV (BSP regulatory ceiling)'),
         ('Benchmark', 'To be selected by the team'), ('Trustee', 'BPI Wealth (proposed)')]
right = [bandrow('KEY FACTS', RW), kv(facts, [RW*0.40, RW*0.60]), Spacer(1, 3), bandrow('ALLOCATION BY KIND OF CAPACITY', RW),
         kv([(k.replace('&', '&amp;'), pct(v)) for k, v in bt.items()] + [('Operating cash', '3.00%')], [RW*0.70, RW*0.30])]
story += [two(left, right, LW, RW, GAP), Spacer(1, 4)]

top10 = PF[:10]
t10 = kv([(f'{x["name"].replace("&", "&amp;")}', CN.get(x['country'], x['country']), x['ctype'].replace('&', '&amp;'), pct(x['weight'])) for x in top10],
         [CW*0.47*0.38, CW*0.47*0.22, CW*0.47*0.27, CW*0.47*0.13], head=['Top 10 holdings', 'Listing', 'Capacity', 'Weight'], right_cols=(3,))
ctab = kv([(CN.get(k, k), pct(v)) for k, v in list(cnt.items())[:8]] + [(f'{len(cnt) - 8} other markets', pct(sum(list(cnt.values())[8:])))],
          [CW*0.24*0.62, CW*0.24*0.38], head=['By listing market', ''], right_cols=(1,))
other = [p(f'<b>Countries are an outcome, not a target.</b> There is no Philippine or global quota; Philippine-listed ICTSI is held at '
           f'{pct(R["ph_now"])} because it passed the same tests as every other company. Listing market is not where revenue is earned.', small),
         Spacer(1, 2), p(f'<b>Overlaps we watch.</b> Data-centre build-out (chips and grid equipment) {pct(bt["Semiconductors"] + bt["Grid & power equipment"])}; '
           f'digital networks at the 25% internal limit.', small)]
story += [two(t10, two(ctab, other, CW*0.24, CW*0.53 - 16 - CW*0.24), CW*0.47, CW*0.53 - 8), Spacer(1, 4)]

story.append(bandrow('PERFORMANCE · HISTORICAL PERFORMANCE OF THE CURRENTLY SELECTED PORTFOLIO, NOT ACTUAL FUND PERFORMANCE', CW))
story.append(Image('growth4.png', width=CW, height=CW*1.7/7.6))
cal = F5['v4']['cal']; cra = F5['acwi']['cal']
calrows = [('Holdings, after costs', *[pct(cal[y], 1, True) for y in ['2021', '2022', '2023', '2024', '2025', '2026']], pct(v4['cagr'], 1, True), pct(v4['vol'], 1), pct(v4['maxdd'], 1)),
           ('MSCI ACWI ETF (reference)', *[pct(cra[y], 1, True) for y in ['2021', '2022', '2023', '2024', '2025', '2026']], pct(aw['cagr'], 1, True), pct(aw['vol'], 1), pct(aw['maxdd'], 1)),
           ('PSEi (FMETF, price only)', *[pct(F5['psei']['cal'][y], 1, True) for y in ['2021', '2022', '2023', '2024', '2025', '2026']], pct(F5['psei']['stats']['cagr'], 1, True), pct(F5['psei']['stats']['vol'], 1), pct(F5['psei']['stats']['maxdd'], 1))]
pt = kv(calrows, [CW*0.22] + [CW*0.078]*9, head=['In pesos', '2021*', '2022', '2023', '2024', '2025', '2026*', 'A year', 'Volatility', 'Worst fall'], right_cols=tuple(range(1, 10)))
story += [pt, Spacer(1, 2), boxed(p(
    f'<b>Read this carefully.</b> These are the past weekly returns of the {NH} companies selected in October 2026 using October 2026 data, '
    f'weighted with only the price history available at each quarter, after the 1.50% fee, 0.30% trading costs and estimated dividend withholding. '
    f'Because the holdings were chosen with hindsight, this is <b>not</b> a backtest of the selection process and not a forecast. '
    f'*2021 from 1 Oct; 2026 to 2 Oct. <b>Longer context:</b> an industry proxy (six US industries standing in for the eight types, 1990–2026, same weighting, fee and costs, no company screens) '
    f'returned {pct(ps["cap"]["cagr"], 1)} a year against {pct(ps["mkt"]["cagr"], 1)} for a same-cost market fund, with a worst fall of '
    f'{pct(ps["cap"]["maxdd"], 0)} and a worst 12 months of {pct(ps["cap"]["worst12"], 0)}. It is context for the theme, not evidence for the company screens.', small), CW)]
story += [Spacer(1, 3), p('<b>IMPORTANT.</b> Firsts Fund is a student competition proposal; no such fund exists and nothing here is an offer, solicitation or '
    'investment advice. Simulated and historical figures do not represent actual trading. The value of units can fall as well as rise and an '
    'investor may get back less than invested. A UITF is not a deposit and is not insured by PDIC.', tiny), PageBreak()]

# ---------- page 2 ----------
SH = {'OMA (Centro Norte airports)': 'OMA (airports)', 'Dr. Sulaiman Al Habib Medical': 'Dr. Sulaiman Al Habib', 'America Movil': 'América Móvil',
      'Bangkok Dusit Medical Services': 'Bangkok Dusit Medical', 'Guangdong Investment': 'Guangdong Investment'}
half = (NH + 1) // 2
def hrows(lst): return [(SH.get(x['name'], x['name']).replace('&', '&amp;'), x['country'], x['ctype'].replace('&', '&amp;').replace('Power generation &amp; grids', 'Power &amp; grids'), pct(x['weight'])) for x in lst]
hw = CW/2 - 4
ht = lambda rows: kv(rows, [hw*0.42, hw*0.08, hw*0.36, hw*0.14], head=['Holding', '', 'Capacity', 'Weight'], right_cols=(3,))
story += [bandrow(f'ALL {NH} HOLDINGS · WEIGHTS SET BY THE RISK MODEL, SOLVED ON DATA TO 2 OCTOBER 2026', CW), Spacer(1, 1),
          two(ht(hrows(PF[:half])), ht(hrows(PF[half:])), hw, hw), Spacer(1, 2),
          p('Weights move as prices change and are reviewed quarterly and when material events affect a holding. Watchlisted and rejected companies, '
            'with reasons, and the full investment assessment for each holding are in the supporting proposal.', tiny), Spacer(1, 4)]
cost = R['costs']['v4']
risks = [('Market', f'Equity prices can fall sharply. In the 36-year industry proxy the worst 12 months lost {pct(-ps["cap"]["worst12"], 0)} and the deepest fall was {pct(-ps["cap"]["maxdd"], 0)}.'),
         ('Concentration', f'Digital networks are at the 25% internal limit; data-centre build-out is about {pct(bt["Semiconductors"] + bt["Grid & power equipment"], 0)}; '
          f'Saudi Arabia {pct(cnt.get("SA", 0), 0)} and US health policy about {pct(sum(x["weight"] for x in PF if x["key"] in ("HCA", "EHC")), 0)}.'),
         ('Currency', f'About {pct(1 - R["ph_now"] - 0.03, 0)} is in non-peso assets and unhedged; a stronger peso lowers peso returns.'),
         ('Liquidity', 'Some holdings trade thinly; each position is limited to what could be sold in five days at 20% of average volume (sized for a ₱1bn fund). '
          'The manager holds operating cash and liquid instruments for redemptions.'),
         ('Country and regulation', 'Holdings in emerging markets, including state-influenced companies, face policy and sanctions risk.'),
         ('Model and data', 'Selection uses one data vendor and team-set thresholds; historical results include hindsight.')]
rw = CW*0.56
fees = [('Management fee (proposed)', '1.50% a year of NAV, charged daily'), ('Trading costs (modelled)', f'about {pct(cost["trading_pa"])} a year'),
        ('Dividend withholding (modelled)', f'about {pct(cost["wht_pa"])} a year'), ('Subscription / redemption fee', 'None proposed'),
        ('Minimum holding period', 'None proposed; 5 years+ is a recommendation')]
fw = CW - rw - 8
red = [bandrow('FEES AND CHARGES', fw), kv(fees, [fw*0.45, fw*0.55]), Spacer(1, 3), bandrow('SUBSCRIPTIONS AND REDEMPTIONS (PROPOSED)', fw),
       p('Units can be bought with a one-time amount, regular subscriptions or voluntary top-ups, and redeemed on any dealing day at the NAV per unit '
         'that day. Settlement follows the plan rules set by the trustee; no instant settlement is promised. Missed regular contributions do not change '
         'the goal date and are not caught up automatically.', small), Spacer(1, 3), bandrow('COMPARED WITH TODAY\'S CHOICES', fw),
       kv([('BPI Global Equity Fund-of-Funds', 'Two fee layers', '₱1,000'), ('BPI Philippine Equity Index Fund', 'One economy', '₱1,000'),
           ('Pag-IBIG MP2', 'Savings; better for < 5 years', '₱500'), ('Firsts Fund (proposed)', 'Direct global shares, one fee', '₱100')],
          [fw*0.48, fw*0.37, fw*0.15], head=['Product', 'Structure', 'Min.'], right_cols=(2,))]
story += [two([bandrow('KEY RISKS', rw), kv(risks, [rw*0.22, rw*0.78], right_cols=())], red, rw, fw), Spacer(1, 4)]
story += [p('<b>Sources.</b> Company data: stockanalysis.com (S&amp;P Global Market Intelligence), 8 Oct 2026. Prices: Yahoo Finance total returns and PSE Edge '
            '(with cash dividends), converted to pesos weekly. Cash: BSP policy rate minus 0.50 pt. Industry proxy: Kenneth French Data Library and BIS exchange '
            'rates. Issuer ceiling: BSP Circular No. 1234 (2026) as reproduced by RCBC Trust, a 20% ceiling, not a target. Comparison funds: BPI Wealth and Pag-IBIG '
            'disclosure statements. Sub-industries assigned by the team. Withholding rates approximate, to be confirmed by tax counsel.', tiny), Spacer(1, 2),
          p('<b>Team Los Angeles 76ers</b>, Ateneo de Manila University: Prince Angelo C. Rivera · Luis Tengonciang · Karol Josef Fuñe · Eric Fabian Thirdy Mendez.', tiny)]
doc.build(story); print('built')
