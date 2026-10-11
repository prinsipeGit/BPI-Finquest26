# Executive summary pages (1-3) and annex (6) for the Firsts Fund fact sheet. exec()'d inside build_factsheet4.py so it
# shares its styles and data (R, PF, bt, v4, nf, ps, XS, X, NH, n_uni0, n_m0, n_el0, helpers p, kv, two, boxed, bandrow).
# Restores the Phase 1 "Hook" (marketing) and "Habit" (customer experience) content, rebuilt on v4 facts (10 Oct 2026).

lead = ParagraphStyle('lead', parent=base, fontSize=9.4, leading=12.4)
SC = float(os.environ.get('EXS', '1.22'))   # text scale for pages 1-3 and the annex, chosen so each page fills
xb = ParagraphStyle('xb', parent=base, fontSize=7.7*SC, leading=10.0*SC)
xs = ParagraphStyle('xs', parent=base, fontSize=7.2*SC, leading=9.1*SC)
h2 = ParagraphStyle('h2', parent=base, fontName='Helvetica-Bold', fontSize=8.6, leading=10.6, textColor=GREEN, spaceBefore=1)
kn = ParagraphStyle('kn', parent=base, fontName='Helvetica-Bold', fontSize=14, leading=16, textColor=DARK, alignment=TA_CENTER)
kl = ParagraphStyle('kl', parent=base, fontSize=6.6, leading=8, textColor=MUTED, alignment=TA_CENTER)
quote = ParagraphStyle('q', parent=base, fontName='Helvetica-Oblique', fontSize=7.4, leading=9.6, textColor=DARK)
big2 = ParagraphStyle('big2', parent=base, fontName='Helvetica-Bold', fontSize=11.5, leading=14, textColor=GREEN)
xc = ParagraphStyle('xc', parent=cell, fontSize=7.1*SC, leading=8.8*SC); xcb = ParagraphStyle('xcb', parent=xc, fontName='Helvetica-Bold')
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

# ======================= PAGES 1-3 · ORIGINAL EXECUTIVE SUMMARY, REVISED TO THE CONSULTATION FINAL DECISIONS =======================
# Base: Phase 1 executive summary (Problem / Hook / Habit). Edited per "Summary of consultation.md" (final decisions) and
# "Final Consultation.md". Removed: "park or gamble". Fund, M·V·P and figures are the current v4 model.
PER = dict(pay=2000, months=60, goal=120000)                 # persona plan (illustrative)
pm = {k: round(PER['goal'] * dca[k], -3) for k in ('median', 'p5', 'worst')}; pg = round(PER['goal'] * dcg['worst'], -3)
psei = F5['psei']['stats']['growth'] if 'growth' in F5['psei']['stats'] else 100 * (1 + F5['psei']['stats']['cagr'])**5
ddp = X['dd_on_5000']; badp = bad * 5000

