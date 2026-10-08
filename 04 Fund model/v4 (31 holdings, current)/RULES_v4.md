# Firsts Fund: selection and weighting rules, v4

Fixed on 8 October 2026, before any v4 selection or performance run. These rules apply the team's Section 2A
("Tightened theme and M.V.P. selection process", 7 Oct 2026). Nothing below is to be changed after seeing results.
If a rule turns out to be wrong, change it openly, log the change, and rerun everything.

## Theme
Listed businesses that own, operate or supply essential capacity supporting everyday life and economic activity,
where replacing that capacity is difficult and the business earns from providing it.

**Research universe.** Eight capacity types, each taking up to the 20 largest listed companies by US$ market value
(minimum US$1bn):

| Type | Kind |
| --- | --- |
| Power generation & grids | Owner |
| Water | Owner |
| Digital networks (telecom, towers, data centres) | Owner |
| Ports | Owner |
| Airports & toll roads | Owner |
| Healthcare facilities (hospitals) — **new in v4** | Owner |
| Grid & power equipment | Supplier |
| Semiconductors | Supplier |

- These types define where we look. They are not allocations.
- Mainland China A-shares are not in the universe, because the fund's access to them is not assumed.

## M · Map the milestone (thematic eligibility: pass or reject)
- **M1 · Material exposure.** One of two tests:
  - the company's GICS sub-industry is on the qualifying list (team-assigned), or
  - at least 50% of its revenue comes from a qualifying segment (conglomerates, latest annual report).

  Health Care Facilities is added to the list. Other healthcare sub-industries (services, REITs, equipment) are not on it.
- **M2 · Earns from the capacity.** Operating cash flow above zero and ROIC above zero (stockanalysis.com, trailing).
  A company that runs scarce capacity but does not yet earn from it fails "credible mechanism for capturing value".
- **No dated capacity target is required.** A published target is recorded as supporting evidence only.
- **Output.** For every company held, an eligibility note covering:
  - the capacity it provides
  - why that capacity is hard to replace (licence or concession, network scale, permits, specialist capability, time and capital to replicate)
  - how it earns from that capacity
  - the main competitive or regulatory risk

## V · Verify the investment (eligible, watchlist, or reject)
Every test below is set per capacity type in advance. No exceptions are made for individual stocks.

**Reject:**
- **V1 · Debt service under stress.** Stressed interest cover = interest cover × (1 − s × EBITDA/EBIT). Reject if below 1.5×.
  - The factor EBITDA/EBIT, which equals (EV/EBIT)/(EV/EBITDA), carries the shock through to EBIT, which has to cover interest.
  - Shock s by type, from each type's worst observed demand or price episode:

    | Type | s | Basis |
    | --- | --- | --- |
    | Water | 10% | Regulated tariffs, inelastic demand |
    | Power | 15% | Regulated or contracted; fuel pass-through lags |
    | Digital networks | 15% | Subscription revenue; price wars |
    | Healthcare facilities | 25% | 2020 elective-procedure shutdowns |
    | Ports | 30% | 2009 trade collapse plus operating leverage |
    | Grid equipment | 35% | Industrial capex downturns |
    | Semiconductors | 50% | 2023 memory downturn |
    | Airports & toll roads | 60% | 2020 traffic collapse |

  - A company with net cash passes.
- **V2 · Leverage outlier.** Reject if net debt/EBITDA exceeds the median of its type's universe by more than 2.0 turns.
  This is a refinancing need well above peers that carry the same business risk.
- **V3 · Investability.** Reject if either:
  - the position cannot reach 1% of a ₱1bn fund within 5 trading days at 20% of average daily value, or
  - the stock has no price history in our data sources.
- **V4 · Governance.** Reject when a material governance concern is on public record at the assessment date:
  - Adani group companies: US DOJ and SEC charges against group founder and executives, November 2024.

**Watchlist:**
- **V5 · Cash conversion.** Operating cash flow below 50% of EBITDA.
- **V6 · Price not justified.** EV/EBITDA above 2× its type's median.
- **V7 · Merit in the bottom half of its type.** Watchlist pending a better price.

**Merit (within type, among names that pass V1 to V4):**
- **Valuation percentile** = average of two percentile ranks:
  - EV/EBITDA (lower is better)
  - cash yield = (operating cash flow − depreciation & amortisation) / EV (higher is better). D&A stands in for maintenance capex, so growth capex does not count against owners. Where D&A is missing, free cash flow is used.
