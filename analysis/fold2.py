# -*- coding: utf-8 -*-
"""
Angle 2: does the AI Layoff Trap contain a trap?

Falk & Tsoukalas hold the income-replacement rate eta EXOGENOUS. But reabsorption
is demand-dependent: displaced workers are rehired only if firms expand, and firms
expand only if demand holds. Close that loop -- eta = eta(D) -- and ask whether the
system still has a unique equilibrium (paper: yes, a dominant strategy) or folds.

    alpha -> D -> eta -> l -> alpha

HOW THIS RELATES TO THE RECAPTURE RESULT. The two live at different
levels and do not conflict:
  * omega (Angle 1) is a FIRM-LEVEL object. It governs each firm's first-order
    condition, i.e. HOW MUCH automation happens.
  * the loop below is an AGGREGATE accounting relation: given an economy-wide
    automation rate, how much spending disappears and how much comes back. Read
    N*L as total employment and Lam as the economy-wide MPC; nothing here needs
    each firm to internalise 1/N.
So the fold is not mounted on the single-sector firm structure that Angle 1
refutes. It is, however, deliberately reduced-form: one aggregate sector, no
input-output detail. Publish it as an illustration of the missing feedback, not
as a calibrated forecast.

RESULT. With threshold-like (logistic) reabsorption the system is bistable above
a critical automation rate; with power-law reabsorption it is not (see fold.py).
Whether the trap has a tipping point is therefore an EMPIRICAL question about the
shape of eta(D) -- which nobody currently measures. That conditionality is the
finding, not a weakness.
"""
import numpy as np

w, N, Lam = 1.0, 7, 0.90


def make(A, eta_max, kappa, Dstar_frac):
    Dfull = A + Lam * w * N
    Dstar = Dstar_frac * Dfull
    eta = lambda D: eta_max / (1 + np.exp(-kappa * (D - Dstar)))
    Dof = lambda a, e: A + Lam * w * N * (1 - (1 - e) * a)
    return Dfull, Dstar, eta, Dof


def roots(alpha, eta, Dof, n=400_001):
    """Fixed points of eta = eta(D(alpha,eta)), each tagged stable/unstable.

    The middle (unstable) root separates the two basins, so it carries the
    whole hysteresis story and has to be labelled.
    """
    e = np.linspace(0, 1, n)
    g = eta(Dof(alpha, e)) - e
    out = []
    for i in np.where(np.diff(np.sign(g)) != 0)[0]:
        lo, hi = e[i], e[i + 1]
        for _ in range(70):
            m = 0.5 * (lo + hi)
            if np.sign(eta(Dof(alpha, lo)) - lo) == np.sign(eta(Dof(alpha, m)) - m):
                lo = m
            else:
                hi = m
        r = 0.5 * (lo + hi)
        h = 1e-6
        slope = ((eta(Dof(alpha, r + h)) - (r + h)) -
                 (eta(Dof(alpha, r - h)) - (r - h))) / (2 * h)
        out.append((r, "stable" if slope < 0 else "UNSTABLE"))
    return out


print("Is the fold generic, or does it need tuning? Sweeping reabsorption sharpness.")
print("(kappa = how threshold-like reabsorption is; kappa->0 is the paper's linear world)\n")
print(f"{'kappa':>7}{'A':>6}{'max #eq':>9}{'alpha_crit':>12}   verdict")
print("-" * 62)
for A in (2.0, 4.0):
    for kappa in (0.5, 1.0, 1.5, 2.0, 3.0, 5.0):
        _, _, eta, Dof = make(A, 0.85, kappa, 0.72)
        best, acrit = 1, None
        for a in np.linspace(0, 1, 201):
            r = roots(a, eta, Dof)
            best = max(best, len(r))
            if len(r) >= 3 and acrit is None:
                acrit = a
        print(f"{kappa:>7.1f}{A:>6.1f}{best:>9}"
              f"{(f'{acrit:.3f}' if acrit else '  -  '):>12}   "
              f"{'FOLD (bistable)' if best >= 3 else 'no fold'}")

# ---------------------------------------------------------------- the detail
KAPPA, A, ETA_MAX, DSTAR = 3.0, 2.0, 0.85, 0.72
print("\n" + "=" * 74)
print(f"Detail at kappa={KAPPA}, A={A}, eta_max={ETA_MAX}, D*={DSTAR}*Dfull, N={N}, Lam={Lam}")
print("=" * 74)
_, _, eta, Dof = make(A, ETA_MAX, KAPPA, DSTAR)
for a in np.linspace(0, 1, 21):
    r = roots(a, eta, Dof)
    tag = ",  ".join(f"eta={x:.3f} D={Dof(a,x):.2f} [{st}]" for x, st in r)
    print(f"  alpha={a:.2f} | {len(r)} eq | {tag}")

a_show = 0.55
r = roots(a_show, eta, Dof)
if len(r) >= 3:
    lo_e, hi_e = r[0][0], r[-1][0]
    dlo, dhi = Dof(a_show, lo_e), Dof(a_show, hi_e)
    print("\n" + "-" * 74)
    print(f"At the onset (alpha={a_show}, kappa={KAPPA}, A={A}) two stable basins coexist:")
    print(f"   HIGH reabsorption: eta={hi_e:.3f}  D={dhi:.2f}")
    print(f"   LOW  reabsorption: eta={lo_e:.3f}  D={dlo:.2f}")
    print(f"   gap = {100*(1-dlo/dhi):.1f}% of sectoral demand, at an UNCHANGED automation rate.")
    print(f"   separatrix (unstable root): eta={r[1][0]:.3f}")
    print("\n   Reading: automation does not push the economy off the cliff. It moves")
    print("   the cliff edge toward it. An ordinary shock then does the pushing, and")
    print("   hysteresis means the economy does not climb back the way it fell.")