# ---------------- PAGE 1 · THE PROBLEM, AND THE FUND THAT ANSWERS IT ----------------
p1l = [bandrow('THE PROBLEM EVERYONE IS SOLVING, AND THE ONE THAT ACTUALLY BINDS', L2), Spacer(1, 3),
  p('<b>At 22, your biggest asset is not money.</b> It is forty years of future earnings: in pesos, tied to one economy, impossible to sell. '
    'A young Filipino already depends almost entirely on the Philippines, without ever choosing to.', xb), Spacer(1, 3),
  p(f'Then look at what is easy to reach. Pag-IBIG MP2 lends those savings to the Philippine government. Local index funds buy the same '
    f'economy again: over the past five years, ₱100 in the PSEi became about ₱{psei:.0f}. Most low-minimum products are built to park money '
    'for the short term, not to grow it over five years or more.', xb), Spacer(1, 3),
  p('<b>Access is no longer the binding constraint, and we will not pretend it is.</b> BPI cut its UITF minimum from ₱10,000 to ₱1,000 in 2023; '
    'some platforms reach ₱50. PSE accounts rose 50.1% in a year, 26.5% of them now held by 18-to-29-year-olds, and the BSP measures financial '
    'literacy rising. Young Filipinos are already here. What is missing is a clear place for money with a five-year-plus purpose.', xb), Spacer(1, 4),
  boxed(p('“Number one: you have to get global exposure… by diversifying some of that local exposure, you\'re actually lowering your volatility.” '
          '<font name="Helvetica" color="#58635C">— Joaquin Rossano U. Veluz, Sun Life Investment Management and Trust Co.</font>', quote), L2, SOFT), Spacer(1, 5),
  bandrow('THE SECOND ERROR: THE RISK MODEL IS POINTED THE WRONG WAY', L2), Spacer(1, 3),
  p('The retail risk framework is built to protect a balance, which is right for someone drawing money out. A young saver is doing the '
    'opposite: paying in every month. For them, a fall early on means buying more units at a lower price.', xb), Spacer(1, 2),
  p(f'<b>The proof is arithmetic.</b> We reordered the fund\'s own {X["months"]} monthly results {X["n_shuffles"]:,} times; the total return stays '
    f'fixed and only the order changes. Link between a strong first half and the final amount:', xb), Spacer(1, 2),
  grid([('Saver paying in ₱1,000 a month', f'{X["corr_contrib"]:.2f}'.replace('-', '−')), ('Someone drawing out ₱900 a month', f'+{X["corr_withdraw"]:.2f}')],
       [L2*0.75, L2*0.25], right=(1,)), Spacer(1, 2),
  p(f'Same returns, opposite outcomes. <b>In pesos:</b> ₱1,000 a month in a money-market fund at 4.5% gives about ₱{X["mm_wealth"]:,.0f} after five years; '
    f'the weakest of all {X["n_shuffles"]:,} orderings of the fund\'s results still gives about ₱{X["contrib_min"]:,.0f}. This is not a claim that falls are '
    'good; a fall that never recovers hurts everyone.', xs)]
p1r = [bandrow('WHAT THIS IMPLIES, AND THE FUND IT PRODUCES', R2), Spacer(1, 3),
  p('<b>The objective changes.</b> Not “minimise the fall”, which is the retiree\'s goal, but <b>maximise the chance the saver is still contributing '
    'in year five</b>, because contributions decide where they end up. The Hook (page 2) and the Habit (page 3) serve that one number.', xb), Spacer(1, 3),
  p(f'<b>The mandate.</b> The proposed Firsts Fund is a peso-denominated, actively managed global equity UITF for goals <b>five years or more</b> away '
    f'(a recommended horizon, not a lock-in). Its theme is <b>global real capacity</b>: it invests directly in {NH} listed businesses providing essential services and '
    f'infrastructure that are hard to replace (power and water, phone and internet networks, ports, airports, hospitals, and the equipment behind them), across {len(R["by_country"])} markets. '
    'Technology exposure is assessed, not excluded. No fund-of-funds layer. ₱100 to start; 1.50% a year (proposed).', xb), Spacer(1, 3),
  p('<b>Chosen by M · V · P</b>, the same published rules for every company:', xb), Spacer(1, 1),
  grid([('<font color="#0F7A45" size="11">M</font> · Map the milestone', f'Essential services a saver\'s firsts depend on: <b>{n_uni0}</b> screened, <b>{n_m0}</b> fit'),
        ('<font color="#0F7A45" size="11">V</font> · Verify the investment', f'Debt stress test; value and quality vs peers: <b>{n_el0}</b> pass'),
        ('<font color="#0F7A45" size="11">P</font> · Position the risk', f'Sized so no company dominates the risk: <b>{NH}</b> held')], [R2*0.43, R2*0.57]), Spacer(1, 2),
  p('Holdings reviewed monthly; weights reset quarterly. Full holdings and process: Fund Fact Sheet (pages 4–5).', xs), Spacer(1, 4),
  tiles([(f'{pct(v4["cagr"], 1)} <font color="#58635C" size="10">vs</font> {pct(nf["cagr"], 1)}', 'a year, 5 years: today\'s holdings (backtested) vs benchmark NFRA')], 4, R2), Spacer(1, 2),
  tiles([(f'₱{ddp:,.0f}', 'deepest drop on a ₱5,000 balance (−7.4%)'), (f'₱{badp:,.0f}', '36-year worst 12 months (−27%) on ₱5,000')], 4, R2), Spacer(1, 2),
  p(f'<b>Every figure in pesos.</b> A first-jobber does not think in percentages, so we show the peso amount beside every risk number. '
    f'<b>Read honestly:</b> the holdings were chosen in 2026 and tested backwards, so {pct(v4["cagr"], 1)} is the historical performance of the '
    f'currently selected portfolio, not a forecast. Without chip and grid-equipment makers it is {pct(XS["cagr"], 1)}; over 36 years the approach earned '
    f'{pct(ps["cap"]["cagr"], 1)} a year, about the world market. Broad indices are market context only.', xs)]
