# Firsts Fund — BPI Wealth FinQuest 2026

Team **Los Angeles 76ers** (Ateneo de Manila): Prince Angelo C. Rivera, Luis Tengonciang, Karol Josef Fuñe, Eric Fabian Thirdy Mendez.

**Firsts Fund** is a proposed actively managed global equity UITF for early-career Filipinos, built around companies that own, operate or supply essential, hard-to-replace capacity. Its message: *"Fund your firsts."*

- Phase 2 submission due **12 Oct 2026**
- Final Showdown **17 Oct 2026**

**Read [`AGENTS.md`](AGENTS.md) first.** It has the decision log, the current rules (v4), the portfolio, headline results, data sources, rerun commands and open items. Update its decision log whenever something changes.

## Layout

| Folder | Contents |
| --- | --- |
| `01 Phase 2 submission/` | Current fact sheet PDF; older versions in `superseded/` |
| `02 Phase 1 submission/` | Phase 1 PDFs and HTML drafts |
| `03 Competition rules/` | Primers and Phase 2 finalist guidelines |
| `04 Fund model/` | One subfolder per version; **`v4 (31 holdings, current)/`** is the live engine (`RULES_v4.md`, `map/`, `engine4.py`, `analyze4.py`, …) |
| `05 36-year backtest/` | Industry-proxy backtests (`backtest_v4.py` is current) |
| `06 Phase 1 working files/` | Original Aug 2026 working folder |
| `Presentation deck/` | Pitch deck (.pptx) and supporting proposal |

## Rerun (v4)

```bash
pip install -r requirements.txt
cd "05 36-year backtest" && python3 backtest_v4.py && cd ..
cd "04 Fund model/v4 (31 holdings, current)"
cd map && python3 funnel4.py && cd ..
python3 engine4.py && python3 analyze4.py && python3 build_factsheet4.py && python3 gen_deck4.py && python3 gen_doc4.py
```

Some v4 scripts still use paths from the original workspace layout (`../v3`, `../../compare`). Adjust them if a script can't find its inputs.

## Conventions

- Use the name **Firsts Fund** everywhere.
- Don't edit superseded versions (v1–v3). They're kept as a record.
- Data files are checksummed (see `AGENTS.md`). Re-verify checksums after you refresh any data.
