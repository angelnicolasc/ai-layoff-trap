# -*- coding: utf-8 -*-
"""The destructive band: where automation is privately profitable but leaves every
firm worse off than if none had automated.

DERIVATION
----------
Generalise the paper's Proposition 1 by replacing the internalisation coefficient
1/N with the measured wallet share omega. Firm i absorbs omega of ALL destruction,
and there are N_econ firms in the consumer economy each destroying l per task:

    pi_i - Pi_0 = L[ s*alpha_i - omega*l*N_econ*alpha_bar - (k/2)*alpha_i^2 ]

d/d alpha_i, with d alpha_bar / d alpha_i = 1/N_econ, gives the first-order
condition  s - omega*l - k*alpha = 0, so

    alpha_NE = (s - omega*l)/k

Substituting back at the symmetric equilibrium:

    pi - Pi_0 = (L/2k) * (s - omega*l) * (s - omega*l*(2*N_econ - 1))

That product is negative — every firm ends up below its no-automation profit —
exactly on the band

    omega*l  <  s  <  omega*l*(2*N_econ - 1)

The lower edge is where automation first becomes privately worthwhile. The upper
edge is where the cost saving finally outruns the demand destroyed. Peak loss is
at s* = omega*l*N_econ, with magnitude (L/2k)*[omega*l*(N_econ - 1)]^2.

N_econ is swept rather than fixed: the upper edge only stops binding once the
consumer economy is fragmented enough, and at small N_econ it binds hard.
"""
import numpy as np

# ---------------------------------------------------------------- parameters
w, eta, k, L = 1.0, 0.30, 1.0, 1.0
LAM   = 0.90                       # displaced worker's economy-wide MPC
OMEGA = (462.415 + 90.238) / 20_956.0   # Walmart + Sam's Club / U.S. PCE = 2.64%
l     = LAM * (1 - eta) * w        # social demand loss per automated task


def edges(omega, l, n_econ):
    return omega * l, omega * l * (2 * n_econ - 1)


def loss(s, omega, l, n_econ, k=k, L=L):
    """Per-firm profit shortfall against no automation. Positive = worse off."""
    return -(L / (2 * k)) * (s - omega * l) * (s - omega * l * (2 * n_econ - 1))


print("=" * 74)
print("THE DESTRUCTIVE BAND")
print("=" * 74)
print(f"  omega = {OMEGA:.4f}   l = Lam(1-eta)w = {l:.4f}   k = {k}   w = {w}")
print(f"  lower edge  s > omega*l = {OMEGA*l:.5f}  ->  c/w < {1 - OMEGA*l:.4f}")
print()
print(f"{'N_econ':>8}{'upper edge s':>15}{'binds?':>10}{'peak at s*':>13}"
      f"{'c/w at peak':>14}{'max loss':>12}")
print("-" * 74)
for n in (7, 20, 30, 38, 60, 100):
    lo, hi = edges(OMEGA, l, n)
    s_star = OMEGA * l * n
    peak   = (L / (2 * k)) * (OMEGA * l * (n - 1)) ** 2
    binds  = "yes" if hi < w else "no"
    cw     = 1 - s_star if s_star <= w else float("nan")
    cw_s   = f"{cw:.3f}" if np.isfinite(cw) and cw >= 0 else "  -  "
    print(f"{n:>8}{hi:>15.4f}{binds:>10}{s_star:>13.4f}{cw_s:>14}{peak:>12.5f}")
print("-" * 74)

n_thresh = next(n for n in range(2, 400) if edges(OMEGA, l, n)[1] >= w)
print(f"  The upper edge stops binding at N_econ = {n_thresh}. For any consumer")
print(f"  economy at least that fragmented, the band covers every capability level")
print(f"  from c/w = 0 up to c/w = {1 - OMEGA*l:.3f}: there is no 'AI so cheap it")
print("  stops hurting' regime to wait for.")

# ---------------------------------------------------------------- comparison
# Each row is internally consistent: the internalisation coefficient and the
# number of firms sharing the consumer wallet are the same object. Reading N as
# industry concentration puts omega at 1/N; measuring it puts omega at the
# wallet share, whose self-consistent N_econ is 1/omega.
print(chr(10) + "=" * 74)

print("READING N AS INDUSTRY CONCENTRATION vs MEASURING THE WALLET SHARE")
print("=" * 74)
print(f"{'reading':>26}{'omega':>10}{'N_econ':>9}{'band lower':>13}"
      f"{'destructive for':>18}{'width':>9}")
