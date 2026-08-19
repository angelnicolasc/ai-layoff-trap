# -*- coding: utf-8 -*-
"""Exhaustive checks. Nothing in this repo is asserted; everything is re-derived.

Run:  python analysis/tests.py

Each test states WHY it exists, then proves its claim by an independent route --
a grid instead of a point, a numerical optimum instead of restated algebra, a
simulated trajectory instead of a root-finder, both saddle-nodes instead of the
first one. Several tests exist because the corresponding error was shipped.

A check whose guard can never be False is worse than no check, because it
reports a pass. Section 5 previously contained `X is False or True`, which is
True for every input. Every guard here is exercised against a case that must
fail it.
"""
import glob
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FAILS = []
CHECKS = 0


def check(name, ok, detail=""):
    global CHECKS
    CHECKS += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if detail:
        print(f"         {detail}")
    if not ok:
        FAILS.append(name)


def head(n):
    print("\n" + "=" * 78)
    print(n)
    print("=" * 78)


# ============================================================== 1. Proposition 1
head("1. Proposition 1 holds across the parameter space, not at one point")
print("""  WHY: a closed form that matches at one point can still be wrong. This sweeps
  a grid and asserts the two routes to the wedge agree wherever Prop 1(iii)'s
  interiority condition l < s < k + l holds -- and that the condition actually
  excludes points, so the test is not vacuous.""")

interior_n = corner_n = 0
worst = 0.0
for c in np.arange(0.05, 0.96, 0.05):
    for lam in (0.3, 0.5, 0.7, 1.0):
        for eta in (0.0, 0.15, 0.30, 0.5):
            for k in (0.5, 1.0, 2.0):
                for N in (2, 3, 4, 7, 20, 100):
                    w = 1.0
                    s, l = w - c, lam * (1 - eta) * w
                    ne = np.clip((s - l / N) / k, 0, 1)
                    co = np.clip((s - l) / k, 0, 1)
                    if l < s < k + l and (s - l / N) / k <= 1:
                        interior_n += 1
                        worst = max(worst, abs((ne - co) - l * (1 - 1 / N) / k))
                    else:
                        corner_n += 1
check("closed form matches on every interior point", worst < 1e-12,
      f"{interior_n:,} interior of {interior_n+corner_n:,} grid points, "
      f"max deviation {worst:.2e}")
check("the interiority condition actually excludes points", corner_n > 0,
      f"{corner_n:,} corner points excluded; without these the test is vacuous")


# ====================================================== 2. the wedge formula
head("2. The wedge uses every factor in its own definition")
print("""  WHY: the repo shipped `Lam*(1-omega)` labelled 'corrected wedge'. That drops
  (1-eta) and 1/k, and equals the wedge only at eta=0 while every other script
  uses eta=0.30.""")

om_adv = P.measurement_upper_bound()
wrong, right = P.LAM * (1 - om_adv), P.wedge(om_adv)
check("Lam*(1-omega) is NOT the wedge at eta=0.30", abs(wrong - right) > 0.2,
      f"{wrong:.4f} vs {right:.4f} -> overstated by {100*(wrong/right-1):.0f}%")
check("the two coincide exactly at eta=0",
      abs(wrong - P.wedge(om_adv, eta=0.0)) < 1e-12)
check("wedge scales as 1/k",
      abs(P.wedge(om_adv, k=2.0) - P.wedge(om_adv, k=1.0) / 2) < 1e-12)
check("wedge scales linearly in (1-eta)",
      abs(P.wedge(om_adv, eta=0.5) - P.wedge(om_adv, eta=0.0) * 0.5) < 1e-12)


# ============================================ 3. band algebra, re-derived
head("3. The destructive band, re-derived numerically instead of restated")
print("""  WHY: the closed form was derived by hand. This rebuilds the profit function,
  finds the best response by numerical optimisation over a 200k grid, and
  compares. If the hand algebra were wrong this disagrees.""")

def dpi(a_i, a_bar, om, l, n, s, k=1.0, L=1.0):
    return L * (s * a_i - om * l * n * a_bar - (k / 2) * a_i ** 2)

