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
story += [p('<b>Firsts Fund</b> helps early-career Filipinos invest for the big “firsts” five or more years away (taking Mom and Dad abroad, a first car, a first '
            'home, a first business) by owning, from ₱100, the companies around the world that run the systems everyday life depends on.', lead), Spacer(1, 5),
          tiles([('₱100', 'to start and per top-up'), (f'{NH}', f'companies, {len(R["by_country"])} markets, held directly'), ('1.50%', 'a year, one fee layer (proposed)'),
                 ('5+ years', 'goals only; shorter ones are routed elsewhere'), (f'₱{bad*5000:,.0f}', f'a bad year on ₱5,000, shown before sign-up')], 6), Spacer(1, 6)]
p1l = [bandrow('THE PROBLEM, AND THE ONE THAT ACTUALLY BINDS', L2), Spacer(1, 3),
  p('<b>At 22, your biggest asset is not money.</b> It is forty years of future earnings: in pesos, tied to one economy, impossible to sell '
    'or hedge. A young Filipino is already all-in on the Philippines, without ever choosing it. Then look at what they can reach: savings '
    'and money-market funds that park the money, the local index that adds more of the same bet, or crypto. Two doors, <b>park or gamble</b>, '
    'and the middle, where a long horizon belongs, is empty.', xb), Spacer(1, 3),
  p('<b>Access is no longer the binding constraint, and we will not pretend it is.</b> BPI cut its UITF minimum from ₱10,000 to ₱1,000 in 2023; '
    'some platforms start at ₱50. PSE accounts rose 50.1% in a year, and 26.5% now belong to 18-to-29-year-olds. The BSP measures financial '
    'literacy rising. Young Filipinos are arriving. What has not changed is the shape of the shelf they arrive at.', xb), Spacer(1, 4),
  boxed(p('“Number one: you have to get global exposure… by diversifying some of that local exposure, you\'re actually lowering your volatility.” '
          '<font name="Helvetica" color="#58635C">— Joaquin Rossano U. Veluz, Sun Life Investment Management and Trust Co.</font>', quote), L2, SOFT), Spacer(1, 5),
  bandrow('THE SECOND ERROR: THE RISK MODEL IS POINTED THE WRONG WAY', L2), Spacer(1, 3),
  p('The retail risk framework is built to protect a <b>balance</b>, which is right for someone drawing money out. A young saver is doing the '
    'opposite: paying in every month. For them, an early fall is a discount, not damage.', xb), Spacer(1, 2),
  p(f'<b>The proof is arithmetic.</b> We reordered the fund\'s own {X["months"]} monthly returns {X["n_shuffles"]:,} times. Reordering keeps the '
    f'total return exactly fixed; only the order changes. Correlation between the first half\'s return and final wealth:', xb), Spacer(1, 2),
  grid([('Saver paying in ₱1,000 a month', f'{X["corr_contrib"]:+.2f}'.replace('-', '−')),
        ('Retiree drawing ₱900 a month', f'{X["corr_withdraw"]:+.2f}'.replace('-', '−'))], [L2*0.75, L2*0.25], right=(1,)), Spacer(1, 2),
  p('Same returns, mirror-image outcomes. Stated precisely, because it will be tested: if you end up in the same place, a saver would rather '
    'have gone down first. That is not a claim that falls are good; a fall that stays down hurts everyone.', xs), Spacer(1, 5),
  bandrow('WHAT THIS IMPLIES', L2), Spacer(1, 3),
  p('<b>The objective changes.</b> Not “minimise the fall”, which is the retiree\'s goal and costs a saver money, but <b>maximise the chance the '
    'investor is still contributing in year five</b>, because contributions decide where they end up. Everything in the Hook (page 2) and the '
    'Habit (page 3) serves that one number.', xb), Spacer(1, 2),
  p('<b>Every figure in pesos.</b> A 22-year-old saving ₱1,000 a month does not think in percentages. A bad year like the worst in our '
    f'36-year history ({pct(-bad, 0)}) on a ₱5,000 balance is <b>₱{bad*5000:,.0f}</b>, about six weeks of saving. We print the peso figure beside '
    'the risk statistic, everywhere.', xb)]

