#!/usr/bin/env python3
"""
THE FIRSTS FUND — Price Data Fetcher  (v2, diagnostic)
FinQuest 2026

Downloads daily closes for the ten holdings, converts everything to Philippine
pesos, and writes prices.csv + benchmark.csv for firsts_fund_engine.py.

v2 changes — v1 failed silently:
  • Fetches each symbol INDIVIDUALLY and reports success/failure per symbol
  • Handles yfinance's MultiIndex column layout across versions
  • Strips timezone-aware indices (PSE/SGX return tz-aware, NYSE does not)
  • Does NOT dropna before writing — one empty column no longer wipes the file
  • Tries fallback symbols automatically (IHH.KL for Q0F.SI, etc.)

    pip3 install yfinance pandas
    python3 fetch_prices.py
"""

import os
import sys

import pandas as pd

try:
    import yfinance as yf
except ImportError:
    sys.exit("Run:  pip3 install yfinance pandas")

START = "2021-07-01"
END   = "2026-08-01"

# Engine ticker -> (candidate Yahoo symbols in priority order, quote currency)
TICKERS = {
    "ICT":  (["ICT.PS"],            "PHP"),   # ICTSI — PSE
    "CNPF": (["CNPF.PS"],           "PHP"),   # Century Pacific Food — PSE
    "ACEN": (["ACEN.PS"],           "PHP"),   # ACEN Corporation — PSE
    "D05":  (["D05.SI"],            "SGD"),   # DBS Group — SGX
    "Q0F":  (["Q0F.SI", "IHH.KL"],  "SGD"),   # IHH Healthcare — SGX, fallback Bursa
    "SU":   (["SU.PA", "SBGSY"],    "EUR"),   # Schneider Electric — Euronext Paris,
                                              #   fallback US OTC ADR (quoted USD)
    "TSM":  (["TSM"],               "USD"),   # TSMC ADR — NYSE
    "VRT":  (["VRT"],               "USD"),   # Vertiv — NYSE
    "SE":   (["SE"],                "USD"),   # Sea Limited ADR — NYSE
    "GRAB": (["GRAB"],              "USD"),   # Grab Holdings — NASDAQ
}

# When a fallback symbol trades in a different currency from the primary listing.
CCY_OVERRIDE = {"IHH.KL": "MYR", "SBGSY": "USD"}

# Yahoo has USDPHP=X but NOT SGDPHP=X or MYRPHP=X. Everything else is derived as a
# cross-rate through the dollar:   XXX->PHP  =  (USD->PHP) / (USD->XXX)
FX_DIRECT = {"USD": ["USDPHP=X", "PHP=X"]}
# Quoted as USD per 1 unit of PHP-target currency  ->  XXX_PHP = USDPHP / quote
FX_CROSS  = {"SGD": "SGD=X",      # USD/SGD
             "MYR": "MYR=X",      # USD/MYR
             "TWD": "TWD=X"}
# Quoted as USD per 1 unit of the currency         ->  XXX_PHP = quote * USDPHP
FX_MULT   = {"EUR": "EURUSD=X",   # USD per EUR
             "GBP": "GBPUSD=X"}

BENCH = {"PSEI.PS": ("PHP", 0.35), "AAXJ": ("USD", 0.65)}

MANUAL_DIR = "manual"   # drop <TICKER>.csv here for anything Yahoo can't serve


def fetch_one(symbol: str) -> pd.Series | None:
    """Download one symbol's adjusted close. Returns None on failure."""
    try:
        df = yf.download(symbol, start=START, end=END,
                         progress=False, auto_adjust=True, threads=False)
    except Exception as exc:
        print(f"      {symbol:<12} ERROR  {type(exc).__name__}: {exc}")
        return None

    if df is None or df.empty:
        print(f"      {symbol:<12} EMPTY  no rows returned")
        return None

    close = df["Close"]
    if isinstance(close, pd.DataFrame):           # MultiIndex layout
        close = close.iloc[:, 0]
    close = close.dropna()

    if close.empty:
        print(f"      {symbol:<12} EMPTY  all-NaN closes")
        return None

    idx = pd.to_datetime(close.index)
    if getattr(idx, "tz", None) is not None:      # PSE/SGX return tz-aware
        idx = idx.tz_localize(None)
    close.index = idx.normalize()

    print(f"      {symbol:<12} OK     {len(close):>5} obs  "
          f"{close.index[0]:%d %b %Y} → {close.index[-1]:%d %b %Y}")
    return close


def fetch_any(symbols: list[str]) -> tuple[pd.Series | None, str | None]:
    """Try candidate symbols in order; return the first that works."""
    for sym in symbols:
        s = fetch_one(sym)
        if s is not None:
            return s, sym
    return None, None


