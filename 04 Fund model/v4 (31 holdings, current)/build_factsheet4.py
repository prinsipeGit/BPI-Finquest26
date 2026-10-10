"""Investor fact sheet (2 pages), simplified per the team's 7 Oct 2026 changes, Section 6. Detailed methodology lives in the
supporting proposal. All numbers from results4.json, plus bench.json (NFRA benchmark and IGF cross-check, in pesos; built by
bench_nfra.py from map/bench_usd.json). Polished 8 Oct 2026: NFRA benchmark, plain language, saver illustration, total cost."""
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

R = json.load(open('results4.json')); F5 = R['five']; PX = R['proxy']; PF = R['portfolio']; bt = R['by_type']
B = json.load(open('bench.json')); NF = B['nfra']; nf = NF['stats']
XS = json.load(open('ex_suppliers.json'))
X = json.load(open('extra4.json'))   # seq4.py: sequence test, Sortino, 1y/3y
_st = [r['stage'] for r in json.load(open('map/universe4.json'))]
n_uni0 = sum(x != 'Outside universe' for x in _st); n_m0 = n_uni0 - sum(x.startswith('Reject (M') for x in _st); n_el0 = _st.count('Eligible')   # same simulation without chip and grid-equipment holdings (ex_suppliers.py)
v4, aw = F5['v4']['stats'], F5['acwi']['stats']; NH = R['n_held']; ps = PX['stats']
CN = {'PH': 'Philippines', 'IN': 'India', 'ES': 'Spain', 'FR': 'France', 'MY': 'Malaysia', 'TW': 'Taiwan', 'DE': 'Germany', 'JP': 'Japan',
      'US': 'United States', 'HK': 'Hong Kong / China', 'CH': 'Switzerland', 'MX': 'Mexico', 'BR': 'Brazil', 'IT': 'Italy', 'KR': 'South Korea',
      'GB': 'United Kingdom', 'NL': 'Netherlands', 'SA': 'Saudi Arabia', 'TH': 'Thailand'}
GREEN = colors.HexColor('#0F7A45'); DARK = colors.HexColor('#1E2622'); RULE = colors.HexColor('#C9D3CD')
SOFT = colors.HexColor('#EEF5F0'); AMBER = colors.HexColor('#FFF4E0'); MUTED = colors.HexColor('#58635C')
def pct(x, d=2, sign=False): return (f'{x*100:+.{d}f}%' if sign else f'{x*100:.{d}f}%').replace('-', '−')

# chart: growth of 100, axis from 0
dates = pd.to_datetime(['2021-10-01'] + R['dates'])
fund = [100] + R['paths']['v4']; ref = [100] + R['paths']['acwi']; pse = [100] + R['paths']['psei']; bmk = [100] + NF['path']
fig, ax = plt.subplots(figsize=(7.6, 1.85), dpi=220)
ax.plot(dates, ref, color='#B4BBB7', lw=0.9, label=f'Market context: world stocks (MSCI ACWI ETF): ₱{ref[-1]:.0f}')
ax.plot(dates, pse, color='#C9761F', lw=0.9, label=f'Market context: Philippine stocks (PSEi, price only): ₱{pse[-1]:.0f}')
ax.plot(dates, bmk, color='#1F4E9C', lw=1.3, label=f'Benchmark: global infrastructure (NFRA ETF): ₱{bmk[-1]:.0f}')
ax.plot(dates, fund, color='#0F7A45', lw=1.7, label=f'Firsts Fund\'s current holdings, after all costs (hindsight): ₱{fund[-1]:.0f}')
top = 50 * int(max(max(fund), max(ref)) / 50 + 1)
ax.set_ylim(0, top); ax.set_yticks(range(0, top + 1, 50)); ax.set_xlim(dates[0], dates[-1])
ax.set_ylabel('Value of ₱100, in pesos', fontsize=6); ax.tick_params(labelsize=6)
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
    t = Table([[flow]], colWidths=[width or CW*0.60])
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
    c.drawString(M + 20, H - M - 23, {1: 'EXECUTIVE SUMMARY · THE PROBLEM, AND THE FUND THAT ANSWERS IT', 2: 'EXECUTIVE SUMMARY · THE HOOK: WHAT MAKES THEM START',
                                      3: 'EXECUTIVE SUMMARY · THE HABIT: WHAT KEEPS THEM INVESTED', 4: 'FUND FACT SHEET · PROPOSED ACTIVELY MANAGED GLOBAL EQUITY UITF',
                                      5: 'FUND FACT SHEET · HOLDINGS, PORTFOLIO CONSTRUCTION, RISKS AND FEES',
                                      6: 'ANNEX · EVIDENCE, METHOD, LIMITS AND REGULATORY POSITION'}[doc.page])
    c.setFont('Helvetica', 6.5); c.setFillColor(MUTED)
    c.drawString(M + 20, H - M - 31, f'A FinQuest 2026 proposal, not an existing BPI product · Portfolio as of 2 October 2026 · Page {doc.page} of 6')
    c.setFillColor(GREEN); c.setFont('Helvetica-BoldOblique', 9); c.drawRightString(W - M, H - M - 14, '“Fund your firsts.”')
    c.setStrokeColor(GREEN); c.setLineWidth(1.2); c.line(M, H - M - 36, W - M, H - M - 36)
    c.restoreState()