p1r = [bandrow('THE FUND IT PRODUCES', R2), Spacer(1, 3),
  p(f'<b>Firsts Fund</b>: a proposed peso UITF that owns, directly, {NH} listed companies around the world that run essential, '
    'hard-to-replace systems: power grids, water, digital networks, ports, airports, hospitals, and the equipment behind them. '
    '<b>₱100 to start. One fee. No feeder funds.</b>', xb), Spacer(1, 3),
  grid([('Map', f'{n_uni0} of the largest listed companies across 8 kinds of capacity'), ('Check the fit', f'{n_m0} earn mostly from that capacity, with positive cash flow'),
        ('Verify the merit', f'{n_el0} survive a debt stress test and compare well on value and quality'), ('Position the risk', f'{NH} held, each adding a similar share of risk')],
       [R2*0.30, R2*0.70]), Spacer(1, 2),
  p('Same published rules for every company, including the Philippines\' ICTSI. Full process on page 5.', xs), Spacer(1, 5),
  tiles([(pct(v4['cagr'], 1), 'a year, today\'s holdings, 5 yrs (hindsight)'), (pct(nf['cagr'], 1), 'benchmark NFRA, same period')], 4, R2), Spacer(1, 2),
  tiles([(pct(XS['cagr'], 1), 'without chips & grid equipment'), (pct(ps['cap']['cagr'], 1), 'a year, 36-year industry history')], 4, R2), Spacer(1, 3),
  p(f'<b>Read honestly.</b> The companies were picked in 2026 and priced backwards, so {pct(v4["cagr"], 1)} is hindsight and an upper bound. The two '
    f'right-hand numbers are the checks: it does not rest on chipmakers, and over 36 years the strategy grew about as fast as the world market '
    f'({pct(ps["mkt"]["cagr"], 1)}) with a worst year of {pct(-bad, 0)}. Expect market-like growth, from businesses people cannot do without.', xs), Spacer(1, 5),
  bandrow('MEASURED AGAINST WHAT A YOUNG FILIPINO CAN BUY TODAY', R2), Spacer(1, 1),
  grid([('Peso money market', 'Short-term debt; ₱50–1,000', 'Safe, but likely to trail inflation over five years.'),
        ('Pag-IBIG MP2', 'Government savings; ₱500', 'Tax-free and never negative. Better for a first 3–5 years away, and our screen routes there.'),
        ('Local equity index', 'PSEi names; ₱1,000', 'More of the one bet the investor cannot hedge.'),
        ('Global fund-of-funds', 'Feeder structure; ₱1,000', 'Global, but with a second fee layer; you cannot see what you own.'),
        ('Firsts Fund', f'{NH} direct shares; ₱100', 'Global capacity ownership, in pesos, one fee: the middle door.')],
       [R2*0.27, R2*0.30, R2*0.43], head=['Product', 'Structure; min.', 'What it still does not solve']), Spacer(1, 2),
  p('A comparison of product shape, not of track records: ours is simulated, theirs are live.', xs)]
story += [two(p1l, p1r, L2, R2, G2), Spacer(1, 4),
  p('Sources: PSE investor profile 2024 (via Manila Bulletin, 2025); BPI Wealth; BSP Consumer Finance and Inclusion Survey 2025. Sequence test: '
    f'v4 holdings\' monthly returns after costs, {X["n_shuffles"]:,} random orderings; the correlation is arithmetic and does not depend on the level of '
    'returns. Industry-level history: Kenneth French Data Library, in pesos.', tiny), PageBreak()]