pos = grid([('Global fund-of-funds (e.g. BPI Global Equity FoF)', 'Owns 11 other funds', '₱1,000', '1.50% + target-fund fees', 'Layered fees; you cannot see the companies you own.'),
            ('Philippine equity index fund', 'Passive, 32 PSEi names', '₱1,000', '1.50%', 'More of the one economy the saver already depends on.'),
            ('Pag-IBIG MP2', 'Government savings', '₱500', 'None', 'Tax-free and never negative. Better for a first 3–5 years away; our goal screen points there.'),
            ('Peso money-market fund / UITF', 'Short-term debt', '₱50–1,000', '~0.5–1.0%', 'Steady, but built for short-term goals.'),
            ('Firsts Fund (proposed)', f'{NH} companies directly', '₱100', '1.50%, one layer', 'Global essential services, in pesos, every company named.')],
           [CW*0.24, CW*0.15, CW*0.08, CW*0.15, CW*0.38], head=['Product', 'Structure', 'Min.', 'Fee', 'What it still does not solve'])
story += [two(p1l, p1r, L2, R2, G2), Spacer(1, 5), bandrow('POSITIONING: MEASURED AGAINST WHAT A YOUNG FILIPINO CAN ACTUALLY BUY TODAY', CW), Spacer(1, 1), pos, Spacer(1, 2),
  p('A comparison of design (fees, minimum, structure), not of track records: ours is backtested, theirs are live. Sources: BPI Global Equity Fund-of-Funds KIIDS '
    '(29 May 2026); BPI Philippine Equity Index Fund KIIDS (30 Jan 2026); Pag-IBIG; PSE investor profile 2024 (via Manila Bulletin, 2025); BPI Wealth; BSP. '
    'Shuffle test: the fund\'s monthly results after costs.', tiny), PageBreak()]

# ---------------- PAGE 2 · THE HOOK · WHAT MAKES THEM START ----------------
p2l = [bandrow('THE MESSAGE', L2), Spacer(1, 4), p('Fund your firsts.', big2), Spacer(1, 3),
  p('Retirement is the wrong hook for a 22-year-old, and not because they are short-termist. It is forty years away, it belongs to a version of '
    'themselves they cannot picture, and every competing product already uses it. <b>A first is different: it has a name, a peso cost and a date.</b> '
    'It is a long-horizon goal a young Filipino can actually see, and it is why the account never closes: there is always another one. The portfolio '
    'supports that promise in the background; how it is built lives in the fact sheet.', xb), Spacer(1, 3),
  grid([('Take Mom and Dad abroad', 'First car', 'First home'), ('First business', 'First ₱100,000', 'Paying for a parent\'s care')], [L2/3]*3, bold_first=False), Spacer(1, 2),
  p('All five years or more away. Each is entered in the app as a peso amount and a date, which turns a feeling into a contribution plan.', xs), Spacer(1, 5),
  bandrow('WHO IT IS FOR', L2), Spacer(1, 3),
  p('<b>Graduating students to entry-level professionals</b> preparing for a meaningful long-term first, with regular income and the risk tolerance for a '
    'stock fund. A first milestone is not the same as a first investment: not every beginner suits this fund. Professionals further along in their '
    'careers can use it too, if their goal is five or more years away.', xb), Spacer(1, 3),
  boxed([p('<b>Meet Bea (illustrative).</b> 23, junior accountant, takes home about <b>₱28,000 a month</b>.', xs), Spacer(1, 2),
         grid([('Rent and bills · Food · Helping at home · Transport', '₱22,000'), ('Emergency savings · Personal', '₱4,000'),
               ('<b>Her first: Japan with her parents in 5 years</b>', '<b>₱2,000</b>')], [L2*0.68, L2*0.20], bold_first=False, right=(1,))], L2, SOFT), Spacer(1, 5),
  bandrow('WHY COMPETENCE AND NOT FOMO: THREE INDEPENDENT LEGS', L2), Spacer(1, 3),
  p('<b>1 · Behaviour.</b> A survey of 191 Filipino students (Susada, 2025) found that feeling capable (knowledge and confidence) was the strongest driver of '
    'intending to invest; pressure from friends and family was not significant. One university, and it measures intention, not behaviour.', xs), Spacer(1, 2),
  p('<b>2 · The regulator\'s measurement.</b> BSP records literacy rising: 74% answer at least half the questions correctly, up from 69%. The gap is '
    'confidence and product shape, not knowledge.', xs), Spacer(1, 2),
  p('<b>3 · Where the appetite went.</b> Crypto awareness rose from 6% of adults to 20%, and 46% of Filipino crypto owners are 18–34. The appetite for '
    'growth exists; it needs a regulated, long-term home.', xs), Spacer(1, 3),
  boxed(p('<b>What this rules out:</b> raffles, cash rewards, referral bounties, leaderboards, countdown timers and streaks; rewards stay a future idea only if '
          'costs and approvals allow. <b>What it keeps:</b> a user can share their plan (the first, the cost, the date), never a sign-up bonus.', xs), L2, SOFT)]