doc = BaseDocTemplate('LosAngeles76ers_FirstsFund_FactSheet.pdf', pagesize=A4, leftMargin=M, rightMargin=M, topMargin=M + 40, bottomMargin=M,
                      title='Firsts Fund — Executive Summary and Fund Fact Sheet', author='Team Los Angeles 76ers, Ateneo de Manila University')
doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(M, M, CW, H - 2*M - 40, 0, 0, 0, 0)], onPage=header)])
story = []

# ---------- pages 1-3: executive summary (Problem, Hook, Habit) ----------
exec(open('exec_pages4.py').read())

# ---------- page 4: fact sheet ----------
LW, RW = CW*0.60, CW*0.38; GAP = CW - LW - RW
cnt = R['by_country']
dca, dcg = PX['contrib']['dca'], PX['contrib']['dca_glide']
saver_box = boxed([p(f'<b>For a regular saver (illustration, not a forecast).</b> ₱1,000 a month for 5 years is ₱60,000 paid in. Across every '
    f'5-year stretch from 1990 to 2026 in the industry-level history ({dca["n"]} start months), the typical saver ended with about '
    f'<b>₱{round(60000*dca["median"], -3):,.0f}</b>. About 1 in {round(1/dca["below1"])} stretches ended below ₱60,000; the worst, ending in '
    f'early 2009, at about ₱{round(60000*dca["worst"], -3):,.0f}. With the proposed goal service, the worst was about ₱{round(60000*dcg["worst"], -3):,.0f}.', small),
    Spacer(1, 1), p('Same fee and costs; contributions at the start of each month. It reflects the theme, not our company choices.', tiny)], None, SOFT)
left = [bandrow('FUND OBJECTIVE AND THEME', LW), Spacer(1, 2),
  p('<b>Objective.</b> Long-term capital growth by investing directly in listed companies around the world that own, operate or supply '
    'essential, hard-to-replace capacity: power and water systems, digital networks, ports, airports, hospitals, and the equipment they run on.'), Spacer(1, 2),
  p('<b>How the fund invests, in one line.</b> We identify businesses providing essential capacity, check their financial strength and value, '
    'and build a portfolio that balances opportunities with risk. How many companies we hold follows from that process. The fund is '
    '<b>actively managed with diversification and risk controls</b>; the manager may change holdings and weights within the mandate.'), Spacer(1, 2),
  p('<b>Why it exists.</b> An early-career Filipino earns and saves in pesos, so their future depends on one economy. Firsts Fund would let '
    'them own a share of essential businesses around the world from ₱100, in pesos, through a fund that holds the shares directly '
    'with a single fee.'), Spacer(1, 2),
  p('<b>Suitable investor.</b> Regular income, a goal at least <b>five years</b> away, and the risk tolerance for an equity fund that can '
    'fall sharply in a bad year. Not suitable for money needed within five years or for emergency savings.'), Spacer(1, 3),
  boxed(p('<b>Goal service (proposed, in the investor\'s own account).</b> Close to a goal date there is little time to recover from a fall. A yearly '
          'goal review, plus a reminder two years before the date, lets the investor choose to move part of their units to a lower-risk fund. Nothing '
          'moves without their permission; it changes only their account, not how this fund invests; units are sold at that day\'s price, and the goal '
          'is not guaranteed.', small), LW), Spacer(1, 4), saver_box]
