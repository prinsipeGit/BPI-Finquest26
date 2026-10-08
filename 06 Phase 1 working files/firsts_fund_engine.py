#!/usr/bin/env python3
"""
THE FIRSTS FUND — Portfolio Construction & Back-Test Engine
FinQuest 2026 | BPI Wealth

Implements the conviction-scored inverse-volatility weighting engine described in
Firsts_Fund_Portfolio_Brief.md, then back-tests the resulting portfolio and emits
every statistic the Fund Fact Sheet requires.

USAGE
-----
    pip install pandas numpy matplotlib
    python firsts_fund_engine.py --prices prices.csv --benchmark benchmark.csv

INPUT FORMAT
------------
prices.csv      Date,ICT,AP,D05,Q0F,CNPF,ACEN,ALI,CNVRG,VRT,SE
                2021-01-04,120.5,32.1,...

                Daily closing prices. All offshore names must be converted to PHP
                before input, or pass --fx to supply a PHP conversion series.

benchmark.csv   Date,Benchmark
                2021-01-04,7100.2

                Policy benchmark: 30% PSEi Total Return + 65% MSCI ACWI (PHP, net TR)
                + 5% 91-day PH T-bill, rebalanced quarterly. This mirrors the Fund's
                own policy weights. Both legs must be total return and PHP-converted
                on the same daily FX basis as the holdings, or the excess return is
                contaminated by FX and by uncredited dividends.

OUTPUT
------
    weights.csv          Final constrained weights
    backtest_stats.txt   CAGR, volatility, Sharpe, Sortino, max drawdown, beta, tracking error
    navps_series.csv     Hypothetical NAVPS series (base 100) for the fact sheet graph
    navps_chart.png      Fund vs. benchmark chart, ALFM house style
"""

import argparse
import sys

import numpy as np
import pandas as pd

TRADING_DAYS = 252
RISK_FREE = 0.0525  # 91-day PH T-bill, ~5.245% at the 29 Jun 2026 auction. Update at submission.
MGMT_FEE  = 0.0100  # Total management fee p.a. ALFM fact sheets report NET of fees.

# --------------------------------------------------------------------------------------
# VOLATILITY OVERLAY (C6)
# Equity exposure is scaled toward a constant risk target rather than held fixed.
# Rationale: the Fund's core retention mechanic is a drawdown pre-commitment shown to a
# first-time investor. Cutting the worst rolling 12-month loss is worth more to this
# product than the return it costs. De-risk only: exposure is never levered above EQ_MAX.
# Scale is set at each month start from trailing volatility observed strictly BEFORE that
# date (the series is lagged one day), so the overlay carries no look-ahead.
# --------------------------------------------------------------------------------------
VOL_TARGET  = 0.12   # C6 — target annualised volatility of the equity sleeve
VOL_LOOKBACK= 60     # trading days of trailing realised vol
EQ_MAX      = 0.95   # maximum equity exposure (= EQUITY_SLEEVE)
EQ_MIN      = 0.60   # floor: the mandate stays a growth mandate in every state
OVERLAY_RESET = "ME" # exposure reset frequency (month end)

# --------------------------------------------------------------------------------------
# HOLDING DEFINITIONS
# Conviction scores are FIRST-framework outputs (0-100). Replace estimates with
# scored values once financials are available.
# --------------------------------------------------------------------------------------
HOLDINGS = {
    #  ticker : (conviction, pillar,     control_group, domicile)
    "ICT":   (88, "MOVE",    None,    "PH"),
    "CNPF":  (78, "THRIVE",  None,    "PH"),
    "ACEN":  (80, "LIVE",    "Ayala", "PH"),
    "D05":   (85, "CONNECT", None,    "OFFSHORE"),
    "SU":    (82, "LIVE",    None,    "OFFSHORE"),   # Schneider Electric (was GEV)
    "TSM":   (86, "EARN",    None,    "OFFSHORE"),
    "Q0F":   (75, "THRIVE",  None,    "OFFSHORE"),
    "VRT":   (76, "CONNECT", None,    "OFFSHORE"),
    "SE":    (72, "EARN",    None,    "OFFSHORE"),
    "GRAB":  (70, "MOVE",    None,    "OFFSHORE"),   # B3 solvency pending — sub: SU
}

# Constraint stack (see Brief §5, Step 3)
EQUITY_SLEEVE   = 0.95   # C5: 5% cash buffer
CAP_SINGLE      = 0.12   # C1
CAP_GROUP       = 0.15   # C2
TARGET_PH       = 0.30   # C4 — Philippine exposure target, ±3pp band
PH_BAND         = 0.03
MAX_ITER        = 200
TOL             = 1e-9


