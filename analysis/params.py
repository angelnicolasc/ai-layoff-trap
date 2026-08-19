# -*- coding: utf-8 -*-
"""Single source of truth for every parameter and derived figure in this repo.

WHY THIS MODULE EXISTS
----------------------
Every published figure was previously written out by hand in the script that
used it and again in the README. Two failures follow from that structurally,
and both occurred:

  * the same quantity drifted between files (a wedge computed with eta=0 in one
    script and eta=0.30 in another), and
  * one label was attached to two different numbers ("ceiling" for both the
    largest single firm and the upper bound across measurement variants).

Nothing here is asserted. Every derived quantity is a function of the raw
inputs below, `tests.py` re-derives each one from first principles, and it also
parses the README and fails if any number there disagrees with this module.
"""

# ----------------------------------------------------------------- raw inputs
# U.S. personal consumption expenditure, calendar 2025, USD bn (BEA / FRED).
PCE = 20_956.0

# Components netted out to build the deliberately adverse denominator. Both are
# spending a laid-off worker cannot cut, so removing them shrinks the base and
# RAISES omega -- i.e. this variant favours the paper, not this analysis.
IMPUTED_RENT = 2_500.3          # BEA, 2025
PCE_HEALTH = 3_551.6            # BEA, PCE health care services, 2025
THIRD_PARTY_HEALTH = 0.90       # CMS NHE: out-of-pocket is ~10% of health spend

# Behavioural and technology parameters. LAM and ETA are choices; see NOTES.
LAM = 0.90                      # displaced worker's economy-wide MPC
ETA = 0.30                      # income-replacement rate
W = 1.0                         # wage, normalised
K = 1.0                         # integration-cost curvature, normalised

# Firm revenues, USD bn. `hh` is U.S. household-facing revenue: the numerator
# that belongs over PCE. `total` is all revenue including non-household and
# non-U.S., used only for the deliberately absurd upper-bound test.
FIRMS = {
    "Walmart":    {"hh": 462.415 + 90.238, "total": 462.415 + 90.238 + 121.885,
                   "rivals": 4, "scope": "U.S. segment + Sam's Club U.S.",
                   "period": "FY2025 (ended 2025-01-31)"},
    "Amazon":     {"hh": 426.0, "total": 716.9,
                   "rivals": 4, "scope": "North America segment",
                   "period": "NA segment FY2025; total is calendar 2025"},
    "Costco":     {"hh": 180.0, "total": 254.0,
                   "rivals": 6, "scope": "U.S.", "period": "FY2025"},
    "Home Depot": {"hh": 152.0, "total": 159.5,
                   "rivals": 2, "scope": "U.S.", "period": "FY2025"},
    "Apple":      {"hh": 160.0, "total": 391.0,
                   "rivals": 3, "scope": "est. U.S. consumer share",
                   "period": "FY2025"},
    "Microsoft":  {"hh": 30.0, "total": 281.7,
                   "rivals": 3, "scope": "consumer segment, ESTIMATED",
                   "period": "FY2025"},
    "Alphabet":   {"hh": 15.0, "total": 350.0,
                   "rivals": 2, "scope": "direct-to-consumer only",
                   "period": "FY2025"},
    "Salesforce": {"hh": 0.2, "total": 38.0,
                   "rivals": 5, "scope": "negligible household revenue",
                   "period": "FY2025"},
    "Block":      {"hh": 6.0, "total": 24.1,
                   "rivals": 5, "scope": "Cash App excl. bitcoin passthrough",
                   "period": "FY2025"},
}

# Firms in the largest consolidation anyone could name, for the merger bound.
MERGER = ["Walmart", "Costco"]
MERGER_EXTRA = {"Kroger": 150.0, "Target": 106.0}   # hh revenue, USD bn

# fold2.py sweep settings, so the README cannot quote a range the code
# does not produce.
FOLD_A_VALUES = (2.0, 4.0)
FOLD_KAPPAS = (0.5, 1.0, 1.5, 2.0, 3.0, 5.0)
FOLD_ETA_MAX = 0.85
FOLD_DSTAR_FRAC = 0.72
FOLD_N = 7


# ------------------------------------------------------------------- derived
def cuttable_pce():
    """PCE net of imputed rent and third-party-paid health services."""
    return PCE - IMPUTED_RENT - THIRD_PARTY_HEALTH * PCE_HEALTH


def l_soc(lam=LAM, eta=ETA, w=W):
    """Social demand loss per automated task: Lam(1-eta)w."""
    return lam * (1 - eta) * w


def omega(rev_hh, denom=None):
    """Share of destroyed consumer spending a firm recaptures."""
    return rev_hh / (PCE if denom is None else denom)


def wedge(om, lam=LAM, eta=ETA, w=W, k=K):
    """Over-automation wedge under the corrected internalisation coefficient.

    (1 - om) * l_soc / k -- the repo's own formula, with every factor present.
    Passing only `om` and letting the rest default is what keeps this from
    silently becoming (1-om)*Lam, which is the wedge only at eta=0.
    """
    return (1 - om) * l_soc(lam, eta, w) / k


def paper_wedge(lam_sector, n, eta=ETA, w=W, k=K):
    """Falk & Tsoukalas Proposition 1: l(1-1/N)/k with l = lam(1-eta)w."""
    return lam_sector * (1 - eta) * w * (1 - 1 / n) / k