p2r = [bandrow('THE CAMPAIGN: THE GOAL CALCULATOR', R2), Spacer(1, 3),
  p('The opening asset is a calculator on one screen in the BPI App (proposed): name your first, enter the cost, pick a date at least five years away. '
    'Before any commitment it shows, with every assumption visible:', xb), Spacer(1, 2),
  grid([('Contributions only', f'₱{PER["goal"]:,} ÷ {PER["months"]} months = <b>₱{PER["pay"]:,} a month</b>'),
        ('Illustrative growth', 'At an assumed 6% a year, about <b>₱1,710 a month</b>; an example, not a promise'),
        ('Rising prices (optional)', 'At 4% inflation the trip costs ~₱146,000: ₱2,430 a month, contributions only')], [R2*0.30, R2*0.70]), Spacer(1, 3),
  p(f'<b>Clear, balanced risk information.</b> Bea\'s plan across every five-year stretch of our 36-year history: typical ₱{pm["median"]:,.0f}; 1 in 20 '
    f'at or below ₱{pm["p5"]:,.0f}; weakest ₱{pm["worst"]:,.0f}. Illustrative, not a forecast. The calculator builds competence rather than excitement, and it is '
    'what people share.', xs), Spacer(1, 5),
  bandrow('THE LAUNCH: CHANNELS, AND A CALENDAR ANCHOR', R2), Spacer(1, 1),
  grid([('Talks and caravans', 'On-site financial-literacy talks and campus caravans. The priority channel.'),
        ('Campus events', 'Student organisations and graduating classes.'),
        ('Early-career workplaces', 'Financial-wellness sessions for new hires, including employers on BPI payroll.'),
        ('Short-form social', 'Kept lean (paid creator content is costly); creators support, not lead.'),
        ('BPI App, “Chat with us”', 'Online visitors can ask a person before starting.')], [R2*0.33, R2*0.67]), Spacer(1, 2),
  p('Every channel has one next action: try the goal calculator.', xs), Spacer(1, 3),
  boxed([p('<b>The anchor: launch on the 13th month.</b>', xs),
         p('The most predictable cash event in the Filipino year: it lands in December and is money no first-jobber budgeted. <i>“Your 13th month was never '
           'in the budget. Give it a first.”</i> December opens the account; the monthly plan keeps it going.', xs)], R2, SOFT), Spacer(1, 5),
  bandrow('THE COMMERCIAL QUESTION A ₱100 MINIMUM INVITES', R2), Spacer(1, 3),
  p(f'₱100 at 1.50% earns ₱1.50 a year; the economics are in steady contributions. A ₱2,000-a-month plan like Bea\'s reaches about ₱{pm["median"]:,.0f} in a '
    f'typical five-year stretch, roughly <b>₱{round(pm["median"]*0.015, -2):,.0f} a year</b> in fees. What decides it is how many are still contributing in month 60. '
    'Flagged: the fund needs seed capital and a minimum size for custody, currency and audit costs; this is the shape of a cost model, not a costed one.', xs), Spacer(1, 5),
  bandrow('FIVE FRICTIONS, AND WHAT REMOVES EACH', R2), Spacer(1, 1),
  grid([('“I don\'t have enough”', '₱100 to start and per top-up.'), ('“I don\'t know what I\'m buying”', f'{NH} named companies. Not a fund of funds.'),
        ('“I\'ll lose it”', 'Clear risk information in pesos before committing.'),
        ('“I\'ll need it back”', 'Goals under five years are pointed to MP2 or a money-market fund.'),
        ('“I stopped and never restarted”', 'A missed month prompts a choice; it never closes the plan.')], [R2*0.40, R2*0.60])]