# --------------------------------------------------------------------------------------
# STEP 1-2: RAW RISK-BUDGETED WEIGHTS
# --------------------------------------------------------------------------------------
def validate(raw: pd.DataFrame, min_coverage: float = 0.0) -> pd.DataFrame:
    """Diagnose the raw panel, then return the clean (dropna'd) frame.

    Reports per-column coverage BEFORE dropping rows, so a single empty or
    short-history ticker is named rather than silently wiping the panel.
    """
    print("\n  Coverage (before dropna)")
    print(f"      Raw rows            {len(raw)}")
    if len(raw):
        print(f"      Raw range           {raw.index[0]:%d %b %Y} → {raw.index[-1]:%d %b %Y}")

    empty, short = [], []
    for c in raw.columns:
        n = int(raw[c].notna().sum())
        first = raw[c].first_valid_index()
        pct = n / len(raw) if len(raw) else 0
        tag = ""
        if n == 0:
            empty.append(c); tag = "  ← EMPTY, kills the panel"
        elif pct < 0.5:
            short.append(c); tag = "  ← short history, truncates the panel"
        start = f"{first:%d %b %Y}" if first is not None else "—"
        print(f"      {c:<7} {n:>5} obs ({pct:>5.0%})  from {start}{tag}")

    if min_coverage > 0:
        weak = [c for c in raw.columns
                if len(raw) and raw[c].notna().sum() / len(raw) < min_coverage]
        if weak:
            print(f"\n      Dropping {weak} (coverage < {min_coverage:.0%})")
            print("      NOTE: these holdings are excluded from weights and back-test.")
            raw = raw.drop(columns=weak)

    prices = raw.dropna()

    if len(prices) == 0:
        print("\n  ERRORS")
        if empty:
            print(f"      • These tickers returned NO data: {empty}")
            print("        Yahoo coverage of SGX/PSE symbols is unreliable. Either")
            print("        re-download them, or remove them from HOLDINGS and re-run")
            print("        with fewer names while you sort out the data source.")
        else:
            print("      • No overlapping dates across all tickers.")
        print("\n      Tip: run with --min-coverage to drop weak tickers automatically:")
        print("           python3 firsts_fund_engine.py --prices prices.csv --min-coverage 0.5\n")
        raise SystemExit(1)

    problems = []

    if len(prices) < 60:
        problems.append(f"Only {len(prices)} usable rows — need at least 60. "
                        "A short-history ticker (e.g. GEV, listed Apr-2024) is "
                        "truncating the whole panel via dropna().")

    nonpos = [c for c in prices.columns if (prices[c] <= 0).any()]
    if nonpos:
        problems.append(f"Non-positive prices in: {nonpos}")

    flat = [c for c in prices.columns if prices[c].nunique() <= 1]
    if flat:
        problems.append(f"Zero price variation (stale or forward-filled series): {flat}")

    rets = np.log(prices / prices.shift(1)).dropna()
    vols = rets.std() * np.sqrt(TRADING_DAYS)
    dead = [c for c in vols.index if not np.isfinite(vols[c]) or vols[c] <= 1e-6]
    if dead:
        problems.append(f"Zero or undefined volatility: {dead}")

    print("\n  Data check (after dropna)")
    print(f"      Rows                {len(prices)}")
    print(f"      Range               {prices.index[0]:%d %b %Y} → {prices.index[-1]:%d %b %Y}")
    print(f"      Tickers             {len(prices.columns)}")
    for c in prices.columns:
        v = vols.get(c, np.nan)
        flag = "  ← PROBLEM" if (not np.isfinite(v) or v <= 1e-6) else ""
        print(f"      {c:<7} vol {v:>7.1%}   unique px {prices[c].nunique():>5}{flag}")

    if problems:
        print("\n  ERRORS")
        for p in problems:
            print(f"      • {p}")
        print("\n  Fix: re-download the offending ticker(s), or drop them from HOLDINGS "
              "and re-run. Do not proceed with a degenerate series — it silently "
              "corrupts every weight and statistic downstream.\n")
        raise SystemExit(1)

    return prices