def load_manual(ticker: str) -> pd.Series | None:
    """Load manual/<TICKER>.csv exported from Investing.com, Stooq, or Yahoo.

    Accepts any of their layouts. Handles quoted numbers with thousands commas
    (Investing.com writes "6,296.64") and both ISO and US date formats.
    """
    path = os.path.join(MANUAL_DIR, f"{ticker}.csv")
    if not os.path.exists(path):
        return None
    try:
        # utf-8-sig strips the byte-order mark Investing.com writes, which would
        # otherwise turn the first header into "﻿Date" and break detection.
        df = pd.read_csv(path, encoding="utf-8-sig")
    except Exception as exc:
        print(f"      {ticker:<12} MANUAL ERROR  {exc}")
        return None

    cols = {c.strip().lstrip("﻿").lower(): c for c in df.columns}
    datecol = next((cols[k] for k in ("date", "fecha", "time") if k in cols), None)
    pricecol = next((cols[k] for k in
                     ("adj close", "close", "price", "close/last", "last")
                     if k in cols), None)
    if datecol is None or pricecol is None:
        print(f"      {ticker:<12} MANUAL ERROR  need a date and a close/price "
              f"column; found {list(df.columns)}")
        return None

    s = df[[datecol, pricecol]].copy()
    s[pricecol] = pd.to_numeric(
        s[pricecol].astype(str).str.replace(r'[",$\s]', "", regex=True),
        errors="coerce")
    s[datecol] = pd.to_datetime(s[datecol], errors="coerce", format="mixed")
    s = s.dropna().set_index(datecol)[pricecol].sort_index()
    if s.empty:
        print(f"      {ticker:<12} MANUAL EMPTY  parsed 0 usable rows")
        return None
    s.index = pd.DatetimeIndex(s.index).normalize()
    print(f"      {ticker:<12} MANUAL {len(s):>5} obs  "
          f"{s.index[0]:%d %b %Y} → {s.index[-1]:%d %b %Y}  ({path})")
    return s