# ======================= PAGE 2 · THE HOOK: WHAT MAKES THEM START =======================
p2l = [bandrow('THE MESSAGE', L2), Spacer(1, 4),
  p('Pondohan ang mga una mo.', big2), p('Fund your firsts. <font color="#58635C">There will always be a new first.</font>', big2), Spacer(1, 4),
  p('Retirement is the wrong hook for a 22-year-old, and not because they are short-termist. It is forty years away, belongs to a version of '
    'themselves they cannot picture, and every competing product already uses it. <b>A first is different: it has a name, a peso cost and a '
    'date.</b> It is the long-horizon goal a young Filipino can actually see, and it is why the account never closes: there is always another one.', xb), Spacer(1, 3),
  grid([('Take Mom and Dad abroad', 'First car', 'First home'), ('First business permit', 'First ₱100,000', 'First month you covered your own rent'),
        ('First time you sent money home and still kept some', 'First laptop that is actually yours', 'First solo trip')],
       [L2/3]*3, bold_first=False), Spacer(1, 2),
  p('Each is entered in the app as a peso amount and a month, which turns a feeling into a contribution plan.', xs), Spacer(1, 5),
  bandrow('WHY COMPETENCE, NOT FOMO: THREE INDEPENDENT LEGS', L2), Spacer(1, 3),
  p('<b>1 · Behaviour.</b> Susada (2025, n = 191) found perceived behavioural control, meaning literacy and self-efficacy, the only strong predictor '
    'of investment intention (β = 0.502, p &lt; .001); peer and family pressure was not significant (r = 0.09). Caveat: one institution, intention not behaviour.', xb), Spacer(1, 2),
  p('<b>2 · The regulator\'s measurement.</b> BSP records literacy rising: 74% answer at least half the questions correctly, up from 69%. The gap is '
    'confidence and product shape, not knowledge.', xb), Spacer(1, 2),
  p('<b>3 · Where the appetite went.</b> Crypto awareness rose from 6% of adults to 20%, and 46% of Filipino crypto owners are 18–34. The appetite '
    'exists; it left for the only place that offered upside.', xb), Spacer(1, 3),
  boxed(p('<b>What this rules out:</b> referral bounties, leaderboards, scarcity timers, streaks that punish a break. <b>What it keeps:</b> peer reach. '
          'A user can share their plan (the first, the cost, the date, the bad year in pesos), never a sign-up bonus. What travels is the calculator, '
          'which is also what builds competence.', xs), L2, SOFT), Spacer(1, 5),
  bandrow('THE COMMERCIAL QUESTION A ₱100 MINIMUM INVITES', L2), Spacer(1, 3),
  p(f'₱100 at a 1.50% fee earns ₱1.50 a year. That pays for nothing, and we will not pretend otherwise. The economics are in <b>contribution flow</b>. '
    f'An account paying ₱1,000 a month plus about ₱300 of Sukli puts in ₱78,000 over five years; at the median of our 36-year history '
    f'({dca["median"]:.2f}× paid-in) that is about <b>₱{round(78000*dca["median"], -3):,.0f}</b>, or roughly <b>₱{round(78000*dca["median"]*0.015, -2):,.0f} a year</b> in fees per mature account. '
    'What decides whether this works is not how many accounts open but how many are still paying in month 60, the same number the fund\'s objective is written around.', xb), Spacer(1, 2),
  p('Flagged, not buried: acquisition is near zero inside BPI\'s payroll base but not on wallet or campus channels; a direct multi-market fund carries '
    'custody, FX and audit costs a small account cannot bear, so the fund needs seed capital and a minimum size before opening; this is the shape of '
    'a cost model, not a costed one.', xs)]