tot = R['costs']['v4']['trading_pa'] + R['costs']['v4']['wht_pa'] + 0.015
facts = [('Structure', 'Global equity UITF (proposed)'), ('Currency', 'Philippine peso; daily NAVPU'),
         ('Horizon', '5 years or longer'), ('Risk classification', 'Aggressive'), ('Minimum (proposed)', '₱100 to start and per top-up'),
         ('Fee (proposed)', '1.50% a year'), ('All-in cost (est.)', f'about {pct(tot, 1)} a year, all costs'),
         ('Buy or sell (proposed)', 'Any business day; paid T+5; no exit fee'),
         ('Holdings', f'{NH} listed companies, {len(cnt)} markets'), ('Cash', 'About 3%, kept to pay redemptions'),
         ('Limit per company', f'20% (BSP rule); largest today {pct(PF[0]["weight"], 1)}'), ('Benchmark', 'NFRA global infrastructure ETF, in pesos'), ('Reviews', 'Holdings monthly; weights quarterly'), ('Trustee', 'BPI Wealth (proposed)')]
right = [bandrow('KEY FACTS', RW), kv(facts, [RW*0.36, RW*0.64], right_cols=()), Spacer(1, 3), bandrow('ALLOCATION BY KIND OF CAPACITY', RW),
         kv([(k.replace('&', '&amp;'), pct(v)) for k, v in bt.items()] + [('Operating cash', '3.00%')], [RW*0.70, RW*0.30])]
story += [two(left, right, LW, RW, GAP), Spacer(1, 4)]

SH0 = {'Bangkok Dusit Medical Services': 'Bangkok Dusit Medical', 'Dr. Sulaiman Al Habib Medical': 'Dr. Sulaiman Al Habib'}
other = [p(f'<b>No country quota.</b> Philippine-listed ICTSI is held at {pct(R["ph_now"])} because it passed the same tests as every '
           f'other company. Where a company is listed is not always where it earns its revenue.', small),
         Spacer(1, 2), p(f'<b>Shared drivers.</b> About {pct(bt["Semiconductors"] + bt["Grid & power equipment"], 0)} depends on data-centre spending '
           f'(chips and grid equipment). Digital networks are at the fund\'s 25% cap per kind of capacity.', small)]
ctab = kv([(CN.get(k, k), pct(v)) for k, v in list(cnt.items())[:8]] + [(f'{len(cnt) - 8} other markets', pct(sum(list(cnt.values())[8:])))],
          [CW*0.30*0.65, CW*0.30*0.35], head=['By listing market', ''], right_cols=(1,))
other = [p(f'<b>Largest holdings.</b> ' + ', '.join(f'{SH0.get(x["name"], x["name"])} {pct(x["weight"], 1)}' for x in PF[:5]) +
           f'. No company is above {pct(PF[0]["weight"], 1)}; all {NH} are listed on page 3.', small), Spacer(1, 3)] + other
story += [two(ctab, other, CW*0.30, CW*0.70 - 10, 10), Spacer(1, 4)]

