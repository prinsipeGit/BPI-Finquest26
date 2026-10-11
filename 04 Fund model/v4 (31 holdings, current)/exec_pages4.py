# Executive summary pages (1-3) and annex (6) for the Firsts Fund fact sheet. exec()'d inside build_factsheet4.py so it
# shares its styles and data (R, PF, bt, v4, nf, ps, XS, X, NH, n_uni0, n_m0, n_el0, helpers p, kv, two, boxed, bandrow).
# Restores the Phase 1 "Hook" (marketing) and "Habit" (customer experience) content, rebuilt on v4 facts (10 Oct 2026).

lead = ParagraphStyle('lead', parent=base, fontSize=9.4, leading=12.4)
xb = ParagraphStyle('xb', parent=base, fontSize=8.1, leading=10.8)
xs = ParagraphStyle('xs', parent=base, fontSize=7.5, leading=9.6)
h2 = ParagraphStyle('h2', parent=base, fontName='Helvetica-Bold', fontSize=8.6, leading=10.6, textColor=GREEN, spaceBefore=1)
kn = ParagraphStyle('kn', parent=base, fontName='Helvetica-Bold', fontSize=14, leading=16, textColor=DARK, alignment=TA_CENTER)
kl = ParagraphStyle('kl', parent=base, fontSize=6.6, leading=8, textColor=MUTED, alignment=TA_CENTER)
quote = ParagraphStyle('q', parent=base, fontName='Helvetica-Oblique', fontSize=7.4, leading=9.6, textColor=DARK)
big2 = ParagraphStyle('big2', parent=base, fontName='Helvetica-Bold', fontSize=11.5, leading=14, textColor=GREEN)
xc = ParagraphStyle('xc', parent=cell, fontSize=7.4, leading=9.2); xcb = ParagraphStyle('xcb', parent=xc, fontName='Helvetica-Bold')
xcr = ParagraphStyle('xcr', parent=xc, alignment=TA_RIGHT)

def grid(rows, widths, head=None, bold_first=True, right=()):
    data = []
    if head: data.append([p(h, xcb) for h in head])
    for r_ in rows:
        data.append([p(str(c), xcb if (i == 0 and bold_first) else (xcr if i in right else xc)) for i, c in enumerate(r_)])
    t = Table(data, colWidths=widths)
    st = [('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 2.5), ('RIGHTPADDING', (0, 0), (-1, -1), 2.5),
          ('TOPPADDING', (0, 0), (-1, -1), 1.6), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.6), ('LINEBELOW', (0, 0), (-1, -1), 0.3, RULE)]
    if head: st.append(('BACKGROUND', (0, 0), (-1, 0), SOFT))
    t.setStyle(TableStyle(st)); return t

def tiles(items, height_pad=5, width=None):
    width = width or CW
    t = Table([[[p(a, kn), p(b, kl)] for a, b in items]], colWidths=[width/len(items)]*len(items))
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SOFT), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), height_pad),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), height_pad), ('LINEAFTER', (0, 0), (-2, -1), 0.6, colors.white)]))
    return t

L2, R2 = CW*0.555, CW*0.425; G2 = CW - L2 - R2
bad = -ps['cap']['worst12']                                  # 36-year industry-level worst 12 months (positive number)
dca, dcg = PX['contrib']['dca'], PX['contrib']['dca_glide']

# ======================= PAGE 1 · THE FUND AT A GLANCE (built from the BPI meeting notes) =======================
PER = dict(pay=2000, months=60, goal=120000)                 # persona plan (illustrative)
pm = {k: round(PER['goal'] * dca[k], -3) for k in ('median', 'p5', 'worst')}; pg = round(PER['goal'] * dcg['worst'], -3)
story += [p('<b>The proposed Firsts Fund</b> is a peso-denominated global equity UITF for graduating students and early-career professionals saving '
            'for a meaningful “first” at least five years away, such as taking their parents abroad, a first car, a first home or a first business.', lead), Spacer(1, 5),
          tiles([('₱100', 'to start and per top-up (proposed)'), (f'{NH}', f'companies in {len(R["by_country"])} markets, held directly'), ('1.50%', 'a year, one fee (proposed)'),
                 ('5+ years', 'recommended horizon, not a lock-in'), ('Pesos', 'key numbers shown in pesos, not just %')], 6), Spacer(1, 6)]
