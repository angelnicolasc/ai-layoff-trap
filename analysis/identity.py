# -*- coding: utf-8 -*-
"""
omega -- the recapture ratio -- derived as a basket share.

It needs no bridge through Lambda or disposable income: a displaced worker
cuts spending across their consumption basket, and a firm's share of that
basket is its revenue over PCE. Lambda enters only the level term l_soc.
"""
PCE = 20_956.0                    # US personal consumption expenditure, 2025, USD bn (BEA/FRED)

# ---------------------------------------------------------------- definition
print("=" * 76)
print("1. DEFINITION  (no Lambda, no DPI, no sector boundary)")
print("=" * 76)
print("""  A displaced worker loses one dollar of income and stops spending Lam of it.
  That reduction is spread across their consumption basket. Under proportional
  cuts, firm i's share of the basket is R_hh / PCE. So:

      spending destroyed          = Lam
      absorbed by firm i          = (R_hh/PCE) * Lam
      => share firm i recaptures  = omega = R_hh / PCE          <- observable

  Lam cancels. omega references no sector, so redrawing sector boundaries
  cannot move it -- this is the invariance claim, stated without the symmetric
  -subdivision assumption the earlier version leaned on.

  The paper is the special case in which the sector IS the economy, where the
  same coefficient reads as lam/(N*Lam). Its wedge is (1-omega)*l_soc/k and its
  corrective rate tau* = (1-omega)*l_soc, with l_soc = Lam(1-eta)w.""")

# ---------------------------------------------------------------- level term
LAM = 0.90                        # conservative; see note
print("=" * 76)
print("2. WHERE LAMBDA STILL LIVES  --  the level, and only the level")
print("=" * 76)
print(f"  l_soc = Lam*(1-eta)*w with Lam = {LAM:.2f}.")
print("  This is a CHOICE, declared against our own interest: the paper itself")
print("  cites a 3.6% personal savings rate (Mar-2026), implying Lam ~ 0.96.")
print("  A larger Lam would raise the level of the externality we are claiming,")
print("  so 0.90 is the conservative end. The level is sector-definition")
print("  dependent; the omega result above is not. Lead with omega.")

# ---------------------------------------------------------------- magnitudes
wmt_us, sams, wmt_intl = 462.415, 90.238, 121.885
wmt_hh   = wmt_us + sams
CUT_PCE  = PCE - 2_500.3 - 0.90 * 3_551.6      # imputed rent + third-party health
om_base, om_adv = wmt_hh / PCE, wmt_hh / CUT_PCE

print("\n" + "=" * 76)
print("3. THE CEILING")
print("=" * 76)
print(f"{'':<48}{'omega':>9}{'1-omega':>10}")
print("-" * 76)
print(f"{'paper, monopoly (N=1)':<48}{1.0:>9.4f}{0.0:>10.4f}")
print(f"{'paper, N=4':<48}{0.25:>9.4f}{0.75:>10.4f}")
print(f"{'measured, Walmart+Sams / total PCE':<48}{om_base:>9.4f}{1-om_base:>10.4f}")
print(f"{'measured, / cuttable PCE (most adverse)':<48}{om_adv:>9.4f}{1-om_adv:>10.4f}")
print("-" * 76)
print(f"  Upper bound across measurement variants: omega <= {om_adv*100:.2f}%")
print(f"  Largest single firm on the baseline measure: {om_base*100:.2f}%")
print("  These are different quantities and are never given the same label.")
l_soc = LAM * (1 - 0.30) * 1.0        # Lam(1-eta)w, eta=0.30 as everywhere else
print(f"  l_soc = Lam(1-eta)w = {l_soc:.4f}   (eta=0.30, w=1, k=1)")
print(f"  Corrected wedge at that omega = (1-omega)*l_soc/k = {(1-om_adv)*l_soc:.4f}")
print(f"  The paper's wedge at N=1 is exactly 0.")
print("  Two numbers, not a ratio: the ratio has zero in the denominator.")
print("  NOTE: (1-omega)*Lam alone is NOT the wedge -- it drops (1-eta) and 1/k,")
print("  and equals the wedge only at eta=0. tests.py section 2 proves this.")

# ------------------------------------------------- pre-empting two objections
print("\n" + "=" * 76)
print("4. OBJECTION A -- 'B2B firms recapture demand indirectly, via their clients'")
print("=" * 76)
print("  (a) The paper's model has no intermediate demand. Its firms sell straight")
print("      to the workers whose wages fund D (eq. 2). It cannot represent a B2B")
print("      firm at all, so the over-extension is the paper's, not ours.")
print("  (b) It does not matter anyway. Attribute 100% of a firm's GLOBAL revenue")
print("      to U.S. final consumption -- an attribution nobody would defend:")
for lab, rev in [("Walmart, all segments incl. International", wmt_hh + wmt_intl),
                 ("Amazon, all segments, calendar 2025",       716.9),
                 ("Apple, all global revenue",                 391.0)]:
    print(f"        {lab:<44} omega <= {rev/PCE*100:.2f}%")
print("      The bound stays under 3.5%. The indirect channel cannot rebuild 1/N = 25%.")

print("\n" + "=" * 76)
print("5. OBJECTION B -- 'if every firm merged, omega = 1 and the escape exists'")
print("=" * 76)
merged = wmt_hh + 150.0 + 180.0 + 106.0    # + Kroger, Costco U.S., Target
print(f"  The only entity with omega = 1 is a monopolist over ALL consumption.")
print(f"  Largest consolidation anyone could name -- Walmart+Sam's+Kroger+Costco+Target:")
print(f"        USD {merged:,.2f}bn  ->  omega = {merged/PCE*100:.2f}%")
print(f"  Still {0.25/(merged/PCE):.1f}x below the 25% the paper assigns to a mere N=4.")
print("  The grand coalition of Prop. 4 is not merely unlikely; it is arithmetically")
print("  out of reach for any legally conceivable combination of U.S. firms.")

# ------------------------------------------------- the paper's own example
print("\n" + "=" * 76)
print("6. BLOCK  --  the paper's opening example, and where its assumption breaks hardest")
print("=" * 76)
print("  Falk & Tsoukalas open with Block: 'In February 2026, Block cut nearly half")
print("  its 10,000-person workforce, with CEO Jack Dorsey stating that AI had made")
print("  many of those roles unnecessary.' It is the paper's motivating anecdote.")
print("  Block is a payments company. Square sells to merchants; Cash App's revenue")
print("  is dominated by bitcoin resale. Its laid-off engineers were never its")
print("  customers. Computing omega under three increasingly generous readings:\n")
for lab, rev in [("Cash App, ex-bitcoin (a fair reading)",  6.0),
                 ("ALL of Cash App incl. bitcoin resale",  15.4),
                 ("100% of Block's global revenue",        24.0)]:
    om = rev / PCE
    print(f"    {lab:<40} omega = {om*100:.3f}%   ->  {om*100:>5.2f} USD per 100 destroyed")
print(f"\n  Even the absurd upper bound leaves Block at ~{24.0/PCE*100:.2f}% -- roughly")
print(f"  {(wmt_hh/PCE)/(24.0/PCE):.0f}x below Walmart and {0.25/(24.0/PCE):.0f}x below the 1/N the paper assigns N=4.")
print("  The paper picked, as its illustration of the trap, the firm whose own")
print("  internalisation is closest to zero.")