story.append(bandrow('PERFORMANCE VS BENCHMARK · PAST RETURNS OF TODAY\'S HOLDINGS, IN PESOS · NOT ACTUAL FUND PERFORMANCE', CW))
head = ParagraphStyle('hd', parent=base, fontSize=8.4, leading=10.5)
story.append(Spacer(1, 2))
story.append(p(f'<b>₱100 invested in October 2021 → ₱{fund[-1]:.0f}</b> for today\'s holdings after all costs, vs <b>₱{bmk[-1]:.0f}</b> for the '
               f'benchmark: <b>{pct(v4["cagr"], 1)}</b> vs <b>{pct(nf["cagr"], 1)}</b> a year. <font color="#9A5B00"><b>Hindsight:</b> these companies '
               f'were chosen in October 2026, so this is not a forecast.</font>', head))
story.append(Image('growth4.png', width=CW, height=CW*1.85/7.6))
cal = F5['v4']['cal']; cra = F5['acwi']['cal']
calrows = [('Firsts Fund holdings, after costs', *[pct(cal[y], 1, True) for y in ['2021', '2022', '2023', '2024', '2025', '2026']], pct(v4['cagr'], 1, True), pct(v4['vol'], 1), pct(v4['maxdd'], 1)),
           ('Benchmark: NFRA infrastructure ETF', *[pct(NF['cal'][y], 1, True) for y in ['2021', '2022', '2023', '2024', '2025', '2026']], pct(nf['cagr'], 1, True), pct(nf['vol'], 1), pct(nf['maxdd'], 1)),
           ('Market context: world (MSCI ACWI ETF)', *[pct(cra[y], 1, True) for y in ['2021', '2022', '2023', '2024', '2025', '2026']], pct(aw['cagr'], 1, True), pct(aw['vol'], 1), pct(aw['maxdd'], 1)),
           ('Market context: Philippines (PSEi)', *[pct(F5['psei']['cal'][y], 1, True) for y in ['2021', '2022', '2023', '2024', '2025', '2026']], pct(F5['psei']['stats']['cagr'], 1, True), pct(F5['psei']['stats']['vol'], 1), pct(F5['psei']['stats']['maxdd'], 1))]
pt = kv(calrows, [CW*0.25] + [CW*0.075]*9, head=['In pesos', '2021*', '2022', '2023', '2024', '2025', '2026*', 'A year', 'Volatility', 'Worst fall'], right_cols=tuple(range(1, 10)), boldrows=(calrows[0],))
vn = B['v4_vs_nfra']
statline = p(f'<b>Also, today\'s holdings over 5 years:</b> last year {pct(X["ret_1y"], 1, True)}; last 3 years {pct(X["ret_3y"], 1, True)} a year · worst 12 months '
             f'{pct(v4["worst12"], 1, True)}, best {pct(v4["best12"], 1, True)} · return for each unit of ups and downs (Sharpe ratio) {v4["sharpe"]:.2f} vs {nf["sharpe"]:.2f} '
             f'for the benchmark · moved about {vn["beta"]:.2f}× as much as the benchmark (beta). <b>In pesos:</b> the deepest drop on a ₱5,000 balance was '
             f'₱{X["dd_on_5000"]:,.0f}; a bad year like the 36-year worst ({pct(ps["cap"]["worst12"], 0)}) would be ₱{-ps["cap"]["worst12"]*5000:,.0f}.', small)
story += [pt, Spacer(1, 2), statline, Spacer(1, 2), boxed(p(
    f'<b>How to read this.</b> These are past returns of the {NH} companies we hold today, after the 1.50% fee, trading costs and dividend taxes; '
    f'because they were picked knowing how they did, the fund\'s real results would likely be lower. <b>Without the {len(XS["excluded"])} chip and '
    f'grid-equipment companies</b>, the other {XS["n"]} returned {pct(XS["cagr"], 1)} a year (₱100 → ₱{XS["growth"]:.0f}), so the lead over the '
    f'benchmark does not rest on them alone. <b>Over the long run:</b> an industry-level '
    f'version of the strategy returned {pct(ps["cap"]["cagr"], 1)} a year from 1990 to 2026, about the same as the world market ({pct(ps["mkt"]["cagr"], 1)}), '
    f'with a worst 12 months of {pct(ps["cap"]["worst12"], 0)}. Benchmark and references are ETFs after their own fees. *2021 from 1 Oct; 2026 to 2 Oct.', small), CW)]