p1l = [bandrow('WHO IT IS FOR', L2), Spacer(1, 3),
  p('<b>Graduating students to entry-level professionals</b> with regular income, a goal at least five years away, and the risk tolerance for a '
    'stock fund. It is not for every beginner: money needed within five years, or emergency savings, belongs in a lower-risk product. People '
    'further along in their careers can use it too, as long as their goal is five or more years away.', xb), Spacer(1, 5),
  bandrow('THE NEED IT ADDRESSES', L2), Spacer(1, 3),
  p('A young earner\'s salary, savings and future plans are all in pesos. The products that are easiest to start with are mostly savings or '
    'money-market funds, built for short-term goals. Global stock funds are usually reached through funds that hold other funds, with a second '
    'layer of fees and a higher minimum. Firsts Fund offers a long-term, global option from ₱100, with one fee, tied to a goal the saver chooses.', xb), Spacer(1, 5),
  bandrow('HOW THE FUND RUNS, END TO END', L2), Spacer(1, 1),
  grid([('1 · Money in', 'Saver sets a monthly plan or tops up in the BPI App. Money is pooled in one UITF, priced daily per unit (NAVPU).'),
        ('2 · Choose companies', 'The M · V · P review (page 5) runs monthly and decides which companies the fund may hold.'),
        ('3 · Set weights', 'Weights are reset quarterly so each holding adds a similar share of risk, within the limits.'),
        ('4 · Keep cash', 'About 3% stays in cash to pay withdrawals without forced selling.'),
        ('5 · Money out', 'Withdraw any business day at that day\'s price; paid on day 6 (T+5). No exit fee, no lock-in.'),
        ('6 · Report', 'In-app progress view, transaction statements, and fund reports at least quarterly.')], [L2*0.25, L2*0.75]), Spacer(1, 5),
  bandrow('WHAT A SAVER SEES, IN PESOS', L2), Spacer(1, 3),
  p(f'Every key figure is shown in pesos, not only percentages. For example, a fall like the worst 12 months in our 36-year industry history '
    f'(−{bad*100:.0f}%) on a ₱5,000 balance would be <b>₱{bad*5000:,.0f}</b>. Risk is explained clearly before the saver commits, alongside balanced '
    'scenarios, without dwelling on the downside.', xb)]
