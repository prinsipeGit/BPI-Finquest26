"""Static inputs for The Firsts Fund rebuild (pulled 7 Oct 2026). See AGENTS.md for provenance."""

# BIS policy rate, Philippines (BSP target RRP rate), % p.a., month-end. Used as the peso yield on the liquid reserve.
PH_POLICY = dict(x.split('=') for x in (
 "1805=3.25 1806=3.5 1807=3.5 1808=4 1809=4.5 1810=4.5 1811=4.75 1812=4.75 1901=4.75 1902=4.75 1903=4.75 1904=4.75 "
 "1905=4.5 1906=4.5 1907=4.5 1908=4.25 1909=4 1910=4 1911=4 1912=4 2001=4 2002=3.75 2003=3.25 2004=2.75 2005=2.75 "
 "2006=2.25 2007=2.25 2008=2.25 2009=2.25 2010=2.25 2011=2 2012=2 2101=2 2102=2 2103=2 2104=2 2105=2 2106=2 2107=2 "
 "2108=2 2109=2 2110=2 2111=2 2112=2 2201=2 2202=2 2203=2 2204=2 2205=2.25 2206=2.5 2207=3.25 2208=3.75 2209=4.25 "
 "2210=4.25 2211=5 2212=5.5 2301=5.5 2302=6 2303=6.25 2304=6.25 2305=6.25 2306=6.25 2307=6.25 2308=6.25 2309=6.25 "
 "2310=6.5 2311=6.5 2312=6.5 2401=6.5 2402=6.5 2403=6.5 2404=6.5 2405=6.5 2406=6.5 2407=6.5 2408=6.25 2409=6.25 "
 "2410=6 2411=6 2412=5.75 2501=5.75 2502=5.75 2503=5.75 2504=5.5 2505=5.5 2506=5.25 2507=5.25 2508=5 2509=5 2510=4.75 "
 "2511=4.75 2512=4.5 2601=4.5 2602=4.25 2603=4.25 2604=4.5 2605=4.5 2606=4.75 2607=4.75 2608=5").split())
PH_POLICY = {k: float(v) for k, v in PH_POLICY.items()}

# Cash dividends per share (PHP) by ex-date, PSE names, from stockanalysis.com dividend history.
# Coverage starts before the simulation window (Oct 2021) for every name.
PH_DIVS = {
 'MER':   [('2026-08-27', 11.758), ('2026-03-25', 16.672), ('2025-08-26', 11.328), ('2025-03-11', 13.736),
           ('2024-08-27', 10.295), ('2024-03-26', 11.235), ('2023-08-29', 8.520), ('2023-03-24', 11.028),
           ('2022-08-18', 5.806), ('2022-03-25', 10.226)],
 'ICT':   [('2026-03-18', 17.850), ('2025-03-19', 14.160), ('2024-03-14', 11.000), ('2023-03-15', 10.000),
           ('2022-03-15', 6.000), ('2021-08-17', 2.630), ('2021-03-25', 2.370)],
 'MWC':   [('2026-03-12', 2.026), ('2025-03-07', 1.841), ('2024-03-15', 1.129), ('2023-04-11', 0.619),
           ('2022-11-28', 0.379), ('2021-11-29', 0.531)],
 'CNVRG': [('2026-03-19', 0.490), ('2025-03-31', 0.430), ('2024-09-23', 0.180)],
 'TEL':   [('2026-08-27', 46.0), ('2026-03-25', 46.0), ('2025-08-27', 48.0), ('2025-03-12', 47.0),
           ('2024-08-22', 50.0), ('2024-03-20', 46.0), ('2023-08-14', 49.0), ('2023-04-03', 59.0),
           ('2022-08-15', 75.0), ('2022-03-14', 42.0)],
}

# Average daily traded value, Jul-Sep 2026. PSE names in PHP (PSE Edge); others local currency (Yahoo close x volume).
ADV_LOCAL = {'CNVRG': 78944021, 'ICT': 1395744994, 'MER': 171529943, 'MWC': 59733271, 'TEL': 117096156,
             'ADPORTS': 3699462108, 'DG': 99737487, 'HITACHI': 58440544025, 'IBE': 173235644, 'NTPC': 2893920738,
             'PGRID': 2399223691, 'SIE': 260842209, 'SU': 220715844, 'TSMC': 57936478327, 'WPRTS': 28939204}
# Local currency per USD (or USD per EUR), late Sep 2026, Yahoo; USDPHP 62.673.
FX_TO_PHP = {'PHP': 1.0, 'INR': 62.673/96.2248, 'MYR': 62.673/4.0835, 'EUR': 62.673*1.125, 'JPY': 62.673/157.927,
             'TWD': 62.673/31.8868}