story += [Spacer(1, 3), p('<b>IMPORTANT.</b> Firsts Fund is a student competition proposal; no such fund exists and nothing here is an offer, solicitation or '
    'investment advice. Simulated and historical figures do not represent actual trading. The value of units can fall as well as rise and an '
    'investor may get back less than invested. A UITF is not a deposit and is not insured by PDIC.', tiny), PageBreak()]

# ---------- page 5 ----------
SH = {'OMA (Centro Norte airports)': 'OMA (airports)', 'Dr. Sulaiman Al Habib Medical': 'Dr. Sulaiman Al Habib', 'America Movil': 'América Móvil',
      'Bangkok Dusit Medical Services': 'Bangkok Dusit Medical', 'Guangdong Investment': 'Guangdong Investment'}
half = (NH + 1) // 2
def hrows(lst): return [(SH.get(x['name'], x['name']).replace('&', '&amp;'), x['country'], x['ctype'].replace('&', '&amp;').replace('Power generation &amp; grids', 'Power &amp; grids'), pct(x['weight']), pct(x['risk_share'], 1)) for x in lst]
hw = CW/2 - 4
ht = lambda rows: kv(rows, [hw*0.36, hw*0.07, hw*0.31, hw*0.13, hw*0.13], head=['Holding', '', 'Capacity', 'Weight', '% of risk'], right_cols=(3, 4))
story += [bandrow(f'ALL {NH} HOLDINGS · WEIGHTED SO EACH COMPANY ADDS A SIMILAR SHARE OF RISK · AS OF 2 OCTOBER 2026', CW), Spacer(1, 1),
          two(ht(hrows(PF[:half])), ht(hrows(PF[half:])), hw, hw), Spacer(1, 2),
          p(f'<b>Read the risk column, not the weight column.</b> Weights run from {pct(min(x["weight"] for x in PF), 1)} to {pct(PF[0]["weight"], 1)}, but the '
            f'{sum(1 for x in PF if not x["binding"])} holdings outside the capped digital networks each carry a similar {pct(min(x["risk_share"] for x in PF if not x["binding"]), 1)}–'
            f'{pct(X["risk_share_max"], 1)} of risk: that is the design. NVIDIA gets {pct([x for x in PF if x["key"] == "NVDA"][0]["weight"], 1)} because it swings far more than a hospital '
            f'operator. The 8 network companies carry less ({pct(min(x["risk_share"] for x in PF), 1)}–{pct(max(x["risk_share"] for x in PF if x["binding"]), 1)}) because their kind '
            f'is at the 25% cap. Chips are {pct(bt["Semiconductors"], 0)} of the money and {pct(sum(x["risk_share"] for x in PF if x["ctype"] == "Semiconductors"), 0)} of the risk. '
            f'Together they behave like about {R["eff_bets"]:.0f} independent groups. Weights are reset quarterly; companies we rejected or are watching are in the supporting proposal.', tiny), Spacer(1, 4)]