p1r = [bandrow('WHAT THE FUND OWNS', R2), Spacer(1, 3),
  p(f'{NH} listed companies around the world that run essential, hard-to-replace services people use every day: power and water, phone and '
    'internet networks, ports, airports, hospitals, and the equipment behind them. Technology exposure is assessed like everything else, not '
    'automatically excluded.', xb), Spacer(1, 3),
  p('<b>Chosen by our M · V · P framework:</b>', xb), Spacer(1, 1),
  grid([('<font color="#0F7A45" size="11">M</font> · Map', f'Find essential-service companies worldwide: <b>{n_uni0}</b> screened, <b>{n_m0}</b> fit the theme'),
        ('<font color="#0F7A45" size="11">V</font> · Verify', f'Debt stress test, and value and quality against peers: <b>{n_el0}</b> pass'),
        ('<font color="#0F7A45" size="11">P</font> · Position', f'Add only what improves diversification, size by risk: <b>{NH}</b> held')],
       [R2*0.25, R2*0.75]), Spacer(1, 2),
  p('Same published rules for every company, including the Philippines\' ICTSI. Full process on page 5.', xs), Spacer(1, 5),
  tiles([(f'{pct(v4["cagr"], 1)} <font color="#58635C" size="10">vs</font> {pct(nf["cagr"], 1)}', 'a year over the past 5 years: today\'s holdings (backtested, hindsight) vs the benchmark, NFRA global infrastructure ETF')], 4, R2), Spacer(1, 2),
  tiles([(pct(XS['cagr'], 1), 'holdings without chip and grid-equipment makers, same 5 years'), (pct(ps['cap']['cagr'], 1), 'a year over 36 years, industry-level history (context)')], 4, R2), Spacer(1, 3),
  p(f'<b>How to read these.</b> These are backtested results, not actual fund performance. The companies were picked in 2026 and tested backwards, '
    f'so {pct(v4["cagr"], 1)} is a best case, not a forecast. The lower two numbers are checks: the result does not rest on chipmakers, and over 36 years the '
    f'approach grew about as fast as the world market ({pct(ps["mkt"]["cagr"], 1)}).', xs), Spacer(1, 5),
  bandrow('HOW IT COMPARES WITH WHAT IS AVAILABLE TODAY', R2), Spacer(1, 1),
  grid([('Money market fund', 'Short-term debt; from ₱50', 'Suited to short-term goals.'),
        ('Pag-IBIG MP2', 'Government savings; ₱500', 'Better for a goal 3–5 years away; we point people there.'),
        ('Local stock index fund', 'PSEi shares; ₱1,000', 'Philippine companies only.'),
        ('Global fund-of-funds', 'Owns other funds; ₱1,000', 'Global, with a second layer of fees.'),
        ('Firsts Fund (proposed)', f'{NH} companies directly; ₱100', 'Global, in pesos, one fee, every company named.')],
       [R2*0.27, R2*0.30, R2*0.43], head=['Product', 'What it is; minimum', 'Best suited to']), Spacer(1, 2),
  p('A comparison of design, not of returns.', xs)]
story += [two(p1l, p1r, L2, R2, G2), Spacer(1, 4),
  p('Backtests: weekly peso returns after the 1.50% fee, trading costs and dividend taxes. 36-year history: Kenneth French Data Library, in pesos; '
    'industry-level context only.', tiny), PageBreak()]

# ======================= PAGE 2 · MARKETING: ONE CLEAR MESSAGE =======================
p2l = [bandrow('ONE MESSAGE', L2), Spacer(1, 4),
  p('Fund your firsts.', big2), Spacer(1, 3),
  p('The central promise is simple: fund a meaningful future first by investing consistently. How the portfolio is built supports that promise in '
    'the background; the details live in the fact sheet (pages 4–5) and the annex.', xb), Spacer(1, 5),
  bandrow('WHO WE TALK TO', L2), Spacer(1, 3),
  p('Young Filipinos preparing for a meaningful long-term first. We separate a person\'s <b>first milestone</b> from their <b>first investment</b>: '
    'the fund suits savers with a five-year-plus goal and the appetite for a stock fund, not every beginner.', xb), Spacer(1, 3),
  boxed([p('<b>Meet Bea (illustrative).</b> 23, first job as a junior accountant, takes home about <b>₱28,000 a month</b>.', xs), Spacer(1, 2),
         grid([('Rent and bills', '₱8,000'), ('Food', '₱7,000'), ('Helping at home', '₱4,000'), ('Transport', '₱3,000'), ('Emergency savings', '₱2,000'),
               ('Personal', '₱2,000'), ('<b>Her first: Japan with her parents in 5 years</b>', '<b>₱2,000</b>')], [L2*0.64, L2*0.24], bold_first=False, right=(1,))],
        L2, SOFT), Spacer(1, 5),
  bandrow('HOW WE TALK ABOUT IT', L2), Spacer(1, 1),
  grid([('Plain language', 'No jargon in customer materials. Detailed method stays in the fact sheet and annex.'),
        ('Concrete, not abstract', '“Essential services” explained through real businesses: the power company that keeps the lights on, the port that brings in goods, the hospital down the road.'),
        ('No safety claims', 'Never “safe” or “guaranteed”. Five years is a recommended horizon, not a promise of a positive return.'),
        ('Pesos first', 'Examples in pesos, supported by percentages where useful.')], [L2*0.28, L2*0.72]), Spacer(1, 5),
  bandrow('WHAT PEOPLE SEE', L2), Spacer(1, 3),
  p('One central story (a relatable person and a concrete first), the goal calculator, and app mock-ups. These are the main visual assets; the '
    'numbers and methodology sit in the appendix.', xb)]
