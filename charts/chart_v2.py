# -*- coding: utf-8 -*-
"""Technical chart: the externality, and the region of the model nobody occupies.

The y-axis is deliberately the EXTERNALITY (1 - omega), not internalisation.
omega enters the wedge as (1 - omega), so a small omega means the externality is
maximal. Plotting internalisation invites the reader to conclude the opposite.

Laid out in pixels against a 1200x1600 canvas (3:4).
"""
from matplotlib.ticker import FuncFormatter
import numpy as np
import style as S

S.setup()
fig = S.figure()

PCE, CUT = 20_956.0, 15_259.0     # total PCE; PCE net of imputed rent + third-party health
WMT      = 462.415 + 90.238       # Walmart U.S. + Sam's Club U.S., FY2025
OM_CEIL  = WMT / CUT * 100        # 3.62 %, the most adverse measurement
FLOOR    = 100 - OM_CEIL          # 96.38 %

L, RGT = 90, 1110

# -------------------------------------------------------------------- header
S.text_px(fig, L,   62, "The recapture ratio", size=15, color=S.INK_SOFT, weight=S.M)
S.text_px(fig, RGT, 62, "Nick Cerutti", size=15, color=S.INK_SOFT, ha="right")
S.rule_px(fig, L, RGT, 100)

S.text_px(fig, L, 178, "Three escape hatches.", size=48, color=S.INK, weight=S.B)
S.text_px(fig, L, 240, "No firm can reach them.", size=44, color=S.INK, weight=S.B)
S.text_px(fig, L, 300,
          "Falk & Tsoukalas prove firms over-automate because each absorbs only 1/N of the demand it destroys —",
          size=14.5, color=S.INK_SOFT)
S.text_px(fig, L, 326,
          "so the model offers a way out: concentrate, merge, or form a coalition. But 1/N is a firm's share of its own",
          size=14.5, color=S.INK_SOFT)
S.text_px(fig, L, 352,
          "sector. Measured as a share of the consumer wallet, every U.S. firm already sits at the model's N→∞ limit.",
          size=14.5, color=S.INK_SOFT)

# ----------------------------------------------------------------- main card
CA_TOP, CA_H = 400, 620
S.card_px(fig, L, CA_TOP, RGT - L, CA_H)
S.text_px(fig, L + 40, CA_TOP + 48,
          "Share of the demand destruction a firm does NOT absorb",
          size=17, color=S.ON_CARD, weight=S.M)

ax = S.axes_px(fig, L + 118, CA_TOP + 84, 852, 424)
S.style_dark_axes(ax)

N = np.logspace(0, 3, 700)
ax.axhspan(0, FLOOR, facecolor="#272C34", zorder=1)
ax.axhspan(FLOOR, 100, facecolor=S.SERIES_B, alpha=.30, zorder=2)
ax.axhline(FLOOR, color=S.SERIES_B, lw=2.4, zorder=5, solid_capstyle="round")
ax.plot(N, 100 * (1 - 1 / N), color=S.SERIES_A, lw=2.4, zorder=4, solid_capstyle="round")

ax.set_xscale("log"); ax.set_xlim(1, 1000); ax.set_ylim(0, 102)
ax.set_yticks([0, 25, 50, 75, 100])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.set_xticks([1, 2, 5, 10, 50, 100, 500, 1000])
ax.set_xticklabels(["1", "2", "5", "10", "50", "100", "500", "1000"])

# right-aligned under the strip, where the model curve has already entered it
ax.text(880, 89, "REALITY", fontsize=14, color=S.SERIES_B, fontweight=S.B, ha="right")
ax.text(880, 81.5,
        "Every operating U.S. firm is in this strip.\n"
        "Walmart is the largest single firm and still\n"
        "leaves 97.4% of what it destroys on others.\n"
        "The strip is drawn at 96.4%, the adverse case.",
        fontsize=13.5, color=S.ON_CARD, ha="right", va="top", linespacing=1.68)

# below the curve, which only rises further to the right of this block
ax.text(4.6, 54, "THE MODEL'S SAFE ZONE", fontsize=14, color=S.ON_CARD_2, fontweight=S.B)
ax.text(4.6, 46.5,
        "Concentration is supposed to internalise the externality\n"
        "here — a monopolist absorbs all of it and needs no\n"
        "correction. Nothing in the U.S. economy is in this region.",
        fontsize=13.5, color=S.ON_CARD, va="top", linespacing=1.68)

# legend in the bottom-left, permanently clear of the curve
for i, (col, lab) in enumerate([(S.SERIES_A, "the model:  1 − 1/N"),
                                (S.SERIES_B, "measured:  1 − ω")]):
    yy = 14 - i * 8.5
    ax.plot([1.13, 1.55], [yy, yy], color=col, lw=2.4, solid_capstyle="round", zorder=6)
    ax.text(1.72, yy, lab, fontsize=13, color=S.ON_CARD_2, va="center")

S.text_px(fig, L + 118 + 426, CA_TOP + 566,
          "Number of competing firms in the sector  (N)",
          size=13.5, color=S.ON_CARD_2, ha="center")
S.text_px(fig, L + 118, CA_TOP + 560, "monopoly", size=11.5, color=S.ON_CARD_2, ha="center")

# ---------------------------------------------------------- robustness card
CB_TOP, CB_H = 1048, 250
S.card_px(fig, L, CB_TOP, RGT - L, CB_H)
S.text_px(fig, L + 40, CB_TOP + 44,
          "Every measurement choice below favours the paper. The upper bound barely moves.",
          size=15, color=S.ON_CARD, weight=S.M)

bx = S.axes_px(fig, L + 300, CB_TOP + 76, 660, 142)
S.style_dark_axes(bx, grid_axis="x")
bx.spines["left"].set_visible(False)
rows = [("Model's internalisation, N=2", 50.00, S.SERIES_A),
        ("Model's internalisation, N=4", 25.00, S.SERIES_A),
        ("Measured: most adverse",        3.62, S.SERIES_B),
        ("Measured: max numerator",       2.64, S.SERIES_B),
        ("Measured: baseline",            2.21, S.SERIES_B)]
yp = np.arange(len(rows))
for y, (lbl, v, col) in zip(yp, rows):
    bx.barh(y, v, height=.52, color=col, zorder=3)
    bx.text(v * 1.15, y, f"{v:.2f}%", va="center", fontsize=12.5,
            color=S.ON_CARD, fontweight=S.M)
bx.set_yticks(yp)
bx.set_yticklabels([r[0] for r in rows], fontsize=12.5, color=S.ON_CARD_2)
bx.invert_yaxis()
bx.set_xscale("log"); bx.set_xlim(1.6, 190)
bx.set_xticks([2, 5, 10, 25, 50, 100])
bx.set_xticklabels(["2%", "5%", "10%", "25%", "50%", "100%"])

# -------------------------------------------------------------------- footer
S.rule_px(fig, L, RGT, 1360)
S.text_px(fig, L, 1392,
          "ω = a firm's U.S. household-facing revenue ÷ U.S. personal consumption expenditure (BEA, USD 20,956bn, 2025). Revenues from FY2025\n"
          "filings. 'Most adverse' nets imputed rent (USD 2,500bn) and third-party-paid health services (90% of USD 3,552bn, CMS) out of the\n"
          "denominator and adds Sam's Club to the numerator. Model curve is Proposition 1: wedge = l(1-1/N)/k, i.e. internalisation = 1/N.",
          size=10.5, color=S.INK_FAINT, va="top", spacing=1.9)

fig.savefig("layoff_trap_v2.png", facecolor=S.BG)
print("saved layoff_trap_v2.png")