story += [two(p2l, p2r, L2, R2, G2), Spacer(1, 4),
  p('Bea and her budget are illustrative; calculator growth and inflation rates are example assumptions shown to the user. Sources: Susada (2025); BSP Consumer '
    'Finance and Inclusion Survey 2025; Triple-A.', tiny), PageBreak()]

# ---------------- PAGE 3 · THE HABIT · WHAT KEEPS THEM INVESTED ----------------
p3l = [bandrow('THE PLATFORM DECISION', L2), Spacer(1, 3),
  p('<b>The account and the plan live in the BPI App</b> (proposed entry point, subject to confirmation). The saver is already verified, so opening is '
    'a confirmation, not an application; the salary usually lands in the same bank, which makes payday a natural trigger. Suitability, statements and '
    'withdrawals stay under one regulated roof, and the goal service needs two funds (growth and lower-risk) that BPI already runs. All Firsts Fund '
    'screens are new and labelled proposed.', xb), Spacer(1, 5),
  bandrow('HOW MONEY GOES IN', L2), Spacer(1, 3),
  p('<b>At launch: a regular monthly plan plus top-ups whenever you like.</b> Either one alone keeps a goal on track.', xb), Spacer(1, 2),
  p('<b>Missed month</b> (not enough money, or skipped): the goal date stays the same unless the saver changes it. The app shows the updated projection and '
    'offers a one-off top-up, a higher amount from now on, or a later date. Debits are never raised automatically.', xb), Spacer(1, 2),
  boxed([p('<b>Sukli: a future enhancement.</b> Spare change from purchases set aside and invested at ₱100. It starts inside the BPI App to prove it works, before '
           'any e-wallet. Still to settle: which purchases count, consent, where the change waits, and when it moves. Spend-only, a balance floor, a monthly '
           'cap and one-tap off are the intended guardrails.', xs)], L2, SOFT), Spacer(1, 5),
  bandrow('THE DESIGN CONSTITUTION: WE OPTIMISE AGAINST ENGAGEMENT', L2), Spacer(1, 3),
  p('Apps chase daily users. A fund whose aim is that people keep contributing should do the opposite, because checking the balance comes before selling.', xb), Spacer(1, 2),
  grid([('1', 'No daily balance notification. Ever.'), ('2', 'The main screen shows goal progress: total put in, current value and gain or loss, in pesos.'),
        ('3', 'Notifications follow payday and the goal date, never the price.'), ('4', 'Checking the balance is one tap further than adding to it.'),
        ('5', 'No streaks. Missing a month should never feel like losing.')], [L2*0.06, L2*0.94]), Spacer(1, 3),
  p('<b>Sign-up, four screens:</b> confirm identity from the BPI record and the standard suitability questions → choose one main first (suggested, typed in, or '
    '“Help me choose my first”) → see the calculator and the risk in pesos → set the monthly plan from ₱100. <b>Details view:</b> units, price per unit and every '
    'transaction. <b>Reports:</b> in-app progress, transaction statements, and fund reports at least quarterly.', xs)]