p2r = [bandrow('THE GOAL CALCULATOR: WHERE EVERY CHANNEL LEADS', R2), Spacer(1, 3),
  p('Name the first, enter the cost and the date (at least five years away). The calculator shows, with its assumptions on screen:', xb), Spacer(1, 2),
  grid([('Contributions only', f'₱{PER["goal"]:,} ÷ {PER["months"]} months = <b>₱{PER["pay"]:,} a month</b>. No growth assumed.'),
        ('With illustrative growth', 'At an assumed 6% a year, about <b>₱1,710 a month</b>. An example, not a promise.'),
        ('Prices rise (optional)', 'At 4% a year inflation the trip costs about ₱146,000 by then: ₱2,430 a month, contributions only.')],
       [R2*0.30, R2*0.70]), Spacer(1, 3),
  p(f'<b>Balanced scenarios before committing.</b> Bea\'s plan (₱2,000 a month for 5 years, ₱120,000 paid in) across every five-year stretch of our '
    f'36-year industry history ({dca["n"]} of them):', xb), Spacer(1, 2),
  grid([('Typical outcome', f'₱{pm["median"]:,.0f}'), ('1 in 20 stretches ended at or below', f'₱{pm["p5"]:,.0f}'),
        ('Weakest stretch (ending early 2009)', f'₱{pm["worst"]:,.0f}'), ('Weakest, with the goal service (page 3)', f'₱{pg:,.0f}')],
       [R2*0.68, R2*0.32], right=(1,)), Spacer(1, 2),
  p('Industry-level history, after the fee and costs; illustrative, not a forecast.', xs), Spacer(1, 5),
  bandrow('WHERE PEOPLE FIND IT', R2), Spacer(1, 1),
  grid([('Talks and caravans', 'On-site financial-literacy talks and campus caravans: the priority channel.'),
        ('Campus events', 'Sessions with student organisations, close to graduation.'),
        ('Early-career workplaces', 'Financial-wellness sessions at employers, timed with a first job.'),
        ('Short-form social', 'Kept lean (paid creator content is costly); creators support, not lead.'),
        ('BPI App, “Chat with us”', 'Online visitors can ask a person before starting.')], [R2*0.34, R2*0.66]), Spacer(1, 2),
  p('Each channel has one next step: try the goal calculator.', xs), Spacer(1, 5),
  bandrow('REWARDS AND PROMOS', R2), Spacer(1, 3),
  p('No raffles or financial rewards in the launch. The fund must be compelling without them; they stay optional future ideas if costs and approvals allow.', xs)]
story += [two(p2l, p2r, L2, R2, G2), Spacer(1, 4),
  p('Bea and her budget are illustrative. Calculator growth and inflation rates are example assumptions shown to the user.', tiny), PageBreak()]