# ---------------------------------------------------------------------------------------------
# MAP + VERIFY results. Every candidate considered, with the test it failed (if any).
# nd = net debt/EBITDA, cov = EBIT/interest, ev = EV/EBITDA (stockanalysis.com, S&P Global data, 7 Oct 2026).
# Debt limit 4.0x (6.0x for GICS Utilities); coverage >= 2.5x; price EV/EBITDA <= 22.2x (EBITDA yield >= 4.5%).
# ---------------------------------------------------------------------------------------------
CANDIDATES = [
 # key, name, country, ccy, role, gics, milestone(s), nd, cov, ev, capacity target, source, result
 ('MER','Meralco','PH','PHP','Owner','Utilities','Housing (power), Business',1.93,5.64,7.62,
  'MGen: 1,500 MW of renewable capacity by 2030','https://matuwid.org/meralco-to-increase-renewable-projects-to-1500-mw-by-30/','PASS'),
 ('MWC','Manila Water','PH','PHP','Owner','Utilities','Housing (water)',5.27,4.91,8.31,
  'More than 3,225 MLD of additional supply capacity by 2037','https://context.ph/2026/08/18/manila-water-scouts-new-sources-as-east-zone-demand-rises/','PASS'),
 ('ICT','ICTSI','PH','PHP','Owner','Industrials','Transport (ports), Business',2.18,8.60,14.78,
  'US$300M to expand MICT, South Luzon and Mindanao terminals, capacity up at all three by 2028','https://context.ph/2026/07/30/ictsi-secures-mict-operations-for-another-25-years/','PASS'),
 ('CNVRG','Converge ICT','PH','PHP','Owner','Communication Services','Education (connectivity), Business',0.76,10.19,3.40,
  'About 1 million new fiber ports in 2026 (P23B capex)','https://newsbytes.ph/2026/03/16/converge-earmarks-₱23b-to-expand-network-add-1m-ports-in-2026/','PASS'),
 ('TEL','PLDT','PH','PHP','Owner','Communication Services','Education (connectivity), Business',3.92,3.15,5.94,
  '100 MW data centre in Cavite, 2026','https://w.media/?p=21203','PASS'),
 ('NTPC','NTPC','IN','INR','Owner','Utilities','Housing (power)',4.46,2.82,9.40,
  '60 GW of renewable capacity by 2032','https://www.pv-magazine-india.com/2021/06/28/ntpc-doubles-its-2032-renewable-energy-target-to-60-gw/','PASS'),
 ('PGRID','Power Grid Corp of India','IN','INR','Owner','Utilities','Housing (grid)',3.67,2.63,9.70,
  'Rs 1.9 trillion transmission capex by 2032','https://powerline.net.in/2023/11/17/powergrid-projects-capex-of-rs-1900-billion-by-2032/','PASS'),
 ('ADPORTS','Adani Ports & SEZ','IN','INR','Owner','Industrials','Transport (ports), Business',2.41,4.53,20.02,
  '1 billion tonnes of cargo capacity by 2030','https://www.tribuneindia.com/news/business/adani-ports-sez-targets-1-billion-tonnes-of-cargo-handling-capacity-by-2030-gautam-adani/','PASS'),
 ('WPRTS','Westports','MY','MYR','Owner','Industrials','Transport (ports)',1.22,12.70,12.95,
  'Capacity from 14M to 27M TEU a year (Westports 2); phase two after 2036','https://theedgemalaysia.com/node/773945','PASS'),
 ('IBE','Iberdrola','ES','EUR','Owner','Utilities','Housing (power, grid)',3.83,4.44,13.66,
  'EUR 58 billion investment by 2028, mainly networks','https://iberdrola.com/about-us/iberdrola-strategic-plan','PASS'),
 ('DG','Vinci','FR','EUR','Owner','Industrials','Travel (airports), Transport (roads)',2.02,5.00,6.47,
  'GBP 500M over five years at Edinburgh Airport, terminal footprint +60%','https://www.ajot.com/news/vinci-airports-announces-the-most-significant-investment-plan-in-edinburgh-airports-history','PASS'),
 ('SU','Schneider Electric','FR','EUR','Supplier','Industrials','Housing, Business (power equipment)',1.91,13.31,18.35,
  'US$700M of US manufacturing capacity investment through 2027','https://www.manufacturingdive.com/news/schneider-electric-700-million-investment-us-data-center-demand-ai/743630/','PASS'),
 ('SIE','Siemens','DE','EUR','Supplier','Industrials','Housing, Business (grid equipment)',3.12,6.08,18.72,
  'EUR 300M switchgear capacity expansion, new plant running by end-Oct 2027','https://assets.new.siemens.com/siemens/assets/api/uuid:0073901b-9dbf-46bf-b278-575671571df8/HQCOPR202606237412EN.pdf','PASS'),
 ('HITACHI','Hitachi','JP','JPY','Supplier','Industrials','Housing (grid equipment)',-0.47,42.83,13.80,
  'Hitachi Energy: additional US$1.5B for transformer capacity by 2027','https://tdworld.com/utility-business/article/55021774/hitachi-energy-to-invest-additional-15-billion-to-ramp-up-global-transformer-manufacturing-capacity-by-2027','PASS'),
 ('TSMC','TSMC','TW','TWD','Supplier','Information Technology','Education (laptops), Business (data centres)',-0.77,210.97,20.33,
  'US$60-64B capital spending in 2026','https://www.itiger.com/hans/news/1103082639','PASS'),
 # ---- failed -----------------------------------------------------------------------------
 ('IHH','IHH Healthcare','MY','MYR','Owner','Health Care','none',2.37,3.95,14.29,'', '', 'FAIL Map: hospitals serve none of the five firsts'),
 ('APOLLO','Apollo Hospitals','IN','INR','Owner','Health Care','none',1.80,8.48,30.81,'', '', 'FAIL Map (no first); FAIL Price (EV/EBITDA 30.8x)'),
 ('CNPF','Century Pacific Food','PH','PHP','-','Consumer Staples','none',1.20,16.45,11.62,'', '', 'FAIL Theme: food manufacturer, no capacity role'),
 ('DBS','DBS Group','SG','SGD','-','Financials','none',None,None,None,'', '', 'FAIL Theme: a bank finances capacity but does not own, build or run it'),
 ('SE','Sea Limited','SG','USD','Platform','Consumer Discretionary','Business',-1.85,123.38,20.18,'', '', 'FAIL Theme: no dated capacity number found'),
 ('GRAB','Grab Holdings','SG','USD','Platform','Industrials','Transport',-13.12,1.42,23.39,'', '', 'FAIL Debt (coverage 1.4x) and Price (23.4x)'),
 ('VRT','Vertiv','US','USD','Supplier','Industrials','Business',0.09,43.65,36.47,'', '', 'FAIL Price: EV/EBITDA 36.5x'),
 ('INDUS','Indus Towers','IN','INR','Owner','Communication Services','Education',0.94,5.75,6.55,'', '', 'FAIL Theme: no dated tower target'),
 ('AIRTEL','Bharti Airtel','IN','INR','Owner','Communication Services','Education',1.25,3.91,10.48,'', '', 'FAIL Theme: no dated capacity target'),
 ('SEMB','Sembcorp Industries','SG','SGD','Owner','Utilities','Housing',10.66,1.96,13.66,'', '', 'FAIL Debt: 10.7x net debt/EBITDA, coverage 2.0x'),
 ('ACEN','ACEN','PH','PHP','Owner','Utilities','Housing',20.54,0.70,24.22,'', '', 'FAIL Debt: 20.5x, coverage 0.7x; FAIL Price'),
 ('AP','Aboitiz Power','PH','PHP','Owner','Utilities','Housing',4.57,2.26,7.83,'', '', 'FAIL Debt: coverage 2.3x'),
 ('FGEN','First Gen','PH','PHP','Owner','Utilities','Housing',2.87,1.98,5.43,'', '', 'FAIL Debt: coverage 2.0x'),
 ('GLO','Globe Telecom','PH','PHP','Owner','Communication Services','Education',5.08,2.12,6.46,'', '', 'FAIL Debt: 5.1x and coverage 2.1x'),
 ('TENAGA','Tenaga Nasional','MY','MYR','Owner','Utilities','Housing',4.54,2.02,7.52,'', '', 'FAIL Debt: coverage 2.0x'),
 ('NEE','NextEra Energy','US','USD','Owner','Utilities','Housing',7.36,2.40,18.49,'', '', 'FAIL Debt: 7.4x'),
 ('EQIX','Equinix','US','USD','Owner','Real Estate','Education',4.93,4.72,27.69,'', '', 'FAIL Debt (4.9x) and Price (27.7x)'),
 ('TCL','Transurban','AU','AUD','Owner','Industrials','Transport',8.20,1.30,26.71,'', '', 'FAIL Debt and Price'),
 ('AOT','Airports of Thailand','TH','THB','Owner','Industrials','Travel',0.73,10.40,25.33,'', '', 'FAIL Price: 25.3x'),
 ('ABB','ABB','CH','CHF','Supplier','Industrials','Housing',0.46,None,25.29,'', '', 'FAIL Price: 25.3x'),
 ('LT','Larsen & Toubro','IN','INR','Supplier','Industrials','Housing',1.41,12.05,16.61,'', '', 'FAIL Theme: target is revenue (Lakshya 31), not capacity'),
 ('NETLINK','NetLink NBN Trust','SG','SGD','Owner','Communication Services','Education',2.76,4.10,15.86,'', '', 'FAIL Theme: no dated capacity number found'),
]

# Control groups for the 15% group cap: same controlling shareholder (>30% or largest holder with control).
GROUP = {'MER': 'First Pacific / MPIC', 'TEL': 'First Pacific / MPIC', 'ICT': 'Razon group', 'MWC': 'Razon group',
         'NTPC': 'Government of India', 'PGRID': 'Government of India', 'ADPORTS': 'Adani group'}
