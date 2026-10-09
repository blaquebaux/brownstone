# brownstone

**Real estate as an archetype — income, rate-beta, or a landmine?**

Real estate was the one whole capital-archetype missing from the corpus. This asks what a
preservation / liability book actually needs to know before it holds REITs: is listed real estate a
distinct *real asset*, or just equity + duration beta in a hard hat — and is the mortgage-REIT yield
carry or a trap? All Alpaca SIP daily, total-return (`adjustment=all`), each test over its own
max-overlap window (2016-01 … 2026-07 for the equity-REIT core).

## Verdict

**NULL as alpha — a documented beta *ingredient*, not an edge.** Listed real estate is equity +
duration beta with **negative** residual alpha; it doesn't even improve a 60/40. Mortgage REITs are a
yield landmine. The archetype is now covered — honestly, as beta you can already build cheaper.

| question | finding |
|---|---|
| Q1 — distinct real asset, or equity+duration? | VNQ/IYR/XLRE/SCHH/RWR all ≈ **0.8·SPY + 0.24·TLT, R²≈50%**, with **negative α (−3 to −8%/yr)** and residual Sharpe ≈ **0.00**. High-yield `KBWY` is worse (+0.97 SPY beta, −8.4%/yr α). Real estate is a *worse-packaged* equity+duration combo. |
| Q2 — mortgage-REIT carry or landmine? | `REM`/`MORT`: Sharpe **+0.26**, **maxDD −70%**, worst day −23%, corr→SPY +0.57. The fat distribution yield is paid back in a crater. **Landmine — rejected.** |
| Q3 — diversifier vs 60/40? | VNQ Sharpe +0.41, **corr→60/40 +0.68**; a 60/40 is +0.83 and adding 10% VNQ **lowers it to +0.80**. Not a diversifier — redundant equity+duration at worse risk-adjusted return. |
| Q4 — rate regime | VNQ **+14.3%/yr when rates fall vs +1.3% when they rise** — a pure long-duration tell. A rate bet, not an inflation hedge. |
| Q5 — sub-sector rotation? | 11 REIT sub-sector ETFs: avg pairwise corr **+0.87**, **1.1 effective bets**. One common rate factor; rotation is noise. |

## What this means for the book

Real estate earns its archetype slot as an **honestly-labeled beta ingredient**: if a preservation or
real-asset mandate *wants* real-estate exposure, a broad equity REIT (VNQ) delivers equity+duration at
a small negative risk-adjusted penalty — hold it as a tilt, size it knowing it is **not** a diversifier
and leans entirely on falling rates. **Avoid mortgage REITs** (the −70% drawdown is the whole story)
and **don't pay for sub-sector rotation** (one rate factor). This is the characterization the
preservation / liability capstones need: REITs are redundant equity-duration, not free diversification.

## `brownstone_2`

The honest next test needs what listed ETFs can't show: **private real-estate fundamentals** — cap
rates, NOI growth, and a private index (NCREIF/ODCE) to test whether property-level signals or the
listed-vs-private premium add anything beyond the duration beta here. That's a WRDS/real-assets-data
job, not an Alpaca one.

## Reproduce

```bash
export ALPACA_KEY_ID=... ALPACA_SECRET_KEY=...
python3 research/brownstone_1.py
```

Equity REITs `VNQ/IYR/XLRE/SCHH/RWR`, mortgage `REM/MORT`, high-yield `KBWY`, sub-sectors
`REZ/SRVR/INDS/NETL/ROOF`, factors `SPY/TLT/IEF/TIP/DBC`. Each test uses its own max-overlap window so
the youngest sub-sector ETF doesn't truncate the equity-REIT core's full history.

---

*Blaque Baux — a Carter Warrens research initiative. Research only; not investment advice. The verdict
falls where the data puts it.*