def annualised_vol(prices: pd.DataFrame, lookback_years: int = 3) -> pd.Series:
    """3-year annualised volatility of daily log returns."""
    window = int(TRADING_DAYS * lookback_years)
    rets = np.log(prices / prices.shift(1)).dropna()
    if len(rets) > window:
        rets = rets.iloc[-window:]
    vols = rets.std() * np.sqrt(TRADING_DAYS)
    if (vols <= 1e-6).any() or not np.isfinite(vols).all():
        bad = [t for t in vols.index if not np.isfinite(vols[t]) or vols[t] <= 1e-6]
        raise SystemExit(f"ERROR: zero/undefined volatility for {bad}. "
                         "Re-download those tickers.")
    return vols


def raw_weights(vols: pd.Series) -> pd.Series:
    """w_raw(i) = ConvictionScore(i) / sigma(i), normalised to the equity sleeve."""
    scores = pd.Series({t: HOLDINGS[t][0] for t in vols.index}, dtype=float)
    raw = scores / vols
    return EQUITY_SLEEVE * raw / raw.sum()


# --------------------------------------------------------------------------------------
# STEP 3: CONSTRAINT STACK — ITERATIVE WATER-FILLING
# --------------------------------------------------------------------------------------
def _waterfill(w: pd.Series, target: float, cap: float) -> pd.Series:
    """Scale a sleeve to sum to `target` with no element exceeding `cap`.

    Classic water-filling: scale to target, freeze anything over the cap at the
    cap, rescale the remainder into the residual, repeat until nothing spills.
    Converges monotonically — unlike scaling and capping in separate passes,
    which oscillates when two constraints pull against each other.
    """
    w = w.astype(float).copy()
    if w.empty:
        return w
    frozen: set = set()
    for _ in range(MAX_ITER):
        free = [t for t in w.index if t not in frozen]
        if not free:
            break
        residual = target - sum(w[t] for t in frozen)
        free_sum = sum(w[t] for t in free)
        if free_sum <= TOL:
            for t in free:
                w[t] = residual / len(free)
        else:
            for t in free:
                w[t] = w[t] * residual / free_sum
        spilled = [t for t in free if w[t] > cap + TOL]
        if not spilled:
            break
        for t in spilled:
            w[t] = cap
            frozen.add(t)
    return w


def apply_constraints(w_raw: pd.Series, verbose: bool = True) -> pd.Series:
    """Apply C1 (single), C2 (control group), C4 (PH exposure) jointly.

    Geography is enforced as a *sleeve target*, and the single-security cap is
    water-filled inside each sleeve. This makes C1 and C4 structurally compatible
    rather than competing.
    """
    ph = [t for t in w_raw.index if HOLDINGS[t][3] == "PH"]
    off = [t for t in w_raw.index if HOLDINGS[t][3] == "OFFSHORE"]
    ph_target = TARGET_PH
    off_target = EQUITY_SLEEVE - TARGET_PH

    # --- Feasibility check --------------------------------------------------------
    for label, names, target in (("Philippine", ph, ph_target),
                                 ("Offshore", off, off_target)):
        if not names:
            raise SystemExit(f"INFEASIBLE: no {label} holdings, but the sleeve "
                             f"target is {target:.0%}.")
        if len(names) * CAP_SINGLE < target - TOL:
            raise SystemExit(
                f"\nINFEASIBLE: the {label} sleeve must hold {target:.0%} across only "
                f"{len(names)} name(s) with a {CAP_SINGLE:.0%} single-security cap "
                f"(maximum achievable {len(names) * CAP_SINGLE:.0%}).\n"
                f"  Fix one of: add holdings to that sleeve, raise CAP_SINGLE, "
                f"or change TARGET_PH.\n"
                f"  If tickers were dropped by --min-coverage, that is the cause.\n")

    w = pd.concat([_waterfill(w_raw[ph], ph_target, CAP_SINGLE),
                   _waterfill(w_raw[off], off_target, CAP_SINGLE)])

    # --- C2: control-group cap ----------------------------------------------------
    groups: dict[str, list[str]] = {}
    for t in w.index:
        g = HOLDINGS[t][2]
        if g:
            groups.setdefault(g, []).append(t)

    for g, members in groups.items():
        if w[members].sum() <= CAP_GROUP + TOL:
            continue
        w[members] *= CAP_GROUP / w[members].sum()
        for names, target in ((ph, ph_target), (off, off_target)):
            rest = [t for t in names if t not in members]
            held = [t for t in names if t in members]
            if not rest:
                continue
            w[rest] = _waterfill(w[rest], target - w[held].sum(), CAP_SINGLE)

    w = w.reindex(w_raw.index)

    if verbose:
        binding = []
        if (w > CAP_SINGLE - TOL).any():
            binding.append("C1 single security")
        for g, members in groups.items():
            if w[members].sum() > CAP_GROUP - TOL:
                binding.append(f"C2 {g} group")
        binding.append("C4 PH exposure")
        print(f"  Binding constraints: {', '.join(binding)}")

        # Post-conditions — assert rather than hope
        assert abs(w.sum() - EQUITY_SLEEVE) < 1e-6, "equity sleeve mis-sized"
        assert w.max() <= CAP_SINGLE + 1e-6, "C1 violated"
        assert abs(w[ph].sum() - TARGET_PH) < 1e-6, "C4 violated"
        for g, members in groups.items():
            assert w[members].sum() <= CAP_GROUP + 1e-6, f"C2 violated for {g}"

    return w


