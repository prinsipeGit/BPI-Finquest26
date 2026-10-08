# Firsts Fund — Deliverables Tracker

**Version:** 1.6  
**Last updated:** 2026-10-08 (Thu)  
**Updated by:** Luis Tengonciang

| Milestone | Date | Days left (from last update) |
| --- | --- | --- |
| Phase 2 submission | **Mon 12 Oct 2026** | 4 |
| Final Showdown (10-min pitch + 10-min Q&A) | **Sat 17 Oct 2026** | 9 |

**Status key:** ✅ Done · 🟡 In progress / draft exists · 🔴 Not started · ❔ Unknown, confirm with the team  
**How to update:** change the status, owner or notes. Bump the version (1.0 → 1.1 for status changes, → 2.0 when scope changes), set *Last updated*, and add a line to the change log at the bottom. Commit the change and push.

---

## A. Phase 2 submission (due 12 Oct, per Phase 2 Finalist Guidelines)

Send by email to **finquest@bpi.com.ph** with the subject **`FINALIST_LosAngeles76ers_Phase2`**, and include a Google Drive link holding the fact sheet, video and deck.

| ID | Deliverable | Format | Owner | Status | Where it lives | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Final fund fact sheet | PDF | Luis | 🟡 | `01 Phase 2 submission/LosAngeles76ers_FirstsFund_FactSheet.pdf` (v4) | Polished 8 Oct (section G). Team read-through; confirm G9 settlement; check numbers against the team pitch |
| A2 | 30-second marketing video (team-made) | .mp4 | TBD | 🟡 | Team's own files | Apply the Section 8 consistency edits to the script. Export as .mp4 and time it at 30 seconds or less |
| A3 | One-slide customer roadmap (discovery → ongoing engagement) | Slide inside A4 | TBD | ❔ | Team's pitch deck | Confirm it's planned in the team deck |
| A4 | Final presentation deck for the 10-minute pitch (team-made; Investment + Marketing + CX pillars) | .pptx | TBD | 🟡 | Team's own files (add to repo when final) | See section B |
| A5 | Google Drive folder with A1, A2, A4 (view access for BPI) | Link | TBD | 🔴 | — | Create the folder, set sharing, test the link from a logged-out browser |
| A6 | Submission email sent | Email | TBD | 🔴 | — | Send by 11 Oct evening as a buffer. Keep the sent confirmation |

## B. Team pitch deck checklist (must all be true before A4 is done)

The 25-slide `Presentation deck/Firsts Fund — Competition Pitch.pptx` is an **internal strategy reference** for the team (and Q&A backup material). It is not the submission deck.

| ID | Item | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| B1 | **Marketing pillar** covered: audience, message ("Fund your firsts."), channels, campaign, how the video fits | TBD | ❔ | Required by the guidelines |
| B2 | **Customer experience pillar** covered: onboarding, ₱100 minimum, account-level glidepath feature, app/site mock-ups | TBD | ❔ | Required. Use the app and site mock-ups after the Section 8 edits |
| B3 | Customer roadmap slide included (= A3) | TBD | ❔ | — |
| B4 | Investment section draws its figures from the reference deck and fact sheet (v4: 31 holdings, 24.95% p.a., NFRA benchmark) | TBD | ❔ | Any figure on a slide must match A1 |
| B5 | Fits **10 minutes**; extra detail moved to an appendix for Q&A | TBD | ❔ | Timing is strictly enforced |
| B6 | Speaker split: who presents which section | TBD | ❔ | — |

## F. Quantitative portfolio and risk (owner: Luis): weighting, simulation, performance

Current model is v4: 31 holdings plus 3% cash, ERC on 156 weekly peso returns, rebalanced quarterly, solved on data to 2 Oct 2026. Figures in the old Google Doc role notes (16 holdings, 17.14%, Vertiv vs IHH, 20,000-sequence shuffle, 24-month glidepath) are out of date. Don't present them.

### F1. Deliverables