p3r = [bandrow('THE LOOP', R2), Spacer(1, 1),
  grid([('1', 'Name the first and its date, five years or more away.'), ('2', 'Fund it: monthly plan and top-ups.'),
        ('3', 'See the risk in pesos, with balanced scenarios, before committing.'),
        ('4', 'Review the goal every year; get a reminder two years before the date.'),
        ('5', 'Reach it, then name the next first in the same account. Suitability is checked again.')], [R2*0.08, R2*0.92]), Spacer(1, 5),
  bandrow('THE GOAL SERVICE: WHY AND HOW, IN SIMPLE WORDS', R2), Spacer(1, 3),
  p('<b>Why.</b> Early on, a fall gives a saver time to recover. Close to the goal date there is no time left. The fund itself cannot slow down for one person, '
    'because everyone in it has a different date.', xs), Spacer(1, 2),
  p('<b>How.</b> It happens in the saver\'s own account, not in the fund. At the yearly review, or the two-year reminder, the saver can choose to move part of '
    f'their units to a lower-risk BPI fund. Nothing moves without their permission; it lowers risk but does not guarantee the goal. In Bea\'s plan over 36 years '
    f'of history, the weakest outcome improves from ₱{pm["worst"]:,.0f} to ₱{pg:,.0f}. A future capability that still needs operational checks.', xs), Spacer(1, 5),
  bandrow('THE WITHDRAWAL SCREEN: WHERE FUNDS LOSE PEOPLE', R2), Spacer(1, 3),
  boxed([p('<b>WITHDRAW · CONFIRM</b>  <font color="#58635C">(proposed screen, example numbers)</font>', xs), p('<b>₱26,500</b>', big2),
         p('You have put in ₱28,000 over 14 months; it is worth ₱26,500 today. You are ₱93,500 from your first: Japan with your parents, October 2031.', xs), Spacer(1, 1),
         p('If you keep saving, your next contributions buy units at a lower price.', xs), Spacer(1, 2),
         p('<b>[ Pause the plan for 3 months ]</b>     Withdraw ₱26,500', xs)], R2, colors.white), Spacer(1, 2),
  p('Pausing comes first on screen; withdrawing stays one tap away. No holding period, no exit fee. Many goals may fall due on the same dates; the manager sees '
    'goal dates ahead and keeps about 3% cash to pay withdrawals.', xs), Spacer(1, 5),
  bandrow('HOW WE WOULD KNOW IT WORKED', R2), Spacer(1, 1),
  grid([('Still contributing in month 60', '≥ 55%', '< 40%'), ('Kept contributing through the first losing quarter', '≥ 80%', '< 60%'),
        ('Chose “pause” over “withdraw”', '≥ 3 to 1', '< 1 to 1'), ('Months contributed in year 1 (median)', '≥ 10 of 12', '< 7'),
        ('Reached a first and named the next one', 'tracked', '')], [R2*0.58, R2*0.21, R2*0.21], head=['Measure', 'Target', 'Rethink if'], right=(1, 2)), Spacer(1, 2),
  p('Not counted as success: money gathered, accounts opened or app visits.', xs)]
story += [two(p3l, p3r, L2, R2, G2), Spacer(1, 4),
  p('IMPORTANT. A FinQuest 2026 student proposal: not an offer or investment advice and not a BPI Wealth product. Performance figures are backtested with '
    'hindsight. Screens and examples are proposed and illustrative. Full disclosures: Fund Fact Sheet and Annex.', tiny), PageBreak()]


def annex():
    out = []
    A = CW*0.49; B = CW - A - 8
    lim = R['portfolio']; grp_max = max(x['weight'] for x in lim if x['key'] in ('ICT', 'MWC', 'ENEL', 'ELE'))
    a1 = [bandrow('A1 · WHAT CHANGED AFTER THE BPI CONSULTATIONS', A), Spacer(1, 1),
      grid([('Horizon', 'Five years or longer throughout; a recommendation, not a lock-in or a promise of returns.'),
            ('Theme', 'Global real capacity, defined as businesses providing essential services and infrastructure; no blanket “non-tech” claim; technology exposure assessed.'),
            ('Selection', 'M · V · P kept: Map the milestone, Verify the investment, Position the risk.'),
            ('Holdings', 'The earlier 16 was not retained; the holdings review under the current rules gives 31.'),
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
            ('One type of service', '≤ 25%', pct(max(bt.values()))), ('Liquidity', 'sell in 5 days at 20% of volume', 'never binds at ₱1bn'),
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
