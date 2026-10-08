# The Firsts Fund — Phase 1 Action Plan
**Submission deadline: Saturday 15 August 2026. Today: 10 August. Five days.**
Target submit date: **Thursday 14 August**, leaving one buffer day.

Team: Prince Angelo Rivera · Luis Tengonciang · Karol Josef Fuñe · Eric Fabian Thirdy Mendez

---

## Scoring weights (Phase 1) — where effort should go

| Criterion | Weight | Our current standing |
|---|---|---|
| **Originality** | **30%** | Strong content, but scattered. A judge cannot find it in one pass. |
| Background & Research | 25% | Our best pillar. Evidence base is verified and sourced. |
| Feasibility | 25% | **Biggest hole.** No unit economics for a ₱100 account. |
| Fund Process | 20% | Very strong. Published engine, constraint stack, disclosures. |

Originality is the largest single block and it is the one we are under-communicating.
Feasibility is the one we are actively failing. Both get dedicated work below.

---

## RED FLAG: the formatting rule could sink us before anyone reads a word

The primer, page 7, under Formatting: **"Font and Size: Arial 11."**
The FAQ reaffirms it: layout is free *"outside of the prescribed Arial 11 font size and A4 document size."*

I re-rendered both documents forcing every element to Arial 11:

| Document | Pages at uniform Arial 11 | Limit | Over by |
|---|---|---|---|
| Executive Summary | **9** | 4 (3 + annex) | 5 |
| Fund Fact Sheet | **5** | 2 | 3 |

We are currently compliant only because we use type as small as **5.9pt** in the fact sheet
and **6.6pt** in the executive summary.

**Judgement call, and the team must make it consciously.** Strict enforcement would make a
2-page fact sheet containing all eleven required elements physically impossible, and BPI
Wealth's own ALFM fact sheets use 6–8pt in tables and footnotes. The defensible position is:

- **All running prose at Arial 11.** Non-negotiable. This is what the rule plainly means.
- **Tables, footnotes and legal disclaimers below 11pt.** Industry-standard, low risk.
- **Nothing below 8pt anywhere.** 5.9pt reads as evading the rule rather than designing.

That last line is the actual work: raising the floor to 8pt costs space, so **content must be
cut, not shrunk.**

---

# DAY 1 — Monday 11 August: compliance and fork resolution

### 1.1 Resolve the two forks (do this first, everything else depends on it)

We currently have two incompatible versions:

| | Prince's fact sheet | Folder version |
|---|---|---|
| Portfolio | 95/5 fixed | Volatility overlay, equity 60–95% |
| Fee | 1.50% | 1.00% |
| Net return | 17.76% | 16.18% |
| Max drawdown | −33.21% | −24.94% |
| Sharpe | 0.75 | 0.87 |
| Benchmark | ACWI PHP total return (good work) | Old spec, marked *restating* |

**Recommended merge:** Prince's ACWI benchmark work **+** the volatility overlay **+** one fee.
Prince's FX and total-return handling on the ACWI leg is correct and should be kept.

**Decision required from the team — the fee.** See 3.2. Do not proceed past Day 2 with two numbers.

**Verify:** grep both documents for every performance figure. No number may appear with two
different values across fact sheet, executive summary, engine output and brief.

### 1.2 Fix the submission mechanics (15 minutes, pure downside if missed)

Primer page 7 specifies exactly:

- **Subject:** `[Submission] - Los Angeles 76ers_The Firsts Fund_Ateneo de Manila University`
- **Attachment:** `LosAngeles76ers_TheFirstsFund.pdf`
- **To:** finquest@bpi.com.ph
- **One PDF** containing Fact Sheet (≤2pp) then Executive Summary (≤3pp + 1 annex)

Our current file is named `[Submission] - [TeamName]_TheFirstsFund_ADMU.pdf`, which uses the
*subject* format as the *filename* and still contains the placeholder `[TeamName]`.

**Verify:** filename matches the pattern exactly; open the merged PDF and count 6 pages total
(2 + 3 + 1); confirm page 1 is the fact sheet.

### 1.3 Raise the font floor to 8pt

**Verify:** `grep -o "font-size: *[0-9.]*pt"` on both files returns nothing below 8pt, and both
documents still render at 2 and 4 pages respectively.

---

# DAY 2 — Tuesday 12 August: correctness

### 2.1 Fix the PSEi total-return error

