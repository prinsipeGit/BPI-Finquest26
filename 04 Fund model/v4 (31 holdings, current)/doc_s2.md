## The rules as applied

Full text and thresholds: `RULES_v4.md` in the fund model folder. Each threshold below was set per capacity type before testing; no exception was made for any stock.

| Step | Test | Outcome if failed |
| --- | --- | --- |
| M1 Material exposure | GICS sub-industry on the qualifying list, or at least 50% of revenue from a qualifying segment | Reject |
| M2 Earns from the capacity | Operating cash flow and ROIC both above zero | Reject |
| V1 Debt under stress | Interest cover after an EBITDA shock (water 10%, power 15%, networks 15%, hospitals 25%, ports 30%, grid equipment 35%, chips 50%, airports & roads 60%) at least 1.5× | Reject |
| V2 Leverage outlier | Net debt/EBITDA no more than 2.0 turns above the type median | Reject |
| V3 Investability | Position of 1% of a ₱1bn fund sellable in 5 days at 20% of volume; price history available | Reject |
| V4 Governance | No material concern on public record (Adani group: US DOJ/SEC charges, Nov 2024) | Reject |
| V5 Cash conversion | Operating cash flow at least 50% of EBITDA | Watchlist |
| V6 Price | EV/EBITDA no more than 2× the type median | Watchlist |
| V7 Merit | Merit at least 0.50 within its type: half valuation (EV/EBITDA; cash yield = (OCF − D&A)/EV), half quality (ROIC − WACC) | Watchlist |
| P1 Duplicate | Weekly correlation with a same-type holding at most 0.80 | Watchlist |
| P3 Sensible size | Risk-based weight at least 1.0% of NAV | Watchlist |
| P4 Diversification | Adding it raises the diversification ratio by at least 0.5% | Watchlist |

**Weighting:** equal risk contribution on the previous 156 weekly peso returns (104 minimum), re-solved quarterly. While the candidate set is too small for the limits to be feasible, the inclusion test uses unconstrained ERC; the final weights apply every limit. This clarification was written during coding, before any results were seen.

**Limits:** single issuer 20% of NAV (regulatory, BSP Circular No. 1234, a ceiling, not a target); company group 20% (internal); capacity type 25% (internal: one shock can hit a whole type); liquidity as V3 (internal). Operating cash modelled at 3%. All limits held at all 21 quarterly rebalances.

**Testing conventions:** weekly Friday closes, 1 Oct 2021 – 2 Oct 2026, total return in pesos; 1.50% fee; 0.30% trading cost on traded value (about 0.21% a year); estimated dividend withholding by listing country (about 0.37% a year, rates to be confirmed by tax counsel); cash at the BSP policy rate minus 0.50 pt. Previous (v3) and revised (v4) rules use identical conventions.