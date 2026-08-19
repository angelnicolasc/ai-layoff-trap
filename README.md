# The AI Layoff Trap — measuring the escape route

An extension of **Falk & Tsoukalas (2026), "The AI Layoff Trap"**, [arXiv:2603.20617](https://arxiv.org/abs/2603.20617) (v3, 3 June 2026).

Every input here is public and every judgement call is listed under **Knobs**, each one set
against this repo's own argument.

---

## The claim

Proposition 1 of the paper gives each firm an internalisation coefficient of `1/N`: a firm absorbs
`1/N` of the demand its automation destroys, so the over-automation wedge is `ℓ(1−1/N)/k` and the
corrective rate is `τ* = ℓ(1−1/N)`. The model's own logic then offers three ways out — concentrate
(`N=1` internalises everything), merge, or form the grand coalition (`M=N` closes the wedge, Prop. 4).

**All three are arithmetically out of reach.** The coefficient that governs internalisation is a
firm's share of the *consumer wallet*, not of its *sector*. Measured, that share is capped at
2.2–3.6% for every firm in the U.S. economy, so `(1−ω) ≥ 96.4%` everywhere. Every firm already sits
at the paper's own `N→∞` limit.

**Direction matters.** ω enters the wedge as `(1−ω)`, so a small ω means the externality is
**maximal**, not small. The trap is larger, uniform and inescapable — never "smaller than claimed",
never "competition barely matters".

### Numbers

| Quantity | Value |
|---|---|
| ω — Walmart U.S. ÷ total PCE | 2.21% |
| ω — + Sam's Club, the maximum numerator | 2.64% |
| ω — + the most adverse denominator | **3.62%** ← ceiling for the whole economy |
| Uninternalised share `(1−ω)` | **≥ 96.4%** |
| Model's `(1−1/N)` at N=1 / N=2 / N=4 | 0% / 50% / 75% |
| Effective N = 1/ω — Walmart / Microsoft / Salesforce | 38 / 699 / 104,780 |
| Largest conceivable merger (Walmart + Sam's + Kroger + Costco + Target) | ω = 4.72% — 5.3× below the 25% the model gives a four-firm market |
| Ceiling if 100% of global revenue is credited to U.S. consumption | ω ≤ 3.22% |
| Block — the paper's own opening example | ω = 0.03%, i.e. 3 cents per $100 destroyed |

At `N=1` the model's wedge is exactly 0 and the corrected one is ≥ 0.867. Those are two numbers,
not a ratio — the ratio has zero in the denominator.

### ω, defined

A displaced worker loses a dollar and stops spending `Λ` of it, spread across their basket. Under
proportional cuts, firm *i*'s share of that basket is `R_hh / PCE`:

```
spending destroyed        = Λ
absorbed by firm i        = (R_hh/PCE) · Λ
share firm i recaptures   = ω = R_hh / PCE        ← observable, Λ cancels
```

**ω references no sector**, so redrawing sector boundaries cannot move it. The paper is the special
case where the sector *is* the economy, in which the same coefficient reads as `λ/(N·Λ)`. `Λ`
survives only in the level term `ℓ_soc = Λ(1−η)w`, which is sector-definition dependent.

### Two objections, pre-empted

**"B2B firms like Salesforce recapture demand indirectly, through their clients."**
The paper's model has no intermediate demand — its firms sell straight to the workers whose wages
fund `D` (eq. 2), so it cannot represent a B2B firm at all. And it does not matter: credit a firm
with 100% of its *global* revenue as U.S. final consumption, an attribution nobody would defend, and
the ceiling is still ~3.2%. The indirect channel cannot rebuild `1/N = 25%`.

**"If every firm merged, ω = 1, so the escape does exist."**
The only entity with ω = 1 is a monopolist over all consumption. The largest combination anyone
could name reaches 4.72%, five times below what the model grants a four-firm market.

### On the N-sweep

The comparative static in N is perfectly legitimate; it is *empirically vacuous over the range that
matters*. The paper's Figure 1 sweeps N = 2…40 and essentially none of that range is populated:
measured wallet shares put every real firm at `N_eff ≥ 28`, already on the flat right-hand tail.

Note also that the wedge is **per displaced task**, while total damage scales with the displaced
wage mass. The correct phrasing is "the wedge is largest for low-wallet-share firms", not "those
sectors are worst hit".

---

## Files

### `analysis/`
| File | What it does |
|---|---|
| `replication.py` | Reproduces Proposition 1 two ways and asserts they match to machine precision. Run this first. |
| `identity.py` | Derives ω as a basket share; the ceiling; both objections above, computed; and Block. |
| `analysis_v2.py` | Invariance, measurement robustness, and the corrected comparative statics. |
| `band.py` | The destructive band — where automation is privately profitable but leaves every firm worse off than if none had automated. Full derivation in the docstring; `N_econ` is swept, not fixed. |
| `fold.py` | Endogenous reabsorption with a power-law `η(D)`. Finds **no** fold: one stable equilibrium throughout. |
| `fold2.py` | The same with threshold-like (logistic) `η(D)`. Saddle-node at α≈0.53–0.73 for κ≥1.5, with stability labels and the separatrix. |

### `charts/`
| File | What it is |
|---|---|
| `style.py` | Shared visual system: SF Pro Display, dark cards on a light ground, one accent, 3:4 canvas, pixel layout helpers. |
| `chart_lay.py` → `lay_waffle.png` | Hero visual for a general audience. 100 squares = $100 of destroyed spending. |
| `chart_v2.py` → `layoff_trap_v2.png` | The externality `(1−ω)` against N, with the empty region and a measurement-robustness panel. |
| `chart_neff.py` → `effective_n.png` | Effective N: competitors a firm has, versus competitors it behaves as if it had. |

### `source/`
`tohtml.py` flattens the arXiv HTML to text while preserving the maths from each
`<math alttext>` attribute. The paper itself is not redistributed — `source/README.md` has the two commands to fetch and convert it.

---

## Running

Python 3.11, `numpy` and `matplotlib` only. Every script is standalone; chart scripts write their
PNG next to themselves.

```bash
python analysis/replication.py && python analysis/identity.py && python analysis/band.py
```

Charts need SF Pro Display installed; substitute the family in `charts/style.py` otherwise.

---

## Knobs

No hidden parameters, but there are choices. Each is set to favour the paper — that is, to weaken
the claim made here:

| Knob | Value | Direction / source |
|---|---|---|
| `Λ` (MPC of a displaced worker) | 0.90 | Conservative. The paper itself cites a 3.6% savings rate (Mar-2026), implying Λ ≈ 0.96. A larger Λ would *raise* the externality claimed here. Enters the level only, never ω. |
| Third-party share of health spending | 0.90 | CMS NHE: out-of-pocket ≈ 10%. A higher share shrinks the denominator and *raises* ω. |
| Imputed rent netted out | USD 2,500bn | Same direction: raises ω. |
| Numerator | Walmart U.S. + Sam's Club | The largest U.S. household-facing revenue there is. |
| Block numerator | Cash App ex-bitcoin | A consistency rule, not a convenience: asset purchases are not consumption and PCE excludes them, so counting bitcoin passthrough would break numerator/denominator consistency. Both looser readings are reported. |
| `fold2.py`: η_max, κ, D* | 0.85, swept 0.5–5, 0.72·D_full | Swept, not fitted. The fold appears for κ ≥ 1.5; the quoted 36% demand gap is at α=0.55, κ=3, A=2. |

---

## Sources

- Paper: [arXiv:2603.20617](https://arxiv.org/abs/2603.20617) · [HTML v3](https://arxiv.org/html/2603.20617v3) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6448898)
- U.S. PCE, 2025 annual: USD 20,956bn — [FRED/BEA](https://fred.stlouisfed.org/series/PCE)
- Imputed rent of owner-occupied housing, 2025: USD 2,500bn — [FRED/BEA](https://fred.stlouisfed.org/series/A2013C1A027NBEA)
- PCE health care services, 2025: USD 3,552bn — [FRED/BEA](https://fred.stlouisfed.org/series/DHLCRC1A027NBEA)
- Walmart U.S. USD 462.415bn, Sam's Club U.S. USD 90.238bn, International USD 121.885bn — [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416925000021/wmt-20250131.htm)
- Other firm revenues: FY2025 filings

---

## Caveats

1. ω assumes displaced workers cut spending proportionally to the average basket. Two effects push ω
   *down*, so 3.62% is a genuine upper bound: Walmart is ~60% grocery and layoffs hit discretionary
   harder than staples; and trade-down shifts displaced spending *toward* Walmart. ω is also
   cohort-specific — a particular local workforce can deviate upward for a particular firm; the
   national basket is used as the benchmark.
2. Numerator and denominator must use the same concept. UnitedHealth and CVS out-earn Walmart but
   mostly on third-party-paid revenue; excluding it from the denominator requires excluding it from
   the numerator too.
3. The *level* of the wedge depends on the sector definition. The *nonexistence of the escape
   hatches* does not.
4. The fold in `fold2.py` requires threshold-like reabsorption; under a power law there is none.
   Whether the trap has a tipping point is an empirical question about the shape of `η(D)` that
   nobody currently measures. That conditionality is the finding.

---

Analysis by Nick Cerutti.