def main() -> int:
    print("\nTHE FIRSTS FUND — PRICE FETCHER")
    print("=" * 72)

    # ---- FX ----------------------------------------------------------------------
    print("\n  [1] FX rates to PHP")
    fx: dict[str, pd.Series] = {}

    usdphp, _ = fetch_any(FX_DIRECT["USD"])
    if usdphp is None:
        print("      !! FATAL: no USD->PHP rate. Cannot convert anything.")
        return 1
    fx["USD"] = usdphp

    for ccy, sym in FX_CROSS.items():
        usd_per = fetch_one(sym)          # USD/XXX
        if usd_per is None:
            print(f"      !! no {sym} — cannot derive {ccy}->PHP")
            continue
        cross = (usdphp.reindex(usd_per.index).ffill().bfill() / usd_per).dropna()
        if cross.empty:
            print(f"      !! {ccy}->PHP cross-rate empty")
            continue
        fx[ccy] = cross
        print(f"      {ccy}->PHP     DERIVED  USDPHP / {sym}   "
              f"latest {cross.iloc[-1]:,.4f}")

    for ccy, sym in FX_MULT.items():
        per_unit = fetch_one(sym)         # USD per 1 XXX
        if per_unit is None:
            print(f"      !! no {sym} — cannot derive {ccy}->PHP")
            continue
        cross = (per_unit * usdphp.reindex(per_unit.index).ffill().bfill()).dropna()
        if cross.empty:
            print(f"      !! {ccy}->PHP cross-rate empty")
            continue
        fx[ccy] = cross
        print(f"      {ccy}->PHP     DERIVED  {sym} x USDPHP   "
              f"latest {cross.iloc[-1]:,.4f}")

    # ---- Holdings ----------------------------------------------------------------
    print("\n  [2] Holdings")
    series: dict[str, pd.Series] = {}
    ccy_used: dict[str, str] = {}
    for name, (cands, ccy) in TICKERS.items():
        s, used = fetch_any(cands)
        if s is None:
            s = load_manual(name)          # fall back to manual/<TICKER>.csv
            if s is not None:
                series[name] = s
                ccy_used[name] = "PHP" if ccy == "PHP" else ccy
                continue
            print(f"      !! {name}: Yahoo failed {cands} and no "
                  f"{MANUAL_DIR}/{name}.csv found")
            continue
        series[name] = s
        ccy_used[name] = CCY_OVERRIDE.get(used, ccy)

    if not series:
        print("\n  FATAL: nothing downloaded. Check your internet connection, or "
              "fall back to manual CSV download (see NOTES at end of file).\n")
        return 1

    # ---- Convert to PHP ----------------------------------------------------------
    print("\n  [3] Converting to PHP")
    panel = pd.DataFrame(series).sort_index()
    panel = panel.ffill()                       # align differing market calendars

    for name in list(panel.columns):
        ccy = ccy_used[name]
        if ccy == "PHP":
            continue
        if ccy not in fx:
            print(f"      !! {name}: no {ccy}->PHP rate — DROPPING "
                  f"(cannot report a PHP fund in {ccy})")
            panel = panel.drop(columns=[name])
            continue
        rate = fx[ccy].reindex(panel.index).ffill().bfill()
        panel[name] = panel[name] * rate
        print(f"      {name:<7} converted from {ccy}")

    panel.index.name = "Date"
    panel.to_csv("prices.csv")

    print(f"\n      prices.csv    {len(panel)} rows x {len(panel.columns)} tickers")
    for c in panel.columns:
        n = int(panel[c].notna().sum())
        print(f"        {c:<7} {n:>5} obs ({n / len(panel):>5.0%})")

    dropped = sorted(set(TICKERS) - set(panel.columns))
    if dropped:
        print(f"\n      !! MISSING from prices.csv: {dropped}")
        print(f"\n         Yahoo no longer serves individual PSE equities. Download")
        print(f"         these by hand and drop them in ./{MANUAL_DIR}/ , then re-run:")
        print()
        for t in dropped:
            print(f"           {MANUAL_DIR}/{t}.csv")
        print()
        print("         Source: investing.com -> search the ticker -> Historical Data")
        print("                 -> set range to 5Y -> Download. Any column layout works;")
        print("                 the loader auto-detects Date + Close/Price.")
        print("         PSE prices are already in PHP, so no FX conversion is needed.")

    # ---- Benchmark ---------------------------------------------------------------
    print("\n  [4] Blended benchmark")
    legs, weights = [], []
    for sym, (ccy, wt) in BENCH.items():
        s = fetch_one(sym)
        if s is None:
            print(f"      !! benchmark leg {sym} unavailable — skipping")
            continue
        if ccy != "PHP":
            if ccy not in fx:
                print(f"      !! no {ccy}->PHP rate for {sym} — skipping leg")
                continue
            s = s * fx[ccy].reindex(s.index).ffill().bfill()
        legs.append(100 * s / s.dropna().iloc[0])
        weights.append(wt)

    if legs:
        frame = pd.concat(legs, axis=1, sort=True).ffill().dropna()
        w = pd.Series(weights, index=frame.columns) / sum(weights)   # renormalise
        if len(legs) < len(BENCH):
            print(f"      NOTE: only {len(legs)}/{len(BENCH)} legs available — "
                  "weights renormalised. Disclose this on the fact sheet.")
        bench = frame.mul(w, axis=1).sum(axis=1).to_frame("Benchmark")
        bench.index.name = "Date"
        bench.to_csv("benchmark.csv")
        print(f"      benchmark.csv  {len(bench)} rows  "
              f"{bench.index[0]:%d %b %Y} → {bench.index[-1]:%d %b %Y}")
    else:
        print("      no benchmark written — run the engine without --benchmark")

    print("\n  Next:")
    print("      python3 firsts_fund_engine.py --prices prices.csv "
          "--benchmark benchmark.csv\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# ----------------------------------------------------------------------------------
# NOTES — MANUAL FALLBACK
# ----------------------------------------------------------------------------------
# If Yahoo keeps failing on the PSE/SGX symbols, download by hand and assemble:
#
#   Investing.com   best PSE coverage; free account; Historical Data -> Download
#   Stooq           stooq.com/q/d/?s=<symbol>  -> direct CSV, no login
#   PSE Edge        official PSE source, clunky but authoritative
#
# You also need USD/PHP and SGD/PHP daily rates (BSP publishes the reference rate).
#
# Required prices.csv layout — every value already converted to PHP:
#
#   Date,ICT,CNPF,ACEN,D05,Q0F,SU,TSM,VRT,SE,GRAB
#   2021-07-01,142.50,18.20,8.95,1210.40,84.10,...
#
# Two silent killers:
#   1. Skipping FX conversion. A PHP-reporting fund must measure offshore holdings
#      in pesos — peso weakness is part of your return, not noise.
#   2. Using raw closes instead of adjusted. Adjusted prices include dividends and
#      splits; without them you understate total return on DBS especially.
#
# Schneider Electric (SU.PA) replaced GE Vernova in v3.1. GEV only listed in
# March 2024, which truncated the whole panel to ~2.3 years — a window that
# happens to be unusually favourable for AI-linked names and would have been
# vulnerable to a cherry-picking challenge. SU has full history and fills the
# same role in the LIVE pillar: grid intelligence and data-centre energy
# management. If SU.PA fails, the script falls back to the US ADR (SBGSY, USD).
