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

# ======================= PAGE 1 · THE PROBLEM, AND THE FUND THAT ANSWERS IT =======================
PER = dict(pay=2000, months=60, goal=120000)                 # persona plan (illustrative)
pm = {k: round(PER['goal'] * dca[k], -3) for k in ('median', 'p5', 'worst')}; pg = round(PER['goal'] * dcg['worst'], -3)
story += [p('<b>Firsts Fund</b> helps early-career Filipinos invest for the big “firsts” five or more years away (taking Mom and Dad abroad, a first car, a first '
            'home, a first business) by owning, from ₱100, the companies around the world that run the services everyday life depends on.', lead), Spacer(1, 5),
          tiles([('₱100', 'to start and per top-up (proposed)'), (f'{NH}', f'companies in {len(R["by_country"])} markets, held directly'), ('1.50%', 'a year, one fee (proposed)'),
                 ('5+ years', 'recommended horizon, not a lock-in'), ('Pesos', 'every key number shown in pesos, not just %')], 6), Spacer(1, 6)]
p1l = [bandrow('THE PROBLEM', L2), Spacer(1, 3),
  p('<b>At 22, your biggest asset is not money.</b> It is forty years of future pay: in pesos, tied to one economy, impossible to sell. A young '
    'Filipino already depends almost entirely on the Philippines, without ever choosing to. Then look at what is easy to buy: savings and '
    'money-market funds that park the money, the local stock index that adds even more Philippine exposure, or crypto. Two doors, '
    '<b>park or gamble</b>, and the middle, where a long-term goal belongs, is empty.', xb), Spacer(1, 3),
  p('<b>Access is no longer the problem.</b> BPI cut its UITF minimum from ₱10,000 to ₱1,000 in 2023; some platforms start at ₱50. PSE accounts rose '
    '50.1% in a year, and 26.5% now belong to 18-to-29-year-olds. Young Filipinos are arriving. What has not changed is what they find when they arrive.', xb), Spacer(1, 4),
  boxed(p('“Number one: you have to get global exposure… by diversifying some of that local exposure, you\'re actually lowering your volatility.” '
          '<font name="Helvetica" color="#58635C">— Joaquin Rossano U. Veluz, Sun Life Investment Management and Trust Co.</font>', quote), L2, SOFT), Spacer(1, 5),
  bandrow('WHY A SAVER SHOULD THINK ABOUT RISK DIFFERENTLY', L2), Spacer(1, 3),
  p('Most risk questions are built to protect a balance you already have, which is right for someone living off their savings. A young saver '
    'does the opposite: they add money every month. <b>For them, a fall early on means buying more units at a lower price.</b>', xb), Spacer(1, 2),
  p(f'<b>We tested it.</b> We took the fund\'s own {X["months"]} monthly results and shuffled their order {X["n_shuffles"]:,} times, so the total return stays the '
    f'same and only the timing changes. How much a strong first half helped the final amount:', xb), Spacer(1, 2),
  grid([('Someone saving ₱1,000 a month', f'it hurt: {X["corr_contrib"]:.2f} (strongly negative)'.replace('-', '−')),
        ('Someone withdrawing ₱900 a month', f'it helped: +{X["corr_withdraw"]:.2f} (strongly positive)')], [L2*0.48, L2*0.52]), Spacer(1, 2),
  p('Same returns, opposite outcomes. This does not mean falls are good; a fall that never recovers hurts everyone. It means a saver with years to go '
    'should not be judged by the same yardstick as a retiree.', xs), Spacer(1, 5),
  bandrow('WHAT THIS MEANS FOR THE FUND', L2), Spacer(1, 3),
  p('<b>Success is people still saving in year five.</b> Contributions decide where a young saver ends up, so everything in how people find the '
    'fund (page 2) and how they use it (page 3) is built to keep them going.', xb), Spacer(1, 2),
  p(f'<b>Numbers in pesos.</b> “−{bad*100:.0f}%” means little to a first-jobber; “₱{bad*5000:,.0f} on a ₱5,000 balance, about six weeks of saving” does. We show the '
    'peso figure next to every percentage that matters.', xb)]
