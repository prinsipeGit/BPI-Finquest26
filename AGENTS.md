# AGENTS.md — Firsts Fund (FinQuest 2026, Team Los Angeles 76ers)

Read this first. It tells an agent (or a teammate) what this project is, what was decided, where every number comes from,
and how to rerun everything. Update the **Decision log** and **Open items** whenever something changes.

## Project
- Competition: BPI Wealth FinQuest 2026. Phase 2 submission due **12 Oct 2026** (fact sheet PDF, 30-s video, 1-slide
  customer roadmap, deck PPT) to finquest@bpi.com.ph, subject `FINALIST_TeamName_Phase2`. Final Showdown **17 Oct 2026**:
  10-min pitch + 10-min Q&A. Judged on Research 20%, Feasibility 20%, Fund Process 20%, Originality 20%, Pitch 10%, Q&A 10%.
- Fund: **Firsts Fund** (use this name everywhere). Proposed **actively managed global equity UITF** investing directly in stocks
  for suitable early-career Filipinos with a first five years or more away. ₱100 minimum (proposed), 1.50% fee (proposed), operating cash
  (no fixed reserve), separate account-level glidepath (proposed platform feature). Central message: "Fund your firsts."
- Team decisions of 7 Oct 2026 ("Firsts Fund — Consolidated Proposed Changes", Sections 1–8) govern all deliverables.
- Team: Prince Angelo C. Rivera, Luis Tengonciang, Karol Josef Fuñe, Eric Fabian Thirdy Mendez (Ateneo, BS AMDS/MS DS).