p2r = [bandrow('THE CAMPAIGN: WE SHOW YOU THE BAD YEAR FIRST', R2), Spacer(1, 3),
  p('Every product here leads with the upside and discloses the downside at purchase. We reverse the order, and make the reversal the ad.', xb), Spacer(1, 2),
  p('The opening asset is a <b>calculator on one screen</b>: name your first, enter the cost, pick the month (at least five years away). It returns the '
    'monthly amount, and, before any sign-up, <b>what a bad year would look like in pesos</b> on that balance.', xb), Spacer(1, 3),
  boxed([p('<b>Example.</b> First home down payment, ₱300,000, June 2031.', xs),
         p(f'→ about <b>₱{300000/56:,.0f} a month</b> for 56 months (contributions only).', xs),
         p(f'→ A bad year like our worst ({pct(-bad, 0)}) when you have ₱100,000 saved: <b>−₱{bad*100000:,.0f}</b>, on paper, while you keep paying in.', xs)], R2, AMBER), Spacer(1, 3),
  p('In a category selling optimism, the unclaimed position is <b>candour</b>. It is cheap to build, hard for a competitor to copy without abandoning '
    'its own creative, and does the one thing the evidence says moves this segment: it makes a beginner feel competent rather than excited. The '
    '30-second ad ends on the same calculator.', xb), Spacer(1, 5),
  bandrow('THE LAUNCH: FOUR CHANNELS AND A DATE', R2), Spacer(1, 1),
  grid([('BPI payroll', 'A first job usually comes with a payroll account. Offer triggers on the first salary credit, already KYC\'d.', 'Near-zero'),
        ('BPI app / e-Invest', 'BPI Wealth\'s existing digital onboarding for first-time investors. The rails are live.', 'Existing'),
        ('GCash, Maya', '94M and 50M users; 58% of adults use an e-wallet. The contribution rail for Sukli (page 3).', 'Revenue share'),
        ('Campus, first jobs', 'Finance orgs and graduate onboarding at partner employers. Content is the calculator.', 'Low')],
       [R2*0.24, R2*0.56, R2*0.20], head=['Channel', 'Why it reaches this segment', 'Cost']), Spacer(1, 4),
  boxed([p('<b>The anchor: launch on the 13th month.</b>', xb),
         p('The most predictable cash event in the Filipino year: legally mandated, it lands in December, and it is money no young worker had budgeted. '
           '<i>“Your 13th month is the only money you were never budgeting. Give it a first.”</i> December opens the account; payday and Sukli keep it '
           'alive through the other eleven months.', xs)], R2, SOFT), Spacer(1, 5),
  bandrow('FIVE FRICTIONS, AND WHAT REMOVES EACH', R2), Spacer(1, 1),
  grid([('“I don\'t have enough”', '₱100 to start and per top-up, and Sukli, which uses money you were not counting.'),
        ('“I don\'t know what I\'m buying”', f'{NH} named companies, each with the job it does. Not a fund of funds.'),
        ('“I\'ll lose it”', 'The bad year in pesos, shown before sign-up rather than after.'),
        ('“I\'ll need it back”', 'Firsts under five years are declined at goal-setting and routed to MP2 or a money-market fund.'),
        ('“I stopped and never restarted”', 'Contributions on payday; a missed month prompts, it does not close.')], [R2*0.36, R2*0.64])]
story += [two(p2l, p2r, L2, R2, G2), Spacer(1, 4),
  p('Sources: Susada (2025); BSP Consumer Finance and Inclusion Survey 2025; Triple-A; company disclosures (GCash, Maya); BSP via the FinQuest 2026 '
    'primer (e-wallet use). Calculator example: 56 monthly contributions, no growth assumed. Fee economics use the 36-year industry-level median and '
    'are illustrative.', tiny), PageBreak()]

# ======================= PAGE 3 · THE HABIT: WHAT KEEPS THEM INVESTED =======================
p3l = [bandrow('THE PLATFORM: THE ACCOUNT LIVES WITH BPI, THE MONEY MOVES IN THE WALLET', L2), Spacer(1, 3),
  p('<b>Why BPI holds the account.</b> The investor is already onboarded and KYC\'d, so opening is a confirmation, not an application. The salary lands '
    'here, so payday is a natural trigger. Suitability, statements and redemptions stay under one regulated roof, and the goal service needs two funds '
    '(growth and money market) that BPI already runs.', xb), Spacer(1, 2),
  p('<b>Why the wallet carries the money.</b> A fund that wants a contribution every month should collect it where the taps already happen.', xb), Spacer(1, 5),
  bandrow('SUKLI: SMALL CHANGE, SWEPT INTO YOUR FIRST', L2), Spacer(1, 3),
  p('Sukli is the change you get back, a word every Filipino has used since childhood. Switch it on once and every discretionary GCash or Maya '
    'payment rounds up to the nearest ₱20; the difference is set aside and, at ₱100, swept into the fund. A ₱137 milk tea becomes ₱140 and ₱3 goes to '
    'your first. At about 30 wallet payments a month (our assumption) that is roughly ₱300, on top of payday.', xb), Spacer(1, 2),
  grid([('Mechanic', 'Round up to the nearest ₱20, or 1–5% of spend (user-set)'), ('Applies to', 'Discretionary spending only; never cash-in, send money, bills or remittances received'),
        ('Guardrails', 'No round-up below a ₱500 wallet balance; monthly cap, default ₱1,000'),
        ('While waiting', 'Held in a money-market fund (no idle cash); one net settlement a day to BPI Wealth'), ('Turn off', 'One tap. No penalty')],
       [L2*0.22, L2*0.78]), Spacer(1, 2),
  p('<b>Why it fits this fund.</b> A monthly contribution is a monthly decision, and every decision is a chance to stop. Sukli removes the decision '
    'without removing control: a commitment device, not a persuasion device. It never suggests or celebrates a purchase, and payday stays the main rail.', xs), Spacer(1, 5),
  bandrow('THE DESIGN RULES: WE OPTIMISE AGAINST ENGAGEMENT', L2), Spacer(1, 3),
  p('Fintech apps chase daily users. A fund whose goal is that people keep contributing should do the opposite, because checking the balance comes '
    'before selling. Product rules, not aspirations:', xb), Spacer(1, 2),
  grid([('1', 'No daily balance notification. Ever.'), ('2', 'The headline number is <b>months funded</b>, not percentage change.'),
        ('3', 'Notifications follow payday and your goal date, never the price.'), ('4', 'Checking the balance is one tap further than adding to it.'),
        ('5', 'The months-funded counter only goes up. A missed month pauses it; nothing resets.')], [L2*0.06, L2*0.94]), Spacer(1, 3),
  p(f'<b>Onboarding, four screens:</b> confirm identity from the BPI record → name the first and its date (under five years is declined, with a reason, '
    f'and routed to MP2 or money market) → see the monthly amount and the bad year in pesos → set the payday amount and switch on Sukli. '
    f'<b>Monitoring shows three things:</b> months funded, pesos still to go, and the {NH} companies you own by name.', xs)]