p1r = [bandrow('THE FUND', R2), Spacer(1, 3),
  p(f'<b>The proposed Firsts Fund</b> is a peso UITF that owns, directly, {NH} listed companies around the world that run essential, '
    'hard-to-replace services: power and water, phone and internet networks, ports, airports, hospitals, and the equipment behind them. '
    '<b>₱100 to start. One fee. No fund-of-funds layer.</b>', xb), Spacer(1, 3),
  grid([('1 · Map', f'{n_uni0} of the largest listed companies in 8 kinds of essential service'), ('2 · Check the fit', f'{n_m0} earn mostly from that service and generate cash'),
        ('3 · Verify', f'{n_el0} pass a debt stress test and compare well with peers on price and quality'), ('4 · Position', f'{NH} held, sized so no single company dominates the risk')],
       [R2*0.27, R2*0.73]), Spacer(1, 2),
  p('Same published rules for every company, including the Philippines\' ICTSI. Full process on page 5.', xs), Spacer(1, 5),
  tiles([(pct(v4['cagr'], 1), 'a year, today\'s holdings, past 5 yrs (hindsight)'), (pct(nf['cagr'], 1), 'benchmark: global infrastructure fund')], 4, R2), Spacer(1, 2),
  tiles([(pct(XS['cagr'], 1), 'same, without chip and grid-equipment makers'), (pct(ps['cap']['cagr'], 1), 'a year over 36 years, industry-level')], 4, R2), Spacer(1, 3),
  p(f'<b>Read honestly.</b> The companies were picked in 2026 and tested backwards, so {pct(v4["cagr"], 1)} is a best case, not a forecast. The two lower '
    f'numbers are the checks: the result does not rest on chipmakers, and over 36 years the approach grew about as fast as the world market '
    f'({pct(ps["mkt"]["cagr"], 1)}) with a worst year of −{bad*100:.0f}%. Expect market-like growth from businesses people cannot do without.', xs), Spacer(1, 5),
  bandrow('HOW IT COMPARES WITH WHAT IS AVAILABLE TODAY', R2), Spacer(1, 1),
  grid([('Money market fund', 'Short-term debt; ₱50–1,000', 'Safe, but likely to trail rising prices over five years.'),
        ('Pag-IBIG MP2', 'Government savings; ₱500', 'Tax-free and never negative. Better for a first 3–5 years away; we point people there.'),
        ('Local stock index fund', 'PSEi shares; ₱1,000', 'Adds more of the Philippine exposure a young earner already has.'),
        ('Global fund-of-funds', 'Owns other funds; ₱1,000', 'Global, but with a second layer of fees, and you cannot see what you own.'),
        ('Firsts Fund (proposed)', f'{NH} companies directly; ₱100', 'Global, in pesos, one fee, and you can see every company.')],
       [R2*0.27, R2*0.30, R2*0.43], head=['Product', 'What it is; minimum', 'What it does not solve']), Spacer(1, 2),
  p('A comparison of design, not of returns: ours are simulated, theirs are real.', xs)]
story += [two(p1l, p1r, L2, R2, G2), Spacer(1, 4),
  p('Sources: PSE investor profile 2024 (via Manila Bulletin, 2025); BPI Wealth. Shuffle test: v4 holdings\' monthly results after costs; the result comes '
    'from the arithmetic of saving versus withdrawing, not from how high the returns were. 36-year history: Kenneth French Data Library, in pesos.', tiny), PageBreak()]

# ======================= PAGE 2 · THE HOOK: WHO IT IS FOR, AND HOW THEY FIND IT =======================
p2l = [bandrow('ONE MESSAGE', L2), Spacer(1, 4),
  p('Fund your firsts.', big2), p('<font color="#58635C">Pondohan ang mga una mo. There will always be a new first.</font>', h2), Spacer(1, 3),
  p('Retirement is too far away for a 22-year-old to picture, and every product already uses it. <b>A first is different: it has a name, a peso '
    'cost and a date.</b> The fund\'s holdings support that promise in the background; the details live in the fact sheet and annex.', xb), Spacer(1, 5),
  bandrow('WHO IT IS FOR', L2), Spacer(1, 3),
  p('<b>Graduating students and early-career professionals</b> with regular income, a goal at least five years away, and the risk tolerance for '
    'a stock fund. Not every beginner: money needed sooner, or emergency savings, belongs elsewhere. Anyone further along with a five-year goal can use it too.', xb), Spacer(1, 3),
  boxed([p('<b>Meet Bea (illustrative).</b> 23, first job as a junior accountant, takes home about <b>₱28,000 a month</b>.', xs), Spacer(1, 2),
         grid([('Rent and bills', '₱8,000'), ('Food', '₱7,000'), ('Helping at home', '₱4,000'), ('Transport', '₱3,000'), ('Emergency savings', '₱2,000'),
               ('Personal', '₱2,000'), ('<b>Her first: Japan with her parents in 5 years</b>', '<b>₱2,000</b>')], [L2*0.64, L2*0.24], bold_first=False, right=(1,))],
        L2, SOFT), Spacer(1, 5),
  bandrow('CHOOSING A FIRST', L2), Spacer(1, 3),
  p('Each user starts with <b>one main first</b>: picked from suggestions, typed in freely, or found with <b>“Help me choose my first”</b>. Saving for '
    'several firsts at once is on the roadmap (page 3).', xb), Spacer(1, 2),
  grid([('Take Mom and Dad abroad', 'First car', 'First home'), ('First business', 'First time sending money home and keeping some', 'Something else: type it in')],
       [L2/3]*3, bold_first=False), Spacer(1, 5),
  bandrow('WHY WE BUILD CONFIDENCE, NOT HYPE', L2), Spacer(1, 3),
  p('A study of Filipino students (Susada, 2025) found that feeling capable, through knowledge and confidence, was the strongest driver of '
    'intending to invest; pressure from friends and family was not. The BSP also measures financial literacy rising (74%, from 69%). So we '
    'explain, we do not push: no raffles, cash rewards, leaderboards or countdown timers in the launch. Rewards stay a future idea if costs and '
    'approvals allow.', xb)]