cost = R['costs']['v4']
# how we build the portfolio (funnel counts from map/funnel4_out.txt / universe4.json)
U4 = json.load(open('map/universe4.json')); st_ = [r['stage'] for r in U4]
n_uni = sum(x != 'Outside universe' for x in st_); n_m = n_uni - sum(x.startswith('Reject (M') for x in st_)
n_rej = sum(x.startswith('Reject (V') for x in st_); n_wl = sum(x.startswith('Watchlist') for x in st_); n_el = st_.count('Eligible')
assert n_m - n_rej - n_wl == n_el, (n_m, n_rej, n_wl, n_el)
FN = R['funnel']; assert (FN['universe'], FN['m_pass'], FN['eligible'], FN['held']) == (n_uni, n_m, n_el, NH)
letter = ParagraphStyle('letter', parent=base, fontName='Helvetica-Bold', fontSize=26, leading=27, textColor=GREEN)
stp = ParagraphStyle('stp', parent=base, fontName='Helvetica-Bold', fontSize=9.2, leading=11, textColor=DARK)
num = ParagraphStyle('num', parent=base, fontName='Helvetica-Bold', fontSize=11.5, leading=13.5, textColor=DARK)
numl = ParagraphStyle('numl', parent=base, fontSize=6.6, leading=8, textColor=MUTED)
arw = ParagraphStyle('arw', parent=base, fontName='DJ', fontSize=12, leading=14, textColor=GREEN, alignment=TA_CENTER)
mvp = [('M', 'Map the capacity', 'Find the companies that own, run or supply essential services: up to the 20 largest listed (at least US$1bn) in each of eight kinds, '
              'anywhere in the world. Keep those that earn at least half their revenue from that service and generate cash.',
        f'{n_uni} → {n_m}', f'{n_uni} screened · {n_m} fit the theme'),
       ('V', 'Verify the merit', f'Check each company is a sound investment: survives a debt stress test sized to its industry, and compares well with its own peers on '
              f'price and quality; tradeable; sound governance.',
        f'{n_m} → {n_el}', f'{n_el} eligible · {n_rej} rejected · {n_wl} on watch'),
       ('P', 'Position the risk', 'Add eligible companies in merit order, only if each one improves diversification. Size them so every holding adds a similar '
              'share of risk, within limits: 20% per company or group, 25% per kind of service, about 3% cash.',
        f'{n_el} → {NH}', f'{NH} held · {FN["watch_p"]} on watch (added too little diversification)')]
cw3, ga = (CW - 2*14) / 3, 14
def hdr(L, t):
    h = Table([[p(L, letter), p(t, stp)]], colWidths=[27, cw3 - 39]); h.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('LEFTPADDING', (1, 0), (1, 0), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    return h
r0, r1, r2 = [], [], []
for i, (L, t, d, n_, nl) in enumerate(mvp):
    r0.append(hdr(L, t)); r1.append(p(d, small)); r2.append([p(n_, num), p(nl, numl)])
    if i < 2: r0.append(''); r1.append(p('→', arw)); r2.append(p('→', arw))
fun = Table([r0, r1, r2], colWidths=[cw3, ga, cw3, ga, cw3])
cols = (0, 2, 4)
fun.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                         ('TOPPADDING', (0, 0), (-1, 0), 5), ('TOPPADDING', (0, 1), (-1, 1), 2), ('BOTTOMPADDING', (0, 1), (-1, 1), 5),
                         ('TOPPADDING', (0, 2), (-1, 2), 5), ('BOTTOMPADDING', (0, 2), (-1, 2), 5),
                         *[('BACKGROUND', (j, 0), (j, 1), SOFT) for j in cols], *[('BACKGROUND', (j, 2), (j, 2), colors.HexColor('#DCEBE2')) for j in cols],
                         *[('LEFTPADDING', (j, 0), (j, -1), 0) for j in (1, 3)], *[('RIGHTPADDING', (j, 0), (j, -1), 0) for j in (1, 3)],
                         *[('VALIGN', (j, 1), (j, 2), 'MIDDLE') for j in (1, 3)]]))
story += [bandrow(f'M · V · P: HOW WE BUILD THE PORTFOLIO · {n_uni} COMPANIES SCREENED → {NH} HELD · THE SAME PUBLISHED RULES FOR EVERY COMPANY', CW), Spacer(1, 3), fun,
          Spacer(1, 3), p('Judgement sits in the published rules, not in picking favourites. Holdings are reviewed monthly and may be removed after a material '
            'event (with the reason logged), but are never resized by hand; weights are reset quarterly. Every company\'s result is in the supporting proposal.', tiny), Spacer(1, 5)]