The fact sheet reports **"Excess vs. PSEi +18.46%"** using the PSEi **price** index. Our holdings
are dividend-adjusted; the price index is not. We are crediting ourselves with dividends the
benchmark never received.

**How:** source PSEi Total Return Index for 9 Aug 2021 – 7 Aug 2026. Recompute. Expect the
figure to fall to roughly +15.5%.

**Verify:** the corrected figure appears identically in fact sheet and executive summary, and
the footnote says "total return" for both legs.

### 2.2 Report two benchmarks, not one

- **Primary (policy):** 30% PSEi TR + 65% ACWI PHP net TR + 5% 91-day T-bill. Mirrors our own
  policy weights, which is the textbook construction.
- **Secondary (disclosed):** ACWI-only, as Prince computed it.

Estimated effect of the policy benchmark: excess rises from +2.77% to roughly +5.6–7.2%,
tracking error falls from 13.88% to roughly 11.5–12.5%, information ratio moves from **0.17 to
roughly 0.45–0.60**.

**Why both:** moving from a benchmark scoring 0.17 to one scoring 0.6 looks like benchmark
shopping if we show only the second. Showing both, and justifying the primary on mandate
grounds, converts the same act into visible rigour.

**Verify:** recompute with the actual PSEi TR series rather than my estimate. Confirm the
policy benchmark weights equal the fund's stated policy weights exactly (30/65/5).

### 2.3 Add the t-statistic disclosure

Prince's point is correct and it is the strongest defensive move available to us.

| | Value | t-stat | Years to reach t = 2 |
|---|---|---|---|
| IR vs ACWI-only | 0.17 | 0.38 | 138 |
| IR vs policy benchmark | ~0.50 | 1.12 | 16 |
| Sharpe (with overlay) | 0.87 | **1.95** | 5 |

Add to the annex, in our own words:

> We do not claim statistically significant alpha, and no five-year simulation could produce it.
> The t-statistic on our excess return is 0.4. What the back-test demonstrates is that the
> methodology yields a coherent, risk-budgeted portfolio, not that these ten securities were
> knowable in 2021.

**Consequence to enforce:** if we invoke statistical insignificance to defuse IR, we must remove
every implicit skill claim elsewhere. Sweep both documents for language that presents the
return gap as proof we pick better. One posture, held everywhere.

**Correct before the defense:** tracking error is a standard deviation; information ratio is a
mean-over-sd ratio, like Sharpe. Conflating them in front of a finance judge would undercut an
otherwise strong argument.

---

# DAY 3 — Wednesday 13 August: the two scoring gaps

### 3.1 Feasibility (25%) — unit economics of a ₱100 account

**This is the hole.** A ₱100 account at a 1.00% fee generates **₱1.00 of revenue per year.**
Every judge on a BPI Wealth screening committee will see this immediately, and we currently say
nothing about it.

Break-even balance:

| Cost to serve / yr | At 1.00% fee | At 1.50% fee |
|---|---|---|
| ₱100 | ₱10,000 | ₱6,667 |
| ₱200 | ₱20,000 | ₱13,333 |
| ₱300 | ₱30,000 | ₱20,000 |

Months for an auto-invest account to cross break-even (12% net growth):

| Monthly contribution | To ₱10k | To ₱20k | To ₱30k |
|---|---|---|---|
| ₱250 | 34 mo | 60 mo | 81 mo |
| ₱500 | 19 mo | 34 mo | 48 mo |
| ₱1,000 | 10 mo | 19 mo | 27 mo |

**The argument to make, in roughly four lines of the annex:**

1. The ₱100 account is not the business. It is customer acquisition, and it is deliberately
   priced below cost.
2. Cost to serve is near zero incrementally because the fund sits inside the BPI app and BPI's
   existing transfer agency. We add no infrastructure.
3. Auto-invest on by default plus round-ups is what carries an account across break-even. Our
   retention mechanics are the unit economics, not a separate feature.
4. The payroll channel means BPI already owns the lifetime relationship. A ₱100 first
   investment at 22 is the cheapest acquisition of a 40-year wealth client BPI will ever make.

That last point is genuinely strong and it turns our weakest commercial number into our best
strategic one.

**Verify:** state our cost-to-serve assumption explicitly and label it an assumption. Do not
present a fabricated figure as sourced.

### 3.2 Decide the fee (team decision, blocks 1.1)

| Option | Case for | Case against |
|---|---|---|
| **1.00%** | Sharper contrast with ALFM's 2.00%. A real, verifiable commitment. | Break-even needs ₱10–30k. Indefensible without the analysis above. |
| **1.50%** | Commercially safer. Still well under ALFM. | Weaker differentiation on an access-led pitch. |