p2r = [bandrow('THE GOAL CALCULATOR: THE CENTRE OF THE CAMPAIGN', R2), Spacer(1, 3),
  p('Name the first, enter the cost and the date (at least five years away). The calculator shows two things side by side, with its assumptions on screen:', xb), Spacer(1, 2),
  grid([('Contributions only', f'₱{PER["goal"]:,} ÷ {PER["months"]} months = <b>₱{PER["pay"]:,} a month</b>. No growth assumed.'),
        ('With illustrative growth', 'At an assumed 6% a year, about <b>₱1,710 a month</b>. An example, not a promise.'),
        ('Prices rise (optional)', f'At 4% a year inflation the trip costs about ₱146,000 by then: ₱2,430 a month, contributions only.')],
       [R2*0.30, R2*0.70]), Spacer(1, 3),
  p('<b>Before committing, clear risk information in pesos.</b> Bea\'s plan (₱2,000 a month for 5 years, ₱120,000 paid in), run through every '
    f'five-year stretch of our 36-year history ({dca["n"]} of them):', xb), Spacer(1, 2),
  grid([('Typical outcome', f'₱{pm["median"]:,.0f}'), ('1 in 20 stretches ended at or below', f'₱{pm["p5"]:,.0f}'),
        ('Worst stretch (ending early 2009)', f'₱{pm["worst"]:,.0f}'), ('Worst, with the goal service (page 3)', f'₱{pg:,.0f}')],
       [R2*0.68, R2*0.32], right=(1,)), Spacer(1, 2),
  p('Industry-level history, after the fee and costs; not a forecast.', xs), Spacer(1, 5),
  bandrow('WHERE PEOPLE FIND IT: EVERY CHANNEL LEADS TO THE CALCULATOR', R2), Spacer(1, 1),
  grid([('Campus talks and caravans', 'On-site financial-literacy sessions with student organisations, close to graduation.'),
        ('Early-career workplace sessions', 'Financial-wellness talks at employers, including companies on BPI payroll, timed with a first job.'),
        ('Short-form social content', 'Short, plain videos built on Bea\'s story; creators support but do not lead, to keep costs down.'),
        ('BPI App, with “Chat with us”', 'Online visitors can ask a person before they start.')], [R2*0.36, R2*0.64]), Spacer(1, 3),
  boxed([p('<b>Launch timing: the 13th month.</b>', xs),
         p('Arrives every December and is money no first-jobber budgeted. <i>“Your 13th month was never in the budget. Give it a first.”</i> '
           'December opens the account; the monthly plan keeps it going.', xs)], R2, SOFT), Spacer(1, 5),
  bandrow('THE BUSINESS CASE FOR A ₱100 MINIMUM', R2), Spacer(1, 3),
  p(f'₱100 at 1.50% earns BPI ₱1.50 a year, so the value is in steady monthly saving. A ₱2,000-a-month plan like Bea\'s reaches about '
    f'₱{pm["median"]:,.0f} in a typical five-year stretch, roughly <b>₱{round(pm["median"]*0.015, -2):,.0f} a year</b> in fees. The fund also needs '
    'seed money and a minimum size before opening, to cover custody and audit costs. A sketch, not a costed model.', xs)]
