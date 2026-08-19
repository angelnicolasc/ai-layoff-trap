# -*- coding: utf-8 -*-
"""
The Recapture Ratio -- v2, corrected framing + measurement robustness.
Falk & Tsoukalas (2026), "The AI Layoff Trap", arXiv:2603.20617 (v3).

omega enters the wedge as (1 - omega): a small omega means the externality is
MAXIMAL, not small. The finding is that the paper's low-externality region
(concentrated markets) is EMPTY -- not that the trap is smaller than claimed.
"""
import numpy as np

# ============================================================ 0. the identity
# Paper, Prop 1:  Rev_i = A/N + lam*w*L - l*L*abar ,  l = lam(1-eta)w
#   d Rev_i / d alpha_i = -l*L/N
# So firm i absorbs (lam/N) of each displaced worker's INCOME.
#
# Let Lam = displaced worker's total MPC across ALL sectors (~0.9).
# Then firm i's share of the CONSUMER WALLET is
#     omega_i = (lam/N)/Lam        <-- directly measurable as R_hh / PCE
# and the model becomes
#     alpha_NE = (s - omega_i*l_soc)/k ,  l_soc = Lam(1-eta)w
#     wedge_i  = (1 - omega_i)*l_soc/k ,  tau*_i = (1 - omega_i)*l_soc
# The paper is the case omega_i = 1/N (i.e. lam = Lam: the sector IS the economy).

print("="*80)
print("A.  WHAT IS BOUNDARY-FREE, AND WHAT ONLY LOOKS IT")
print("="*80)
print("  The paper internalises l/N per task, l = lam(1-eta)w. Per unit of lost")
print("  worker INCOME that is lam/N.")
print()
print("  lam/N is invariant under SYMMETRIC subdivision only:")
for d in (1, 2, 4, 8):
    print(f"    lam={0.50/d:.4f} N={8//d}  ->  lam/N = {(0.50/d)/(8//d):.5f}")
print()
print("  Under a realistic ASYMMETRIC partition it moves:")
print(f"    whole economy  lam=0.90 N=38  ->  {0.90/38:.5f}")
print(f"    grocery only   lam=0.08 N=6   ->  {0.08/6:.5f}   (a factor of "
      f"{(0.90/38)/(0.08/6):.2f})")
print()
print("  So the lemma is scope-limited and cannot by itself answer the sector-")
print("  boundary objection. What can is omega = R_hh / PCE: it names no sector,")
print("  so it is boundary-free by construction rather than by argument.")
print(f"    measured directly: omega(Walmart) = {552.653/20_956.0:.5f}")
PCE_2025_annual   = 20_956.0   # BEA/FRED, annual 2025, $bn
IMPUTED_RENT      =  2_500.3   # BEA/FRED, 2025 -- a laid-off owner cannot cut this
PCE_HEALTH_SVCS   =  3_551.6   # BEA/FRED, 2025 -- mostly third-party paid
THIRD_PARTY_SHARE =    0.90    # CMS NHE: out-of-pocket ~10% of health spending

CUTTABLE_PCE = PCE_2025_annual - IMPUTED_RENT - THIRD_PARTY_SHARE*PCE_HEALTH_SVCS

WMT_US    = 462.415            # Walmart U.S. segment, FY2025 10-K
SAMS_US   =  90.238            # Sam's Club U.S. segment, FY2025 10-K
WMT_TOTAL = WMT_US + SAMS_US

print("\n" + "="*80)
print("B.  ROBUSTNESS OF THE CEILING  --  each variant chosen to FAVOUR the paper")
print("="*80)
print(f"  total PCE 2025                     ${PCE_2025_annual:>9,.0f} bn")
print(f"  less imputed rent                  ${IMPUTED_RENT:>9,.0f} bn")
print(f"  less third-party health ({THIRD_PARTY_SHARE:.0%})        ${THIRD_PARTY_SHARE*PCE_HEALTH_SVCS:>9,.0f} bn")
print(f"  = 'cuttable' PCE                   ${CUTTABLE_PCE:>9,.0f} bn\n")