p3r = [bandrow('THE LOOP', R2), Spacer(1, 1),
  grid([('1', 'Name the first and the date. Under five years is declined, with a reason.'), ('2', 'Fund it three ways: payday, Sukli, top-ups. Any one is enough.'),
        ('3', 'See the risk in pesos before it happens.'), ('4', 'Near the date, the goal service glides part of the balance into a money-market fund (proposed).'),
        ('5', 'Then name the next one. The account reopens; it does not close.')], [R2*0.08, R2*0.92]), Spacer(1, 5),
  bandrow('THE REDEMPTION SCREEN: WHERE FUNDS LOSE PEOPLE', R2), Spacer(1, 3),
  boxed([p('<b>REDEEM · CONFIRM</b>', xs), p('<b>₱4,138</b>', big2),
         p('That is 14 months of contributions, and ₱21,860 short of your first: Siargao, June 2029.', xs), Spacer(1, 2),
         p(f'<b>One thing worth knowing first.</b> You are down 9.4% and still paying in. For a saver, a weak stretch followed by recovery ends ahead of a '
           f'strong start (correlation {X["corr_contrib"]:.2f}). Selling is the only version where that stops being true.'.replace('-', '−'), xs), Spacer(1, 2),
         p('<b>[ Pause contributions for 3 months instead ]</b>   ·   Withdraw ₱4,138', xs)], R2, colors.white), Spacer(1, 2),
  p('Pausing beats redeeming, and the screen should say so. Redemption stays one tap away; we propose no friction that traps money, only that the '
    'cheaper option comes first and the loss is counted in months, because months are what was spent. Illustrative mock-up.', xs), Spacer(1, 5),
  bandrow('THE GOAL SERVICE CLOSES THE LOOP', R2), Spacer(1, 3),
  p(f'Near the date the saver becomes a spender, the balance becomes the thing to protect, and the correlation flips sign. An account-level rule '
    f'between two funds BPI already runs moves part of the balance to money market. In {dca["n"]} five-year stretches of our 36-year history, '
    f'₱1,000 a month: worst outcome <b>₱{round(60000*dca["worst"], -3):,.0f} → ₱{round(60000*dcg["worst"], -3):,.0f}</b> with the glidepath; stretches '
    f'ending below ₱60,000 paid in: {pct(dca["below1"], 0)} → {pct(dcg["below1"], 0)}; typical cost ₱{round(60000*(dca["median"]-dcg["median"]), -2):,.0f}. '
    'One fund price cannot glide to dates its investors do not share, so it sits outside the fund.', xs), Spacer(1, 5),
  bandrow('HOW WE WOULD KNOW IT WORKED', R2), Spacer(1, 1),
  grid([('Still contributing in month 60', '≥ 55%', '< 40%'), ('Kept contributing through the first negative quarter', '≥ 80%', '< 60%'),
        ('Pause-to-redeem ratio', '≥ 3 : 1', '< 1 : 1'), ('Sukli switched on by month 6', '≥ 40%', '< 15%'), ('Median months funded, year 1', '≥ 10 of 12', '< 7')],
       [R2*0.58, R2*0.21, R2*0.21], head=['Metric', 'Target', 'Failure'], right=(1, 2)), Spacer(1, 2),
  p('What we would refuse to report as success: assets gathered, accounts opened, daily users, app sessions. Each can rise while the thing the '
    'fund exists to do is failing.', xs)]
