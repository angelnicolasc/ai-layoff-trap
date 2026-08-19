# The AI Layoff Trap — measuring the escape route

An extension of **Falk & Tsoukalas (2026), "The AI Layoff Trap"**, [arXiv:2603.20617](https://arxiv.org/abs/2603.20617) (v3, 3 June 2026).

Every input is public. Every judgement call is listed under **Knobs**, each set against this
analysis rather than for it. Every published figure is re-derived by `analysis/tests.py`, which
also parses this file and fails if any number here disagrees with the code.

---

## The claim

Proposition 1 of the paper gives each firm an internalisation coefficient of `1/N`: a firm absorbs
`1/N` of the demand its automation destroys, so the over-automation wedge is `ℓ(1−1/N)/k` and the
corrective rate is `τ* = ℓ(1−1/N)`. Within that model the arithmetic is correct, and
`analysis/replication.py` reproduces it exactly. The model's own logic then offers three ways out:
concentrate (`N=1` internalises everything), merge, or form the grand coalition (`M=N` closes the
wedge, Prop. 4).

**Measured against economy-wide consumption, no firm is positioned anywhere near the
internalisation those routes require.** The coefficient that governs internalisation is a firm's
share of the *consumer wallet*, not of its *sector*. That share is at most 2.2–3.6% for every firm
in the U.S. economy, so `(1−ω) ≥ 96.4%` everywhere.

This is a measurement result about the world, not a defect in the paper's algebra. The paper's
`N=1` case is a monopolist over *its own sector*, whose sectoral externality is zero by
construction; a real firm's `ω` is measured economy-wide. The two are different objects and are
never compared as though they were the same one.

**Direction matters.** ω enters the wedge as `(1−ω)`, so a small ω means the externality is
**maximal**, not small. The trap is larger, uniform and inescapable — never "smaller than claimed",
never "competition barely matters".

### Numbers

| Quantity | Value |
|---|---|
| ω — Walmart U.S. ÷ total PCE | 2.21% |
| ω — + Sam's Club, the maximum numerator | 2.64% ← the highest any single firm reaches |
| ω — + the most adverse denominator | **3.62%** ← upper bound across all measurement variants |
| Uninternalised share `(1−ω)` | **≥ 96.4%** |
| Model's `(1−1/N)` at N=1 / N=2 / N=4 | 0% / 50% / 75% |
| Effective N = 1/ω — Walmart / Microsoft / Salesforce | 38 / 699 / 104,780 |
| Corrected wedge `(1−ω)·ℓ_soc/k` at the upper bound | **0.607** (Λ=0.90, η=0.30, w=1, k=1) |
| Largest conceivable merger (Walmart + Sam's + Kroger + Costco + Target) | ω = 4.72% |
| Bound if 100% of global revenue were credited to U.S. consumption | ω ≤ 3.42% |
| Block — the paper's own opening example | ω = 0.03%, i.e. 3 cents per $100 destroyed |

The wedge figure carries its parameters because it is not scale-free: `(1−ω)·Λ(1−η)w/k`. Quoting
`(1−ω)·Λ` alone drops `(1−η)` and `1/k` and is the wedge only at η=0. `tests.py` §2 proves the
difference and pins the value.

### ω, defined

A displaced worker loses a dollar and stops spending `Λ` of it, spread across their basket. Under
proportional cuts, firm *i*'s share of that basket is `R_hh / PCE`:

```
spending destroyed        = Λ
absorbed by firm i        = (R_hh/PCE) · Λ
share firm i recaptures   = ω = R_hh / PCE        ← observable, Λ cancels
```

**ω names no sector**, so redrawing sector boundaries cannot move it. That is the whole of the
boundary-invariance argument, and it does not rest on any lemma about `λ/N`.

`λ/N` is invariant only under **symmetric** subdivision. Under a realistic asymmetric partition it
moves — 0.90/38 = 0.0237 for the whole economy against 0.08/6 = 0.0133 for grocery, a factor of
1.78 — so that lemma cannot carry the argument on its own. `tests.py` §4 proves both the holding
case and the failing one.

`Λ` survives only in the level term `ℓ_soc = Λ(1−η)w`, which is sector-definition dependent.

### Two objections, pre-empted

**"B2B firms like Salesforce recapture demand indirectly, through their clients."**
The paper's model has no intermediate demand — its firms sell straight to the workers whose wages
fund `D` (eq. 2), so it cannot represent a B2B firm at all. And it does not matter: credit a firm
with 100% of its *global* revenue as U.S. final consumption, an attribution nobody would defend,
and the bound is still 3.42%.

**"If every firm merged, ω = 1, so the escape does exist."**
The only entity with ω = 1 is a monopolist over all consumption. The largest combination anyone
could name reaches 4.72%, five times below what the model grants a four-firm market.

### On the N-sweep

The comparative static in N is legitimate; it is *empirically vacuous over the range that matters*.
Measured wallet shares put every real firm at `N_eff ≥ 28`, on the flat right-hand tail where the
wedge has already converged to `ℓ/k`.

The wedge is **per displaced task**, while total damage scales with the displaced wage mass. The
correct phrasing is "the wedge is largest for low-wallet-share firms", not "those sectors are worst
hit".

---

## Files

### `analysis/`
| File | What it does |
|---|---|
| `params.py` | **Single source of truth.** Every raw input and every derived figure. Scripts and this README both draw from it, so a number cannot drift between them. |
| `tests.py` | **Run this first.** Re-derives every published figure by an independent route, proves the scope limits of two lemmas, and cross-checks this README number by number. |
| `replication.py` | Reproduces Proposition 1 two ways, asserts interiority rather than assuming it, and asserts the two routes match to machine precision. |
| `identity.py` | Derives ω as a basket share; both bounds; both objections, computed; and Block. |
| `analysis_v2.py` | What is boundary-free and what only looks it; measurement robustness; corrected comparative statics. |
| `band.py` | The destructive band, with the derivation in the docstring, `N_econ` swept, and a heterogeneity section showing where the result stops holding. |
| `fold.py` | Endogenous reabsorption with a power-law `η(D)`. Finds **no** fold: one stable equilibrium throughout. |
| `fold2.py` | The same with threshold-like (logistic) `η(D)`. Reports the bistability *window* — both saddle-nodes, not just the onset — plus stability labels and the separatrix. |

### `charts/`
| File | What it is |
|---|---|
| `style.py` | Shared visual system: SF Pro Display, dark cards on a light ground, one accent, 3:4 canvas, pixel layout helpers. |
| `chart_lay.py` → `lay_waffle.png` | General-audience visual. 100 squares = $100 of destroyed spending. |
| `chart_v2.py` → `layoff_trap_v2.png` | The externality `(1−ω)` against N, with a measurement-robustness panel. |
| `chart_neff.py` → `effective_n.png` | Effective N: competitors a firm has, versus competitors it behaves as if it had. |

### `source/`
`tohtml.py` flattens the arXiv HTML to text while preserving the maths from each
`<math alttext>` attribute. The paper itself is not redistributed — `source/README.md` has the two
commands to fetch and convert it.

---

## Running

Python 3.11, `numpy` and `matplotlib` only.

```bash
python analysis/tests.py
```

It exits non-zero on any failure. Charts need SF Pro Display installed; substitute the family in
`charts/style.py` otherwise.

---

## Knobs

No hidden parameters, but there are choices. Each is set to favour the paper — that is, to weaken
the claim made here:

| Knob | Value | Direction / source |
|---|---|---|
| `Λ` (MPC of a displaced worker) | 0.90 | Conservative. The paper cites a 3.6% savings rate (Mar-2026), implying ~0.96 for the *average* household; a displaced worker's MPC is higher still. A larger Λ raises the externality claimed here. |
| `η` (income replacement) | 0.30 | From the displaced-worker earnings-loss literature the paper itself cites. It enters `ℓ_soc`; omitting it inflates the wedge by 43%. |
| Third-party share of health spending | 0.90 | CMS NHE: out-of-pocket ≈ 10%. A higher share shrinks the denominator and *raises* ω. |
| Imputed rent netted out | USD 2,500bn | Same direction: raises ω. |
| Numerator | Walmart U.S. + Sam's Club | The largest U.S. household-facing revenue there is. |
| Block numerator | Cash App ex-bitcoin | A consistency rule, not a convenience: asset purchases are not consumption and PCE excludes them. Both looser readings are reported and neither exceeds 0.12%. |
| `fold2.py`: η_max, κ, D* | η_max = 0.85 and D* = 0.72·D_full are FIXED; only κ is swept, over 0.5–5. Caveat 6 states what the sweep produces. |

---

## Sources

- Paper: [arXiv:2603.20617](https://arxiv.org/abs/2603.20617) · [HTML v3](https://arxiv.org/html/2603.20617v3) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6448898)
- U.S. PCE, 2025 annual: USD 20,956bn — [FRED/BEA](https://fred.stlouisfed.org/series/PCE)
- Imputed rent of owner-occupied housing, 2025: USD 2,500bn — [FRED/BEA](https://fred.stlouisfed.org/series/A2013C1A027NBEA)
- PCE health care services, 2025: USD 3,552bn — [FRED/BEA](https://fred.stlouisfed.org/series/DHLCRC1A027NBEA)
- Walmart U.S. USD 462.415bn, Sam's Club U.S. USD 90.238bn, International USD 121.885bn — [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416925000021/wmt-20250131.htm)
- Other firm revenues: FY2025 filings; Amazon's global figure is calendar 2025

---

## Caveats

1. **Proportional cuts.** ω assumes displaced workers cut spending proportionally to the average
   basket. Two effects push ω *down*, so the stated bound is genuine: Walmart is ~60% grocery and
   layoffs hit discretionary harder than staples; and trade-down shifts displaced spending *toward*
   Walmart. ω is also cohort-specific — a particular local workforce can deviate upward for a
   particular firm; the national basket is the benchmark.
2. **Period mismatch.** Numerators are fiscal-year filings (Walmart's FY2025 closed 2025-01-31);
   the denominator is calendar-2025 PCE. Rolling the numerator forward raises ω, which weakens this
   analysis, so the sensitivity is computed rather than assumed: a 10% forward roll takes the
   adverse-basis ω from 3.62% to 3.98%, still an order of magnitude under 25%.
3. **Numerator/denominator consistency.** UnitedHealth and CVS out-earn Walmart but mostly on
   third-party-paid revenue; excluding it from the denominator requires excluding it from the
   numerator too. Microsoft's consumer segment is an estimate, not a reported segment.
4. **The level is sector-dependent; the result is not.** The *magnitude* of the wedge depends on how
   a sector is drawn. The finding that no firm reaches the required internalisation does not.
5. **The band result assumes a symmetric economy.** `band.py` derives it with one ω for all firms
   and `N_econ = 1/ω`. Solving the heterogeneous case instead — every firm plays its dominant
   `α_i = (s−ω_iℓ)/k`, with `Σω_j = 1` — gives
   `π_i − Π₀ = (L/k)[(s²−ω_i²ℓ²)/2 − ω_iℓ(Ns−ℓ)]`. A firm with ω ≈ 0 ends up *better* off. The
   crossover is strongly `N_econ`-dependent and therefore not publishable as a single number: it
   sits at 1.50% for `N_econ`=38 and 0.03% for `N_econ`=2007. The aggregate stays negative in every
   case, so the trap survives heterogeneity even though the per-firm claim does not.
6. **The fold is a bounded window, and conditional on the shape of η(D).** Under a power law there
   is no fold at all (`fold.py`), and that is structural rather than a choice of sigmoid: a convex
   η gives a convex fixed-point map, which admits at most two crossings and so never three. Under a
   logistic η the system is bistable over a *window* in α, not everywhere past an onset. At A=2,
   κ=1.5 the window is [0.62, 0.70]; at A=4, κ=1.0 it is [0.79, 0.80] — quoted to two
   decimals because the fourth depends on the root-finding method, not on the model. Both branches
   survive to α=1 only for κ ≥ 3 (A=2) and κ ≥ 2 (A=4). Where the window closes, automation alone
   destroys the high-reabsorption equilibrium and no external shock is needed; where it persists,
   automation narrows the basin and a shock does the pushing. Which regime holds is an empirical
   question about η(D) that nobody currently measures.
7. **Figure comparisons.** Claims about the paper's own figures are limited to what its text states.
   The paper does not give the axis range of its Figure 1, so no range is asserted here.

---

Analysis by Nick Cerutti. MIT licensed.