# ======================= PAGE 3 · CUSTOMER EXPERIENCE: HOW THEY KEEP GOING =======================
p3l = [bandrow('WHERE IT LIVES: THE BPI APP', L2), Spacer(1, 3),
  p('The BPI App is the proposed home for Firsts Fund. Users are already verified there, so opening is a confirmation, not a new application, '
    'and pay usually lands in the same bank. All Firsts Fund screens would be new and are labelled as proposed.', xb), Spacer(1, 5),
  bandrow('SIGN-UP IN FOUR SCREENS', L2), Spacer(1, 1),
  grid([('1', 'Confirm identity from the existing BPI record; the standard suitability questions.'),
        ('2', 'Choose one main first: suggested, typed in, or “Help me choose my first”. A first under five years away gets a suggestion of a better-suited option, such as MP2 or a money market fund.'),
        ('3', 'See the monthly amount (contributions only, and with illustrative growth) and the risk in pesos.'),
        ('4', 'Set the monthly plan: amount and payday. Start from ₱100.')], [L2*0.06, L2*0.94]), Spacer(1, 5),
  bandrow('HOW MONEY GOES IN', L2), Spacer(1, 3),
  p('<b>At launch: a regular monthly plan plus top-ups whenever you like.</b> Either one alone is enough to keep a goal on track.', xb), Spacer(1, 2),
  p('<b>If a month is missed</b> (not enough money, or skipped), the goal date stays the same unless the user changes it. The app shows the missed '
    'amount and the updated projection, and offers three choices: a one-off top-up, a higher amount from now on, or a later goal date. '
    'Debits are never raised automatically.', xb), Spacer(1, 5),
  bandrow('WHAT THE USER SEES', L2), Spacer(1, 1),
  grid([('Main screen', 'Total put in · current value · gain or loss in pesos · progress to the goal'),
        ('Details', 'Units held, price per unit, every transaction'), ('Reminders', 'Payday and the goal date, never daily price moves'),
        ('Reports', 'In-app progress view; transaction statements; fund reports at least quarterly')], [L2*0.22, L2*0.78]), Spacer(1, 2),
  p('No streaks or counters that reset: missing a month should never feel like losing.', xs), Spacer(1, 5),
  bandrow('HOW WE WOULD KNOW IT WORKED', L2), Spacer(1, 1),
  grid([('Still contributing in month 60', '≥ 55%', '< 40%'), ('Kept contributing through the first losing quarter', '≥ 80%', '< 60%'),
        ('Chose “pause” over “withdraw”', '≥ 3 to 1', '< 1 to 1'), ('Months contributed in year 1 (median)', '≥ 10 of 12', '< 7'),
        ('Reached a first and set a new one', 'tracked', '')],
       [L2*0.60, L2*0.20, L2*0.20], head=['Measure', 'Target', 'Rethink if'], right=(1, 2)), Spacer(1, 2),
  p('Not counted as success: money gathered, accounts opened or app visits. Each can rise while people quietly stop saving.', xs)]
p3r = [bandrow('THE GOAL SERVICE (PROPOSED): WHY AND HOW', R2), Spacer(1, 3),
  p('<b>Why.</b> Early on, a fall gives a saver time to recover. Close to the goal date there is no time left, so a bad year then can shrink the goal. '
    'The fund itself cannot slow down for one person, because everyone in it has a different date.', xb), Spacer(1, 2),
  p('<b>How.</b> The change happens in the user\'s own account, not in the fund. Every year the app runs a goal review; two years before the date it sends an '
    'extra reminder. The user can then choose to move part of their units into a lower-risk BPI fund. <b>Nothing moves without their say-so</b>, '
    'and it reduces risk without guaranteeing the goal.', xb), Spacer(1, 2),
  p(f'<b>What it can do</b> (Bea\'s plan, 36-year history, illustrative): the worst five-year stretch improves from ₱{pm["worst"]:,.0f} to '
    f'₱{pg:,.0f}; the typical outcome is a little lower (₱{round(PER["goal"]*dcg["median"], -3):,.0f} vs ₱{pm["median"]:,.0f}), the price of less risk. A move to another '
    'fund is a future capability that still needs operational checks.', xs), Spacer(1, 5),
  bandrow('BEFORE SOMEONE WITHDRAWS', R2), Spacer(1, 3),
  boxed([p('<b>WITHDRAW · CONFIRM</b>  <font color="#58635C">(proposed screen, example numbers)</font>', xs), p('<b>₱26,500</b>', big2),
         p('You have put in ₱28,000 over 14 months; it is worth ₱26,500 today. You are ₱93,500 from your first: Japan with your parents, October 2031.', xs), Spacer(1, 1),
         p('Markets are down right now. If you keep saving, you are buying units at a lower price.', xs), Spacer(1, 2),
         p('<b>[ Pause the plan for 3 months ]</b>     Withdraw ₱26,500', xs)], R2, colors.white), Spacer(1, 2),
  p('Pausing comes first on screen; withdrawing is still one tap away. No holding period, no exit fee, nothing locked in.', xs), Spacer(1, 5),
  bandrow('REACHING A FIRST, THEN THE NEXT', R2), Spacer(1, 3),
  p('When the goal is reached the user can withdraw, or keep the balance invested and name the next first, without starting over. The app '
    'suggests a next first at that moment, because there will always be one.', xb), Spacer(1, 5),
  bandrow('LATER: FUTURE ENHANCEMENTS', R2), Spacer(1, 1),
  grid([('Sukli round-ups', 'Spare change from purchases set aside and invested at ₱100. Starts inside the BPI App to test it, before any e-wallet. '
                            'Needs consent, spending rules and a waiting account to be settled first.'),
        ('Several firsts at once', 'More than one goal per user, each with its own date and plan.'),
        ('Rewards', 'Only if the costs and approvals work; the fund must stand without them.')], [R2*0.28, R2*0.72])]