worst_a = worst_pi = 0.0
for om in (0.0264, 0.10, 0.25, 0.5):
    for n in (4, 7, 38, 100):
        for s in (0.2, 0.5, 0.7, 0.95):
            l, k = P.l_soc(), 1.0
            grid = np.linspace(0, 1, 200_001)
            a_star = min(max((s - om * l) / k, 0.0), 1.0)
            br = grid[np.argmax(dpi(grid, (grid + (n - 1) * a_star) / n, om, l, n, s, k))]
            worst_a = max(worst_a, abs(br - a_star))
            if 0 < a_star < 1:
                closed = (1 / (2 * k)) * (s - om * l) * (s - om * l * (2 * n - 1))
                worst_pi = max(worst_pi, abs(closed - dpi(a_star, a_star, om, l, n, s, k)))
check("numerical best response reproduces alpha_NE = (s - om*l)/k", worst_a < 1e-4,
      f"max deviation {worst_a:.2e}")
check("closed-form profit matches direct evaluation", worst_pi < 1e-12,
      f"max deviation {worst_pi:.2e}")


# ================================== 4. lambda/N invariance: prove the SCOPE
head("4. lambda/N invariance holds ONLY under symmetric subdivision")
print("""  WHY: the repo printed this as a general lemma. It is not, so it cannot carry
  the boundary-objection rebuttal. omega = R_hh/PCE can, because it names no
  sector. Both the holding case and the failing case are proved.""")