print("-" * 74)
rows = [("industry concentration, N=2", 1 / 2), ("industry concentration, N=4", 1 / 4),
        ("industry concentration, N=7", 1 / 7), ("measured wallet share", OMEGA)]
for tag, om in rows:
    n_econ = 1 / om
    lo, hi = edges(om, l, n_econ)
    width = min(hi, w) - lo
    print(f"{tag:>26}{om:>10.4f}{n_econ:>9.0f}{lo:>13.4f}"
          f"{'c/w < ' + format(1 - lo, '.3f'):>18}{width:>9.4f}")
print("-" * 74)
print("  Reading N as concentration confines the destructive band to expensive AI.")
print("  Measuring the same coefficient pushes the lower edge down by an order of")
print("  magnitude, so the band covers essentially the whole capability range.")
print("  Same model, same algebra - only the coefficient is measured, not assumed.")

# ------------------------------------------------ heterogeneity: the caveat
# The band above is a SYMMETRIC-economy result: one omega for every firm, with
# N_econ = 1/omega. Under heterogeneity omega and N_econ are independent. Hold
# N_econ fixed and vary omega, and the sign of (pi - Pi_0) flips: a small firm
# absorbs almost none of the aggregate destruction and profits from automating.
# So "leaves every firm worse off" is a claim about the symmetric economy, not
# about a heterogeneous one, and has to be stated that way.
N_FIXED, S_FIXED = 38, 0.7
print()
print("=" * 74)
print("HETEROGENEITY -- why the band result is conditional on symmetry")
print("=" * 74)
print(f"  N_econ held at {N_FIXED}, s = {S_FIXED}, omega varied:")
print(f"{'omega':>12}{'alpha_NE':>12}{'pi - Pi_0':>14}   outcome")
print("-" * 74)
for om in (OMEGA, 0.010, 0.005, 0.001, 1e-5):
    a = min(max((S_FIXED - om * l) / k, 0), 1)
    dpi = (L / (2 * k)) * (S_FIXED - om * l) * (S_FIXED - om * l * (2 * N_FIXED - 1))
    verdict = "WORSE off than not automating" if dpi < 0 else "BETTER off"
    print(f"{om:>12.5f}{a:>12.4f}{dpi:>+14.5f}   {verdict}")
print("-" * 74)
print("  The collective-harm claim therefore applies to firms with a meaningful")
print("  share of the consumer wallet, not to every firm in the economy.")

# ------------------------------------- the heterogeneous case, solved properly
# The section above holds N_econ fixed and varies omega, which is a sensitivity,
# not an equilibrium. Solving it properly: the demand term is linear in the sum
# of automation rates, so each firm's first-order condition is independent of
# its rivals and every firm plays its dominant alpha_i = (s - om_i*l)/k. With
# Sum(om_j) = 1 the aggregate is Sum(alpha_j) = (N*s - l)/k, giving
#
#     pi_i - Pi_0 = (L/k) [ (s^2 - om_i^2 l^2)/2  -  om_i * l * (N*s - l) ]
#
# The crossover omega* where a firm stops being harmed is strongly N_econ
# dependent, so it is a sensitivity result, not a single publishable number.
s_h = 0.7
het = lambda om, N: (L / k) * ((s_h ** 2 - (om * l) ** 2) / 2 - om * l * (N * s_h - l))
named = {"Walmart": 0.026372, "Amazon": 0.020328, "Costco": 0.008589,
         "Home Depot": 0.007253, "Microsoft": 0.001431, "Salesforce": 0.0000095}
print()
print("=" * 74)
print("HETEROGENEOUS EQUILIBRIUM -- and why the crossover is not one number")
print("=" * 74)
print(f"{'N_econ':>9}{'crossover omega*':>20}{'named firms worse off':>26}")
print("-" * 74)
for N_e in (38, 100, 500, 2007):
    gg = np.linspace(1e-9, 0.5, 200001)
    vv = het(gg, N_e)
    idx = np.where(np.diff(np.sign(vv)) != 0)[0]
    star = gg[idx[0]] if len(idx) else float("nan")
    n_bad = sum(het(o, N_e) < 0 for o in named.values())
    print(f"{N_e:>9}{star*100:>19.3f}%{n_bad:>20} of {len(named)}")
print("-" * 74)
print("  At N_econ=38 only the two largest firms are individually worse off; at a")
print("  realistic firm count almost all of them are. The aggregate stays negative")
print("  throughout, so the trap survives heterogeneity even where the per-firm")
print("  claim does not.")
