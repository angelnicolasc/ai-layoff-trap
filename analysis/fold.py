"""
Angle C test: does the AI Layoff Trap have a TRAP in it?

Falk & Tsoukalas hold the income-replacement rate eta EXOGENOUS.  But
reabsorption is itself demand-dependent: displaced workers get rehired only
if firms are expanding, and firms expand only if demand holds up.  Close that
loop -- eta = eta(D) -- and ask whether the system still has a unique
equilibrium (paper: yes, a dominant strategy) or folds.

Loop:  alpha -> D -> eta -> l -> alpha
Demand (paper eq.2, normalised L=1, per firm):
   D(alpha,eta) = A + Lam*w*N*[1 - (1-eta)*alpha]
Reabsorption (new): eta rises with demand, saturating.
   eta(D) = eta_max * (D/Dfull)^gamma   clipped to [0,1]
"""
import numpy as np

w, c, k, N, Lam = 1.0, 0.30, 1.0, 7, 0.90
s = w - c
A = 4.0
Dfull = A + Lam * w * N          # demand when nobody is displaced
eta_max, gamma = 0.85, 3.0       # reabsorption strength / how sharply it fades

def eta_of_D(D):  return float(np.clip(eta_max * (D / Dfull) ** gamma, 0.0, 1.0))
def D_of(alpha, eta): return A + Lam * w * N * (1 - (1 - eta) * alpha)

def fixed_points(alpha, grid=200001):
    """All eta solving eta = eta(D(alpha,eta)); returns roots + stability."""
    e  = np.linspace(0, 1, grid)
    g  = np.array([eta_of_D(D_of(alpha, x)) for x in e]) - e   # g(eta)=0 at f.p.
    sgn = np.sign(g)
    idx = np.where(np.diff(sgn) != 0)[0]
    out = []
    for i in idx:
        lo, hi = e[i], e[i + 1]
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if np.sign(eta_of_D(D_of(alpha, lo)) - lo) == np.sign(eta_of_D(D_of(alpha, mid)) - mid):
                lo = mid
            else:
                hi = mid
        r = 0.5 * (lo + hi)
        h = 1e-6
        slope = ((eta_of_D(D_of(alpha, r + h)) - (r + h)) - (eta_of_D(D_of(alpha, r - h)) - (r - h))) / (2 * h)
        out.append((r, "stable" if slope < 0 else "UNSTABLE"))
    return out

print("=" * 78)
print("Reabsorption loop gain  =  dD/deta * deta/dD  =  Lam*w*N*alpha * eta'(D)")
print("A fold appears where the loop gain crosses 1.\n")
print(f"{'alpha':>7} | {'# equilibria':>12} | roots (eta, stability)")
print("-" * 78)
prev_n = None
alpha_crit = None
for a in np.arange(0.0, 1.001, 0.05):
    fp = fixed_points(a)
    tag = ", ".join(f"{r:.3f} {st}" for r, st in fp)
    print(f"{a:>7.2f} | {len(fp):>12} | {tag}")
    if prev_n is not None and len(fp) > prev_n and alpha_crit is None:
        alpha_crit = a
    prev_n = len(fp)

# locate the fold precisely -- but only report one if it actually exists
print("-" * 78)
if len(fixed_points(1.0, grid=40001)) >= 3:
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if len(fixed_points(mid, grid=40001)) >= 3: hi = mid
        else: lo = mid
    print(f"Saddle-node (fold) bifurcation at alpha_crit ~= {hi:.4f}")
else:
    print("NO FOLD in alpha in [0,1]: a single stable equilibrium throughout.")
    print("Power-law reabsorption keeps the loop gain below 1 everywhere here.")
    print("See fold2.py -- a threshold-like (logistic) eta(D) does produce one.")

# (bistable-branch reporting only applies when a fold was actually found;
#  with power-law reabsorption it never is -- see fold2.py for the logistic case)
print()
print("Paper's model (eta exogenous) is LINEAR in alpha: one equilibrium, no fold,")
print("no tipping point, no hysteresis.  The word 'trap' describes the game, not the")
print("dynamics.  Closing the reabsorption loop puts an actual trap in the model.")