story += [two(p2l, p2r, L2, R2, G2), Spacer(1, 4),
  p('Bea and her budget are illustrative. Calculator growth and inflation rates are example assumptions shown to the user. Sources: Susada (2025), '
    'n = 191, one institution, measures intention; BSP Consumer Finance and Inclusion Survey 2025.', tiny), PageBreak()]

# ======================= PAGE 3 · THE HABIT: HOW THEY KEEP GOING =======================
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
    a1 = [bandrow('A1 · EVIDENCE BASE: EVERY LOAD-BEARING CLAIM AND ITS SOURCE', A), Spacer(1, 1),
      grid([('Young Filipinos are arriving', '18–29 = 26.5% of PSE accounts, from 19.5%; PSE accounts +50.1% in a year', 'PSE investor profile 2024, via Manila Bulletin (2025)'),
            ('Access and literacy improved', 'BPI UITF minimum ₱10,000 → ₱1,000 (2023); 74% answer half the literacy questions, from 69%', 'BPI Wealth; BSP CFIS 2025'),
            ('Cash loses in real terms', 'Inflation 6.2% in July 2026', 'PSA (2026)'),
            ('Risk appetite went to crypto', 'Awareness 20% of adults, from 6%; 46% of owners are 18–34', 'BSP CFIS 2025; Triple-A'),
            ('Confidence, not peers, drives investing', 'Strongest driver β = 0.502 (p < .001); peer pressure not significant', 'Susada (2025), n = 191'),
            ('A saver gains from an early fall', f'Link between a strong start and the final amount: {X["corr_contrib"]:.2f} saving, +{X["corr_withdraw"]:.2f} withdrawing'.replace('-', '−'), f'Our shuffle test, {X["n_shuffles"]:,} orders')],
           [A*0.30, A*0.42, A*0.28], head=['Claim', 'Figure', 'Source']), Spacer(1, 4),
      bandrow('A2 · WHAT WE KILLED, AND WHY', A), Spacer(1, 1),
      grid([('“The suitability check is the barrier”', 'Access clearly improved; the claim argued against its own evidence.'),
            ('“Participation fell 36% → 23%”', 'Could not be confirmed from BSP releases; not used.'),
            ('A fixed 30% Philippines share', 'No basis. Countries now follow from the same tests (ICTSI 4.8%).'),
            ('A 10% cash reserve; 16 fixed holdings', 'About 3% cash covers withdrawals; the count follows from the rules (31).'),
            ('“Show the bad year first” as its own step', 'Consultants: balanced risk information, not a scare step. Now in the calculator.'),
            ('Streaks and a months-funded counter', 'Replaced by contributions, value, gain or loss and goal progress.'),
            ('Sukli at launch, through e-wallets', 'A future enhancement, tested inside the BPI App first.'),
            ('Automatic glidepath with set transfer rates', 'The user decides, after a yearly review; no promised schedule or protection.'),
            ('A blanket “non-tech” label', 'Technology exposure is assessed, not excluded (chips 8%).')],
           [A*0.40, A*0.60]), Spacer(1, 4),
      bandrow('A6 · WHAT WOULD CHANGE OUR MIND', A), Spacer(1, 3),
      p('The shuffle result is arithmetic. But the case rests on people <b>continuing to contribute</b>, modelled as 60 uninterrupted monthly payments, '
        'which no source we found measures for this group. If people stop much more often, the fund\'s risk level should come down. How often people '
        'keep going through a losing year is the first thing we would test with real data, and the honest weak point of this proposal.', xs)]
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
      p('<b>Suitability.</b> We are not asking BPI to relax the Client Suitability Assessment, to allow an education-based override, or to sell an '
        'aggressive fund to a client rated conservative. We propose recording the investor\'s horizon and contribution plan in the suitability file, '
        'with an audit trail, and letting the goal service carry risk down as the date approaches.', xs), Spacer(1, 2),
      p('<b>Sukli (future).</b> Starts inside the BPI App. Needs clear, revocable consent, rules on which purchases count, and a regulated place for '
        'spare change to wait before it is invested; e-wallets only after that works and partner agreements exist.', xs), Spacer(1, 2),
      p('<b>Reports.</b> Separate in-app progress view, transaction statements, and fund disclosures, with fund reports at least quarterly.', xs)]
    out += [two(a1, a2, A, B, 8), Spacer(1, 4),
            p('<b>Team Los Angeles 76ers</b>, Ateneo de Manila University: Prince Angelo C. Rivera · Luis Tengonciang · Karol Josef Fuñe · '
              'Eric Fabian Thirdy Mendez. A FinQuest 2026 proposal; not an offer, solicitation or investment advice, and not a BPI Wealth product.', tiny)]
    return out