# --------------------------------------------------------------------------------------
# BACK-TEST
# --------------------------------------------------------------------------------------
def backtest(prices: pd.DataFrame, weights: pd.Series,
             benchmark: pd.Series | None = None,
             rebalance: str = "QE",
             overlay: bool = True) -> tuple[pd.Series, dict]:
    """Quarterly-rebalanced back-test. Returns (NAVPS series base 100, stats dict)."""
    rets = prices.pct_change().dropna()

    # Cash sleeve accrues at the risk-free rate
    cash_daily = (1 + RISK_FREE) ** (1 / TRADING_DAYS) - 1

    # --- C6 volatility overlay -------------------------------------------------------
    # Trailing realised vol of the fixed-weight sleeve, LAGGED ONE DAY so the exposure
    # in force on day t uses only information available at the close of day t-1.
    sleeve_rets = (rets * weights).sum(axis=1) / weights.sum()
    trailing_vol = (sleeve_rets.rolling(VOL_LOOKBACK).std()
                    * np.sqrt(TRADING_DAYS)).shift(1)
    equity_exp = pd.Series(EQ_MAX, index=rets.index, dtype=float)
    if overlay:
        for _, blk in rets.groupby(pd.Grouper(freq=OVERLAY_RESET)):
            if blk.empty:
                continue
            v = trailing_vol.get(blk.index[0], np.nan)
            e = EQ_MAX * VOL_TARGET / v if (np.isfinite(v) and v > 0) else EQ_MAX
            equity_exp.loc[blk.index] = float(np.clip(e, EQ_MIN, EQ_MAX))

    port_rets = []
    current = weights.copy()

    for _, idx in rets.groupby(pd.Grouper(freq=rebalance)):
        if idx.empty:
            continue
        drift = current.copy()
        for date, row in idx.iterrows():
            scale = equity_exp[date] / weights.sum()
            r = float((drift * row[drift.index]).sum()) * scale \
                + (1.0 - equity_exp[date]) * cash_daily
            port_rets.append((date, r))
            drift = drift * (1 + row[drift.index])          # let weights drift
            drift = drift / drift.sum() * weights.sum()      # renormalise to sleeve
        current = weights.copy()                             # quarterly reset to target

    pr = pd.Series(dict(port_rets)).sort_index()

    # Net of fees: accrue the management fee daily against NAV, as a real fund does.
    fee_daily = (1 + MGMT_FEE) ** (1 / TRADING_DAYS) - 1
    pr_net = pr - fee_daily

    # Anchor the series at exactly 100 on the inception date (the day BEFORE the first
    # return). Without this the series starts at 100*(1+r1), so the first day's move is
    # excluded from the compounding base and the reported CAGR is inconsistent with a
    # "base 100" NAVPS label.
    base_date = prices.index[0]
    base = pd.Series([100.0], index=[base_date])
    navps_gross = pd.concat([base, 100 * (1 + pr).cumprod()])
    navps = pd.concat([base, 100 * (1 + pr_net).cumprod()])   # NET is the reported series

    years = (navps.index[-1] - navps.index[0]).days / 365.25
    cagr_gross = (navps_gross.iloc[-1] / 100.0) ** (1 / years) - 1
    cagr = (navps.iloc[-1] / 100.0) ** (1 / years) - 1
    vol = pr_net.std() * np.sqrt(TRADING_DAYS)
    downside = pr_net[pr_net < 0].std() * np.sqrt(TRADING_DAYS)
    sharpe = (cagr - RISK_FREE) / vol if vol else np.nan
    sortino = (cagr - RISK_FREE) / downside if downside else np.nan
    running_max = navps.cummax()
    max_dd = ((navps - running_max) / running_max).min()
    worst_12m = navps.pct_change(TRADING_DAYS).min()
    best_12m = navps.pct_change(TRADING_DAYS).max()
    pos_12m = (navps.pct_change(TRADING_DAYS).dropna() > 0).mean()

    stats = {
        "Period": f"{navps.index[0]:%d %b %Y} – {navps.index[-1]:%d %b %Y} ({years:.2f} yrs)",
        "Fund NAVPS (base 100)": f"{navps.iloc[-1]:.2f}",
        "Annualised return, GROSS": f"{cagr_gross:.2%}",
        "Annualised return, NET of fees": f"{cagr:.2%}",
        "Annualised volatility": f"{vol:.2%}",
        "Sharpe ratio": f"{sharpe:.2f}",
        "Sortino ratio": f"{sortino:.2f}",
        "Maximum drawdown": f"{max_dd:.2%}",
        "Worst rolling 12-month": f"{worst_12m:.2%}",
        "Best rolling 12-month": f"{best_12m:.2%}",
        "% of 12-month periods positive": f"{pos_12m:.0%}",
        "Management fee applied": f"{MGMT_FEE:.2%}",
        "Risk-free rate used": f"{RISK_FREE:.2%}",
        "Vol overlay": (f"target {VOL_TARGET:.0%}, equity {EQ_MIN:.0%}-{EQ_MAX:.0%}, "
                        f"{OVERLAY_RESET} reset" if overlay else "off"),
        "Average equity exposure": f"{equity_exp.mean():.0%}",
        "Minimum equity exposure": f"{equity_exp.min():.0%}",
    }

    if benchmark is not None:
        bm = benchmark.reindex(pr_net.index).ffill().pct_change().dropna()
        common = pr_net.index.intersection(bm.index)
        p, b = pr_net.loc[common], bm.loc[common]
        beta = np.cov(p, b)[0, 1] / np.var(b)
        active = p - b
        te = active.std() * np.sqrt(TRADING_DAYS)
        # Rebase the benchmark to 100 on the SAME inception date as the fund, so both
        # CAGRs are computed on an identical basis over an identical window.
        bm_lvl = benchmark.reindex(navps.index).ffill().bfill()
        bm_lvl = 100 * bm_lvl / bm_lvl.iloc[0]
        bm_cagr = (bm_lvl.iloc[-1] / 100.0) ** (1 / years) - 1
        stats["Benchmark NAVPS (base 100)"] = f"{bm_lvl.iloc[-1]:.2f}"
        stats["Benchmark annualised return"] = f"{bm_cagr:.2%}"
        stats["Excess return vs. benchmark"] = f"{cagr - bm_cagr:+.2%}"
        stats["Beta vs. benchmark"] = f"{beta:.2f}"
        stats["Tracking error"] = f"{te:.2%}"
        stats["Information ratio"] = f"{(active.mean() * TRADING_DAYS) / te:.2f}" if te else "n/a"
        stats["Correlation"] = f"{np.corrcoef(p, b)[0, 1]:.2f}"

    return navps, stats