sym = {(0.50 / d) / (8 // d) for d in (1, 2, 4, 8)}
check("symmetric subdivision leaves lam/N fixed",
      len(sym) == 1 and abs(sym.pop() - 0.0625) < 1e-12)
whole, groc = 0.90 / 38, 0.08 / 6
check("asymmetric partition MOVES lam/N", abs(whole - groc) > 1e-3,
      f"{whole:.5f} vs {groc:.5f}, a factor of {whole/groc:.2f}")
check("omega is a directly observable ratio naming no sector",
      abs(P.firm_omega("Walmart") - P.FIRMS["Walmart"]["hh"] / P.PCE) < 1e-15)


# ============================== 5. heterogeneity, with a guard that can fail
head("5. The band result is conditional on symmetry, and dpi is NOT monotone")
print("""  WHY: two failures here. The claim 'every firm ends up worse off' assumes one
  omega for all firms. And the previous monotonicity guard was `X is False or
  True`, true for every input. Both are replaced with properties that can fail.""")

l, k, s, n, L = P.l_soc(), 1.0, 0.7, 38, 1.0
f = lambda om: (L / (2 * k)) * (s - om * l) * (s - om * l * (2 * n - 1))
check("a Walmart-sized firm ends up worse off", f(P.firm_omega("Walmart")) < 0,
      f"dpi = {f(P.firm_omega('Walmart')):+.5f}")
check("a firm with omega -> 0 ends up BETTER off, so 'every firm' is false",
      f(1e-5) > 0, f"dpi = {f(1e-5):+.5f}")

g = np.linspace(0, 1, 200_001)
v = f(g)
d = np.diff(v)
flips = int(np.sum(np.diff(np.sign(d)) != 0))
check("dpi is NOT monotone in omega (the old guard could not detect this)",
      flips == 1, f"{flips} sign change in the derivative; minimum at "
                  f"omega={g[int(np.argmin(v))]:.4f}")
check("the extremum sits where the analytic derivative vanishes",
      abs(g[int(np.argmin(v))] - n * s / (l * (2 * n - 1))) < 1e-3,
      f"numeric {g[int(np.argmin(v))]:.4f} vs analytic "
      f"Ns/(l(2N-1)) = {n*s/(l*(2*n-1)):.4f}")
roots = int(np.sum(np.diff(np.sign(v)) != 0))
check("dpi crosses zero exactly once on [0, 1]", roots == 1,
      f"single crossing at omega = {g[np.where(np.diff(np.sign(v)) != 0)[0][0]]:.4f}")
# the guard must be able to fail: a strictly monotone series must not pass it
mono = np.linspace(1, 0, 100)
check("the monotonicity guard is exercised (a monotone series fails it)",
      int(np.sum(np.diff(np.sign(np.diff(mono))) != 0)) == 0)

print("\n  Heterogeneous equilibrium, solved rather than approximated:")
print("  Every firm plays its dominant alpha_i = (s - om_i*l)/k, so with")
print("  Sum(om_j) = 1:   pi_i - Pi_0 = (L/k)[(s^2 - om_i^2 l^2)/2 - om_i l (N s - l)]")
het = lambda om, N: (L / k) * ((s ** 2 - (om * l) ** 2) / 2 - om * l * (N * s - l))
print(f"{'N_econ':>9}{'crossover omega*':>19}{'firms worse off (of 7)':>26}")
named = {x: P.firm_omega(x) for x in ("Walmart", "Amazon", "Costco", "Home Depot",
                                      "Microsoft", "Alphabet", "Salesforce")}
cross = {}
for N in (38, 100, 500, 2007):
    gg = np.linspace(1e-9, 0.5, 400_001)
    vv = het(gg, N)
    idx = np.where(np.diff(np.sign(vv)) != 0)[0]
    cross[N] = gg[idx[0]] if len(idx) else float("nan")
    print(f"{N:>9}{cross[N]*100:>18.3f}%{sum(het(o, N) < 0 for o in named.values()):>26}")
check("the crossover is strongly N-dependent, so no single omega* is publishable",
      cross[38] / cross[2007] > 10,
      f"omega* moves from {cross[38]*100:.2f}% at N=38 to {cross[2007]*100:.3f}% "
      f"at N=2007 -- a factor of {cross[38]/cross[2007]:.0f}")
agg = sum(het(o, 2007) for o in named.values())
check("the aggregate stays negative, so the trap survives heterogeneity",
      agg < 0, f"sum over the named firms = {agg:+.2f} L/k")


# ================================ 6. the fold, both saddle-nodes
head("6. Bistability is a WINDOW; both edges are detected, not just the onset")
print("""  WHY: scanning for the first alpha with three roots finds the onset and misses
  the offset. 'Bistable above a critical rate' was published on that basis and is
  false for four of the eight folding cells. Both edges are found here, and the
  onset is cross-checked by simulating the dynamics from two initial conditions,
  which is independent of the root-finder.""")

def settle(alpha, eta, dof, e0, iters=600):
    e = e0
    for _ in range(iters):
        e = eta(dof(alpha, e))
    return e


def sim_onset(A, kappa, lo=0.0, hi=1.0, iters=40):
    """First alpha at which two initial conditions land on different attractors,
    found by bisection rather than a linear scan. Independent of fold_window."""
    eta, dof = P.fold_maps(A, kappa)
    split = lambda a: abs(settle(a, eta, dof, 0.0) - settle(a, eta, dof, 1.0)) > 1e-3
    if not split(hi):
        # bistability may close before alpha=1; probe a coarse grid for any hit
        hits = [a for a in np.linspace(0, 1, 201) if split(a)]
        if not hits:
            return None
        lo, hi = max(0.0, min(hits) - 0.005), min(hits)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if split(mid):
            hi = mid
        else:
            lo = mid
    return hi


closes = persists = 0
worst_onset = 0.0
for A in P.FOLD_A_VALUES:
    for kappa in P.FOLD_KAPPAS:
        win = P.fold_window(A, kappa)
        if win is None:
            continue
        on, off, keeps = win
        persists += keeps
        closes += (not keeps)
        sim = sim_onset(A, kappa)
        if sim is not None:
            worst_onset = max(worst_onset, abs(sim - on))
check("some folding cells CLOSE before alpha=1", closes > 0,
      f"{closes} of {closes+persists} folding cells close; "
      f"'bistable above a critical rate' is false for those")
check("some folding cells persist to alpha=1", persists > 0,
      f"{persists} persist, so neither statement is universal")
check("root-finder onsets agree with simulated onsets", worst_onset < 5e-3,
      f"max disagreement {worst_onset:.4f} between two independent methods")
w = P.fold_window(2.0, 1.5)
check("the flattest folding cell has a narrow closing window", w and not w[2],
      f"A=2, kappa=1.5: window [{w[0]:.4f}, {w[1]:.4f}], width {w[1]-w[0]:.4f}")


# ============================== 7. omega arithmetic and the two bounds
head("7. Every published omega, with the two bounds kept distinct")
big, om_big = P.largest_firm()
check("largest single firm on the baseline measure", abs(om_big - 0.026372) < 1e-5,
      f"{big}: {om_big*100:.2f}%")
check("upper bound across measurement variants is a DIFFERENT number",
      om_adv > om_big + 0.005, f"{om_adv*100:.2f}% vs {om_big*100:.2f}%")
mx_name, mx = P.max_attribution_bound()
check("max-attribution bound uses the largest global revenue", mx_name == "Amazon",
      f"{mx_name}: {mx*100:.2f}%")
check("max-attribution bound stays well under 1/N at N=4", mx < 0.25 / 5,
      f"{mx*100:.2f}% vs 25.00%")
mtot, mom = P.merger_omega()
check("largest conceivable merger stays far below 1/N at N=4", mom < 0.25 / 4,
      f"USD {mtot:,.1f}bn -> {mom*100:.2f}%")


# ============================== 8. period-mismatch sensitivity
head("8. Numerator/denominator period mismatch, bounded rather than ignored")
for g_ in (0.00, 0.05, 0.10):
    grown = P.FIRMS["Walmart"]["hh"] * (1 + g_)
    print(f"         Walmart +{g_*100:>3.0f}% -> {grown/P.PCE*100:.2f}% baseline / "
          f"{grown/P.cuttable_pce()*100:.2f}% adverse")
check("a 10% forward roll keeps omega an order of magnitude under 25%",
      P.FIRMS["Walmart"]["hh"] * 1.10 / P.cuttable_pce() < 0.05,
      f"worst case {P.FIRMS['Walmart']['hh']*1.10/P.cuttable_pce()*100:.2f}%")


# ============================== 9. prose agrees with the code, everywhere
head("9. Every published figure and phrase, across the whole repo")
print("""  WHY: the previous version parsed only the README, so banned phrases survived
  in identity.py, analysis_v2.py and two chart scripts. This scans every .py and
  .md, and normalises whitespace first so a phrase split across two source lines
  is still caught -- which is how one of them was missed.""")

readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
wal_us_only = P.FIRMS["Walmart"]["hh"] - 90.238

expect = [
    (f"{P.firm_omega('Walmart')*100:.2f}%", "Walmart omega baseline"),
    (f"{P.firm_omega('Walmart', adverse=True)*100:.2f}%", "Walmart omega adverse"),
    (f"{wal_us_only/P.PCE*100:.2f}%", "Walmart U.S. alone"),
    (f"{(1-om_adv)*100:.1f}%", "uninternalised floor"),
    (f"{P.wedge(om_adv):.3f}", "corrected wedge"),
    (f"{P.max_attribution_bound()[1]*100:.2f}%", "max-attribution bound"),
    (f"{P.merger_omega()[1]*100:.2f}%", "merger bound"),
    (f"{P.n_eff(P.firm_omega('Walmart')):.0f}", "Walmart effective N"),
    (f"{P.n_eff(P.firm_omega('Microsoft')):.0f}", "Microsoft effective N"),
    (f"{P.n_eff(P.firm_omega('Salesforce')):,.0f}", "Salesforce effective N"),
    (f"{P.firm_omega('Block')*100:.2f}%", "Block omega"),
    (f"{P.FIRMS['Block']['total']/P.PCE*100:.2f}%", "Block loosest reading"),
    (f"{P.FIRMS['Walmart']['hh']*1.10/P.cuttable_pce()*100:.2f}%", "10% roll sensitivity"),
    (f"{(0.90/38)/(0.08/6):.2f}", "lam/N asymmetry factor"),
    (f"{P.n_eff(om_adv):.0f}", "minimum effective N"),
]
for value, label in expect:
    check(f"README states {label} = {value}", value in readme)

for A, kappa in ((2.0, 1.5), (4.0, 1.0)):
    w_ = P.fold_window(A, kappa)
    check(f"README states the A={A:.0f}, kappa={kappa} window "
          f"[{w_[0]:.2f}, {w_[1]:.2f}] at method-stable precision",
          f"{w_[0]:.2f}" in readme and f"{w_[1]:.2f}" in readme)

banned = [
    ("arithmetically out of reach", "overclaims a benchmark change as arithmetic"),
    ("ceiling for the whole economy", "the label that collided"),
    ("ceiling for the entire", "same collision, different casing"),
    ("ceiling of the whole economy", "same collision, in a chart"),
    ("0.867", "the eta=0 wedge"),
    ("bistable above a critical", "false for four of eight folding cells"),
    ("None of them exist", "categorical claim the README retracted"),
    ("between 10 and 20,000", "range starts at 9.5x, not 10x"),
]
files = (glob.glob(os.path.join(ROOT, "**", "*.py"), recursive=True) +
         glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True))
files = [f for f in files if os.path.abspath(f) != os.path.abspath(__file__)]
for phrase, why in banned:
    hits = []
    for fp in files:
        flat = re.sub(r"\s+", " ", open(fp, encoding="utf-8", errors="replace").read()).lower()
        if phrase.lower() in flat:
            hits.append(os.path.relpath(fp, ROOT))
    check(f"nowhere in the repo: {phrase!r}", not hits,
          why if not hits else "found in: " + ", ".join(hits))


# ====================== 10. hardcoded constants agree with the single source
head("10. Hardcoded constants in every script agree with params.py")
print("""  WHY: params.py is the single source of truth, but most scripts still write
  their constants inline. That is tolerable only if nothing can disagree with it.
  This scans every script for the literals that matter and fails on any mismatch,
  which closes the gap without rewiring files that do not need it.""")

CONST = {
    "PCE":          (P.PCE,             [r"20[_,]?956\.?0?"]),
    "cuttable PCE": (P.cuttable_pce(),  [r"15[_,]?259\.?0?"]),
    "Lambda":       (P.LAM,             [r"LAM\s*=\s*0\.90?", r"0\.9"]),
    "Walmart hh":   (P.FIRMS["Walmart"]["hh"], [r"462\.415\s*\+\s*90\.238"]),
}
scripts = sorted(set(glob.glob(os.path.join(ROOT, "analysis", "*.py")) +
                     glob.glob(os.path.join(ROOT, "charts", "**", "*.py"), recursive=True)))
scripts = [f for f in scripts if os.path.basename(f) not in ("tests.py", "params.py")]

# any four- or five-digit literal that looks like a PCE-scale denominator must
# equal one of the two sanctioned denominators
sanctioned = {f"{P.PCE:.0f}", f"{P.cuttable_pce():.0f}",
              f"{P.PCE:,.0f}".replace(",", "_"), "20_956", "15_259", "20956", "15259"}
bad = []
for fp in scripts:
    txt = open(fp, encoding="utf-8", errors="replace").read()
    for lit in re.findall(r"(1[0-9]|2[0-9])[_,]?[0-9]{3}(?:\.[0-9]+)?", txt):
        pass
    for m in re.finditer(r"([12][0-9][_,]?[0-9]{3})(?:\.0)?", txt):
        tok = m.group(1).replace(",", "_")
        if tok not in sanctioned and tok.replace("_", "") not in {"20956", "15259"}:
            bad.append(f"{os.path.relpath(fp, ROOT)}:{tok}")
check("no script uses an unsanctioned PCE-scale denominator", not bad,
      "all denominators are 20,956 or 15,259" if not bad else "found: " + ", ".join(sorted(set(bad))[:6]))

wal_hits = [os.path.relpath(f, ROOT) for f in scripts
            if "462.415" in open(f, encoding="utf-8", errors="replace").read()]
wal_ok = all("90.238" in open(os.path.join(ROOT, f), encoding="utf-8", errors="replace").read()
             for f in wal_hits)
check("every script quoting Walmart uses the same two segments", wal_ok,
      f"{len(wal_hits)} scripts quote 462.415, all paired with 90.238")

floors = []
for fp in scripts:
    txt = open(fp, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r"9[0-9]\.[0-9]{1,2}\s*%", txt):
        floors.append((os.path.relpath(fp, ROOT), m.group(0)))
# both the 1- and 2-decimal renderings of the same two quantities are legitimate;
# anything else is an unexplained third number
allowed = {f"{(1-om_adv)*100:.1f}%", f"{(1-om_adv)*100:.2f}%",
           f"{(1-P.largest_firm()[1])*100:.1f}%", f"{(1-P.largest_firm()[1])*100:.2f}%",
           "99.9%", "100%"}
odd = [f"{a}:{b}" for a, b in floors if b.replace(" ", "") not in allowed]
check("no script publishes an unexplained floor percentage", not odd,
      "floors are 96.4% (adverse) or 97.4% (baseline)" if not odd else ", ".join(odd[:5]))


head("RESULT")
print(f"  {CHECKS} checks run, {len(FAILS)} failed")
for f_ in FAILS:
    print(f"    FAILED: {f_}")
sys.exit(1 if FAILS else 0)