- **Quality percentile** = ROIC − WACC.
- **Merit** = average of the valuation and quality percentiles.
- **Eligible** when merit is at least 0.50 and V5 and V6 do not apply.
- **Output.** A decision record for every name: rule results, ratios, peer medians, merit and the reason for the decision.

Passing M does not guarantee passing V. Passing V does not guarantee a position.

## P · Position the risk (portfolio construction)
**Default weighting.** Equal risk contribution (ERC):
- uses the previous 156 weekly peso returns, with at least 104 required
- re-solved quarterly
- needs no return forecasts and stops any one stock dominating risk

Every report also shows equal weight and inverse volatility on the same holdings, so the value ERC adds is visible.

**Inclusion and the holdings count.** Eligible names are processed in merit order (ties go to higher ROIC − WACC). Each candidate:
1. **Duplicate.** If its weekly return correlation with an already-held name of the same type is above 0.80, it goes to the watchlist ("duplicates existing exposure").
2. **Added and re-solved.** The candidate is added and the weights re-solved under the limits below.
3. **Negligible position.** If the candidate's weight is below 1.0% of NAV, it goes to the watchlist. If an earlier holding falls below 1.0%, the lowest-merit such holding moves to the watchlist and the weights are re-solved.
4. **Diversification.** If the portfolio's diversification ratio (Σ wᵢσᵢ / σₚ) does not rise by at least 0.5%, the candidate goes to the watchlist ("adds too little diversification").

The holdings count is whatever this process leaves.

**Limits:**

| Limit | Level | Source |
| --- | --- | --- |
| Single issuer | 20% of NAV | **Regulatory:** BSP Circular 1234 (2026) as reproduced by RCBC Trust; above 15% must be exchange-traded equity of that issuer |
| Control group (Razon: ICTSI + Manila Water; Enel + Endesa) | 20% combined | **Internal:** treated as one issuer, the prudent reading |
| Capacity type | 25% | **Internal:** one regulation, cycle or demand shock hits a whole type (airports 2020, memory 2023) |
| Liquidity | Each weight ≤ its V3 liquidity capacity | **Internal** |
| Cash | Operating cash for redemptions, settlement and expenses, modelled at 3% of NAV (illustrative, not a commitment) | **Internal** |

There are no country quotas, no owner/supplier quotas and no fixed reserve.

**Review.** Quarterly, and whenever a material event affects the thesis:
- M and V are re-run on the then-available data.
- Positions may be increased, reduced or exited.
- Every decision is logged with its reason.
- Quarterly review does not mean quarterly trading.

## Testing conventions (identical for v3 and v4)
- **Period and data.** 1 Oct 2021 – 2 Oct 2026, weekly Friday closes, total return, converted to pesos at the week's rate.
- **Fee.** 1.50% a year on NAV.
- **Trading cost.** 0.30% of traded value, covering commission, spread and transaction taxes on average across markets. It is charged on the initial build and on every quarterly re-solve.
- **Dividend withholding.** Approximate rate for the listing country × trailing dividend yield, deducted weekly. Rates are listed in the code and need confirmation from tax counsel.
- **Cash.** Earns the BSP policy rate minus 0.50 pt (the overnight deposit facility). The policy rate itself is not assumed.
- **Selection look-ahead.** Holdings are chosen once, on October 2026 data. Results are therefore labelled **"historical performance of the currently selected portfolio"**. They are not a backtest of the M.V.P. process. Weights use only past returns.
- **Reference indexes.** The iShares MSCI ACWI ETF (global equity) and the iShares Global Tech ETF (context), both in pesos after their own ETF costs.
  - Neither is the fund's benchmark. The team will select the benchmark separately.
- **Long-run evidence.** Ken French US industry portfolios mapped to the eight types, 1990–2026.
  - Labelled **"industry proxy, context only"**. It does not validate the company screens.
- **Investor outcomes.** Rolling 60-month regular-contribution outcomes on the proxy, with and without the account-level glidepath, reported separately from fund-only performance.

## Implementation clarification (written while coding the engine, before any v4 result was seen)
- While the candidate set is too small for the limits to be feasible (fewer than five names cannot meet a 20% issuer ceiling with 97% invested), the P inclusion tests use unconstrained ERC weights. Final weights, and every quarterly re-solve in testing, apply all limits.
- P2 is folded into the inclusion order: candidates without 104 weeks of price history at the decision date go to the watchlist.
