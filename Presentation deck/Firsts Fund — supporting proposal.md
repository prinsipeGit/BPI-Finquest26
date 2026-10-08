# Firsts Fund — supporting proposal (revised rules, v4)

Oct 8, 2026 · @Luis

## Summary

The revised rules hold **31 companies** in eight kinds of capacity, chosen and weighted by a process fixed on 8 October 2026 before any results were run. The holdings count, country mix and every weight are outputs; nothing was set by hand.

- **What changed:** healthcare facilities added to the theme; no dated-target requirement; debt tested under a stress set per capacity type; valuation judged against same-type peers with a cash-flow measure; eligible, watchlist or reject for every company; holdings count from inclusion tests; BSP's 20% single-issuer ceiling instead of our 10% cap; operating cash instead of a fixed 10% reserve; no owner/supplier or country quotas.
- **Funnel:** 140 companies → 129 pass Map → 49 eligible after Verify (35 rejected, 45 watchlisted) → 31 held (18 watchlisted at Position).
- **Philippines:** 4.8% (ICTSI). Manila Water moved to the watchlist on cash conversion.
- **Evidence, labelled:** the five-year figures are the *historical performance of the currently selected portfolio* (25.0% a year after all modelled costs, against 16.2% for the MSCI ACWI ETF). They include selection hindsight and are not a backtest of the process. The 36-year industry proxy (12.0% a year against 12.2% for a same-cost market fund) is context for the theme only.
- **Benchmark:** to be selected by the team; the ETFs here are references, not the benchmark.

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

## Holdings assessment

Theme fit makes a company eligible, Verify decides whether it is worth owning, and Position sets the weight; the milestone line is the investor story, never the reason to buy. Ratios: stockanalysis.com, 8 Oct 2026; medians are among same-type companies that passed V1–V4; weights solved on data to 2 Oct 2026.