risks = [('Market', f'Share prices can fall sharply. In 36 years of industry-level history the worst 12 months lost {pct(-ps["cap"]["worst12"], 0)} and the deepest fall was {pct(-ps["cap"]["maxdd"], 0)}.'),
         ('Concentration', f'Digital networks are at the fund\'s 25% cap; data-centre spending drives about {pct(bt["Semiconductors"] + bt["Grid & power equipment"], 0)} of the fund but more of its past return '
          f'(memory-chip makers are near a cyclical peak); '
          f'Saudi Arabia {pct(cnt.get("SA", 0), 0)} and US health policy about {pct(sum(x["weight"] for x in PF if x["key"] in ("HCA", "EHC")), 0)}.'),
         ('Currency', f'About {pct(1 - R["ph_now"] - 0.03, 0)} is in foreign currencies and not hedged; a stronger peso lowers returns in pesos.'),
         ('Liquidity', 'Each holding is kept small enough to sell within a week without moving its price much (sized for a ₱1bn fund), and about 3% '
          'is kept in cash. Many goals may fall due on the same dates (for example December); the manager sees goal dates in advance and can raise cash early.'),
         ('Country and regulation', 'Companies in emerging markets, including some partly owned by governments, face policy and sanctions risk.'),
         ('Selection', 'Companies are screened with one data provider and thresholds set by the team; the past results shown include hindsight.')]
rw = CW*0.56
fees = [('Management fee (proposed)', '1.50% a year of fund value, accrued daily'), ('Trading costs (modelled)', f'about {pct(cost["trading_pa"])} a year'),
        ('Dividend withholding (modelled)', f'about {pct(cost["wht_pa"])} a year'), ('Subscription / redemption fee', 'None proposed'),
        ('Minimum holding period', 'None proposed; 5 years+ is a recommendation'), ('Estimated all-in cost', f'about {pct(tot, 1)} a year')]
fw = CW - rw - 8
red = [bandrow('FEES AND CHARGES', fw), kv(fees, [fw*0.45, fw*0.55], boldrows=(fees[-1],)), Spacer(1, 3), bandrow('SUBSCRIPTIONS AND REDEMPTIONS (PROPOSED)', fw),
       p('Buy units with a one-time amount, a regular monthly plan, or top-ups whenever you like. Sell on any business day at that day\'s price '
         'per unit (NAVPU); the money is paid on day 6, end of day, in line with BPI\'s peso global equity funds. A missed monthly contribution '
         'does not change your goal date and is not taken automatically later.', small), Spacer(1, 3),
       p('<b>Compared with other products</b> a young Filipino can buy today: see page 1.', small)]
story += [two([bandrow('KEY RISKS', rw), kv(risks, [rw*0.22, rw*0.78], right_cols=())], red, rw, fw), Spacer(1, 4)]
story += [p('<b>Sources.</b> Company data: stockanalysis.com (S&amp;P Global Market Intelligence), 8 Oct 2026. Prices: Yahoo Finance total returns and PSE Edge '
            '(with cash dividends), converted to pesos weekly. Benchmark: FlexShares STOXX Global Broad Infrastructure Index Fund (NFRA), Yahoo Finance '
            'adjusted close in pesos; cross-check iShares Global Infrastructure ETF (IGF) returned ' + pct(B['igf']['stats']['cagr'], 1) + ' a year. '
            'Cash: BSP policy rate minus 0.50 pt. Industry-level history: Kenneth French Data Library and BIS exchange rates. Single-company limit: '
            'BSP Circular No. 1234, Series of 2026 (20 May 2026), a 20% ceiling, not a target. Comparison funds: BPI Wealth fund pages and Pag-IBIG. '
            'Industry classifications assigned by the team. Dividend tax rates approximate, to be confirmed.', tiny), Spacer(1, 2),
          p('<b>Team Los Angeles 76ers</b>, Ateneo de Manila University: Prince Angelo C. Rivera · Luis Tengonciang · Karol Josef Fuñe · Eric Fabian Thirdy Mendez.', tiny)]
story += [PageBreak()] + annex()
doc.build(story); print('built')