variants = [
    ("V1  Walmart U.S. / total PCE",              WMT_US,    PCE_2025_annual),
    ("V2  + Sam's Club U.S. (max numerator)",     WMT_TOTAL, PCE_2025_annual),
    ("V3  + cuttable PCE (max adverse denom.)",   WMT_TOTAL, CUTTABLE_PCE),
]
print(f"{'variant':<44}{'omega':>9}{'externality':>14}{'N_eff=1/omega':>15}")
print("-"*80)
ceil_om = 0
for name, num, den in variants:
    om = num/den; ceil_om = max(ceil_om, om)
    print(f"{name:<44}{om*100:>8.2f}%{(1-om)*100:>13.2f}%{1/om:>15.0f}")
print("-"*80)
print(f"  Two further effects both push omega DOWN, so V3 is a genuine upper bound:")
print(f"   - Walmart is ~60% grocery; laid-off workers cut discretionary harder than")
print(f"     staples, so Walmart's share of the CUT is below its share of the LEVEL.")
print(f"   - Trade-down: displaced workers shift spending TOWARD Walmart, offsetting")
print(f"     the revenue loss further (omega could even be negative).")
print(f"\n  CEILING FOR THE ENTIRE U.S. ECONOMY: omega <= {ceil_om*100:.2f}%"
      f"  ->  externality >= {(1-ceil_om)*100:.2f}%")

# ==================================================== 2. the firm cross-section
firms = [
    ("Walmart (U.S. + Sam's Club)",  WMT_TOTAL,  4),
    ("Amazon (North America seg.)",      426.0,  4),
    ("Costco (U.S.)",                    180.0,  6),
    ("Home Depot",                       152.0,  2),
    ("Microsoft (consumer slice)",        30.0,  3),
    ("Alphabet (direct-to-consumer)",     15.0,  2),
    ("Salesforce",                         0.2,  5),
    ("Typical B2B SaaS",                   0.0, 30),
]
print("\n" + "="*80)
print("C.  CROSS-SECTION  --  translated back into the paper's own variable")
print("="*80)
print(f"{'firm':<32}{'omega':>9}{'externality':>13}{'N_eff':>11}{'actual N':>10}{'ratio':>9}")
print("-"*80)
for name, rev, n in firms:
    om = rev/PCE_2025_annual
    ne = 1/om if om > 0 else np.inf
    r  = ne/n
    nes = f"{ne:,.0f}" if np.isfinite(ne) else "inf"
    rs  = f"{r:,.0f}x" if np.isfinite(r) else "inf"
    print(f"{name:<32}{om*100:>8.3f}%{(1-om)*100:>12.2f}%{nes:>11}{n:>10}{rs:>9}")

# ==================================================== 3. what actually changes
print("\n" + "="*80)
print("D.  WHAT THE CORRECTION DOES TO THE PAPER'S RESULTS")
print("="*80)
om_max = ceil_om
print(f"{'':<38}{'paper':>18}{'corrected':>20}")
print("-"*80)
for lbl, pv, cv in [
    ("paper: sectoral monopolist",     "0%",     "not comparable"),
    ("largest real firm, baseline",    "n/a",    f"{(1-552.653/20_956.0)*100:.1f}%"),
    ("largest real firm, adverse",     "n/a",    f"{(1-om_max)*100:.1f}%"),
    ("externality as N->inf",          "100%",   "100%"),
    ("range over all market structures","0-100%", f"{(1-om_max)*100:.1f}-100%"),
    ("grand coalition of automators",  "closes it", "leaves >=96% open"),
    ("largest wedge per task",         "fragmented", "low wallet-share"),
]:
    print(f"{lbl:<38}{pv:>18}{cv:>20}")
print("-"*80)
print("  The first row is NOT a like-for-like comparison and is marked so. The")
print("  paper's N=1 case is a monopolist over its own SECTOR, whose externality")
print("  is zero by construction of that model; a real firm's omega is measured")
print("  economy-wide. The finding is not that the paper's arithmetic fails. It")
print("  is that no real firm is positioned anywhere near the internalisation its")
print("  escape routes would require, so severity is uniform across market")
print("  structures instead of graded by them.")