story += [two(p3l, p3r, L2, R2, G2), Spacer(1, 4),
  p('Sukli would need e-money partner agreements with GCash or Maya, recurring debit authority and regulatory review not yet obtained. Glidepath '
    'figures use the industry-level history and an illustrative schedule; the redemption screen is a mock-up with example numbers.', tiny), PageBreak()]


def annex():
    out = []
    A = CW*0.49; B = CW - A - 8
    lim = R['portfolio']; grp_max = max(x['weight'] for x in lim if x['key'] in ('ICT', 'MWC', 'ENEL', 'ELE'))
    a1 = [bandrow('A1 · EVIDENCE BASE: EVERY LOAD-BEARING CLAIM AND ITS SOURCE', A), Spacer(1, 1),
      grid([('Young Filipinos are arriving', '18–29 = 26.5% of PSE accounts, from 19.5%; PSE accounts +50.1% in a year', 'PSE investor profile 2024, via Manila Bulletin (2025)'),
            ('Access and literacy improved', 'BPI UITF minimum ₱10,000 → ₱1,000 (2023); 74% answer half the literacy questions, from 69%', 'BPI Wealth; BSP CFIS 2025'),
            ('Cash loses in real terms', 'Inflation 6.2% in July 2026', 'PSA (2026)'),
            ('Risk appetite went to crypto', 'Awareness 20% of adults, from 6%; 46% of owners are 18–34', 'BSP CFIS 2025; Triple-A'),
            ('The money moves in wallets', 'GCash 94M, Maya 50M users; 58% of adults use e-wallets', 'Company disclosures; BSP via FinQuest primer'),
            ('Competence, not peers, predicts investing', 'β = 0.502 (p < .001); peer influence r = 0.09 (n.s.)', 'Susada (2025), n = 191'),
            ('A saver gains from an early fall', f'Correlation {X["corr_contrib"]:+.2f} paying in, {X["corr_withdraw"]:+.2f} drawing down'.replace('-', '−'), f'Our test, {X["n_shuffles"]:,} orderings')],
           [A*0.30, A*0.42, A*0.28], head=['Claim', 'Figure', 'Source']), Spacer(1, 4),
      bandrow('A2 · WHAT WE KILLED, AND WHY', A), Spacer(1, 1),
      grid([('“The suitability gate is the barrier”', 'Access demonstrably improved; the claim argued against its own evidence.'),
            ('“Participation fell 36% → 23%”', 'Could not be confirmed from BSP releases; not used.'),
            ('A fixed 30% Philippines sleeve', 'No basis. Countries are now an outcome of the same tests (ICTSI 4.8%).'),
            ('A 10% cash reserve', 'Cost return; about 3% operating cash covers redemptions.'),
            ('Requiring a dated capacity target', 'Evidence, not a buy reason; the story never picks a stock.'),
            ('Referral bounties, streaks, education-gated unlocks', 'Against the evidence (Susada); a streak you can break is a reason to quit.')],
           [A*0.40, A*0.60]), Spacer(1, 4),
      bandrow('A6 · WHAT WOULD CHANGE OUR MIND', A), Spacer(1, 3),
      p('The sequence result is arithmetic. But the product case rests on <b>contribution continuity</b>, modelled as 60 uninterrupted monthly payments, '
        'which no source we found measures for this segment. If continuity is materially worse, the risk level should come down. Sukli exists to raise '
        'continuity without relying on discipline, but its uptake and its durability through a fall are unmeasured too. Those are the first two tests we '
        'would run with real data, and the honest weak point of this proposal.', xs)]
    a2 = [bandrow('A3 · BACK-TEST METHOD AND ITS LIMITS', B), Spacer(1, 3),
      p(f'<b>Method.</b> Weekly peso total returns, 1 Oct 2021 – 2 Oct 2026. Weights re-solved each quarter on the previous 156 weeks only (no look-ahead '
        f'in the weights), under every limit; {R["rebalances"]} rebalances. After the 1.50% fee, 0.30% trading cost and dividend withholding. '
        'Benchmark NFRA in pesos.', xs), Spacer(1, 2),
      grid([('Selection is hindsight', 'Companies chosen in Oct 2026 with Oct 2026 data, priced backwards. Upper bound.'),
            ('Survivorship', 'Universe is today\'s largest companies; failures since 2021 are missing.'),
            ('One cycle', f'Chips are {pct(bt["Semiconductors"], 0)} of the money but {pct(sum(x["risk_share"] for x in lim if x["ctype"] == "Semiconductors"), 0)} of the risk, '
                          f'near a cyclical peak; without chips and grid equipment, {pct(XS["cagr"], 1)} a year.'),
            ('Tax approximation', 'Today\'s dividend yields × approximate treaty rates, every year; to be confirmed by counsel.')], [B*0.28, B*0.72]), Spacer(1, 2),
      p('The first three flatter the figures. None is corrected in the numbers shown; the 36-year industry history is our “what to expect”.', xs), Spacer(1, 4),
      bandrow('A4 · LIMITS: RULE VS ACTUAL (ALL HOLD AT EVERY REBALANCE)', B), Spacer(1, 1),
      grid([('One company', '≤ 20% (BSP)', pct(PF[0]['weight'])), ('One group (e.g. Razon)', '≤ 20%', pct(grp_max)),
            ('One kind of capacity', '≤ 25%', pct(max(bt.values()))), ('Liquidity', 'sell in 5 days at 20% of volume', 'never binds at ₱1bn'),
            ('Operating cash', 'about 3%', '3.00%'), ('Country quota', 'none', f'Philippines {pct(R["ph_now"])} ({pct(R["ph_range"][0], 1)}–{pct(R["ph_range"][1], 1)})')],
           [B*0.36, B*0.32, B*0.32], head=['Limit', 'Rule', 'Actual'], right=(2,)), Spacer(1, 2),
      p(f'<b>Concentration, disclosed:</b> about {R["eff_bets"]:.1f} independent exposures among {NH} holdings; the two largest shared drivers explain '
        f'{pct(R["top2_factor"], 0)} of risk. Holdings outside the capped networks each carry 3.3–3.9% of risk.', xs), Spacer(1, 4),
      bandrow('A5 · REGULATORY POSITION', B), Spacer(1, 3),
      p('<b>The fund.</b> A peso UITF holding foreign shares directly, priced daily (NAVPU), with a 20% single-company ceiling per BSP Circular No. 1234 '
        '(2026). Our reading, not reviewed by counsel; any launch would need that review first.', xs), Spacer(1, 2),
      p('<b>Suitability.</b> We are not asking BPI to relax the Client Suitability Assessment, to allow an education-based override, or to sell an '
        'aggressive fund to a client rated conservative. We propose recording the investor\'s horizon and contribution plan in the suitability file, '
        'with an audit trail, and letting the goal service carry risk down as the date approaches.', xs), Spacer(1, 2),
      p('<b>Sukli.</b> Needs itemised, revocable debit authority from the wallet holder, an e-money partner agreement, and treatment of the waiting '
        'balance under BSP e-money rules. The design anticipates it: spend-only, balance floor, user cap, one-tap off, and a waiting balance held in a '
        'regulated fund rather than a distributor\'s float.', xs)]
    out += [two(a1, a2, A, B, 8), Spacer(1, 4),
            p('<b>Team Los Angeles 76ers</b>, Ateneo de Manila University: Prince Angelo C. Rivera · Luis Tengonciang · Karol Josef Fuñe · '
              'Eric Fabian Thirdy Mendez. A FinQuest 2026 proposal; not an offer, solicitation or investment advice, and not a BPI Wealth product.', tiny)]
    return out