# --------------------------------------------------------------------------------------
def chart(navps: pd.Series, benchmark: pd.Series | None, path: str) -> None:
    """ALFM house-style NAVPS chart: green fund line, grey benchmark.

    Self-verifying: the terminal value of each series is printed ON the chart and
    echoed to the console, so a stale or mislabelled image is immediately obvious.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.plot(navps.index, navps.values, color="#00833F", linewidth=2.0,
            label=f"Fund  (ends {navps.iloc[-1]:.2f})", zorder=3)
    ax.annotate(f"{navps.iloc[-1]:.1f}", xy=(navps.index[-1], navps.iloc[-1]),
                xytext=(4, 0), textcoords="offset points", fontsize=8.5,
                color="#00833F", fontweight="bold", va="center", zorder=4)

    bm_end = None
    if benchmark is not None:
        bm = benchmark.reindex(navps.index).ffill().bfill()
        bm = 100 * bm / bm.iloc[0]
        bm_end = float(bm.iloc[-1])
        ax.plot(bm.index, bm.values, color="#9A9A9A", linewidth=1.6,
                label=f"Benchmark*  (ends {bm_end:.2f})", zorder=2)
        ax.annotate(f"{bm_end:.1f}", xy=(bm.index[-1], bm_end),
                    xytext=(4, 0), textcoords="offset points", fontsize=8.5,
                    color="#6A6A6A", va="center", zorder=4)

    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_ylabel("NAVPS (base 100)", fontsize=9)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8)
    ax.margins(x=0.06)
    fig.tight_layout()
    fig.savefig(path, dpi=200)

    print(f"  Chart written to {path}")
    print(f"      GREEN  Fund       ends {navps.iloc[-1]:8.2f}")
    if bm_end is not None:
        print(f"      GREY   Benchmark  ends {bm_end:8.2f}")
        hi = "Fund" if navps.iloc[-1] > bm_end else "Benchmark"
        print(f"      -> the HIGHER line on the chart must be the {hi.upper()}. "
              f"If it is not, your PNG is stale — delete it and re-run.")


# --------------------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="The Firsts Fund construction engine")
    ap.add_argument("--prices", required=True, help="CSV: Date + one column per ticker (PHP)")
    ap.add_argument("--benchmark", help="CSV: Date,Benchmark")
    ap.add_argument("--outdir", default=".", help="Output directory")
    ap.add_argument("--min-coverage", type=float, default=0.0,
                    help="Drop tickers with data coverage below this fraction "
                         "(e.g. 0.5). Use to exclude empty or short-history names.")
    args = ap.parse_args()

    raw = pd.read_csv(args.prices, index_col=0, parse_dates=True).sort_index()
    missing = set(HOLDINGS) - set(raw.columns)
    if missing:
        print(f"ERROR: prices.csv is missing columns: {sorted(missing)}", file=sys.stderr)
        return 1
    raw = raw[list(HOLDINGS)]

    bm = None
    if args.benchmark:
        bm = pd.read_csv(args.benchmark, index_col=0, parse_dates=True).sort_index().iloc[:, 0]

    print("\nTHE FIRSTS FUND — CONSTRUCTION ENGINE")
    print("=" * 72)

    prices = validate(raw, args.min_coverage)

    print("\n[1] Volatility (3-yr annualised)")
    vols = annualised_vol(prices)
    for t, v in vols.sort_values(ascending=False).items():
        print(f"      {t:<7} {v:>7.1%}")

    print("\n[2] Raw risk-budgeted weights  (conviction / volatility)")
    w_raw = raw_weights(vols)

    print("\n[3] Constraint stack")
    w = apply_constraints(w_raw)

    out = pd.DataFrame({
        "Pillar":       [HOLDINGS[t][1] for t in w.index],
        "Group":        [HOLDINGS[t][2] or "—" for t in w.index],
        "Domicile":     [HOLDINGS[t][3] for t in w.index],
        "Conviction":   [HOLDINGS[t][0] for t in w.index],
        "Volatility":   vols.reindex(w.index).round(4),
        "Raw weight":   w_raw.round(4),
        "Final weight": w.round(4),
    }).sort_values("Final weight", ascending=False)

    print("\n[4] Final weights")
    print(out.to_string())
    print(f"\n      Equity sleeve      {w.sum():.2%}")
    print(f"      Cash buffer        {1 - w.sum():.2%}")
    ayala = [t for t in w.index if HOLDINGS[t][2] == "Ayala"]
    print(f"      Ayala group        {w[ayala].sum():.2%}   (cap {CAP_GROUP:.0%})")
    phs = [t for t in w.index if HOLDINGS[t][3] == "PH"]
    offs = [t for t in w.index if HOLDINGS[t][3] == "OFFSHORE"]
    print(f"      Philippines        {w[phs].sum():.2%}   (target {TARGET_PH:.0%} ±{PH_BAND:.0%})")
    print(f"      Offshore           {w[offs].sum():.2%}")
    print(f"      Largest position   {w.max():.2%}   (cap {CAP_SINGLE:.0%})")

    print("\n[5] Back-test")
    navps, stats = backtest(prices, w, bm)
    for k, v in stats.items():
        print(f"      {k:<28} {v}")

    out.to_csv(f"{args.outdir}/weights.csv")
    navps.to_csv(f"{args.outdir}/navps_series.csv", header=["NAVPS"])
    with open(f"{args.outdir}/backtest_stats.txt", "w") as fh:
        fh.write("THE FIRSTS FUND — HYPOTHETICAL BACK-TEST\n")
        fh.write("Gross of fees. Past simulated performance is not a guarantee of future results.\n")
        fh.write("=" * 72 + "\n")
        for k, v in stats.items():
            fh.write(f"{k:<32}{v}\n")
    chart(navps, bm, f"{args.outdir}/navps_chart.png")

    print("\n  Written: weights.csv, navps_series.csv, backtest_stats.txt, navps_chart.png")
    print("\n  ⚠  Label all output on the fact sheet as HYPOTHETICAL and GROSS OF FEES.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