**Recommendation:** keep **1.00% only if 3.1 ships with it.** A defended 1.00% beats an
undefended 1.00% and also beats a 1.50% with no economics section. If we cannot finish 3.1 by
end of Day 3, revert to 1.50%.

### 3.3 Originality (30%) — make it findable

Our original elements exist but are spread across three pages. A judge scoring this criterion
should be able to point at one block. Add a compact list, near the top of the executive summary:

1. **Horizon-weighted suitability.** We do not route around the CSA, we rebuild it to price time
   horizon and human capital. Nobody in the market does this.
2. **Education as the compliance pathway.** The unlock module is not a tutorial bolted on. It is
   the mechanism by which a conservatively-scored investor legitimately reaches a growth asset.
3. **Drawdown pre-commitment.** The investor types −22.18% before investing ₱1. We lead with the
   loss.
4. **Published optimiser.** Verifiability instead of assurance. Anyone can rerun our weights.
5. **Human-capital diversification.** 30/65 is not a country view. It is the hedge against an
   asset the investor already owns and cannot sell.
6. **Fractional units at ₱100.** Structural, not promotional. Mutual fund shares cannot do this.

**Frame each as a reimagining, not an improvement**, because that is the literal wording of the
criterion. "We rebuilt the suitability test" scores; "we made onboarding easier" does not.

**Verify:** hand the executive summary to someone outside the team. Ask them to name three
things that do not exist in the market today. If they cannot, the section has failed.

### 3.4 Team credentials (required element, currently thin)

The primer requires: *"Who are the members of the team, and what are their credentials?
(Education, Work Experience, Certifications)."* We currently list names and degree programmes only.

Add per member: degree and year, relevant internships or work, any certifications in progress,
and the specific role played on this submission. Two lines each. This is a required element we
are leaving points on.

---

# DAY 4 — Thursday 14 August: assemble, verify, submit

### 4.1 Cut to fit at the 8pt floor

Cut in this order, protecting the highest-weighted criteria:

1. Repetition between fact sheet and executive summary
2. Any sentence that asserts without evidence
3. Methodology detail that the published engine already documents
4. **Never cut:** the disclosure passages. They are our single strongest credibility asset and
   they read directly onto Background & Research and Fund Process.

### 4.2 Merge to one PDF, fact sheet first

### 4.3 Final verification checklist

| Check | How | Pass condition |
|---|---|---|
| Page count | Count PDF pages | 2 + 3 + 1 = 6, fact sheet first |
| Font floor | grep font-size declarations | Nothing below 8pt; prose at 11pt |
| Paper size | PDF page dimensions | 595 × 842 pt (A4) on every page |
| Figure consistency | grep each statistic across all files | Every number appears with exactly one value |
| No stale figures | grep 17.74, 33.25, 30.22, 1.50%, 10.32, 18.46 | Zero hits unless deliberately retained |
| Required elements | Tick against primer page 6 list | All 11 present in the fact sheet |
| Guide questions | Tick against primer page 8 list | All investment questions answered |
| Filename & subject | Compare to primer page 7 | Exact match, no placeholders |
| Feeder fund rule | Confirm 0% CIS holdings | Explicitly stated |
| Links and sources | Open every cited URL | All resolve |

### 4.4 Send on Thursday, not Friday

---

# Known risks we are choosing to carry

Be ready to name these before a judge does. Naming them first has been our strongest move all week.

1. **Ten securities chosen in 2026, tested on 2021–26 data.** Hindsight bias. Disclosed in A2.
2. **The window flattered the theme.** 2023–25 was the best possible period for AI and datacentre
   capex, and the Buildout Test selects for exactly that. Disclosed for GE Vernova, but the issue
   is broader than one holding. Consider widening that disclosure.
3. **Conviction scores are estimates.** They drive every weight. The ±10-point sensitivity test
   defends this reasonably; be ready to say so plainly.
4. **No operating history.** Everything is simulated.

---

# If we make the Top 5

Phase 2 runs 1 September to 12 October, defense on 17 October at Makati Diamond Hotel. Two new
deliverables beyond the refined fact sheet: a **30-second marketing video** and a **customer
roadmap graphic**. Phase 2 adds Pitch (10%) and Q&A (10%), and the Q&A criterion rewards exactly
the disclose-your-own-weakness posture we have been building. Do not start these before the 15th.