def n_eff(om):
    """The N a firm behaves as if it faced: 1/omega."""
    return float("inf") if om == 0 else 1 / om


def firm_omega(name, adverse=False):
    return omega(FIRMS[name]["hh"], cuttable_pce() if adverse else None)


def largest_firm(adverse=False):
    """The single firm with the highest omega, and that omega."""
    best = max(FIRMS, key=lambda n: FIRMS[n]["hh"])
    return best, firm_omega(best, adverse)


def measurement_upper_bound():
    """Highest omega any firm reaches under ANY of the measurement variants.

    Distinct from largest_firm(): that is the highest firm on one basis; this
    is the highest value the quantity takes across bases. Conflating the two is
    the naming failure this module exists to prevent.
    """
    return max(firm_omega(n, adv) for n in FIRMS for adv in (False, True))


def max_attribution_bound():
    """Ceiling if 100% of a firm's GLOBAL revenue were credited to U.S.
    household consumption -- an attribution nobody would defend."""
    name = max(FIRMS, key=lambda n: FIRMS[n]["total"])
    return name, FIRMS[name]["total"] / PCE


def merger_omega():
    """Largest legally conceivable consumer-retail consolidation."""
    tot = sum(FIRMS[n]["hh"] for n in MERGER) + sum(MERGER_EXTRA.values())
    return tot, tot / PCE


NOTES = {
    "LAM": "Chosen at 0.90, conservative. The paper cites a 3.6% personal "
           "savings rate (Mar-2026), implying ~0.96 for the average household; "
           "a displaced worker's MPC is higher still. A larger LAM raises the "
           "externality claimed here, so 0.90 understates it.",
    "ETA": "0.30, from the displaced-worker earnings-loss literature the paper "
           "itself cites. It enters l_soc; forgetting it inflates the wedge.",
    "period": "Numerators are fiscal-year filings; the denominator is calendar "
              "2025 PCE. Walmart's FY2025 closed 2025-01-31, so the numerator "
              "leads the denominator by up to a year. Growing the numerator "
              "forward RAISES omega, which weakens the claim made here; "
              "tests.py bounds that sensitivity explicitly.",
}


# ------------------------------------------------- fold detection, shared
# fold2.py and tests.py both call these, so the onset/offset published in the
# README cannot drift from what the code produces. The previous version had
# fold2.py printing 0.620/0.795 (coarse scan) while the README said 0.618/0.792
# (fine simulation): two numbers for one quantity, the failure this file exists
# to prevent.
def fold_maps(A, kappa, n=FOLD_N, eta_max=FOLD_ETA_MAX, dstar=FOLD_DSTAR_FRAC):
    import numpy as np
    d_full = A + LAM * W * n
    d_star = dstar * d_full
    eta = lambda D: eta_max / (1 + np.exp(-kappa * (D - d_star)))
    dof = lambda a, e: A + LAM * W * n * (1 - (1 - e) * a)
    return eta, dof


def fold_roots(alpha, eta, dof, grid=40_001):
    """Fixed points of eta = eta(D(alpha, eta)), with stability."""
    import numpy as np
    e = np.linspace(0, 1, grid)
    g = eta(dof(alpha, e)) - e
    out = []
    for i in np.where(np.diff(np.sign(g)) != 0)[0]:
        lo, hi = e[i], e[i + 1]
        for _ in range(70):
            m = 0.5 * (lo + hi)
            if np.sign(eta(dof(alpha, lo)) - lo) == np.sign(eta(dof(alpha, m)) - m):
                lo = m
            else:
                hi = m
        r = 0.5 * (lo + hi)
        h = 1e-6
        slope = ((eta(dof(alpha, r + h)) - (r + h)) -
                 (eta(dof(alpha, r - h)) - (r - h))) / (2 * h)
        out.append((r, "stable" if slope < 0 else "UNSTABLE"))
    return out


def fold_window(A, kappa, coarse=201, refine=30):
    """Both saddle-nodes: (onset, offset, persists_to_alpha_1) or None.

    Bistability is a WINDOW in alpha, not a half-line. Scanning only for the
    first alpha with three roots finds the onset and silently misses the second
    edge, which is how the half-line version got published: false for four of
    the eight folding cells in this sweep.

    A coarse scan brackets the window, then each edge is bisected. Scanning the
    whole interval finely is ~20x slower for the same answer to 1e-4.
    """
    import numpy as np
    eta, dof = fold_maps(A, kappa)
    tri = lambda a: len(fold_roots(a, eta, dof, 20_001)) >= 3
    grid = np.linspace(0, 1, coarse)
    flags = [tri(a) for a in grid]
    if not any(flags):
        return None
    first = flags.index(True)
    last = len(flags) - 1 - flags[::-1].index(True)

    def edge(lo, hi, want_true_at_hi):
        for _ in range(refine):
            m = 0.5 * (lo + hi)
            if tri(m) == want_true_at_hi:
                hi = m
            else:
                lo = m
        return hi if want_true_at_hi else lo

    on = grid[0] if first == 0 else edge(grid[first - 1], grid[first], True)
    if last == len(grid) - 1:
        return on, 1.0, True
    off = edge(grid[last], grid[last + 1], False)
    return on, off, False
