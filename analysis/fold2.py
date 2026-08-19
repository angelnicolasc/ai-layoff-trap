# -*- coding: utf-8 -*-
"""Does the AI Layoff Trap contain a trap?

Falk & Tsoukalas hold the income-replacement rate eta EXOGENOUS. Reabsorption is
demand-dependent: displaced workers are rehired only if firms expand, and firms
expand only if demand holds. Close that loop -- eta = eta(D) -- and ask whether
the system still has a unique equilibrium (paper: yes, a dominant strategy).

    alpha -> D -> eta -> l -> alpha

HOW THIS RELATES TO THE RECAPTURE RESULT. The two live at different levels and
do not conflict. omega is a FIRM-LEVEL object governing each firm's first-order
condition, i.e. how much automation happens. The loop below is an AGGREGATE
accounting relation: given an economy-wide automation rate, how much spending
disappears and how much comes back. Read N*L as total employment and Lam as the
economy-wide MPC; nothing here needs each firm to internalise 1/N.

RESULT, stated precisely. Bistability is a WINDOW in alpha, not a half-line. It
opens at one saddle-node and, for the flatter reabsorption curves, closes again
at a second one. Whether the high-reabsorption branch survives all the way to
full automation depends on kappa:

  * kappa at the flat end (A=2: 1.5-2.0; A=4: 1.0-1.5) -- the window CLOSES. The
    high branch ceases to exist, so automation alone drives the economy to the
    low-reabsorption state. No external shock is needed.
  * kappa at the sharp end (A=2: >=3; A=4: >=2) -- both branches persist to
    alpha=1. Automation narrows the basin of the good equilibrium; an ordinary
    shock does the pushing, and hysteresis keeps the economy down.

An earlier version of this file scanned only for the first alpha with three
roots and reported bistability as holding everywhere past an onset. That finds the onset and
silently misses the offset, and the claim is false for four of the eight
folding cells below. Both edges are detected here, via params.fold_window.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P

print("=" * 78)
print("BISTABILITY WINDOW  --  both saddle-nodes, not just the onset")
print("=" * 78)
print(f"  eta_max={P.FOLD_ETA_MAX}, D*={P.FOLD_DSTAR_FRAC}*D_full, N={P.FOLD_N}, "
      f"Lam={P.LAM}  (only kappa and A are swept)")
print()
print(f"{'A':>5}{'kappa':>8}{'onset':>10}{'offset':>12}{'width':>9}   verdict")
print("-" * 78)
for A in P.FOLD_A_VALUES:
    for kappa in P.FOLD_KAPPAS:
        win = P.fold_window(A, kappa)
        if win is None:
            print(f"{A:>5.1f}{kappa:>8.1f}{'-':>10}{'-':>12}{'-':>9}   no fold")
            continue
        on, off, persists = win
        off_s = "persists" if persists else f"{off:.4f}"
        width = "to a=1" if persists else f"{off - on:.4f}"
        verdict = ("both branches reach alpha=1" if persists
                   else "window CLOSES: high branch dies")
        print(f"{A:>5.1f}{kappa:>8.1f}{on:>10.4f}{off_s:>12}{width:>9}   {verdict}")
print("-" * 78)
print("  A power-law eta(D) produces no fold at all (fold.py). That is not an")
print("  artefact of choosing a sigmoid: a convex eta gives a convex fixed-point")
print("  map, which admits at most two crossings and therefore never three.")

# ------------------------------------------------------------------ the detail
KAPPA, A = 3.0, 2.0
print()
print("=" * 78)
print(f"Detail at kappa={KAPPA}, A={A} -- a case where both branches persist")
print("=" * 78)
eta, dof = P.fold_maps(A, KAPPA)
for a in np.linspace(0, 1, 21):
    r = P.fold_roots(a, eta, dof)
    tag = ",  ".join(f"eta={x:.3f} D={dof(a, x):.2f} [{st}]" for x, st in r)
    print(f"  alpha={a:.2f} | {len(r)} eq | {tag}")

a_show = 0.55
r = P.fold_roots(a_show, eta, dof)
if len(r) >= 3:
    lo_e, hi_e = r[0][0], r[-1][0]
    dlo, dhi = dof(a_show, lo_e), dof(a_show, hi_e)
    print()
    print("-" * 78)
    print(f"At the onset (alpha={a_show}, kappa={KAPPA}, A={A}) two stable basins coexist:")
    print(f"   HIGH reabsorption: eta={hi_e:.3f}  D={dhi:.2f}")
    print(f"   LOW  reabsorption: eta={lo_e:.3f}  D={dlo:.2f}")
    print(f"   gap = {100*(1-dlo/dhi):.1f}% of sectoral demand, at an UNCHANGED "
          f"automation rate.")
    print(f"   separatrix (unstable root): eta={r[1][0]:.3f}")
    print()
    print("   Reading, for this kappa only: automation does not push the economy")
    print("   off the cliff, it narrows the basin. An ordinary shock does the")
    print("   pushing, and hysteresis keeps it down. At flatter kappa the high")
    print("   branch disappears outright and automation alone suffices -- see the")
    print("   window table above. Which regime holds is an empirical question")
    print("   about the shape of eta(D) that nobody currently measures.")