story += [two(p3l, p3r, L2, R2, G2), Spacer(1, 4),
  p('Screens and numbers on this page are proposed and illustrative. Measures and targets are the team\'s own, to be tested with real data.', tiny), PageBreak()]



def annex():
    out = []
    A = CW*0.49; B = CW - A - 8
    lim = R['portfolio']; grp_max = max(x['weight'] for x in lim if x['key'] in ('ICT', 'MWC', 'ENEL', 'ELE'))
    a1 = [bandrow('A1 · WHAT CHANGED AFTER THE BPI CONSULTATIONS', A), Spacer(1, 1),
      grid([('Horizon', 'Five years or longer throughout; a recommendation, not a lock-in or a promise of returns.'),
            ('Theme', 'No blanket “non-tech” claim; essential services and infrastructure, with technology exposure assessed.'),
            ('Selection', 'M · V · P kept; how many companies are held now follows from the rules (31), not a fixed number.'),
            ('Philippine share', 'The fixed 30% Philippines / 70% global split was dropped; countries follow from the same tests.'),
            ('Benchmark', 'NFRA global infrastructure ETF in pesos; world and Philippine indices shown as market context only.'),
            ('Performance', 'Labelled as backtested, never as actual fund results; calendar years and balanced risk shown.'),
            ('Persona and goals', 'Early-career saver; one main first; “Help me choose my first”; several firsts later.'),
            ('Calculator', 'Contributions-only plus an illustrative scenario, optional inflation, assumptions visible.'),
            ('Contributions', 'Monthly plan plus top-ups at launch; Sukli a future enhancement, starting in the BPI App.'),
            ('Missed months', 'Goal date unchanged; user chooses a top-up, a higher amount or a later date; no automatic increase.'),
            ('Dashboard', 'Contributions, value, gain or loss, goal progress; no streaks.'),
            ('Risk messaging', 'No “bad year first” step; clear risk information before committing, balanced scenarios.'),
            ('Goal service', 'Account-level, explained simply; yearly review and a reminder two years before; the user decides.'),
            ('Marketing', 'One message, “Fund your firsts”; talks, caravans, campus and workplaces first; no raffles at launch.'),
            ('Structure and platform', 'A peso global UITF; the BPI App as the proposed entry point; new screens labelled proposed.')],
           [A*0.27, A*0.73]), Spacer(1, 4),
      bandrow('A2 · STILL TO BE VALIDATED', A), Spacer(1, 1),
      grid([('Goal service', 'Moving units to a lower-risk fund for one saver needs operational checks; it is not promised as automatic.'),
            ('Sukli', 'Which purchases count, consent, where spare change waits, and when it moves; BPI App first.'),
            ('Running costs', 'Custody, currency and audit costs of holding foreign shares directly; the fund needs seed money and a minimum size.'),
            ('Dividend taxes', 'Rates are approximate; to be confirmed by a tax adviser.'),
            ('Staying power', 'How many savers keep contributing through a losing year; the first thing to test with real data.')],
           [A*0.27, A*0.73])]
    a2 = [bandrow('A3 · BACK-TEST METHOD AND ITS LIMITS', B), Spacer(1, 3),
      p(f'<b>Method.</b> Weekly peso returns including dividends, 1 Oct 2021 – 2 Oct 2026. Each quarter, weights were set using only the previous three '
        f'years of prices, under every limit ({R["rebalances"]} times). After the 1.50% fee, 0.30% trading cost and dividend taxes. Benchmark NFRA, in pesos.', xs), Spacer(1, 2),
      grid([('Selection is hindsight', 'Companies chosen in Oct 2026 with Oct 2026 data, priced backwards. Upper bound.'),
            ('Survivorship', 'Universe is today\'s largest companies; failures since 2021 are missing.'),
            ('One cycle', f'Chips are {pct(bt["Semiconductors"], 0)} of the money but {pct(sum(x["risk_share"] for x in lim if x["ctype"] == "Semiconductors"), 0)} of the risk, '
                          f'near a cyclical peak; without chips and grid equipment, {pct(XS["cagr"], 1)} a year.'),
            ('Tax estimate', 'Dividend tax rates are approximate; to be confirmed by a tax adviser.')], [B*0.28, B*0.72]), Spacer(1, 2),
      p('The first three make the figures look better than reality. We do not adjust for them; the 36-year industry history is our “what to expect”. '
        'Withdrawals and goal-service moves are ordinary sales of units, paid from cash first and then by selling shares, at the 0.30% trading cost.', xs), Spacer(1, 4),
      bandrow('A4 · LIMITS: RULE VS TODAY (ALL MET AT EVERY QUARTERLY RESET)', B), Spacer(1, 1),
      grid([('One company', '≤ 20% (BSP)', pct(PF[0]['weight'])), ('One group (e.g. Razon)', '≤ 20%', pct(grp_max)),
            ('One kind of capacity', '≤ 25%', pct(max(bt.values()))), ('Liquidity', 'sell in 5 days at 20% of volume', 'never binds at ₱1bn'),
            ('Operating cash', 'about 3%', '3.00%'), ('Country quota', 'none', f'Philippines {pct(R["ph_now"])} ({pct(R["ph_range"][0], 1)}–{pct(R["ph_range"][1], 1)})')],
           [B*0.36, B*0.32, B*0.32], head=['Limit', 'Rule', 'Actual'], right=(2,)), Spacer(1, 2),
      p(f'<b>Concentration, disclosed:</b> the {NH} holdings behave like about {R["eff_bets"]:.0f} independent groups; the two biggest common influences explain '
        f'{pct(R["top2_factor"], 0)} of the ups and downs. Holdings outside the capped networks each carry 3.3–3.9% of the risk.', xs), Spacer(1, 4),
      bandrow('A5 · REGULATORY POSITION', B), Spacer(1, 3),
      p('<b>The fund.</b> A peso UITF holding foreign shares directly, priced daily (NAVPU), with a 20% single-company ceiling per BSP Circular No. 1234 '
        '(2026). Our reading, not reviewed by counsel; any launch would need that review first.', xs), Spacer(1, 2),
      p('<b>Suitability.</b> The standard BPI suitability assessment applies unchanged. The saver\'s goal and date are recorded with their plan; '
        'goals under five years are pointed to lower-risk options.', xs), Spacer(1, 2),
      p('<b>Sukli (future).</b> Starts inside the BPI App. Needs clear, revocable consent, rules on which purchases count, and a regulated place for '
        'spare change to wait before it is invested; e-wallets only after that works and partner agreements exist.', xs), Spacer(1, 2),
      p('<b>Reports.</b> Separate in-app progress view, transaction statements, and fund disclosures, with fund reports at least quarterly.', xs)]
    out += [two(a1, a2, A, B, 8), Spacer(1, 4),
            p('<b>Team Los Angeles 76ers</b>, Ateneo de Manila University: Prince Angelo C. Rivera · Luis Tengonciang · Karol Josef Fuñe · '
              'Eric Fabian Thirdy Mendez. A FinQuest 2026 proposal; not an offer, solicitation or investment advice, and not a BPI Wealth product.', tiny)]
    return out