| ID | Deliverable | Status | Next action |
| --- | --- | --- | --- |
| F1.1 | Rerunnable v4 model (internal only; judges won't run it). **Needed only if a number changes** (e.g. C1 rates, beta vs NFRA, supplier attribution) | 🔴 | Low priority until then. Fix paths in `engine4.py` / `analyze4.py` (they expect `../v3`, `../yret.json`, `../inputs.py`, `../../compare/ixn.txt`, `../../backtest`). Recover `ixn.txt`, which is missing from the repo and the Downloads folder (check the `_duplicates` .tgz bundles). Rerun and confirm the headline numbers match |
| F1.2 | Quant slides for the team pitch (about 2–3 slides): how weights are set, the risk limits, performance vs benchmark | 🔴 | Lead with returns vs benchmark (mentor feedback). Keep the method to one line plus one visual |
| F1.3 | Performance table: 5-year CAGR, vol, Sharpe, max drawdown, worst 12 months, beta, calendar-year returns vs NFRA / ACWI / PSEi | 🟡 | Exists in `results4.json` and the reference deck. Re-verify after F1.1 |
| F1.4 | Weighting explainer: ERC vs equal-peso weights, why a holding gets a small weight (NVIDIA 1.64% example) | 🟡 | Reference deck slides 8, 11 and 14 have the content. Simplify for the pitch |
| F1.5 | Bias and limitations statement (one slide or appendix) | 🟡 | See F2. Every number must carry the label "historical performance of the currently selected portfolio" |
| F1.6 | Stress / contribution evidence: 36-year proxy, rolling 60-month ₱1,000/month results, glidepath effect | 🟡 | `05 36-year backtest/backtest_v4.py`. Confirm C6 (bad-year figure) with the team |
| F1.7 | Sensitivity of the holdings count to the P thresholds | 🟡 | `sens4.py` → `sens4.json`. Put one line in the appendix |
| F1.8 | Q&A answers for the quant judge questions (F3) | 🔴 | Write them, then drill with the backup (Fund lead) |
| F1.9 | Figures handed to the fact sheet / pitch / video owners match `results4.json` | 🔴 | Same as D4. Do it last |

### F2. Verify before presenting

| ID | Check | Status | Why it matters |
| --- | --- | --- | --- |
| F2.1 | **Selection look-ahead**: the 31 holdings were chosen with Oct 2026 ratios and then backtested over 2021–26. The 24.95% is hindsight, an upper bound | 🔴 | The biggest credibility risk. Options: (a) label it clearly (current approach); (b) re-run selection at past dates (point-in-time) if data allow; (c) lead with the 36-year proxy for "expected" behaviour |
| F2.2 | Survivorship: the universe is today's 20 largest per type ≥ US$1bn | 🔴 | Biases returns up. State it |
| F2.3 | Weights are walk-forward (only data before each quarterly rebalance) | ✅ | Checked in `engine4.simulate`: `window(R, t, …)` uses data up to t−1 day |
| F2.4 | ERC solver converges and all limits hold at every rebalance (issuer 20%, group 20%, type 25%, liquidity) | 🟡 | `analyze4.py` logs violations. Confirm the list is empty after F1.1, and spot-check that risk contributions are roughly equal for the final weights |
| F2.5 | Costs: 1.50% fee (weekly accrual), 0.30% trading cost on turnover (≈0.21% a year), dividend withholding (≈0.37% a year) | 🟡 | Withholding = today's dividend yield × approximate treaty rate, applied to every past year. Small drag, but the rates need C1. Missing weekly returns: **0 of 8,091**, checked ✅ |
| F2.6 | Sharpe definition: (CAGR − cash rate) / annualised weekly vol, with cash = BSP policy − 0.50 pt | 🟡 | Mixes geometric return with arithmetic vol. Fine if stated. Check the cash-rate series covers 2021–26 |
| F2.7 | Beta and correlation are measured vs ACWI, but the benchmark is NFRA. **vs NFRA: beta 0.59, correlation 0.71** (`bench.json`) | ✅ | Report beta vs NFRA too, or say explicitly "beta vs world market" |
| F2.8 | NFRA benchmark series: peso conversion, checksum 2523099084, 10.02% p.a. | 🟡 | Re-derive once. The comparison is vs an ETF *after its fee*, while the fund is shown after 1.50%; state that |
| F2.9 | Currency: all returns are in PHP, unhedged on purpose | 🟡 | Have the one-line rationale ready, plus how much of the return came from USD/PHP |
| F2.10 | Liquidity cap = (avg daily volume × price × 20% of volume × 5 days) ÷ ₱1bn fund size | 🟡 | Never binds at ₱1bn (tightest: OMA 12.1% vs 1.98% held). A smaller fund only loosens it. It would bind at roughly ₱6bn+ (OMA). Have one line ready on why ₱1bn |
| F2.11 | Memory makers (SK hynix, Micron) at a cyclical peak; suppliers contributed about 71% p.a. | 🔴 | Show the result with suppliers removed, or at least the attribution |
| F2.12 | Early quarters hold fewer names (a name needs 104 weeks of history) | ✅ | 29 names (Q4 2021–Q1 2022), 30 (Q2–Q3 2022), 31 from Oct 2022. Footnote only |
| F2.13 | 36-year proxy is industry-level, not our screens: "context only" label on every chart | ✅ | Already labelled in the reference deck |

### F3. Judge questions to prepare (v4 versions)

- "Is a 24.95% return credible?" → No, as a forecast. It's the hindsight performance of today's selection. Point to the proxy (11.96% p.a., about the market's return) and the costs included.
- "How is ERC calculated?" → Each holding contributes the same share of portfolio volatility, using 3-year weekly covariance in pesos, re-solved quarterly under the limits.
- "Why does NVIDIA get only 1.64%?" → High volatility and high correlation with the other chip names, so a small weight already carries an equal share of the risk.
- "What biases exist?" → Selection look-ahead, survivorship, a constant withholding approximation, and the liquidity cap assuming ₱1bn AUM.
- "Why unhedged?" / "How do you know the glidepath helps?" → Rolling 60-month result: worst 0.65× without the glidepath vs 0.87× with it (proxy, illustrative).

## G. Fact sheet polish plan (A1)

Source: `04 Fund model/v4 (31 holdings, current)/build_factsheet4.py` (reportlab) → PDF. Edit the script, then regenerate. Don't edit the PDF by hand.
Inputs: Phase 2 guidelines (strategy, objective, portfolio construction, suitability, risks, value proposition), mentor feedback ("returns vs benchmark", "too technical", no "bets", label proposed terms), 7 Oct team decisions.

| ID | Change | Priority | Owner | Status |
| --- | --- | --- | --- | --- |
| G1 | **Benchmark = NFRA everywhere** (rebuilt 8 Oct: `bench_nfra.py`, `map/bench_usd.json` → `bench.json`; reproduces stored ACWI to 0.002% over 5 years): Key facts still say "To be selected by the team". Add an NFRA line to the chart and a row to the table (10.02% a year, ₱100 → 161, worst fall −12.6%); keep ACWI and PSEi as references. `map/infra.json` is not in the repo; find the 8 Oct version | P0 | Luis | ✅ |
| G2 | Verify the regulatory citation "BSP Circular No. 1234 (2026)". Verified: real, issued 20 May 2026, single-issuer limit raised 15% → 20% | P0 | TBD | ✅ |
| G3 | Reconcile every figure with the team pitch and the proposal (holdings 31, markets 14, PH 4.80%, fee 1.50%, cash 3%). Fact sheet checked against `results4.json` + `bench.json` ✅; team pitch still to check | P0 | Luis | 🟡 |
| G4 | Performance block leads with **fund vs benchmark** in pesos (headline: ₱100 → 306 vs NFRA 161). Cut the "Read this carefully" paragraph to two plain sentences. The hindsight label stays on page 1, next to the number | P1 | Luis | ✅ |
| G5 | Plain-language pass (customer-facing). Replace: "risk model", "industry proxy", "operating cash", "issuer ceiling", "dealing", "Overlaps we watch", "Countries are an outcome, not a target", "data vendor", "sub-industries" | P1 | TBD | ✅ |
| G6 | "Why it exists": drop the performance digs at BPI's own index fund (0.52%) and fund of funds (−4.19 pts). The judges are BPI Wealth. Keep the structural point (one fee layer, direct global shares, ₱100) | P1 | TBD | ✅ |
| G7 | Add a small "For a regular saver" box: ₱1,000 a month for 5 years, historical range (median 1.33× paid in; 11% of periods ended below paid-in), labelled illustrative. Depends on C5/C6 | P1 | Luis | ✅ |
| G8 | Fees: add an estimated total annual cost line (1.50% + about 0.21% trading + about 0.37% withholding ≈ 2.1%) | P1 | Luis | ✅ |
| G9 | Replace vague product terms: "Redemption settlement: per plan rules" → now "paid day 6 (T+5)", matching BPI's peso global equity class. **Product lead: confirm** | P1 | Product lead | 🟡 |
| G10 | Light visual polish within 2 A4 pages. Done: taller chart, headline line, page-1 gap filled. Not done: allocation chart (optional) | P2 | TBD | 🟡 |
| G11 | Final proofread, export, and file name `LosAngeles76ers_FirstsFund_FactSheet.pdf`; copy into `01 Phase 2 submission/`. Exported and copied; team proofread pending | P0 | TBD | 🟡 |

## C. Model and evidence open items (from AGENTS.md)

| ID | Item | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| C1 | Confirm dividend withholding rates (tax counsel) | TBD | 🔴 | Currently approximate, by listing country |
| C2 | Cite real episodes for each stress shock per capacity type | TBD | 🔴 | Water 10%, power 15%, networks 15%, hospitals 25%, ports 30%, grid eq. 35%, chips 50%, airports 60% |
| C3 | Check GICS sub-industries, especially healthcare facilities and Kamigumi | TBD | 🔴 | Team-assigned today |
| C4 | Spot-check debt, cash flow and ROIC for the 31 holdings | TBD | 🔴 | Memory makers are at a cyclical peak; flag this in Q&A |
| C5 | Calculator: contributions-only baseline + balanced scenarios (5-year+ only); label the glidepath schedule illustrative | TBD | 🔴 | — |
| C6 | Confirm calculator "bad year" = 36-year worst 12 months (−27.0%) | TBD | ❔ | Waiting on team confirmation |
| C7 | Make sure the superseded v2 "changes" deck is never presented | TBD | ✅ | Note only |

## D. Consistency pass (Section 8 of the 7 Oct consolidated changes)

| ID | Item | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| D1 | Video script uses "Firsts Fund", v4 facts, proposed-feature wording | TBD | 🔴 | Feeds into A2 |
| D2 | Website mock-up updated | TBD | 🔴 | Feeds into B2 |
| D3 | App mock-up updated | TBD | 🔴 | Feeds into B2 |
| D4 | Fact sheet, deck, proposal doc and video all quote the same figures | TBD | 🔴 | Final check before A6 |

## E. Final Showdown prep (17 Oct)

| ID | Item | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| E1 | Mock presentation + Q&A with lead mentor (5–9 Oct window) | TBD | ❔ | Confirm the date and whether it happened |
| E2 | Full timed run-throughs (at least 3) at 10:00 or less | TBD | 🔴 | — |
| E3 | Q&A drill: the 6 prepared answers + pillar questions on Marketing and CX | TBD | 🔴 | Owners per topic |
| E4 | Backup copies of the deck and video (USB + Drive), plus a PDF of the deck | TBD | 🔴 | — |

---

## Change log

| Version | Date | Change |
| --- | --- | --- |
| 1.6 | 2026-10-08 | Fact sheet polished: NFRA benchmark rebuilt and added, plain language, saver illustration, all-in cost, settlement terms, citation verified. Beta vs NFRA added (F2.7). |
| 1.5 | 2026-10-08 | Added section G: fact sheet polish plan. Found the repo fact sheet still has no benchmark (NFRA missing). |
| 1.4 | 2026-10-08 | F1.1 downgraded: the repo is for team version control; a rerun is needed only if a figure changes. |
| 1.3 | 2026-10-08 | F2.5, F2.10, F2.12 checked against `sim4.pkl`: no missing returns, liquidity cap never binds, holdings 29→31 by Oct 2022. |
| 1.2 | 2026-10-08 | Added section F: quantitative portfolio and risk deliverables, verification checks and judge questions (owner: Luis). |
| 1.1 | 2026-10-08 | Pitch deck and video are team-made; the 25-slide deck is an internal strategy reference. Section B is now a checklist for the team deck. |
| 1.0 | 2026-10-08 | Tracker created from the Phase 2 Finalist Guidelines and the AGENTS.md open items. Statuses were checked against the repo contents. |