## Decision log
| Date | Decision |
| --- | --- |
| 2026-10-07 | 30/70 Philippines/global split removed (no basis). |
| 2026-10-07 | Holdings rebuilt with MVP; failures replaced and flagged (user's choice). v1: 15 holdings, PH 30.82%. |
| 2026-10-07 | PH ~30% traced to Map sourcing, not the model. v2: region-balanced Map (7 types × 3 regions), 33 holdings, PH 8.29%. Superseded. |
| 2026-10-07 | **v3 (current).** User: theme is GLOBAL, so **no geographic constraint at all** (no regions, no country cap). Theme tightened: "essential" is not enough. MVP re-cut: **M = theme fit, V = investment merit, P = portfolio role**. Milestones are the story only, never a buy reason. User picks: **top 3 per capacity type by merit**; **country cap replaced by capacity-type cap 25%**; **conglomerates need ≥50% revenue** from qualifying capacity. |
| 2026-10-07 | Position produces a numerical weight (ERC). Judgment lives only in the published rules and a quarterly review that may remove (never resize) a holding, logged. |
| 2026-10-07 | 36-year proxy re-aligned to v3 types (Util, Telcm, Trans owners; ElcEq, Chips suppliers; health and banks removed): `backtest_v3.py`. |
| 2026-10-07 | Calculator bad year: use 36-year worst 12 months (now −27.0%, Aug 2001–Jul 2002). Awaiting team confirmation. |
| 2026-10-08 | **v4 (current).** Team's consolidated changes (Section 2A) applied. Rules fixed in `04 Fund model/v4 (31 holdings, current)/RULES_v4.md` before any rerun. Healthcare facilities added; no dated-target test; debt stress per type; valuation peer-relative incl. cash yield; eligible/watchlist/reject; holdings count from P inclusion tests (duplicate 0.80, min weight 1%, diversification +0.5%); BSP 20% issuer ceiling; group 20%, type 25%, liquidity (internal); 3% operating cash; no role/country quotas. User chose: re-select under new rules; keep performance but relabel. |
| 2026-10-08 | PSEi added as a local reference line (FMETF tracker price from PSE Edge, `map/psei.json`, checksum 1242366098): 5y −1.67% a year, ₱100 → 92. No benchmark chosen yet; MSCI ACWI ETF and PSEi are references only. |
| 2026-10-08 | NFRA/IGF benchmark series rebuilt (original `map/infra.json` not in the repo): `v4/bench_nfra.py` + `map/bench_usd.json` → `bench.json` (NFRA 10.02% a year, ₱100 → 161, max DD −12.63%; IGF 13.66%; fund beta vs NFRA 0.59). Fact sheet polished and regenerated with NFRA as benchmark. |
| 2026-10-08 | Testing conventions for v3 and v4 alike: 0.30% trading cost, dividend withholding by listing country (approx.), cash at BSP policy − 0.50 pt. 5-year results labelled "historical performance of the currently selected portfolio"; 36-year proxy "industry proxy, context only" (now incl. Hlth, `backtest_v4.py`). |
| 2026-10-10 | **Ad v2** (Remotion, `07 Video ad/v2/`): fast-paced (124 BPM, beat-cut), aimed at "is this for me?" with no fund technicals. Story: firsts 5+ years away → onboarding calculator (name, amount, years ≥ 5 → monthly = amount ÷ months, contributions only) → "There's always a new first" → "Fund your firsts." CTA "Start with as little as ₱100". v1 code is not in this repo. Music is a synthesised placeholder until a licensed track is chosen. |
| 2026-10-10 | Ad v2 redesigned (user): **English only**, clean and modern look (paper, ink, emerald; Geist). Intro "You just got your first paycheck. What do you do first?" Six firsts, each with its own motion graphic and a chained transition (flight path → road → building → zoom through window → awning → shop → sign flips into notebook). Sound and ElevenLabs voice-over come next. |
| 2026-10-10 | Ad v2 tweaks (user): labels use Geist (no mono font); "I do" removed, so five firsts at about 1.7 s each; home → business is now a zoom through the lit window that folds into the shop's awning. |
| 2026-10-10 | Ad v2 sound: ElevenLabs voice-over ("Justin Case - Warm, Trustworthy, Clear", eleven_v4, take 3 of 4) cut into 16 lines on the cuts; 13 ElevenLabs sound effects. The silent pause beat was dropped (the voice sets the rhythm). Music is still the synthesised placeholder because the ElevenLabs connector in this workspace has no music generation. |
| 2026-10-10 | Ad v2 voiced cut reworked (user: voice and sound did not fit): voice now **Bella - Professional, Bright, Warm** (eleven_v4, take 2), lines on the half-beat grid with EQ/compression/small room; new warm music bed `music_vo.wav` for the voiced cut (the dance beat stays in the no-voice cut); effects at half volume under the voice. A no-voice cut (`*_noVO.mp4`) also exists. |
| 2026-10-10 | Ad v2 voiced cut, take 3: user's revised script ("Take Mom and Dad abroad? Get your first car? … Then, move on to your next first."), voice **Emma - Youthful, Upbeat Commercial** (eleven_v4, take 3), lines on the half-beat grid; dance-beat soundtrack back under the voice (user preferred it); warm bed dropped. |
| 2026-10-10 | Ad v2 retimed (user: second half felt rushed): firsts 1.55 s each (was 1.7), calculator 8.7 s (was 8.2, longer "when" and "result" steps), payoff 2.4 s, logo 3.4 s (was 2.9); voice lines re-placed with almost no speed-up. |
| 2026-10-10 | Ad v2 mix (user: voice too loud): voice at 0.6 (≈ −4.4 dB), music dips to 0.32 instead of 0.2 under it. |
| 2026-10-10 | Fact sheet: page-2 portfolio-construction funnel (140 → 129 → 49 → 31); without the 7 chip and grid-equipment holdings the same simulation gives 18.7% a year, ₱100 → 237 (`v4/ex_suppliers.py`, reproduces 24.95% first), disclosed on page 1 and in Key risks; Key facts tidied. |
| 2026-10-10 | Fact sheet checked against the BPI meeting notes (Mac folder, `BPI FinQuest Meeting (1).md`, `(2).md`, not in repo): CX and marketing pages rewritten to the decisions (persona Bea; Sukli future, BPI App first; no bad-year-first step; no streaks; goal service user-decided with yearly review; holdings reviewed monthly). Open: revenue look-through. Benchmark confirmed NFRA by user on 10 Oct (notes' blended idea not used). |
| 2026-10-10 | User: features from the 6-page Phase 1 submission must not be lost. Fact sheet is now 6 pages: executive summary (Problem & fund, Hook, Habit; `exec_pages4.py`), fact sheet (pp 4–5), annex (p 6). Sequence test rerun on v4 (`seq4.py` → `extra4.json`: −0.85 / +0.85, 20,000 orderings). Retired by v3/v4 decisions and not restored: 30% PH, 10% reserve, role quotas, MSCI ACWI benchmark, dated-target test, performance digs at BPI funds. |
| 2026-10-10 | User: fact sheet must include the executive summary, and holdings should appear once. PDF is now 3 pages (executive summary, then fact sheet); top-10 table dropped. Same file name, built by `build_factsheet4.py`. |

## The rules (v4, current; full text in `04 Fund model/v4 (31 holdings, current)/RULES_v4.md`)
- **Theme**: listed businesses that own, operate or supply essential, hard-to-replace capacity and earn from it. Eight types (research
  universe, not allocations): power & grids, water, digital networks, ports, airports & toll roads, healthcare facilities (owners);
  grid & power equipment, semiconductors (suppliers). Universe = up to 20 largest per type, ≥ US$1bn: 140 names.
- **M**: M1 GICS on list or ≥50% qualifying revenue; M2 OCF > 0 and ROIC > 0. No dated target required (evidence only).
- **V**: reject on stressed interest cover < 1.5× (EBITDA shock water 10, power 15, networks 15, hospitals 25, ports 30, grid eq. 35,
  chips 50, airports 60%), net debt/EBITDA > type median + 2.0, investability (liq < 1% or no prices), governance (Adani group).
  Watchlist on OCF/EBITDA < 50%, EV/EBITDA > 2× type median, merit < 0.50. Merit = mean(valuation pct [EV/EBITDA, (OCF−D&A)/EV], quality pct [ROIC−WACC]) within type.
- **P**: eligible names in merit order; watchlist if same-type corr > 0.80, ERC weight < 1%, or diversification ratio gain < 0.5%.
  ERC on 156 weekly PHP returns, quarterly. Limits: issuer 20% (BSP), group 20%, type 25%, liquidity; 3% cash.
  Funnel: 140 → 129 pass M → 35 rejected / 45 watchlist at V → 49 eligible → 31 held (18 watchlist at P).

## Current portfolio (v4, solved on data to 2 Oct 2026; 31 holdings + 3% cash)
Exelon 5.81 · Westports 5.23 · ICTSI 4.80 · Engie 4.57 · Bangkok Dusit 4.49 · E.ON 4.48 · Sulaiman Al Habib 4.41 · Guangdong Inv. 4.36 ·
KDDI 3.81 · Encompass 3.78 · AT&T 3.77 · Mouwasat 3.52 · China Telecom 3.33 · Sabesp 3.31 · China Mobile 3.29 · HCA 3.19 · Enel 2.98 ·
Saudi Telecom 2.97 · Bharti Airtel 2.97 · Deutsche Telekom 2.85 · Bumrungrad 2.79 · Qualcomm 2.27 · América Móvil 2.01 · OMA 1.98 ·
Advantest 1.74 · HD Hyundai Elec. 1.65 · NVIDIA 1.64 · Vistra 1.38 · SK hynix 1.37 · Micron 1.12 · Siemens Energy 1.11.
Types: networks 25.00 (cap), healthcare 22.19, power 19.22, ports 10.04, chips 8.13, water 7.68, grid eq. 2.76, airports 1.98.
PH 4.80 (ICTSI; range 3.2–5.3); Manila Water watchlist (OCF 28% of EBITDA). ~9.4 independent exposures.

## Headline results (v4; all after 1.50% fee, 0.30% trading, withholding)
- 5 years (historical performance of the currently selected portfolio): 24.95% p.a. (ACWI 16.21, IXN 27.37, v3 same costs 22.20) · vol 10.24 ·
  Sharpe 2.00 · max DD −7.43 · worst 12m +4.34 · beta 0.49. EW 31.76% (vol 12.26, DD −8.94); inverse vol 24.77%.
- 36-year industry proxy (context only): 11.96% p.a. (market 12.25, tech 15.73) · max DD −44.4 (−46.8, −73.2) · worst 12m −27.3 ·
  recovery 69 months (72, 192). Rolling 60-month ₱1,000/month: median 1.33×, worst 0.65×, 11% below paid-in; with illustrative glidepath worst 0.87×, 9%.

## Superseded (v3), kept for reference
### Rules (v3)
- **Theme**: listed companies that own long-lived, hard-to-replicate physical capacity in short supply, or make the critical
  equipment it cannot be built without. Seven types: power generation & grids, water, digital networks (telecom, towers, data
  centres), ports, airports & toll roads (Owners); grid & power equipment, semiconductors (Suppliers).
- **M · Map the capacity (theme fit)**: universe = up to the 20 largest listed per type by US$ market value (121 names; only 12 water
  and 9 ports of size). GICS sub-industry on the list (team-assigned); conglomerates ≥50% revenue in a qualifying segment
  (Siemens 29%, Hitachi 30%, Mitsubishi Electric 25%, Samsung 39%, Vinci 16%, Ferrovial 15% → out; Quanta = construction → out).
  Every holding must cite a dated, numbered capacity target (Guangdong Investment had none → out). Investability only: no mainland
  A-shares; e& (Abu Dhabi) excluded for lack of price history in our sources.
- **V · Verify the merit (investment merit)**: gates net debt/EBITDA ≤ 4.0× (6.0× utilities) and interest cover ≥ 2.5×; EV/EBITDA
  ≤ 22.2×; liquidity cap ≥ 1%. Then merit = average of valuation percentile (EV/EBITDA, cheaper better) and quality percentile
  (ROIC − WACC, from stockanalysis) among gate-passers of the same type worldwide; ties → higher ROIC − WACC. Top 3 per type held.
  Funnel: 121 → 114 theme fit → 58 pass gates (30 debt, 28 price, 1 liquidity; some both) → 56 with evidence/data → 21 held.
- **P · Position the risk (portfolio role)**: ERC on previous 156 weekly peso returns (min 104), quarterly. Limits: issuer ≤ 10%,
  control group ≤ 15% (Razon: ICT+MWC; Enel: ENEL+ELE), capacity type ≤ 25%, Owners ≥ 45%, Suppliers ≤ 25%, reserve 10%.
  No country rule; countries reported. All rules hold at all 21 rebalances (checked).

### Portfolio (solved on data to 2 Oct 2026; 21 holdings + 10% reserve)
Saudi Telecom 10.00 (issuer cap) · Kamigumi 6.90 · Deutsche Telekom 6.67 · Westports 6.35 · ICTSI 5.42 · Engie 5.08 · Endesa 4.91 ·
Manila Water 4.18 (liquidity cap) · Sabesp 4.10 · Japan Airport Terminal 4.00 · Enel 3.87 · Veolia 3.78 · América Móvil 3.76 · TSMC 3.73 ·
ASUR 3.13 · Nexans 2.93 · OMA 2.79 · Schneider 2.71 · HD Hyundai Electric 2.26 · SK hynix 1.78 · Micron 1.65.
By type: networks 20.43, ports 18.67, power 13.86, water 12.06, airports & roads 9.92, grid equipment 7.90, chips 7.16.
Countries: FR 14.50, JP 10.89, SA 10.00, MX 9.68, **PH 9.60** (range 8.5–10.4), DE 6.67, MY 6.35, ES 4.91, BR 4.10, KR 4.04, IT 3.87,
TW 3.73, US 1.65. Owners 74.94 / Suppliers 15.06. ~5.9 independent bets; top-2 factors 42.6%. Overlaps: AI/data-centre ~12.1%.

### Results
- 5 years (1 Oct 2021 – 2 Oct 2026, weekly, PHP, net): 22.89% p.a. (ACWI 16.21%, global tech ETF IXN 27.4%) · vol 10.82% (14.79%,
  23.6%) · Sharpe 1.65 (0.76, 0.95) · max DD −10.25% (−18.20%, −26.6%) · worst 12m −6.13% · beta 0.50. Calendar fund/ACWI:
  2021* 3.88/6.34, 2022 −0.01/−11.35, 2023 22.81/21.54, 2024 22.13/24.70, 2025 46.07/23.73, 2026 YTD 23.64/20.24.
  **Upper bound only**: selection uses Oct-2026 ratios (memory chips at a cyclical peak).
- 36-year aligned proxy (1990–Aug 2026): 11.7% p.a. (market fund 11.7%, tech 15.1%) · vol 14.4% · max DD −41.2% (−43.9%, −69.0%) ·
  recovery 67 months (71, 181) · worst 12m −27.0% · USD Sharpe 0.49 (0.48, 0.53) · beta 0.85. Crises (cap/mkt/tech): 1997–98
  +111.1/+104.1/+120.2; dot-com −8.5/−16.0/−58.6; 2008 −35.2/−38.0/−34.8; COVID −8.7/−3.8/+4.7; 2022 −9.6/−11.7/−19.1.
- Glidepath stress (worst 12m in final year): worst ₱49,005 → ₱62,711, wins 100%; normal-market median cost ₱12,465.

## Folder layout (Downloads/FinQuest 2026 - The Firsts Fund)
| Folder | Contents |
| --- | --- |
| `AGENTS.md` | This file |
| `01 Phase 2 submission/` | `LosAngeles76ers_FirstsFund_FactSheet.pdf`: 6 pages: executive summary (3), fact sheet (2), annex (1), v4. `superseded/` holds older versions |
| `02 Phase 1 submission/` | Phase 1 PDFs and HTML drafts |
| `03 Competition rules/` | Primers and Phase 2 finalist guidelines |
| `04 Fund model/` | One subfolder per version. `v4 (31 holdings, current)/` = current engine (RULES_v4.md, map/, engine4.py, analyze4.py, build_factsheet4.py, gen_deck4.py, gen_doc4.py, notes4.py, sens4.py, results4.json). `v3 (21 holdings, superseded)/`, `v2 (33 holdings, superseded)/`, `v1 (15 holdings, superseded)/` |
| `05 36-year backtest/` | `backtest.py` (original proxy), `backtest_v3.py` (→ `results_v3.pkl`), `backtest_v4.py` (current, incl. Hlth → `results_v4.pkl`) |
| `06 Phase 1 working files/` | Original Aug 2026 `finquest` folder |
| `07 Video ad/v2/` | 30-s ad v2 in Remotion (`README.md` has the storyboard and render steps; renders in `out/`) |
| `_duplicates/` | Byte-identical extra copies, old AGENTS.md and transfer bundles (.tgz); safe to delete |

### Files in `04 Fund model/v3 (21 holdings, superseded)/`
| File | What it is |
| --- | --- |
| `inputs.py` | BSP rates, PSE dividends, ADV, FX, **CANDIDATES** (165 names: result HELD/Ranked/Fail/Outside universe), **MERIT** (ROIC, WACC, gap, percentiles, rank, peer medians), **SEGMENT** (conglomerate revenue shares + sources), GROUP |
| `yret.json`, `ph.txt` | Weekly PHP total returns ×1e5 (19 non-PH holdings + ACWI, USDPHP); PSE closes for ICT, MWC |
| `engine.py` → `sim.pkl` | ERC with capacity-type cap, 5-year simulation |
| `analyze.py` → `results.json` | All statistics; stress test uses `../05 36-year backtest/results_v3.pkl` |
| `build_factsheet.py` | Builds the fact sheet PDF (page 2 = holdings table: theme fit · merit · role) |
| `make_annex.py` → `annex.md` | Every candidate per type with ratios, merit rank, result, weight, target |
| `map/` | `st3.txt`, `st3_extra.txt` (stockanalysis stats incl. ROIC/WACC, checksummed), `universe3.py`, `funnel3.py`, `build3.py`, `d0–d1.txt` (returns, checksummed) |

Rerun v4: in `05 36-year backtest`: `python3 backtest_v4.py`; in `04 Fund model/v4 (31 holdings, current)`: `cd map && python3 funnel4.py && cd .. && python3 engine4.py && python3 analyze4.py && python3 build_factsheet4.py && python3 gen_deck4.py && python3 gen_doc4.py`. v4 data: `map/st4.txt` (checksum 3742345854), `map/yret_new.json` (26 new weekly series, checksum 2917459399). Paths inside the v4 scripts assume the workspace layout (`../v3`, `../../compare`); adjust if run from Downloads.
Rerun v3: `cd "05 36-year backtest" && python3 backtest.py && python3 backtest_v3.py`; then in `04 Fund model/v3 (21 holdings, superseded)`: `cd map && python3 funnel3.py && python3 build3.py && cd .. && python3 engine.py && python3 analyze.py && python3 build_factsheet.py && python3 make_annex.py`. (`build3.py` reads v1/v2 inputs and returns from the superseded folders: adjust the two relative paths if moved.)

## Data sources
Workspace reaches only GitHub/PyPI; everything else came through the built-in browser on Luis's Mac, copied with checksums:
PSE Edge (`/common/DisclosureCht.ax`, JSON POST), Yahoo chart API (adjclose; no PSE or Abu Dhabi tickers), stockanalysis.com
statistics pages (market cap, volume, EV/EBITDA, interest coverage, net cash, EBITDA, ROIC, WACC), BIS SDMX (policy rate, USD/PHP),
Ken French library. Conglomerate segment shares from annual reports (links in `inputs.py` SEGMENT).

## Open items
- [x] Benchmark: NFRA (fact sheet updated 8 Oct 2026).
- [ ] Confirm dividend withholding rates (tax counsel) and stress shocks per type (cite episodes).
- [ ] Check GICS sub-industries (team-assigned), esp. healthcare facilities and Kamigumi.
- [ ] Spot-check debt, cash flow, ROIC for the 31 holdings; memory makers at cyclical peak.
- [ ] Calculator: contributions-only baseline + balanced scenarios (5-year+ examples only); glidepath schedule labelled illustrative.
- [ ] Video script, site and app mock-ups: apply Section 8 consistency edits (not in this workspace).
- [ ] Ad v2: real music (full ElevenLabs connector or a licensed track); team check of voice-over, lines and legal text.
- [ ] Older "changes" deck (v2) is superseded; do not present it.

## Links
- **Competition pitch deck (current, v4, 25 slides with speaker notes):** https://claude.ai/artifact/JDnfFgK8cZhYG9cTJyTcgZ
- **Supporting proposal doc (v4: rules, holdings assessment, evidence; Decision record tab):** https://claude.ai/code/artifact/194a3d45-b897-4f5e-a20f-ceeb59da286b
- Changes deck (v2, superseded): https://claude.ai/artifact/CdPnMiKcrTEGKfPPBzCz3s
- 36-year backtest page (original proxy): https://claude.ai/artifact/8gezP9QG3mGW6w9Ne3FnE6