| Holding | Capacity | Theme and milestone | Fundamentals and valuation | Key risks | Portfolio role | Weight and rationale |
| --- | --- | --- | --- | --- | --- | --- |
| Exelon (US) | Power generation & grids | Regulated electricity and gas delivery networks in Chicago, Philadelphia, Baltimore and Washington DC (ComEd, PECO, BGE, Pepco). Hard to replace: State-franchised monopoly networks; no competing wires can be built. Earns: Regulated return on a growing rate base. *First home: the power behind the electricity bill* | EV/EBITDA 11.2× (median 12.1×); cash yield 3.7% (median 3.3%); ROIC − WACC −0.7 pts (median −0.7); merit #6 of 15; net debt 6.1× EBITDA, stressed cover 1.8× | Rate-case outcomes; highest leverage of the power holdings (6.1× net debt/EBITDA) | Vol. 20%; avg. correlation 0.08 | **5.81%**; 3.9% of risk |
| Westports (MY) | Ports | Container terminals at Port Klang, Malaysia, on the Strait of Malacca. Hard to replace: Long-dated government concession and deep-water berths on a scarce site. Earns: Per-container handling tariffs. Evidence: [Capacity from 14M to 27M TEU a year (Westports 2)](https://theedgemalaysia.com/node/773945). *First business: goods coming in and going out* | EV/EBITDA 13.0× (median 13.0×); cash yield 5.7% (median 5.0%); ROIC − WACC +14.3 pts (median +4.5); merit #1 of 5; net debt 1.2× EBITDA, stressed cover 8.2× | Tariff approvals and execution of the Westports 2 expansion | Vol. 22%; avg. correlation 0.06 | **5.23%**; 3.8% of risk |
| ICTSI (PH) | Ports | Global container-port operator; home base Manila International Container Terminal. Hard to replace: Multi-decade port concessions; MICT renewed for another 25 years in 2026. Earns: Handling fees under long concessions in emerging markets. Evidence: [US$300M to expand MICT, South Luzon and Mindanao terminals by 2028](https://context.ph/2026/07/30/ictsi-secures-mict-operations-for-another-25-years/). *First business: goods coming in and going out* | EV/EBITDA 14.8× (median 13.0×); cash yield 5.0% (median 5.0%); ROIC − WACC +13.9 pts (median +4.5); merit #2 of 5; net debt 2.2× EBITDA, stressed cover 5.6× | Emerging-market concession, currency and political risk | Vol. 30%; avg. correlation 0.02 | **4.80%**; 3.6% of risk |
| Engie (FR) | Power generation & grids | French gas and power networks plus renewable and thermal generation. Hard to replace: Regulated network concessions; licensed generation sites. Earns: Regulated network returns plus contracted and merchant power. Evidence: [95 GW of renewables and storage by 2030 (57.2 GW end-2025)](https://www.engie.com/app/uploads/2026/03/PR-ENGIE-FY-2025-VDEF.pdf). *First home: the power behind the electricity bill* | EV/EBITDA 8.2× (median 12.1×); cash yield 3.6% (median 3.3%); ROIC − WACC +0.8 pts (median −0.7); merit #2 of 15; net debt 4.2× EBITDA, stressed cover 3.4× | Power prices; French state influence over tariffs | Vol. 21%; avg. correlation 0.08 | **4.57%**; 3.7% of risk |
| Bangkok Dusit Medical Services (TH) | Healthcare facilities | Thailand's largest private hospital network. Hard to replace: Hospital licences, specialist staff and referral networks built over decades. Earns: Patient fees from insured, self-pay and international patients. *First family: the hospital beds and specialists a family relies on* | EV/EBITDA 12.1× (median 17.2×); cash yield 4.7% (median 4.2%); ROIC − WACC +7.6 pts (median +7.9); merit #8 of 16; net debt 0.6× EBITDA, stressed cover 40.5× | Medical-tourism demand; Thai economy and staff costs | Vol. 23%; avg. correlation 0.06 | **4.49%**; 3.6% of risk |
| E.ON (DE) | Power generation & grids | Electricity distribution grids in Germany and across Europe, one of the continent's largest. Hard to replace: Regulated distribution concessions. Earns: Regulated return on grid investment. *First home: the power behind the electricity bill* | EV/EBITDA 8.2× (median 12.1×); cash yield 4.3% (median 3.3%); ROIC − WACC +0.1 pts (median −0.7); merit #3 of 15; net debt 3.9× EBITDA, stressed cover 2.5× | German regulator resets allowed returns; heavy capex to fund | Vol. 21%; avg. correlation 0.09 | **4.48%**; 3.7% of risk |
| Dr. Sulaiman Al Habib Medical (SA) | Healthcare facilities | Saudi Arabia's largest private hospital group. Hard to replace: Licensed hospitals and scarce specialist workforce. Earns: Fees from insurers and government contracts. *First family: the hospital beds and specialists a family relies on* | EV/EBITDA 24.9× (median 17.2×); cash yield 3.8% (median 4.2%); ROIC − WACC +12.3 pts (median +7.9); merit #7 of 16; net debt 2.2× EBITDA, stressed cover 4.8× | Valuation above healthcare peers (24.9× vs 17.2× median); Saudi reimbursement policy | Vol. 24%; avg. correlation 0.08 | **4.41%**; 3.7% of risk |
| Guangdong Investment (HK) | Water | Dongshen bulk-water scheme supplying most of Hong Kong's fresh water, plus Guangdong water networks. Hard to replace: The only bulk link of its kind; supply agreement with the Hong Kong government. Earns: Contracted water-supply fees. *First home: a reliable water connection* | EV/EBITDA 7.7× (median 12.3×); cash yield 8.1% (median 4.2%); ROIC − WACC +2.5 pts (median +0.4); merit #1 of 9; net debt 0.6× EBITDA, stressed cover 11.1× | State-owned group with property exposure; renegotiation of the Hong Kong water price | Vol. 38%; avg. correlation 0.01 | **4.36%**; 3.7% of risk |
| KDDI (JP) | Digital networks | Japan's second-largest mobile and fibre network (au). Hard to replace: Spectrum licences and nationwide network. Earns: Subscription revenue. *First job: the network behind every phone, laptop and payment* | EV/EBITDA 8.6× (median 8.1×); cash yield 4.1% (median 6.5%); ROIC − WACC +5.1 pts (median +3.8); merit #6 of 16; net debt 2.5× EBITDA, stressed cover 22.6× | Government pressure on mobile tariffs; competition | Vol. 19%; avg. correlation 0.05 | **3.81%**; 1.8% of risk; capacity-type limit 25% |
| Encompass Health (US) | Healthcare facilities | Largest US operator of inpatient rehabilitation hospitals. Hard to replace: Certificate-of-need rules in many states; Medicare-certified facilities. Earns: Mostly Medicare reimbursement per patient stay. *First family: the hospital beds and specialists a family relies on* | EV/EBITDA 10.1× (median 17.2×); cash yield 5.8% (median 4.2%); ROIC − WACC +7.8 pts (median +7.9); merit #5 of 16; net debt 1.9× EBITDA, stressed cover 6.0× | Medicare rate changes | Vol. 24%; avg. correlation 0.11 | **3.78%**; 3.8% of risk |
| AT&T (US) | Digital networks | US nationwide wireless and fibre network. Hard to replace: Spectrum licences and fibre that takes years to replicate. Earns: Subscription revenue. *First job: the network behind every phone, laptop and payment* | EV/EBITDA 7.0× (median 8.1×); cash yield 7.2% (median 6.5%); ROIC − WACC +3.6 pts (median +3.8); merit #7 of 16; net debt 3.3× EBITDA, stressed cover 2.9× | Leverage (3.3×) and heavy network capex | Vol. 22%; avg. correlation 0.06 | **3.77%**; 2.3% of risk; capacity-type limit 25% |
| Mouwasat Medical Services (SA) | Healthcare facilities | Private hospitals in Saudi Arabia (Eastern Province, Riyadh). Hard to replace: Hospital licences and specialist staff. Earns: Patient fees from insurers. *First family: the hospital beds and specialists a family relies on* | EV/EBITDA 11.9× (median 17.2×); cash yield 6.6% (median 4.2%); ROIC − WACC +13.4 pts (median +7.9); merit #2 of 16; net debt 0.9× EBITDA, stressed cover 32.0× | Small listing and thin trading, though its weight is well inside its liquidity limit | Vol. 27%; avg. correlation 0.09 | **3.52%**; 3.7% of risk |
| China Telecom (HK) | Digital networks | China's fibre-broadband and mobile network, plus cloud data centres. Hard to replace: State telecom licence; national fibre network. Earns: Subscription and cloud revenue. *First job: the network behind every phone, laptop and payment* | EV/EBITDA 4.1× (median 8.1×); cash yield 12.1% (median 6.5%); ROIC − WACC −0.5 pts (median +3.8); merit #8 of 16; net cash | State control; US sanctions history (delisted from NYSE in 2021) | Vol. 28%; avg. correlation 0.06 | **3.33%**; 2.6% of risk; capacity-type limit 25% |
| Sabesp (BR) | Water | Water and sewage for São Paulo state. Hard to replace: Municipal concession; regulated monopoly network. Earns: Regulated tariffs. Evidence: [About R$70bn of works to universalise water and sewage by 2029](https://www.infomoney.com.br/mercados/sabesp-supera-metas-de-novas-ligacoes-e-reforca-plano-de-universalizar-ate-2029/). *First home: a reliable water connection* | EV/EBITDA 10.0× (median 12.3×); cash yield −5.6% (median 4.2%); ROIC − WACC +4.1 pts (median +0.4); merit #2 of 9; net debt 2.2× EBITDA, stressed cover 2.3× | Large capex plan keeps free cash flow negative; Brazilian real | Vol. 31%; avg. correlation 0.08 | **3.31%**; 3.6% of risk |
| China Mobile (HK) | Digital networks | World's largest mobile network by subscribers, plus AI computing. Hard to replace: State licences; spectrum. Earns: Subscription and computing revenue. Evidence: [100 EFLOPS of AI computing power by 2028](https://www.scmp.com/business/article/3328842/china-mobile-aims-triple-ai-computing-power-using-homegrown-chips-2028). *First job: the network behind every phone, laptop and payment* | EV/EBITDA 4.4× (median 8.1×); cash yield 10.8% (median 6.5%); ROIC − WACC +3.5 pts (median +3.8); merit #4 of 16; net cash | State control; sanctions exposure | Vol. 15%; avg. correlation 0.10 | **3.29%**; 2.0% of risk; capacity-type limit 25% |
| HCA Healthcare (US) | Healthcare facilities | Largest US hospital operator. Hard to replace: Certificate-of-need laws and local scale in its markets. Earns: Patient revenue from insurers, Medicare and Medicaid. *First family: the hospital beds and specialists a family relies on* | EV/EBITDA 9.2× (median 17.2×); cash yield 5.1% (median 4.2%); ROIC − WACC +13.8 pts (median +7.9); merit #1 of 16; net debt 3.2× EBITDA, stressed cover 3.5× | US health policy (Medicaid funding); leverage 3.2× | Vol. 27%; avg. correlation 0.11 | **3.19%**; 3.6% of risk |
| Enel (IT) | Power generation & grids | Italy's main electricity distribution grid plus renewables in Europe and Latin America. Hard to replace: Regulated grid concessions. Earns: Regulated returns plus generation. Evidence: [Installed capacity from \~68 GW to over 80 GW by 2028](https://www.teleborsa.it/AMP/News/2026/02/23/enel-il-50percent-dei-capex-per-rinnovabili-e-in-europa-capacita-installata-salira-a-80-gw-17.html). *First home: the power behind the electricity bill* | EV/EBITDA 8.1× (median 12.1×); cash yield 3.6% (median 3.3%); ROIC − WACC +1.4 pts (median −0.7); merit #1 of 15; net debt 3.3× EBITDA, stressed cover 3.7× | Regulation and Latin American exposure; controls Endesa (watchlist, P4) | Vol. 20%; avg. correlation 0.17 | **2.98%**; 3.6% of risk |
| Saudi Telecom (SA) | Digital networks | Saudi Arabia's main telecom network and data centres (center3). Hard to replace: Licences, spectrum and the national backbone. Earns: Subscription and data-centre revenue. Evidence: [center3 targets 1 GW of data-centre capacity by 2030](https://www.datacenterdynamics.com/en/news/saudis-center3-targets-1gw-of-data-center-capacity-by-2030/). *First job: the network behind every phone, laptop and payment* | EV/EBITDA 9.3× (median 8.1×); cash yield 6.8% (median 6.5%); ROIC − WACC +12.1 pts (median +3.8); merit #2 of 16; net cash | State ownership; one-country concentration | Vol. 16%; avg. correlation 0.11 | **2.97%**; 1.9% of risk; capacity-type limit 25% |
| Bharti Airtel (IN) | Digital networks | India's second-largest mobile network, plus Africa. Hard to replace: Spectrum and nationwide towers and fibre. Earns: Subscription revenue. Evidence: [Nxtra data-centre capacity doubled to 400 MW by 2026](https://w.media/nxtra-planning-200-mw-data-center-in-hyderabad/). *First job: the network behind every phone, laptop and payment* | EV/EBITDA 10.6× (median 8.1×); cash yield 6.1% (median 6.5%); ROIC − WACC +10.5 pts (median +3.8); merit #5 of 16; net debt 1.2× EBITDA, stressed cover 2.9× | Indian regulation and the rupee | Vol. 22%; avg. correlation 0.10 | **2.97%**; 2.4% of risk; capacity-type limit 25% |
| Deutsche Telekom (DE) | Digital networks | Germany's largest telecom network; majority owner of T-Mobile US. Hard to replace: Spectrum and fibre. Earns: Subscription revenue. Evidence: [Fibre to every household and business in Germany by 2030](https://report.telekom.com/annual-report-2024/management-report/group-strategy/investments.html). *First job: the network behind every phone, laptop and payment* | EV/EBITDA 6.3× (median 8.1×); cash yield 8.1% (median 6.5%); ROIC − WACC +3.9 pts (median +3.8); merit #3 of 16; net debt 3.3× EBITDA, stressed cover 2.9× | Leverage (3.3×); overlaps US telecom exposure through T-Mobile US | Vol. 20%; avg. correlation 0.11 | **2.85%**; 2.4% of risk; capacity-type limit 25% |
| Bumrungrad Hospital (TH) | Healthcare facilities | International hospital in Bangkok, a regional medical-tourism hub. Hard to replace: Specialist staff, accreditation and international referral base. Earns: Patient fees, a large share from foreign patients. *First family: the hospital beds and specialists a family relies on* | EV/EBITDA 13.9× (median 17.2×); cash yield 4.3% (median 4.2%); ROIC − WACC +33.0 pts (median +7.9); merit #3 of 16; net cash | Dependence on medical tourism (Middle East, Asia) | Vol. 34%; avg. correlation 0.07 | **2.79%**; 3.5% of risk |
| Qualcomm (US) | Semiconductors | Wireless modem and processor chips plus standard-essential patents for mobile networks. Hard to replace: Patent portfolio embedded in 4G/5G standards; design scale. Earns: Chip sales and patent licensing. *Every first: the chips inside phones, laptops and data centres* | EV/EBITDA 16.3× (median 35.9×); cash yield 5.5% (median 1.7%); ROIC − WACC +12.9 pts (median +22.8); merit #7 of 17; net debt 0.6× EBITDA, stressed cover 6.4× | Losing Apple modem business; China exposure; cycle | Vol. 42%; avg. correlation 0.09 | **2.27%**; 3.5% of risk |
| America Movil (MX) | Digital networks | Latin America's largest telecom network (Telcel, Claro). Hard to replace: Spectrum and the region's largest fibre network. Earns: Subscription revenue. Evidence: [Over 5,400 km of new fibre in Peru during 2026](https://www.claro.com.pe/portal/pe/recursos_contenido/pdf/NP_Proyeccion_Despliegue-FO2026-140826.pdf). *First job: the network behind every phone, laptop and payment* | EV/EBITDA 5.8× (median 8.1×); cash yield 8.1% (median 6.5%); ROIC − WACC +5.4 pts (median +3.8); merit #1 of 16; net debt 1.9× EBITDA, stressed cover 2.4× | Mexican regulation and Latin American currencies | Vol. 24%; avg. correlation 0.14 | **2.01%**; 2.6% of risk; capacity-type limit 25% |
| OMA (Centro Norte airports) (MX) | Airports & toll roads | 13 airports in north-central Mexico, including Monterrey. Hard to replace: Government concessions; airports cannot be duplicated nearby. Earns: Regulated passenger charges plus commercial income. Evidence: [MXN 16bn 2026-30 plan; Monterrey capacity up \~50% to over 18M passengers](https://www.elfinanciero.com.mx/empresas/2026/06/05/oma-destina-16-mil-mdp-a-tecnologia-y-expansion-de-sus-aeropuertos/). *First trip: the airport and the road to it* | EV/EBITDA 9.3× (median 10.5×); cash yield 6.9% (median 5.7%); ROIC − WACC +22.8 pts (median +9.9); merit #1 of 4; net debt 1.2× EBITDA, stressed cover 2.1× | Air traffic shocks (60% EBITDA stress still passes); peso | Vol. 37%; avg. correlation 0.12 | **1.98%**; 3.5% of risk |
| Advantest (JP) | Semiconductors | Test equipment that every advanced chip must pass before shipping. Hard to replace: Leading share of system-on-chip testers; years of customer qualification. Earns: Equipment and service sales. *Every first: the chips inside phones, laptops and data centres* | EV/EBITDA 50.3× (median 35.9×); cash yield 1.4% (median 1.7%); ROIC − WACC +57.0 pts (median +22.8); merit #5 of 17; net cash | Cycle and valuation (50× EV/EBITDA against a 35.9× semiconductor median) | Vol. 60%; avg. correlation 0.07 | **1.74%**; 3.4% of risk |
| HD Hyundai Electric (KR) | Grid & power equipment | Power transformers and switchgear for grids and data centres. Hard to replace: Transformer factories take years to build and qualify; long order backlog. Earns: Equipment sales from a multi-year backlog. Evidence: [KRW 397bn to expand Ulsan and Alabama transformer capacity by 2028](https://transformer-magazine.com/news/hd-hyundai-electric-to-invest-272-3-m-in-transformer-production/). *First home: the transformers and cables that connect it* | EV/EBITDA 18.3× (median 22.3×); cash yield 4.3% (median 3.9%); ROIC − WACC +55.3 pts (median +12.5); merit #2 of 11; net cash | Orders at a cyclical high | Vol. 57%; avg. correlation 0.08 | **1.65%**; 3.4% of risk |
| NVIDIA (US) | Semiconductors | AI accelerator chips and data-centre networking. Hard to replace: CUDA software ecosystem and design scale competitors have not matched. Earns: Hardware and systems sales to cloud and enterprise data centres. *Every first: the chips inside phones, laptops and data centres* | EV/EBITDA 28.4× (median 35.9×); cash yield 2.3% (median 1.7%); ROIC − WACC +75.7 pts (median +22.8); merit #2 of 17; net cash | Customer concentration; export controls; AI capex cycle | Vol. 45%; avg. correlation 0.12 | **1.64%**; 3.4% of risk |
| Vistra (US) | Power generation & grids | US power generation fleet (gas and nuclear) and retail electricity in Texas. Hard to replace: Licensed plants, including nuclear, that take a decade to replace. Earns: Power sales, part contracted. *First home: the power behind the electricity bill* | EV/EBITDA 11.4× (median 12.1×); cash yield 4.3% (median 3.3%); ROIC − WACC +0.0 pts (median −0.7); merit #5 of 15; net debt 3.0× EBITDA, stressed cover 2.8× | Wholesale power prices; leverage 3.0× | Vol. 53%; avg. correlation 0.12 | **1.38%**; 3.4% of risk |
| SK hynix (KR) | Semiconductors | DRAM and high-bandwidth memory (HBM) for AI. Hard to replace: Few firms can make leading-edge memory; HBM qualification with AI chipmakers. Earns: Memory sales. Evidence: [KRW 19tn Cheongju HBM packaging fab by end-2027](https://www.trendforce.com/news/2026/01/13/news-sk-hynix-to-build-cheongju-advanced-packaging-fab-boosting-hbm-output-by-2027/). *Every first: the chips inside phones, laptops and data centres* | EV/EBITDA 8.5× (median 35.9×); cash yield 9.0% (median 1.7%); ROIC − WACC +44.4 pts (median +22.8); merit #3 of 17; net cash | Memory cycle at a peak | Vol. 60%; avg. correlation 0.10 | **1.37%**; 3.4% of risk |
| Micron (US) | Semiconductors | DRAM, high-bandwidth memory and NAND. Hard to replace: One of three leading-edge DRAM makers worldwide. Earns: Memory sales. Evidence: [Idaho DRAM fab output from 2027](https://www.trendforce.com/news/2025/06/13/news-micron-to-invest-200b-in-u-s-amid-trumps-reshoring-drive-targeting-40-dram-made-in-america/). *Every first: the chips inside phones, laptops and data centres* | EV/EBITDA 10.7× (median 35.9×); cash yield 6.9% (median 1.7%); ROIC − WACC +77.0 pts (median +22.8); merit #1 of 17; net cash | Memory cycle at a peak | Vol. 63%; avg. correlation 0.12 | **1.12%**; 3.3% of risk |
| Siemens Energy (DE) | Grid & power equipment | Gas turbines, grid technology (transformers, HVDC links) and wind turbines. Hard to replace: One of a handful of makers of large turbines and HVDC systems. Earns: Equipment and long-term service contracts. *First home: the transformers and cables that connect it* | EV/EBITDA 22.3× (median 22.3×); cash yield 7.5% (median 3.9%); ROIC − WACC +75.5 pts (median +12.5); merit #1 of 11; net cash | Wind-turbine losses and execution | Vol. 52%; avg. correlation 0.17 | **1.11%**; 3.4% of risk |

Weights are equal-risk-contribution outputs: each holding contributes an equal share of risk (about 3.6% each) unless a limit binds (digital networks at the 25% type limit, so each telecom carries less). Overlaps: data-centre build-out (chips and grid equipment) 10.9%; US health policy (HCA, Encompass) 7.0%; Chinese state telecoms 6.6%. The portfolio behaves like about 9.4 independent exposures. Every company not held, with its reason, is in the Decision record tab.

## Weighting: does the risk model earn its complexity?

Equal weight returned more over these five years, inverse volatility nearly matched the risk model but would breach the 25% type limit (telecoms 34%), and we keep equal risk contribution because it was chosen before testing and applies the limits inside the solve.

| Same 31 holdings, same costs (alternatives without the 25% type limit) | Risk model (ERC) | Inverse volatility | Equal weight |
| --- | --- | --- | --- |
| Return a year | 25.0% | 24.8% | 31.8% |
| Volatility | 10.2% | 10.3% | 12.3% |
| Worst fall | −7.4% | −7.8% | −8.9% |
| ₱100 became | 306 | 304 | 399 |
| Semiconductors today | 8.1% | 8.1% | 15.6% |

Equal weight's extra return came mainly from holding about twice as much in chipmakers through the AI rally; it also had higher volatility and a deeper fall.

## Performance evidence

The current holdings beat the world index over five years with less volatility, but that history includes selection hindsight. Over 36 years the industry proxy roughly matched a same-cost market fund, with shallower worst falls.

**1 · Historical performance of the currently selected portfolio** (weekly, in pesos, after all modelled costs; not actual fund performance and not a backtest of the selection process):

|  | Firsts Fund holdings (v4) | Previous rules (v3), same costs | MSCI ACWI ETF (reference) | Global tech ETF (context) |
| --- | --- | --- | --- | --- |
| Return a year | 25.0% | 22.2% | 16.2% | 27.4% |
| Volatility | 10.2% | 10.8% | 14.8% | 23.6% |
| Sharpe (cash = BSP rate − 0.5 pt) | 2.00 | 1.64 | 0.79 | 0.97 |
| Worst fall | −7.4% | −10.5% | −18.2% | −26.6% |
| Worst 12 months | +4.3% | −6.8% | −11.4% | −23.8% |
| ₱100 became | 306 | 274 | 213 | 337 |
| Beta to ACWI | 0.49 | 0.50 | 1.00 | 1.39 |

| Calendar year | 2021 (from 1 Oct) | 2022 | 2023 | 2024 | 2025 | 2026 (to 2 Oct) |
| --- | --- | --- | --- | --- | --- | --- |
| Firsts Fund holdings (v4) | 3.8% | 10.6% | 25.4% | 32.9% | 34.9% | 18.5% |
| Previous rules (v3) | 3.5% | −0.5% | 22.2% | 21.5% | 45.3% | 23.1% |
| MSCI ACWI ETF | 6.3% | −11.4% | 21.5% | 24.7% | 23.7% | 20.2% |
| Global tech ETF | 13.3% | −23.8% | 52.1% | 33.6% | 26.1% | 52.4% |

Revised beat previous rules in this period, but both were selected with October 2026 data, so this does not show the new rules are better; the gain may mostly come from adding hospitals and spreading wider, which we have not attributed.

**2 · Industry proxy, 1990–Aug 2026** (six US industries standing in for the eight types, no company screens, same ERC, 25% type limit, 3% cash, 1.50% fee, 0.30% trading cost; context only):

|  | Firsts method | Same-cost market fund | Tech fund |
| --- | --- | --- | --- |
| Return a year | 12.0% | 12.2% | 15.7% |
| Volatility | 15.3% | 15.6% | 22.9% |
| Worst fall | −44.4% | −46.8% | −73.2% |
| Months, peak to recovery | 69 | 72 | 192 |
| Worst 12 months | −27.3% | −30.4% | −57.6% |
| USD Sharpe | 0.48 | 0.49 | 0.53 |
| Asian crisis, Jul 1997 – Dec 1998 | 87.3% | 99.4% | 123.4% |
| Dot-com, Mar 2000 – Sep 2002 | −9.8% | −26.9% | −70.1% |
| Global financial crisis, Nov 2007 – Feb 2009 | −40.4% | −44.4% | −44.6% |
| COVID, Jan – Jun 2020 | −9.2% | −4.1% | 4.6% |
| 2022 rate shock | −12.4% | −13.3% | −21.0% |

Ahead of the market in 19 of 37 calendar years and of tech in 15. No downside protection is claimed: the method did worse than the market in COVID and gained less in 1997–98.

**3 · Investor outcomes, reported separately from fund performance** (₱1,000 a month for 60 months, every start month on the proxy, 381 windows; illustrative glidepath: from 24 months before the goal, the target equity share falls in a straight line to 20%, the rest in T-bills as the lower-risk-fund proxy):

| Ending value ÷ total paid in | Fund only | With glidepath |
| --- | --- | --- |
| Median | 1.33× | 1.27× |
| Worst 5% of windows | 0.92× | 0.94× |
| Worst window | 0.65× | 0.87× |
| Windows ending below what was paid in | 11% | 9% |

The glidepath raised the worst outcome and gave up some median return; it does not guarantee capital or goal completion.

**Sensitivity of the Position thresholds (report only; rules unchanged):**

| Diversification gain | Minimum weight | Holdings | Return a year | Volatility | Worst fall |
| --- | --- | --- | --- | --- | --- |
| 0.00% | 1.0% | 33 | 22.7% | 9.6% | −6.2% |
| 0.25% | 1.0% | 33 | 24.4% | 10.1% | −7.5% |
| 0.50% (rule) | 1.0% | 31 | 25.0% | 10.2% | −7.4% |
| 1.00% | 1.0% | 24 | 24.5% | 10.4% | −8.1% |
| 0.50% | 0.5% | 31 | 25.0% | 10.2% | −7.4% |
| 0.50% | 2.0% | 26 | 20.2% | 9.8% | −8.5% |

Across these thresholds the holdings count moves between 24 and 33 and the five-year return between 20.2% and 25.0%. The pre-set rule sits at the top of that range, one more reason to read the five-year figure as hindsight, not a forecast.

## Regulatory note and open items

RCBC Trust's official notice reproduces the amended exposure provision under BSP Circular No. 1234 (2026): UITFs invested in exchange-traded equities have a 20% single-issuer ceiling, and exposure above 15% must consist solely of that issuer's exchange-traded equity. The ceiling is regulatory context, not a target weight. [RCBC — Updated Exposure Limits for RCBC Trust UITFs](https://www.rcbc.com/updated-exposure-limits-for-rcbc-trust-uitfs)

- [ ] Team selects the benchmark (methodology, weights, currency treatment) before final performance comparisons
- [ ] Confirm dividend withholding rates by listing country with tax counsel
- [ ] Check team-assigned GICS sub-industries, especially the eight healthcare facilities and Kamigumi
- [ ] Spot-check debt, cash flow and ROIC for the 31 holdings against annual reports; memory makers are at a cyclical peak
- [ ] Confirm the stress shocks per capacity type with a source for each episode
- [ ] Decide whether the illustrative glidepath schedule appears in app mock-ups (label it illustrative)
- [ ] Calculator: contributions-only baseline plus balanced scenarios, not the five-year history

## Error log

18 errors were found in the Phase 1 documents and one more in our first rebuild (the Philippine weight credited to the model); all are fixed in the new fact sheet. The last four rows were found while applying the team's revised rules (7 Oct 2026) and are fixed in the v4 deck, fact sheet and model. The first nine are arithmetic or wording errors; the rest are method gaps a judge could press on.

| Error | Where | Fix |
| --- | --- | --- |
| Index calendar years compound to 214.0 (16.4% a year), but the chart ends at 204.8 and the table says 15.41% | Fact sheet p1 | Every figure now comes from one run. Calendar years chain to the chart's end value and to the since-start rate |
| Fund calendar years chain to 219.0 against a chart end of 220.7 | Fact sheet p1 | Same fix |
| "Single group ≤ 15%: actual 5.36%" cannot be right, because IHH alone was 9.39% | Fact sheet p2 | Groups are defined by controlling shareholder. Largest is the Razon group (ICTSI + Manila Water) at 8.29% |
| "Lost to the index in three of the five calendar years shown", but the table has six rows | Fact sheet p1 | Reworded from the computed figures: led in 2022, 2023 and 2025; trailed in 2024 and in both partial years |
| Philippines at exactly 30.01% while claiming "every weight came out of the risk model" | Fact sheet p2 | The rule is gone, and so is home-first sourcing: 8.29%, 2 of 33 holdings |
| "About ₱90,000 by year five on the simulated path" is the 8% planning figure, not the simulated path | Exec summary p2 | Use ₱95,400 at the 8% planning rate (₱1,300 a month) |
| Calculator dated to August: ₱662 a month for 35 months | Exec summary p2 | From October: ₱730 a month for 32 months |
| Suitability says the investor must sit through "a fall of about a sixth" | Fact sheet p2 | Changed to "a fall of up to half, as in 2008" |
| 1-year gap printed as 11.74 points while the displayed figures give 11.75 | Fact sheet p1 | Gaps are now computed from the displayed figures |
| Beta 0.37 and −17% worst fall shown with no long-run context | Fact sheet p1 | Added a 36-year panel: −48.1% worst fall, beta 0.88 |
| Covariance solved on the whole five years (look-ahead) | Simulation | Weights re-solved each quarter on the previous 156 weeks only |
| PSE holdings priced without dividends | Simulation | PSE cash dividends added on ex-dates |
| Sharpe ratio's risk-free rate never stated | Fact sheet p1 | BSP policy rate, average 4.99% a year, printed under the table |
| Price test said "pass or fail" with no threshold | Fact sheet p2 | EV/EBITDA at most 22.2x (EBITDA yield at least 4.5%, the money-market rate) |
| Utilities allowed 6.0x "under four published conditions" that were never published | Fact sheet p2 | 6.0x applies to GICS Utilities; no other exception |
| Debt test "still outstanding" for every holding | Fact sheet p2 | Completed for all 105 candidates, with ratios in the annex |
| Three holdings did not fit the theme (Century Pacific, DBS, Sea) | Holdings | Failed the Theme test and replaced |
| Glidepath result (₱68,855 → ₱77,736, wins 100%) could not be reproduced from any stated method | Fact sheet p2, exec summary p3 | Replaced with a stated stress test: the worst 12 months in 36 years placed in the final year |
| Price ceiling compared EBITDA/EV with the money-market yield, but EBITDA/EV is not a cash yield paid to investors | Rules, deck, fact sheet | 22.2× cut-off removed; valuation is now peer-relative, with a cash yield after maintenance spending |
| Five-year results presented as a backtest although the holdings were chosen with 2026 data | Deck, fact sheet | Relabelled “historical performance of the currently selected portfolio”; proxy labelled context only |
| Protection claims (“protected peso savers in 1997”, glidepath “wins 100%”) drawn from a few favourable episodes | Deck, fact sheet | Removed; crises table shows where the method did worse; investor outcomes reported as a distribution over every start month |
| Trading costs and withholding not modelled; cash assumed to earn the full policy rate | Simulation | 0.30% trading cost on turnover, withholding by listing country, cash at policy rate − 0.50 pt; v3 and v4 rerun on the same basis |

## Calculator note (open comment thread)

The calculator's bad year should use the 36-year figure. The 5-year simulation's worst twelve months (now +4.3% under the revised rules: not one losing 12-month period) would understate the risk, and the deck's own promise is to show "our worst real fall".
