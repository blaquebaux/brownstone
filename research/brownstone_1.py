#!/usr/bin/python3
# =============================================================================
# brownstone_1.py — real estate as an archetype: income, rate-beta, or a landmine?
#
# The real-estate archetype was the one whole gap in the corpus. This asks the honest questions a
# preservation/liability book needs answered before it holds REITs:
#   Q1  Is a broad equity REIT (VNQ) a distinct real asset, or just equity + duration beta?
#   Q2  Mortgage REITs (REM/MORT) — is the fat yield carry, or a negative-skew landmine?
#   Q3  Is equity-REIT a genuine diversifier vs a 60/40, or the same risk wearing a building?
#   Q4  Rate-regime conditioning: REITs are long-duration — do they get hurt when rates rise?
#   Q5  Sub-sector dispersion — is there a rotation edge, or one common rate factor?
# All Alpaca SIP daily, total-return (adjustment=all). Honest prior: REITs are mostly equity+duration
# beta (a real-asset INGREDIENT, not alpha), and mortgage REITs are a yield trap.
# =============================================================================
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from _brownstone_common import panel, rets, stats, skew_of, corr, beta

EQREIT = ["VNQ", "IYR", "XLRE", "SCHH", "RWR"]     # broad equity REIT
MREIT  = ["REM", "MORT"]                            # mortgage REIT (levered rate/credit carry)
HIYLD  = ["KBWY"]                                   # high-dividend REIT
SUBSEC = ["REZ", "SRVR", "INDS", "NETL", "ROOF"]    # residential / data-center / industrial / net-lease
FACT   = ["SPY", "TLT", "IEF", "TIP", "DBC"]        # equity, duration, rates, inflation, commodity

def ols(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None); resid = y - X @ b
    r2 = 1 - resid.var() / y.var() if y.var() > 0 else float("nan")
    return b, r2, resid

def aligned(subset):
    """Max-overlap returns for just this subset (avoids the youngest ETF truncating everyone)."""
    P, d = panel(subset); keep = [s for s in subset if s in P]
    return {s: rets(P[s]) for s in keep}, d

def main():
    print("=" * 94); print("BROWNSTONE — real estate: income, rate-beta, or a landmine?"); print("=" * 94)

    # ---- Q1: is VNQ a distinct real asset or equity+duration beta? (per-REIT max history) ----
    print("\n  Q1  EQUITY-REIT factor decomposition (ret ~ a + b1·SPY + b2·TLT), each over its own full window")
    print(f"      {'reit':6}{'yrs':>5}{'β-SPY':>8}{'β-TLT':>8}{'R²':>7}{'α/yr':>8}{'resid-Sh':>10}")
    for s in EQREIT + HIYLD:
        Rp, dp = aligned([s, "SPY", "TLT"])
        if s not in Rp: continue
        y, spy_, tlt_ = Rp[s], Rp["SPY"], Rp["TLT"]; L = len(y)
        b, r2, resid = ols(y, np.column_stack([np.ones(L), spy_, tlt_]))
        rsh = resid.mean() / resid.std() * math.sqrt(252) if resid.std() > 0 else float("nan")
        print(f"      {s:6}{L/252:>5.1f}{b[1]:>+8.2f}{b[2]:>+8.2f}{r2*100:>6.0f}%{b[0]*252*100:>+7.1f}%{rsh:>+10.2f}")

    # ---- Q2: mortgage-REIT landmine (each over its own full window) --------------------------
    print("\n  Q2  MORTGAGE-REIT carry vs tail (the yield is not free)")
    print(f"      {'reit':6}{'Sharpe':>8}{'CAGR':>8}{'maxDD':>8}{'skew':>7}{'worst-day':>11}{'corr→SPY':>10}")
    for s in MREIT:
        Rp, _ = aligned([s, "SPY"])
        if s not in Rp: continue
        st = stats(Rp[s])
        print(f"      {s:6}{st['sh']:>+8.2f}{st['cagr']*100:>+7.1f}%{st['dd']*100:>+7.0f}%{skew_of(Rp[s]):>+7.2f}{Rp[s].min()*100:>+10.1f}%{corr(Rp[s], Rp['SPY']):>+10.2f}")

    # ---- Q3: diversifier vs 60/40? ---------------------------------------------------------
    print("\n  Q3  EQUITY-REIT (VNQ) as a diversifier")
    Rp, dp = aligned(["VNQ", "SPY", "TLT"]); vnq, spy_, tlt_ = Rp["VNQ"], Rp["SPY"], Rp["TLT"]
    s6040 = 0.6 * spy_ + 0.4 * tlt_
    print(f"      window {dp[0]}..{dp[-1]} ({len(dp)/252:.1f}y)")
    print(f"      VNQ  Sharpe {stats(vnq)['sh']:+.2f}  maxDD {stats(vnq)['dd']*100:+.0f}%  corr→SPY {corr(vnq, spy_):+.2f}  corr→60/40 {corr(vnq, s6040):+.2f}")
    print(f"      60/40 Sharpe {stats(s6040)['sh']:+.2f}  vs  90/10+VNQ Sharpe {stats(0.9*s6040 + 0.1*vnq)['sh']:+.2f}  (does a 10% REIT sleeve help?)")

    # ---- Q4: rate-regime conditional -------------------------------------------------------
    print("\n  Q4  RATE REGIME — VNQ when rates RISING vs FALLING (TLT 63-day trend)")
    v, t = vnq, tlt_; tltpx = np.cumprod(1 + t)
    trend = np.array([tltpx[i] > tltpx[max(0, i-63)] for i in range(len(t))])   # TLT up = rates falling
    ann = lambda a: (a.mean() * 252 * 100) if len(a) > 20 else float("nan")
    print(f"      rates FALLING (TLT up): VNQ {ann(v[trend]):+.1f}%/yr   |   rates RISING: VNQ {ann(v[~trend]):+.1f}%/yr")
    print("      → long-duration tell: REITs lean on falling rates" if ann(v[trend]) > ann(v[~trend]) else "      → no clean rate tell")

    # ---- Q5: sub-sector dispersion / rotation (broad set, common window) ---------------------
    want = EQREIT + HIYLD + SUBSEC
    Rp, dp = aligned(want); sub = [s for s in want if s in Rp]
    if len(sub) >= 3:
        Lm = min(len(Rp[s]) for s in sub); M = np.vstack([Rp[s][-Lm:] for s in sub]); C = np.corrcoef(M)
        avg = (C.sum() - len(sub)) / (len(sub) ** 2 - len(sub)); w = np.ones(len(sub)) / len(sub)
        eff = 1.0 / float(w @ C @ w)
        print(f"\n  Q5  SUB-SECTOR dispersion ({len(sub)} REIT ETFs, {dp[0]}..{dp[-1]}): avg pairwise corr {avg:+.2f}  effective bets {eff:.1f}")
        print(f"      → {'one common rate factor (rotation is noise)' if eff < 2 else 'some genuine dispersion to rotate'}")

    print("\n  READ: if VNQ is high-R² to SPY+TLT with ~0 residual, real estate is an equity+duration")
    print("  INGREDIENT (fine for a preservation/real-asset tilt), not alpha. Mortgage REITs' yield is a")
    print("  negative-skew landmine. Sub-sectors that collapse to ~1 effective bet are one rate factor.")

if __name__ == "__main__":
    main()
